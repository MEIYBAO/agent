import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

def check_md5(md5_str:str):
    '''检查传入的md5是否已被处理过''' 

    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w',encoding='utf-8').close()  # 创建文件
        return False
    else:
        for line in open(config.md5_path, 'r',encoding='utf-8').readlines():  # 读取文件内容 
            line = line.strip()  # 处理前后空格和回车
            if line == md5_str:  # 如果md5值已存在，说明已处理过
                return True
        return False  


def save_md5(md5_str:str):
    
    with open(config.md5_path, 'a',encoding='utf-8') as f:
        f.write(md5_str + '\n')  # 将md5值写入文件，换行分隔
    

def get_string_md5(input_str:str,encoding='utf-8'):
    '''获取字符串的md5值'''
    
    str_bytes = input_str.encode(encoding = encoding)  # 将字符串编码为字节
    md5 = hashlib.md5()
    md5.update(str_bytes)

    return md5.hexdigest()


class KnowledgeBaseService(object):

    def __init__(self):

        os.makedirs(config.persist_directory, exist_ok=True)  # 创建向量存储目录

        #向量存储的示例
        self.chroma = Chroma(
            collection_name=config.collection_name, #数据库表名
            embedding_function=DashScopeEmbeddings(model = "text-embedding-v4"), #向量化函数
            persist_directory=config.persist_directory, #向量存储路径
        )  

        #文本分割器的对象
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,  # 分割后的文本块大小
            chunk_overlap=config.chunk_overlap,  # 分割后的文本块重叠部分大小
            separators=config.separators,  # 分割文本的分隔符列表
            length_function=len,  # 计算文本长度的函数，这里使用内置的len函数
        )


    def upload_by_str(self,data:str,filename):
        '''通过字符串上传数据到知识库'''
        
        md5_str = get_string_md5(data)  

        if check_md5(md5_str):  
            return "[跳过]数据已存在"
        
        #文本分割
        if len(data) > config.max_split_char_number:
            knowledge_chunks = self.splitter.split_text(data)  

        else:
            knowledge_chunks = [data]  # 如果文本长度不超过最大分割字符数，则直接使用原文本作为一个块

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "admin",
            }  
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks],
        )  

        save_md5(md5_str)  
        
        return "[成功]数据已上传!"

if __name__ == "__main__":
    service = KnowledgeBaseService()
    service.upload_by_str("这是一个测试文本。", "test.txt")

