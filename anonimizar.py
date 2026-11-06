"""Remove do currículo dados que não dizem nada sobre competência e abrem espaço
para viés: nome, contatos, documentos, endereço, idade, estado civil e foto."""
from __future__ import annotations

import re

PADROES = [
    (r"[\w.+-]+@[\w-]+\.[\w.]+", "[e-mail]"),
    (r"https?://\S+|www\.\S+|linkedin\.com/\S+", "[link]"),
    (r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b", "[CPF]"),
    (r"\b\d{2}\.?\d{3}\.?\d{3}-?[\dxX]\b", "[RG]"),
    (r"\(?\b\d{2}\)?\s?9?\d{4}-?\d{4}\b", "[telefone]"),
    (r"\b\d{5}-?\d{3}\b", "[CEP]"),
    (r"\b\d{1,2}/\d{1,2}/(19|20)\d{2}\b", "[data]"),
    (r"\b\d{2}\s+anos\b", "[idade]"),
]

CAMPOS_PESSOAIS = re.compile(
    r"^\s*(nome|endere[cç]o|bairro|cidade|data de nascimento|nascimento|idade|estado civil|"
    r"nacionalidade|naturalidade|g[eê]nero|sexo|filhos|foto|religi[aã]o)\s*:.*$",
    re.IGNORECASE | re.MULTILINE,
)


def anonimizar(texto: str) -> str:
    linhas = texto.strip().splitlines()
    # A primeira linha não vazia de um currículo costuma ser o nome.
    if linhas and ":" not in linhas[0] and len(linhas[0].split()) <= 6:
        linhas[0] = "[nome removido]"
    texto = "\n".join(linhas)
    texto = CAMPOS_PESSOAIS.sub(lambda m: f"{m.group(1).capitalize()}: [removido]", texto)
    for padrao, troca in PADROES:
        texto = re.sub(padrao, troca, texto)
    return texto
