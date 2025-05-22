from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
import os

# === Modelo LLM ===
llm_id = "mistralai/Mistral-7B-Instruct-v0.2"
llm_path = "models/mistral-7b-instruct"
os.makedirs(llm_path, exist_ok=True)

# === Modelo de embeddings ===
embed_id = "intfloat/e5-large-v2"
embed_path = "models/e5-large-v2"
os.makedirs(embed_path, exist_ok=True)

# === Descargar modelo LLM (Mistral) ===
print("🔽 Descargando modelo LLM Mistral...")
AutoTokenizer.from_pretrained(llm_id, cache_dir=llm_path, trust_remote_code=True, use_fast=False)
AutoModelForCausalLM.from_pretrained(llm_id, cache_dir=llm_path, trust_remote_code=True)
print("✅ Mistral descargado en", llm_path)

# === Descargar modelo de embeddings E5 ===
print("🔽 Descargando modelo de embeddings E5...")
SentenceTransformer(embed_id, cache_folder=embed_path)
print("✅ Embeddings descargados en", embed_path)