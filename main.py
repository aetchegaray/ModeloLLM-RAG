# === main.py (API con FastAPI) ===
from fastapi import FastAPI
from pydantic import BaseModel
from app.embedding_store import load_vectorstore
from app.rag_chain import build_rag_chain, format_docs
from langchain.chains import RetrievalQA
import time
import logging
import os

# Crear carpeta logs si no existe
os.makedirs("logs", exist_ok=True)

# Configuración de logging
logging.basicConfig(level=logging.INFO, filename="logs/api.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Inicializar FastAPI
app = FastAPI(title="Asistente de Políticas Internas")

# Inicializar recursos compartidos
vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
rag_chain = build_rag_chain(retriever)

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def query_rag(req: QueryRequest):
    start_time = time.perf_counter()
    question = req.question

    # Recuperar documentos relevantes
    docs = retriever.get_relevant_documents(question)

    # Preparar fragmentos contextuales
    context_docs = [
        {
            "articulo": doc.metadata.get("articulo", ""),
            "titulo": doc.metadata.get("titulo", ""),
            "capitulo": doc.metadata.get("capitulo", ""),
            "subcapitulo": doc.metadata.get("subcapitulo", ""),
            "subtitulo": doc.metadata.get("subtitulo", ""),
            "contenido": doc.page_content
        }
        for doc in docs
    ]
    formatted_context = format_docs(docs)

    # Ejecutar RAG
    result = rag_chain.invoke({"question": question})

    # Fallback: usar primer fragmento si el modelo no responde
    if result.strip().lower().startswith("no lo sé") or not result.strip():
        print("Aplicando fallback: mostrando fragmento en lugar del LLM")
        result = docs[0].page_content if docs else "No se encontró contenido relevante."

    elapsed = time.perf_counter() - start_time

    # Indicar si se activó el fallback
    fallback_used = result.strip().lower() == docs[0].page_content.strip().lower()

    return {
    "answer": result,
    "response_time": f"{elapsed:.2f}s",
    "context_docs": context_docs,
    "fallback": fallback_used
    }