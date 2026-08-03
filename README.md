# 🤖 BI Copiloto — Agente Text-to-SQL em Português

<p align="left">
  <img src="https://img.shields.io/badge/status-em%20desenvolvimento-yellow" alt="status"/>
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white" alt="python"/>
  <img src="https://img.shields.io/badge/PostgreSQL-local-336791?logo=postgresql&logoColor=white" alt="postgresql"/>
  <img src="https://img.shields.io/badge/Google_Gemini-2.5%20Flash-8E75B2?logo=googlegemini&logoColor=white" alt="gemini"/>
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license"/>
</p>

> Um agente de IA que entende perguntas de negócio em **linguagem natural (PT-BR)**, traduz para **SQL**, executa em um banco de dados relacional e devolve a resposta — inspirado no **Genie (Databricks)**, construído do zero e integrado ao **Google Gemini**.

---

## 📑 Sumário

- [Objetivo do Projeto](#-objetivo-do-projeto)
- [Demonstração](#-demonstração)
- [Arquitetura](#️-arquitetura-visão-geral)
- [Fonte de Dados e Modelo Relacional](#️-fonte-de-dados)
- [Stack Técnica](#️-stack-técnica)
- [Status Atual](#-status-atual-do-projeto)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Como Rodar o Projeto](#-como-rodar-o-projeto)
- [Roadmap](#️-roadmap)
- [Autor](#-autor)

---

## 🎯 Objetivo do Projeto

Empresas de grande porte (bancos, e-commerces, fintechs) vêm investindo em ferramentas de **"self-service BI" com IA generativa**, nas quais qualquer pessoa do negócio — sem saber SQL — consegue fazer perguntas em linguagem natural e obter respostas analíticas na hora.

Este projeto reproduz esse conceito de forma independente e documentada ponta a ponta, com três objetivos centrais:

1. **Demonstrar domínio prático de engenharia de dados** — modelagem relacional, ETL e SQL avançado — combinado com **GenAI aplicada a dados**.
2. **Entender e reimplementar, na prática, os componentes internos** de uma ferramenta como o Genie: introspecção de schema, geração de SQL via LLM, execução segura e formatação de resposta.
3. **Construir um artefato de portfólio de alto impacto**, unindo BI tradicional e IA generativa — uma das áreas de maior demanda no mercado de dados hoje.

---

## 🖥️ Demonstração

Exemplo real de uso do agente no terminal (versão atual, `agente_manual.py`):

```text
Você: Quantos clientes temos no estado de São Paulo (SP)?

🔎 SQL gerado pelo Gemini:
SELECT COUNT(*) AS total_clientes
FROM clientes
WHERE estado_cliente = 'SP';

📊 Resultado:
 total_clientes
----------------
     41746
```

> O agente recebe a pergunta em português, monta o prompt com o schema do banco (via introspecção), gera a query com o Gemini, executa no PostgreSQL via SQLAlchemy e apresenta o resultado formatado.

---

## 🏗️ Arquitetura (visão geral)

```text
┌─────────────────────────────┐
│   Pergunta do usuário        │
│         (PT-BR)              │
└──────────────┬───────────────┘
               ▼
┌─────────────────────────────┐
│  Introspecção do Schema      │
│  (information_schema)        │
└──────────────┬───────────────┘
               ▼
┌─────────────────────────────┐
│  Agente Text-to-SQL          │
│  Google Gemini 2.5/2.0 Flash │
└──────────────┬───────────────┘
               ▼
┌─────────────────────────────┐
│  Geração da query SQL        │
└──────────────┬───────────────┘
               ▼
┌─────────────────────────────┐
│  Execução no PostgreSQL      │
│  via SQLAlchemy              │
└──────────────┬───────────────┘
               ▼
┌─────────────────────────────┐
│  Resposta estruturada        │
│  (colunas, linhas, resultado)│
└─────────────────────────────┘
```

**Por que esse desenho?** Ele espelha o padrão usado por ferramentas comerciais de Text-to-SQL: o LLM nunca "adivinha" a estrutura do banco — ele recebe o schema real como contexto (introspecção), o que reduz alucinação e aumenta a taxa de acerto das queries geradas.

---

## 🗃️ Fonte de Dados

Dataset público **[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)**, com ~100 mil pedidos reais de um marketplace brasileiro (2016–2018), incluindo dados de clientes, produtos, pagamentos, avaliações e vendedores.

### Modelo relacional implementado

| Tabela (PT-BR) | Origem (CSV Olist) | Papel no modelo |
| --- | --- | --- |
| `clientes` | `olist_customers_dataset.csv` | Dados do cliente e localização |
| `pedidos` | `olist_orders_dataset.csv` | Tabela central — datas e status do pedido |
| `itens_pedido` | `olist_order_items_dataset.csv` | Itens, preços e frete de cada pedido |
| `produtos` | `olist_products_dataset.csv` | Catálogo de produtos e categoria |
| `vendedores` | `olist_sellers_dataset.csv` | Dados do vendedor |
| `pagamentos_pedido` | `olist_order_payments_dataset.csv` | Forma de pagamento e valores |
| `avaliacoes_pedido` | `olist_order_reviews_dataset.csv` | Notas e comentários de avaliação |
| `traducao_categoria` | `product_category_name_translation.csv` | Tradução das categorias de produto |
| `geolocalizacao` | `olist_geolocation_dataset.csv` | Coordenadas geográficas (uso futuro/opcional) |

Todas as tabelas possuem chaves primárias e relacionamentos (FKs) definidos, garantindo integridade referencial e permitindo consultas com JOINs complexos — essencial para que o LLM gere SQL correto em perguntas que cruzam múltiplas tabelas.

---

## 🛠️ Stack Técnica

| Camada | Tecnologia |
| --- | --- |
| Banco de dados | PostgreSQL (local) |
| Linguagem | Python 3.11 |
| ETL & Conexão | Pandas, SQLAlchemy, Psycopg2 |
| IA Generativa | Google GenAI SDK (`google-genai`) |
| Modelo LLM | Gemini 2.5 / 2.0 Flash |
| Introspecção de schema | `information_schema` (nativo PostgreSQL) |

---

## 📌 Status Atual do Projeto

**Concluído**
- [x] Modelagem do banco de dados relacional (9 tabelas)
- [x] Script de carga automatizada dos CSVs para o PostgreSQL (`carregar_olisit.py`)
- [x] Definição de chaves primárias e estrangeiras (`adicionar_relacionamento_nas_tabelas.sql`)
- [x] Correção de inconsistências do dataset original (categorias de produto faltantes)
- [x] Camada de introspecção de schema para contexto do LLM (`introspeccao.py`)
- [x] Agente Text-to-SQL manual funcional (`agente_manual.py`), integrado ao PostgreSQL e ao Gemini

**Em andamento / próximos passos**
- [ ] Camada de segurança avançada (validação de SQL, usuário read-only, `LIMIT` automático)
- [ ] Geração automática de gráfico conforme o shape do resultado
- [ ] Geração de resumo executivo via LLM
- [ ] Interface em Streamlit
- [ ] Testes com bateria de perguntas de negócio (taxa de acerto)

---

## 📂 Estrutura do Repositório

```text
bi_text_to_sql/
├── README.md
├── agente_manual.py                          # Script principal do Agente Text-to-SQL (Gemini + PostgreSQL)
├── carregar_olisit.py                        # ETL: carrega os CSVs Olist no PostgreSQL
├── adicionar_relacionamento_nas_tabelas.sql   # Criação de PKs, FKs e correções de dados
└── introspeccao.py                           # Extração de schema do information_schema para contexto de IA
```

---

## 🚀 Como Rodar o Projeto

1. **Banco de dados**: tenha o PostgreSQL rodando localmente (ou via Docker) e crie um banco vazio chamado `projeto_BI_TEXT_TO_SQL`.
2. **Dados**: baixe o dataset Olist no [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) e execute a carga com `carregar_olisit.py`, seguida do script `adicionar_relacionamento_nas_tabelas.sql`.
3. **Dependências**:
   ```bash
   pip install pandas sqlalchemy psycopg2-binary google-genai
   ```
4. **Chave de API do Gemini**:
   ```bash
   export GEMINI_API_KEY="sua_chave_aqui"
   ```
5. **Executar o agente**:
   ```bash
   python agente_manual.py
   ```

---

## 🗺️ Roadmap

O projeto está evoluindo em três frentes principais, do agente manual até uma solução com interface completa:

1. **Fase atual — Agente manual (Gemini puro)**: prompt engineering direto, sem framework, para dominar os fundamentos do Text-to-SQL.
2. **Próxima fase — Migração para LangChain**: uso de *SQL Agents* e *tools* para orquestração mais robusta, com validação e retries automáticos.
3. **Fase futura — Interface Streamlit**: camada visual para que qualquer usuário de negócio interaja com o agente sem precisar do terminal.
4. **Fase opcional — Refatoração com LangGraph**: fluxo multi-etapas (geração → validação → execução → resumo) modelado como grafo de estados.

---

## 👤 Autor

**Vinícius Caetano**
Analista de Dados Jr. | Estudante de Análise e Desenvolvimento de Sistemas (ADS)

[GitHub](https://github.com/Caetanodassis) · [LinkedIn](https://linkedin.com/in/viniciusasiss)