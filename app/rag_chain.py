import os
from transformers import AutoTokenizer, T5ForConditionalGeneration, pipeline
from langchain_community.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from huggingface_hub import login

# === Autenticación opcional para modelos gated ===
hf_token = os.environ.get("HF_TOKEN")
if hf_token:
    login(token=hf_token)

# === Modelo FLAN-T5-LARGE ===
REMOTE_ID = "google/flan-t5-large"
print("Usando modelo LLM Flan-T5-Large desde Hugging Face")

# === Cargar tokenizer y modelo ===
tokenizer = AutoTokenizer.from_pretrained(REMOTE_ID)
model = T5ForConditionalGeneration.from_pretrained(REMOTE_ID)

# === Enviar a CPU ===
device = "cpu"
model = model.to(device)

# === Crear pipeline con parámetros custom ===
pipe = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    temperature=0.1,
    do_sample=True,
    repetition_penalty=1.1
)

llm = HuggingFacePipeline(pipeline=pipe)

# === Prompt personalizado ===
def get_prompt():
    return PromptTemplate(
        input_variables=["context", "question"],
        template=""" 
Eres un asistente especializado en el reglamento interno de una firma de servicios profesionales.
A continuación se presenta una consulta sobre el reglamento interno de una firma de servicios profesionales.
Basate únicamente en el contexto proporcionado para responder en español y de forma conversacional.
Indicá claramente Título, Capítulo y Subcapítulo si están presentes.
Si no sabés la respuesta, escribí: "No lo sé".
Finalizá siempre con: "Recomendación: Consultá con Talento y Cultura para más información."

=== CONTEXTO ===
{context}

=== PREGUNTA ===
{question}

=== RESPUESTA ===

"""
    )

# === Formatear documentos con truncado por tokens ===
def format_docs(docs, max_tokens=900):
    combined = "\n\n".join(
        f"Artículo: {doc.metadata.get('articulo', '')} | "
        f"Capítulo: {doc.metadata.get('capitulo', '')} | "
        f"Subcapítulo: {doc.metadata.get('subcapitulo', '')} - {doc.metadata.get('subtitulo', '')}\n"
        f"{doc.page_content.strip()}"
        for doc in docs
    )
    inputs = tokenizer(combined, return_tensors="pt", truncation=True, max_length=max_tokens)
    return tokenizer.decode(inputs.input_ids[0], skip_special_tokens=True)

# === Cargar LLM para FastAPI ===
def load_llm():
    return llm

# === Cadena RAG estilo LangChain Core ===
def build_rag_chain(retriever):
    prompt = get_prompt()

    return (
        {
            "context": (lambda x: x["question"]) | retriever | (lambda docs: format_docs(docs)),
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )