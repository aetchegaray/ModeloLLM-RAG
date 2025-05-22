# app/parser.py
import re
from pdfminer.high_level import extract_text
from langchain_core.documents import Document

def parsear_politicas(path_pdf):
    texto = extract_text(path_pdf)
    
    # Dividir por artículos, conservando los encabezados si están presentes
    articulos_raw = re.split(r"(?:Artículo|Articulo)\s+\d+", texto, flags=re.IGNORECASE)
    articulos_raw = [a.strip() for a in articulos_raw if a.strip()]

    politicas = []
    for i, articulo in enumerate(articulos_raw, start=1):
        match_titulo = re.search(r"T[ií]tulo:\s*(.*?)\n", articulo)
        match_contenido = re.search(r"Contenido:\s*(.*)", articulo, re.DOTALL)
        if not match_titulo or not match_contenido:
            continue

        titulo = match_titulo.group(1).strip()
        contenido = match_contenido.group(1).strip()

        capitulos_raw = re.split(r"\n(?=\d+\.\s*Cap[ií]tulo:)", contenido)
        capitulos = []
        for cap in capitulos_raw:
            match_cap = re.match(r"(\d+\.\s*Cap[ií]tulo:\s*.*)", cap.strip(), re.DOTALL)
            if not match_cap:
                continue
            cap_texto = match_cap.group(1).strip()
            cap_titulo = re.search(r"\d+\.\s*Cap[ií]tulo:\s*(.*)", cap_texto)
            cap_titulo = cap_titulo.group(1).strip() if cap_titulo else "Sin título"

            subcap_matches = re.findall(
                r"(\d+\.\d+)\.\s*Subcap[ií]tulo:\s*(.?)\n(.?)(?=\n\d+\.\d+\.|$)",
                cap_texto,
                re.DOTALL
            )
            subcaps = [{
                "subnumero": s[0].strip(),
                "subtitulo": s[1].strip(),
                "subcontenido": s[2].strip()
            } for s in subcap_matches]

            capitulos.append({
                "titulo": cap_titulo,
                "contenido": cap_texto,
                "subcapitulos": subcaps
            })

        politicas.append({
            "articulo": f"Artículo {i}",
            "titulo": titulo,
            "capitulos": capitulos
        })
    return politicas


def convertir_a_documentos(politicas):
    documentos = []
    for politica in politicas:
        for cap in politica["capitulos"]:
            if not cap["subcapitulos"]:
                texto_cap = (
                    f"{politica['articulo']} - TÍTULO: {politica['titulo']} - CAPÍTULO: {cap['titulo']}\n\n{cap['contenido']}"
                )
                documentos.append(Document(
                    page_content=texto_cap,
                    metadata={
                        "articulo": politica["articulo"],
                        "titulo": politica['titulo'],
                        "capitulo": cap["titulo"]
                    }
                ))
            else:
                for sub in cap["subcapitulos"]:
                    texto_sub = (
                        f"{politica['articulo']} - TÍTULO: {politica['titulo']} - CAPÍTULO: {cap['titulo']} - "
                        f"SUBCAPÍTULO {sub['subnumero']}: {sub['subtitulo']}\n\n{sub['subcontenido']}"
                    )
                    documentos.append(Document(
                        page_content=texto_sub,
                        metadata={
                            "articulo": politica["articulo"],
                            "titulo": politica['titulo'],
                            "capitulo": cap["titulo"],
                            "subcapitulo": sub["subnumero"],
                            "subtitulo": sub["subtitulo"]
                        }
                    ))
    return documentos