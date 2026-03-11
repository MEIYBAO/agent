from langchain_community.chat_models.tongyi import ChatTongyi
import os

model = ChatTongyi(
    model="qwen3-max",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

messages = [
    ('system', "你是一个人工智能助手，名字叫小梅梅，协助用户完成任务，并且不说废话简单回答。"),
    ('user', "告诉我你的名字是什么？"),
]

res = model.stream(input = messages)

for chunk in res:
    print(chunk.content, end="", flush=True)
