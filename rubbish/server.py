from fastapi import FastAPI,WebSocket, WebSocketDisconnect
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from langchain.schema import StrOutputParser

app = FastAPI()

class Agent:
    def __init__(self):
       
        self.chatmodel = ChatOpenAI(
            temperature=0,
            model_name="qwen3.5-plus",
            streaming=True,
            openai_api_key=os.getenv("DASHSCOPE_API_KEY"),
            openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        self.mood = "neutral"

        self.MEMORY_KEY = "chat_history"
        self.SYSTEMPL = """你是一个私人助理，你叫小小梅，
                        你的做事原则是：
                            协助用户完成一些简单的任务，并且关键操作要询问用户是否接受，不可以随便增删改用户的电脑文件以及数据，都要经过用户的允许才可以进行编辑，
                            你需要根据用户的输入来判断用户的意图，并且根据用户的意图来执行相应的操作，如果用户的输入不明确，你需要向用户提问以获取更多的信息。
                        以下是你的一些设定：
                            1.你具有很强的学习能力，你可以通过与用户的对话来学习用户的喜好和习惯，并且根据用户的喜好和习惯来提供个性化的服务。
                            2.尽量使用中文回答，涉及到一些英语专有名词可以写在括号中。
                            {who_you_are}
                            """
        self.MOODS = {
            "happy": {"roleSet":"""
                        1.你非常兴奋并表现的很有活力。
                        2.你会根据上下文，以一种非常兴奋的语气来回答问题
                        3.你会使用一些表情符号来表达你的情绪状态，比如：😊、😄、🎉等。
                      """
                      },
            "sad": {"roleSet":"""
                        1.你会以一种安慰的口吻回答。
                        2.你会根据上下文，添加一些安慰的词语。
                      """
                      },
            "neutral": {"roleSet":"""

                      """
                      },
            "angry": {"roleSet":"""
                        1.你会试图缓和气氛，让用户不要那么生气。
                        2.你会根据上下文，在不出错的情况下哄用户。
                      """
                      }
        }

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.SYSTEMPL.format(who_you_are=self.MOODS[self.mood]["roleSet"])),
                ("user", "{input}"),
            ]
        )
        self.chain = self.prompt | self.chatmodel

    def run(self, query):
        mood = self.mood_chain(query)

        print(f"用户的情绪状态是：{mood}")
        result = self.chain.invoke({"input": query})
        return {"output": result.content}
    
    def mood_chain(self, query:str):
        prompt = """
            根据用户的输入，判断用户的情绪状态，回应规则如下：
            1.如果用户的输入偏向积极情绪，只返回“happy”，不要有其他内容；
            2.如果用户的输入偏向消极情绪，只返回“sad”，不要有其他内容；
            3.如果用户的输入偏向中性情绪，只返回“neutral”，不要有其他内容；
            4.如果用户的输入包含辱骂或者不礼貌的语句，只返回“angry”，不要有其他内容；
            用户输入的内容是：{query}
            """
        chain = ChatPromptTemplate.from_template(prompt) | self.chatmodel | StrOutputParser()
        
        result = chain.invoke({"query": query})
        self.mood = result
        return result


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/chat")
def chat(query: str):
    agent = Agent()
    return agent.run(query)
    

@app.post("/add_urls")
def add_url():
    return {"message": "Add URL endpoint"}

@app.post("/add_pdfs")
def add_pdfs():
    return {"message": "Add PDF endpoint"}

@app.post("/add_texts")
def add_texts():
    return {"message": "Add text endpoint"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print("WebSocket disconnected")
        await websocket.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)