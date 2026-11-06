"""Interface Streamlit da triagem inclusiva."""
import time
from pathlib import Path

import pandas as pd
import streamlit as st
from pypdf import PdfReader

from anonimizar import anonimizar
from triagem import triar

st.set_page_config(page_title="Triagem inclusiva com IA", page_icon="🤝", layout="wide")
st.title("🤝 Triagem inclusiva de currículos com IA")
st.caption("Demonstração com currículos fictícios. A ferramenta organiza; quem decide é a pessoa recrutadora.")

vaga_exemplo = Path("exemplos/vaga.txt").read_text(encoding="utf-8")
vaga = st.text_area("Requisitos da vaga", vaga_exemplo, height=200)
arquivos = st.file_uploader("Currículos (PDF ou TXT)", type=["pdf", "txt"], accept_multiple_files=True)


def ler(arquivo) -> str:
    if arquivo.name.lower().endswith(".pdf"):
        return "\n".join(p.extract_text() or "" for p in PdfReader(arquivo).pages)
    return arquivo.read().decode("utf-8")


if st.button("Triar", type="primary", disabled=not arquivos):
    inicio = time.perf_counter()
    linhas = []
    for n, arquivo in enumerate(arquivos, start=1):
        codigo = f"Candidato {n:02d}"
        anonimo = anonimizar(ler(arquivo))
        with st.spinner(f"Analisando {codigo}..."):
            resultado = triar(vaga, anonimo)
        with st.expander(codigo, expanded=n == 1):
            col1, col2 = st.columns(2)
            col1.markdown("**Currículo anonimizado**")
            col1.text(anonimo)
            col2.markdown("**Requisitos**")
            col2.dataframe(pd.DataFrame(resultado["requisitos"]), hide_index=True)
            col2.markdown("**Roteiro de entrevista estruturada**")
            col2.markdown("\n".join(f"{i}. {p}" for i, p in enumerate(resultado["perguntas"], 1)))
        linhas += [{"candidato": codigo, **r} for r in resultado["requisitos"]]
    st.success(f"{len(arquivos)} currículo(s) triado(s) em {time.perf_counter() - inicio:.0f} s.")
    st.download_button("Baixar planilha (CSV para Excel/Google Sheets)",
                       pd.DataFrame(linhas).to_csv(index=False).encode("utf-8-sig"), "triagem.csv", "text/csv")
