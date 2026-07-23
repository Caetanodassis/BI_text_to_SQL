# 🤖 BI Copiloto — Agente Text-to-SQL em Português

> Um agente de IA que entende perguntas de negócio em linguagem natural, traduz para SQL, executa no banco de dados e responde com gráfico + resumo executivo — inspirado no **Genie (Databricks)**, construído do zero e rodando 100% local com **PostgreSQL**.

---

## 🎯 Objetivo do Projeto

Empresas de grande porte (bancos, e-commerces, fintechs) estão investindo em ferramentas de **"self-service BI" com IA generativa**, onde qualquer pessoa do negócio — sem saber SQL — consegue fazer perguntas e obter respostas analíticas na hora.

Este projeto reproduz esse conceito de forma independente, com o objetivo de:

- Demonstrar domínio prático de **engenharia de dados** (modelagem relacional, ETL, SQL avançado) combinado com **GenAI/agentes de IA** (LangChain/LangGraph);
- Entender e implementar, na prática, os componentes internos de uma ferramenta como o Genie: introspecção de schema, geração de SQL via LLM, camada de segurança, escolha automática de visualização e sumarização executiva;
- Construir um artefato de portfólio que una **BI tradicional** e **IA aplicada a dados**, área de forte demanda no mercado.

**Pergunta que o agente deve responder, por exemplo:**
> *"Qual foi o produto com maior queda de vendas no segundo trimestre?"*

E devolver: a query SQL gerada, o gráfico correspondente e um resumo em linguagem natural da resposta.

---

## 🏗️ Arquitetura (visão geral)

```
Pergunta do usuário (PT-BR)
        │
        ▼
Agente Text-to-SQL (LangChain/LangGraph)
   │  contexto: schema do banco (information_schema)
   ▼
Geração de query SQL
        │
        ▼
Camada de validação e segurança
   (permite apenas SELECT, usuário read-only, LIMIT automático)
        │
        ▼
Execução no PostgreSQL
        │
        ▼
   ┌────┴────┐
   ▼         ▼
Gráfico    Resumo executivo
(Plotly)   (LLM)
        │
        ▼
Interface (Streamlit)
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

Todas as tabelas possuem chaves primárias e relacionamentos (FKs) definidos, garantindo integridade referencial para permitir consultas com JOINs complexos — essencial para o agente responder perguntas de negócio reais.

---

## 🛠️ Stack Técnica

- **Banco de dados:** PostgreSQL (local)
- **Linguagem:** Python
- **ETL:** Pandas + SQLAlchemy
- **Agente de IA:** LangChain / LangGraph (em desenvolvimento)
- **LLM:** API Claude/OpenAI (em desenvolvimento)
- **Visualização:** Plotly (em desenvolvimento)
- **Interface:** Streamlit (em desenvolvimento)

---

## 📌 Status Atual do Projeto

- [x] Modelagem do banco de dados relacional (9 tabelas)
- [x] Script de carga automatizada dos CSVs para o PostgreSQL (`carregar_olisit.py`)
- [x] Definição de chaves primárias e estrangeiras (`adicionar_relacionamento_nas_tabelas.sql`)
- [x] Correção de inconsistências do dataset original (categorias de produto faltantes)
- [ ] Camada de introspecção de schema (`information_schema`) para contexto do LLM
- [ ] Agente Text-to-SQL (versão manual, sem framework)
- [ ] Migração para LangChain (`create_sql_agent` / `SQLDatabaseChain`)
- [ ] Camada de segurança (validação de SQL, usuário read-only, `LIMIT` automático)
- [ ] Geração automática de gráfico conforme o shape do resultado
- [ ] Geração de resumo executivo via LLM
- [ ] Interface em Streamlit
- [ ] Testes com bateria de perguntas de negócio (taxa de acerto)
- [ ] (v2) Refatoração do fluxo para LangGraph com auto-correção de erros de SQL

---

## 📂 Estrutura do Repositório

```
bi_text_to_sql/
├── README.md
├── carregar_olisit.py                          # Script de ETL: carrega os CSVs Olist no PostgreSQL
└── adicionar_relacionamento_nas_tabelas.sql     # Criação de PKs, FKs e correções de dados
```

*(estrutura será atualizada conforme novas etapas forem implementadas)*

---

## 🚀 Como Rodar (setup atual)

1. Tenha o PostgreSQL rodando localmente (ou via Docker)
2. Crie um banco de dados vazio (ex: `projeto_BI_TEXT_TO_SQL`)
3. Baixe o dataset Olist no [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) e ajuste os caminhos dos arquivos em `carregar_olisit.py`
4. Instale as dependências:
   ```bash
   pip install pandas sqlalchemy psycopg2-binary
   ```
5. Execute a carga dos dados:
   ```bash
   python carregar_olisit.py
   ```
6. Execute o script de relacionamentos no seu client SQL (DBeaver, pgAdmin, ou via `psql`):
   ```bash
   psql -U postgres -d projeto_BI_TEXT_TO_SQL -f adicionar_relacionamento_nas_tabelas.sql
   ```

*(passos de instalação do agente de IA e da interface serão adicionados nas próximas etapas)*

---

## 🗺️ Próximos Passos

Ver seção [Status Atual do Projeto](#-status-atual-do-projeto) acima — cada item será marcado como concluído e documentado com mais detalhe conforme o desenvolvimento avança.

---

## 👤 Autor

**Vinícius Caetano**
Analista de Dados Jr. | Estudante de ADS
[GitHub](https://github.com/Caetanodassis)
