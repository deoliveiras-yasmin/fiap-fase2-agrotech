# 🌾 Comparador de colheita de Cana (Agrotech)
**Projeto da Fase 2 - FIAP: Agronegócio e Phython**
**Autora:** Yasmin de Oliveira e Silva
**Curso:** Inteligência Artificial
**Data:** Outubro / 2025
**Repositório GitHub:** [https://github.com/deoliveiras-yasmin/fiap-fase2-agrotech]

---

## 🧭 Contexto

O agronegócio brasileiro é um dos pilares da economia nacional, responsável por uma grande fatia do PIB e por milhões de empregos.  
Dentro deste universo, o setor **sucroalcooleiro (cana-de-açúcar)** se destaca mundialmente, mas ainda enfrenta perdas significativas no processo de colheita.

- A **colheita manual** apresenta **menores perdas** (≈5%), mas é lenta e de alto custo operacional.  
- A **colheita mecanizada** é muito mais rápida, porém pode gerar **perdas de até 15%** da produção.

Este projeto propõe uma **solução Agrotech** que ajuda o produtor rural a comparar os dois métodos de colheita, estimando o impacto financeiro real — considerando o tempo, o custo e a penalidade por atraso.

---

## 💡 Solução e Inovação

O **Comparador de Colheita de Cana** simula de forma prática a produtividade, as perdas e o lucro líquido de cada método, permitindo uma análise comparativa clara e objetiva.

### 🔍 Funcionalidades Principais:
- Cálculo de perdas (básicas e penalidades por atraso);
- Comparação de lucro líquido, tempo de colheita e custos;
- Armazenamento automático dos resultados em arquivos locais:
  - `outputs/simulacoes_cana.json`
  - `outputs/relatorio_simples.txt`

### 🌱 Inovação:
Além da comparação direta entre métodos, o projeto introduz o **fator tempo** como variável crítica.  
Isso permite entender como **atrasos no ciclo de colheita** impactam o lucro final — uma visão mais realista e alinhada à dinâmica do campo moderno.

---

## 🧩 Estrutura Técnica

Toda a lógica foi construída em **Python 3**, aplicando os conceitos dos **Capítulos 3 a 6** da Fase 2 da disciplina.

| Capítulo | Conteúdo Didático | Aplicação no Projeto |
|-----------|-------------------|----------------------|
| 3 | Subalgoritmos (Funções e Procedimentos) | Funções como `calcular_resultados()` e `comparar_metodos()` |
| 4 | Estruturas de Dados (Listas, Tuplas e Dicionários) | Uso de **tuplas** para constantes, **dicionários** para dados de simulação e **listas** para o histórico |
| 5 | Manipulação de Arquivos (TXT e JSON) | Gravação de relatórios `.txt` e histórico `.json` |
| 6 | Banco de Dados e Exceções | Simulação de conexão Oracle com `try/except` e validação de entrada de dados |

---

### Pré-requisitos
- **Python 3.x** instalado  
- (Opcional) Biblioteca `cx_Oracle` para simulação de conexão com banco de dados

### Instalação da dependência (opcional)
```bash
pip install cx_Oracle
```

## 🏗️ Estrutura de pastas esperada:
```bash
comparador-de-colheita/
├─ src/
│  └─ comparador_de_colheita_de_cana.py
├─ outputs/
│  ├─ simulacoes_cana.json
│  └─ relatorio_simples.txt
└─ README.md
```

## ▶️ Execução

Na raiz do projeto, execute:

`python src/comparador_de_colheita_de_cana.py`

Siga o menu interativo exibido no terminal para realizar as simulações.

## 💾 Simulação de Conexão Oracle

**Nota sobre Conexão Oracle (Simulação):**
A conexão com banco de dados Oracle é apenas uma **simulação** implementada via blocos try/except.
Por motivos de segurança e privacidade, não foram incluídas credenciais reais nem tentativas de conexão remota.

Caso o avaliador deseje testar a conexão em ambiente controlado, basta instalar o driver `cx_Oracle` e atualizar a função `conectar_oracle()` com as credenciais e parâmetros do serviço.

Essa abordagem garante privacidade e segurança dos dados e demonstra domínio técnico do processo de conexão, mesmo sem acesso ao ambiente real.

> **📊 Exemplo de Saída Simplificada**
>
>```bash
> Método: Colheita Manual
> Área: 100 ha | Produção Esperada: 9000 t
> Tempo: 10 dias | Custo: R$ 50.000 | Perdas: 5%
> Lucro Líquido: R$ 430.000
>
> Método: Colheita Mecânica
> Área: 100 ha | Produção Esperada: 9000 t
> Tempo: 3 dias | Custo: R$ 35.000 | Perdas: 15%
> Lucro Líquido: R$ 400.000
>
> ✅ Resultado: A colheita manual gera maior lucro, mas demanda mais tempo.
>```

## 🧠 Conceitos Aplicados

- Estruturas de dados complexas (listas, tuplas e dicionários)

- Subalgoritmos com passagem de parâmetros

- Manipulação eficiente de arquivos texto e JSON

- Simulação de conexão com banco Oracle

- Tratamento robusto de exceções e validação de entrada

## 🤖 Observação Ética e Acadêmica

Este projeto foi desenvolvido pela estudante **Yasmin de Oliveira e Silva**, com base nos conteúdos das apostilas da FIAP (Fase 2 – Capítulos 3 a 6).

O desenvolvimento contou com o **apoio técnico** de assistentes de IA (ChatGPT e Gemini) para otimização e revisão de código, mas toda a lógica, estrutura e conceito Agrotech foram definidos pela autora, refletindo compreensão prática dos temas estudados.

## 📜 Licença

Projeto educacional - FIAP 2025

> ⚠️ Projeto acadêmico de autoria de **Yasmin de Oliveira e Silva**, desenvolvido para a disciplina de Computational Thinking with Python (FIAP 2025). Uso e reprodução proibidos sem referência.
