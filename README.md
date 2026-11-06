# Triagem inclusiva de currículos com IA

Ferramenta que anonimiza currículos, compara cada um com os requisitos da vaga e gera um roteiro de entrevista estruturada. Ela **não dá nota, não ranqueia e não aprova ninguém**: organiza a informação para a pessoa recrutadora decidir.

> Demonstração com vaga e currículos **fictícios**.

## O problema

Em recrutamento de alto volume, a triagem manual cansa e abre espaço para viés: nome, idade, endereço, estado civil e pausas na carreira pesam mais do que deveriam. Já conduzi processos com mais de 150 candidatos por mês, incluindo vagas remotas voltadas principalmente a mulheres e mães no pós-pandemia; este projeto mostra como a IA pode deixar esse primeiro filtro mais justo e mais rápido.

## Como funciona

1. **Anonimização sem IA** (`anonimizar.py`): regras fixas removem nome, e-mail, telefone, CPF, RG, CEP, links, datas, idade, endereço, estado civil e campos parecidos. Por ser determinística, é testável e não depende do modelo.
2. **Comparação com a vaga** (`triagem.py`): o Claude recebe só o texto anonimizado e responde por uma ferramenta com esquema fixo: para cada requisito, **Evidenciado**, **Parcial** ou **Não evidenciado**, com o trecho que comprova.
3. **Regras contra viés no prompt:** lacuna de carreira não é ponto negativo; "não evidenciado" quer dizer que o currículo não mostra, não que a pessoa não sabe; proibido dar nota ou recomendar decisão.
4. **Roteiro de entrevista estruturada:** perguntas sobre os requisitos, iguais para qualquer candidato.
5. O resultado pode ser baixado em CSV e aberto no Excel ou no Google Sheets.

## Executar

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows  (Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
set ANTHROPIC_API_KEY=sua_chave   # Linux/Mac: export ANTHROPIC_API_KEY=sua_chave
streamlit run app.py
```

Use os arquivos de `exemplos/curriculos/`. A vaga de exemplo já vem preenchida e pode ser editada na tela. O modelo pode ser trocado pela variável `CLAUDE_MODEL`.

## Testes

```bash
pytest
```

Os testes conferem a anonimização nos currículos de exemplo e simulam a API, então rodam sem chave e sem internet.

## Estrutura

```
app.py            # interface Streamlit
anonimizar.py     # remoção de dados pessoais por regras
triagem.py        # prompt, chamada ao Claude e validação da resposta
exemplos/         # vaga e currículos fictícios
tests/            # testes
```

## Limitações

- A anonimização por regras cobre os formatos mais comuns, não todos; revise o texto anonimizado mostrado na tela.
- O próprio conteúdo da experiência pode revelar informações pessoais (por exemplo, "pausa para cuidar dos filhos"). Por isso o prompt proíbe tratar lacunas como ponto negativo.
- A decisão é sempre humana.

Feito por Danila Moraes com o apoio do Claude.
