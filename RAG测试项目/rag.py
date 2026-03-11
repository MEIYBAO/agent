from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnablePassthrough  
from langchain_core.documents import Document  
from langchain_core.output_parsers import StrOutputParser

class RagService:
    def __init__(self):
        
        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model = config.embedding_model_name)
        )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system", 
                    "以我提供的已知参考资料为主，"
                    "简介和专业的回答用户问题。参考资料{context}。"
                    "如果不知道，请告知用户。" 
                ),

                ("user", "请回答用户提问{input}")
            ]
        )

        self.chat_model = ChatTongyi(model = config.chat_model_name)

        self.chain = self.__getchain()

    def __getchain(self):
        
        retriever = self.vector_service.get_retriever()

        def format_document(docs:list[Document]):
            '''格式化retriever的输出，变成prompt能用的形式'''
            if not docs:
               return "无相关资料"

            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"
            
            return formatted_str

        chain = (
           {
               "input":RunnablePassthrough(),
               "context":retriever | format_document
           } | self.prompt_template | self.chat_model | StrOutputParser()
       )
        
        return chain

if __name__ == "__main__":
    rag_service = RagService()
    res = rag_service.chain.invoke("我的专业是什么？")
    print(res)