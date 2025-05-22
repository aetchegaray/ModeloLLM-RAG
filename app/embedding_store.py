# app/embedding_store.py
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

#LOCAL_PATH = "models/e5-large-v2"
REMOTE_ID = "intfloat/e5-large-v2"

def get_embedding_model():
    # if os.path.exists(LOCAL_PATH):
    #     print("Usando embeddings locales")
    #     return HuggingFaceEmbeddings(
    #         model_name=LOCAL_PATH
    #     )
    # else:
    print("Usando embeddings desde Hugging Face")
    return HuggingFaceEmbeddings(
        model_name=REMOTE_ID
    )

def build_vectorstore(documentos, persist_path="app/model_data/faiss_index"):
    embeddings = get_embedding_model()
    db = FAISS.from_documents(documentos, embeddings)
    db.save_local(persist_path)
    return db

def load_vectorstore(persist_path="app/model_data/faiss_index"):
    embeddings = get_embedding_model()
    return FAISS.load_local(persist_path, embeddings, allow_dangerous_deserialization=True)