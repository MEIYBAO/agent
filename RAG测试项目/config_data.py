
md5_path = "./md5.text"  # 存储已处理的md5值的文件路径

#chroma
collection_name = "rag"  # 向量存储的数据库表名
persist_directory = "./chroma_db"  # 向量存储的路径

#splitter
chunk_size = 1000  # 分割后的文本块大小
chunk_overlap = 100  # 分割后的文本块重叠部分大小
separators = ["\n\n", "\n", ".", "!", "?", ",", "，", "。", "！", "？"," ",""]  # 分割文本的分隔符列表
max_split_char_number = 1000  

#
similarity_threshold = 2  # 向量检索的文档个数

embedding_model_name = "text-embedding-v4"  # 向量化模型名称
chat_model_name = "qwen3-max"  # 聊天模型名称

session_config = {
    "configurable": {
        "session_id": "user_001",
    }
}