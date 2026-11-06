"""Compara um currículo anonimizado com os requisitos da vaga e gera um roteiro
de entrevista estruturada. Não dá nota, não ranqueia e não aprova ninguém."""
from __future__ import annotations

import os

MODELO_PADRAO = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5")
SITUACOES = ("Evidenciado", "Parcial", "Não evidenciado")

FERRAMENTA = {
    "name": "registrar_triagem",
    "description": "Registra, para cada requisito da vaga, o que o currículo evidencia.",
    "input_schema": {
        "type": "object",
        "properties": {
            "requisitos": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "requisito": {"type": "string"},
                        "situacao": {"type": "string", "enum": list(SITUACOES)},
                        "evidencia": {"type": "string", "description": "Trecho do currículo, ou o que perguntar na entrevista."},
                    },
                    "required": ["requisito", "situacao", "evidencia"],
                },
            },
            "perguntas": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Perguntas de entrevista estruturada sobre os requisitos, iguais para qualquer candidato.",
            },
        },
        "required": ["requisitos", "perguntas"],
    },
}


def montar_prompt(vaga: str, curriculo_anonimo: str) -> str:
    return (
        "Você apoia uma triagem de currículos sem viés. Compare o currículo com cada requisito da vaga "
        "e chame registrar_triagem.\n"
        "Regras:\n"
        "- Avalie só competências e experiências descritas. Ignore nome, gênero, idade, endereço, "
        "estado civil, filhos, origem ou instituição de ensino como critério.\n"
        "- Lacunas de carreira não são ponto negativo.\n"
        "- Não dê nota, não compare com outros candidatos e não recomende aprovar ou reprovar.\n"
        "- 'Não evidenciado' significa que o currículo não mostra, não que a pessoa não sabe.\n"
        "- As perguntas devem ser objetivas, sobre os requisitos, e servir para qualquer candidato.\n\n"
        f"<vaga>\n{vaga}\n</vaga>\n\n<curriculo>\n{curriculo_anonimo}\n</curriculo>"
    )


def interpretar_resposta(resposta) -> dict:
    entrada = next(
        (b.input for b in resposta.content if getattr(b, "type", "") == "tool_use" and b.name == "registrar_triagem"),
        None,
    )
    if entrada is None:
        raise ValueError("O modelo não devolveu a triagem estruturada.")
    requisitos = []
    for r in entrada.get("requisitos", []):
        situacao = r.get("situacao") if r.get("situacao") in SITUACOES else "Não evidenciado"
        requisitos.append({"requisito": r.get("requisito", ""), "situacao": situacao, "evidencia": r.get("evidencia", "")})
    return {"requisitos": requisitos, "perguntas": list(entrada.get("perguntas", []))}


def triar(vaga: str, curriculo_anonimo: str, cliente=None, modelo: str = MODELO_PADRAO) -> dict:
    if cliente is None:
        import anthropic
        cliente = anthropic.Anthropic()  # lê ANTHROPIC_API_KEY do ambiente
    resposta = cliente.messages.create(
        model=modelo,
        max_tokens=3000,
        tools=[FERRAMENTA],
        tool_choice={"type": "tool", "name": "registrar_triagem"},
        messages=[{"role": "user", "content": montar_prompt(vaga, curriculo_anonimo)}],
    )
    return interpretar_resposta(resposta)
