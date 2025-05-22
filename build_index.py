import sys
import os
from app.parser import parsear_politicas, convertir_a_documentos
from app.embedding_store import build_vectorstore
pdf_path = "data/politicas_internas.pdf"
print("Parseando el documento...")
politicas = parsear_politicas(pdf_path)
print("Convirtiendo a documentos...")
documentos = convertir_a_documentos(politicas)
print("Construyendo vectorstore FAISS...")
build_vectorstore(documentos)
print("¡Índice creado y guardado exitosamente!")
