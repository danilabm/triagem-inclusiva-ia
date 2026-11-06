from pathlib import Path
from types import SimpleNamespace

from anonimizar import anonimizar
from triagem import montar_prompt, triar

EXEMPLOS = Path(__file__).parent.parent / "exemplos" / "curriculos"


def test_anonimiza_dados_pessoais():
    texto = anonimizar((EXEMPLOS / "curriculo_01.txt").read_text(encoding="utf-8"))
    for dado in ["Carla", "carla.ficticia@exemplo.com", "91234-5678", "Rua Inventada", "12/03/1985", "casada"]:
        assert dado not in texto, dado
    assert "relatórios semanais de indicadores" in texto  # competência continua


def test_anonimiza_cpf_link_e_idade():
    texto = anonimizar((EXEMPLOS / "curriculo_02.txt").read_text(encoding="utf-8"))
    for dado in ["Rafael", "123.456.789-00", "linkedin.com/in/rafael-exemplo", "29 anos", "99876-5432"]:
        assert dado not in texto, dado
    assert "Power BI" in texto


def test_prompt_proibe_nota_e_decisao():
    prompt = montar_prompt("vaga", "cv")
    assert "Não dê nota" in prompt and "Lacunas de carreira não são ponto negativo" in prompt


class ClienteFalso:
    def __init__(self, entrada):
        self.entrada = entrada
        self.messages = self

    def create(self, **kwargs):
        bloco = SimpleNamespace(type="tool_use", name="registrar_triagem", input=self.entrada)
        return SimpleNamespace(content=[bloco])


def test_situacao_invalida_vira_nao_evidenciado():
    cliente = ClienteFalso({"requisitos": [{"requisito": "Excel", "situacao": "Aprovado", "evidencia": "x"}],
                            "perguntas": ["Conte um relatório que você montou."]})
    resultado = triar("vaga", "cv", cliente=cliente)
    assert resultado["requisitos"][0]["situacao"] == "Não evidenciado"
    assert resultado["perguntas"] == ["Conte um relatório que você montou."]
