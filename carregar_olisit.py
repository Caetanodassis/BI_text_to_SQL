# IMPORTANDO BIBLIOTECAS
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# CREDENCIAIS DE CONEXÃO COM O BANCO DE DADOS
USUARIO = 'postgres'
SENHA = 'Assisdcaetano17@'
HOST = 'localhost'
PORTA = '5432'
BANCO = 'projeto_BI_TEXT_TO_SQL'

# VARIAVEL DE CONEXÃO
# URL.create trata corretamente caracteres especiais presentes na senha, como "@".
string_conexao = URL.create(
    drivername="postgresql+psycopg2",
    username=USUARIO,
    password=SENHA,
    host=HOST,
    port=int(PORTA),
    database=BANCO,
)
engine = create_engine(string_conexao)

# MAPEAR AS TABELAS / PADRONIZAR AS TEBELAS
arquivos = {
    'clientes': '/home/vinicius/Downloads/PROJETOS_DADOS/text_to_sql/datasets/olist_customers_dataset.csv',
    'geolocalizacao': '/home/vinicius/Downloads/PROJETOS_DADOS/text_to_sql/datasets/olist_geolocation_dataset.csv',
    'itens_pedido': '/home/vinicius/Downloads/PROJETOS_DADOS/text_to_sql/datasets/olist_order_items_dataset.csv',
    'pagamentos_pedido': '/home/vinicius/Downloads/PROJETOS_DADOS/text_to_sql/datasets/olist_order_payments_dataset.csv',
    'avaliacoes_pedido': '/home/vinicius/Downloads/PROJETOS_DADOS/text_to_sql/datasets/olist_order_reviews_dataset.csv',
    'pedidos': '/home/vinicius/Downloads/PROJETOS_DADOS/text_to_sql/datasets/olist_orders_dataset.csv',
    'produtos': '/home/vinicius/Downloads/PROJETOS_DADOS/text_to_sql/datasets/olist_products_dataset.csv',
    'vendedores': '/home/vinicius/Downloads/PROJETOS_DADOS/text_to_sql/datasets/olist_sellers_dataset.csv',
    'traducao_categoria': '/home/vinicius/Downloads/PROJETOS_DADOS/text_to_sql/datasets/product_category_name_translation.csv'
}

# ENVIA TABELAS PARA O POSTGRESQL
for nome_tabela, nome_arquivo in arquivos.items():
    print(f"lendo arquivo {nome_arquivo} para a tabela {nome_tabela}...")
    
    df = pd.read_csv(nome_arquivo)
    print(f"enviando tabela {nome_tabela} para o banco de dados...")
    df.to_sql(
        name=nome_tabela,
        con=engine,
        if_exists='replace',
        index=False,
        chunksize=10000   
    )
    
    print(f"tabela {nome_tabela} enviada com sucesso!")
    
print("TODAS AS TABELAS FORAM ENVIADAS COM SUCESSO!")