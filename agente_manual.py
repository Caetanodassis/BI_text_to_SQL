import os
from google import genai
from sqlalchemy import create_engine, text

# 1. Configuração das credenciais do Banco de Dados PostgreSQL
DB_USER = "postgres"
DB_PASS = "Assisdcaetano17@"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "projeto_BI_TEXT_TO_SQL"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# 2. Configuração do Cliente do Google GenAI
# O cliente buscará automaticamente a chave configurada na variável de ambiente GEMINI_API_KEY
client = genai.Client()

# 3. Contexto do Schema do Banco
SCHEMA_CONTEXT = """
Você é um especialista em SQL e PostgreSQL. O banco de dados é do e-commerce Olist e possui as seguintes tabelas e colunas:

- clientes: customer_id (PK), customer_unique_id, customer_zip_code_prefix, customer_city, customer_state
- pedidos: order_id (PK), customer_id (FK), order_status, order_purchase_timestamp, order_approved_at, order_delivered_customer_date, order_estimated_delivery_date
- itens_pedido: order_id (PK/FK), order_item_id (PK), product_id (FK), seller_id (FK), price, freight_value
- produtos: product_id (PK), product_category_name (FK), product_weight_g, etc.
- pagamentos_pedido: order_id (PK/FK), payment_sequential (PK), payment_type, payment_installments, payment_value
- avaliacoes_pedido: review_id (PK), order_id (FK), review_score, review_comment_message, etc.
- vendedores: seller_id (PK), seller_city, seller_state
- traducao_categoria: product_category_name (PK), product_category_name_english

Regras obrigatórias:
1. Retorne APENAS o código SQL puro, sem formatações markdown (como ```sql), sem explicações adicionais.
2. Certifique-se de que a query seja compatível com PostgreSQL.
3. SE o usuário citar um estado, cidade ou filtro específico na pergunta (ex: "em São Paulo", "estado SP"), você DEVE obrigatoriamente incluir a cláusula WHERE correspondente (ex: WHERE customer_state = 'SP').
"""

def gerar_sql(pergunta_usuario: str) -> str:
    """Envia a pergunta e o schema para o Gemini gerar a query SQL."""
    prompt_completo = f"""
    {SCHEMA_CONTEXT}
    
    Converta esta pergunta em uma query SQL PostgreSQL: {pergunta_usuario}
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_completo,
    )
    
    sql_query = response.text.strip()
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    return sql_query

def executar_consulta(sql_query: str):
    """Executa a query SQL gerada no banco de dados PostgreSQL."""
    try:
        with engine.connect() as conexao:
            resultado = conexao.execute(text(sql_query))
            colunas = resultado.keys()
            linhas = resultado.fetchall()
            return colunas, linhas
    except Exception as e:
        return None, f"Erro ao executar o SQL: {e}"

# --- FLUXO PRINCIPAL INTERATIVO COM INPUT ---
if __name__ == "__main__":
    print("🤖 Agente Text-to-SQL Manual (Via Google Gemini Nuvem) Iniciado!")
    print("Digite sua pergunta de negócio ou 'sair' para encerrar.\n")
    
    while True:
        pergunta = input("💬 Pergunta: ").strip()
        
        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("Encerrando o agente. Até logo!")
            break
            
        if not pergunta:
            continue
            
        print("\n[1/3] Gerando SQL com o Gemini...")
        sql_gerado = gerar_sql(pergunta)
        print(f"SQL Gerado:\n{sql_gerado}")
        
        print("\n[2/3] Executando query no banco de dados...")
        colunas, dados = executar_consulta(sql_gerado)
        
        print("\n[3/3] Resultado da Consulta:")
        if isinstance(dados, str):
            print(dados)
        else:
            print(list(colunas))
            if not dados:
                print("(Nenhum registro encontrado)")
            else:
                for linha in dados:
                    print(linha)
        print("-" * 50 + "\n")