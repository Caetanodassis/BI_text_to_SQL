```markdown
# 🤖 BI Copiloto — Agente Text-to-SQL em Português

> Um agente de IA que entende perguntas de negócio em linguagem natural, traduz para SQL, executa no banco de dados e responde com análise — inspirado no **Genie (Databricks)**, construído do zero e integrado via **Google Gemini (Nuvem)** com **PostgreSQL**.

---

## 🎯 Objetivo do Projeto

Empresas de grande porte (bancos, e-commerces, fintechs) estão investindo em ferramentas de **"self-service BI" com IA generativa**, onde qualquer pessoa do negócio — sem saber SQL — consegue fazer perguntas e obter respostas analíticas na hora.

Este projeto reproduz esse conceito de forma independente, com o objetivo de:

- Demonstrar domínio prático de **engenharia de dados** (modelagem relacional, ETL, SQL avançado) combinado com **GenAI/agentes de IA**;
- Entender e implementar, na prática, os componentes internos de uma ferramenta como o Genie: introspecção de schema, geração de SQL via LLM e execução integrada;
- Construir um artefato de portfólio que una **BI tradicional** e **IA aplicada a dados**, área de forte demanda no mercado.

**Pergunta que o agente já responde, por exemplo:**
> *"Quantos clientes temos no estado de São Paulo (SP)?"*

E devolve no terminal: a query SQL gerada pelo Gemini e o resultado executado diretamente no PostgreSQL.

---

## 🏗️ Arquitetura (visão geral)


```

Pergunta do usuário (PT-BR)
│
▼
Agente Text-to-SQL (Google Gemini 2.5 Flash / 2.0 Flash)
│  contexto: schema do banco Olist (PostgreSQL)
▼
Geração de query SQL
│
▼
Execução no PostgreSQL via SQLAlchemy
│
▼
Exibição de colunas, linhas e resultados estruturados no terminal

```

---

## 🗃️ Fonte de Dados

Dataset público **[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)**, contendo ~100 mil pedidos reais de um marketplace brasileiro (2016-2018), com informações de clientes, produtos, pagamentos, avaliações e vendedores.

### Modelo relacional implementado

| Tabela (PT-BR) | Origem (CSV Olist) | Papel no modelo |
|---|---|---|
| `clientes` | `olist_customers_dataset.csv` | Dados do cliente e localização |
| `pedidos` | `olist_orders_dataset.csv` | Tabela central — datas e status do pedido |
| `itens_pedido` | `olist_order_items_dataset.csv` | Itens, preços e frete de cada pedido |
| `produtos` | `olist_products_dataset.csv` | Catálogo de produtos e categoria |
| `vendedores` | `olist_sellers_dataset.csv` | Dados do vendedor |
| `pagamentos_pedido` | `olist_order_payments_dataset.csv` | Forma de pagamento e valores |
| `avaliacoes_pedido` | `olist_order_reviews_dataset.csv` | Notas e comentários de avaliação |
| `traducao_categoria` | `product_category_name_translation.csv` | Tradução das categorias de produto |
| `geolocalizacao` | `olist_geolocation_dataset.csv` | Coordenadas geográficas (uso futuro/opcional) |

Todas as tabelas possuem chaves primárias e relacionamentos (FKs) definidos, garantindo integridade referencial para permitir consultas com JOINs complexos.

---

## 🛠️ Stack Técnica

- **Banco de dados:** PostgreSQL (local)
- **Linguagem:** Python
- **ETL & Conexão:** Pandas + SQLAlchemy + Psycopg2
- **IA Generativa:** Google GenAI SDK (`google-genai`)
- **Modelo LLM:** Gemini (Flash)

---

## 📌 Status Atual do Projeto

- [x] Modelagem do banco de dados relacional (9 tabelas)
- [x] Script de carga automatizada dos CSVs para o PostgreSQL (`carregar_olisit.py`)
- [x] Definição de chaves primárias e estrangeiras (`adicionar_relacionamento_nas_tabelas.sql`)
- [x] Correção de inconsistências do dataset original (categorias de produto faltantes)
- [x] Camada de introspecção de schema (`information_schema`) para contexto do LLM (`introspeccao.py`)
- [x] **Agente Text-to-SQL manual funcional (`agente_manual.py`) integrado ao PostgreSQL e Gemini**
- [ ] Camada de segurança avançada (validação de SQL, usuário read-only, `LIMIT` automático)
- [ ] Geração automática de gráfico conforme o shape do resultado
- [ ] Geração de resumo executivo via LLM
- [ ] Interface em Streamlit
- [ ] Testes com bateria de perguntas de negócio (taxa de acerto)

---

## 📂 Estrutura do Repositório


```

bi_text_to_sql/
├── README.md
├── agente_manual.py                    # Script principal do Agente Text-to-SQL (Gemini + PostgreSQL)
├── carregar_olisit.py                  # Script de ETL: carrega os CSVs Olist no PostgreSQL
├── adicionar_relacionamento_nas_tabelas.sql     # Criação de PKs, FKs e correções de dados
└── introspeccao.py                     # Extração de schema do information_schema para contexto de IA

```

---

## 🚀 Como Rodar o Projeto

1. Tenha o PostgreSQL rodando localmente (ou via Docker).
2. Crie um banco de dados vazio chamado `projeto_BI_TEXT_TO_SQL`.
3. Baixe o dataset Olist no [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) e execute a carga dos dados com `carregar_olisit.py` e o script SQL de relacionamentos.
4. Instale as dependências do projeto:
   ```bash
   pip install pandas sqlalchemy psycopg2-binary google-genai

```

5. Configure a sua chave de API do Gemini como uma variável de ambiente no terminal:
```bash
export GEMINI_API_KEY="sua_chave_aqui"

```


6. Execute o agente interativo:
```bash
python agente_manual.py

```



---

## 👤 Autor

**Vinícius Caetano**

Analista de Dados Jr.

[GitHub](https://github.com/Caetanodassis)

```

```