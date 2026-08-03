from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

USUARIO = 'postgres'
SENHA = 'Assisdcaetano17@'
HOST = 'localhost'
PORTA = '5432'
BANCO = 'projeto_BI_TEXT_TO_SQL'

string_conexao = URL.create(
    drivername="postgresql+psycopg2",
    username=USUARIO,
    password=SENHA,
    host=HOST,
    port=int(PORTA),
    database=BANCO,
)
engine = create_engine(string_conexao)

def obter_schema_banco():
    query = """
    SELECT
        c.table_name,
        c.column_name,
        c.data_type,
        COALESCE(tc.constraint_type, '') AS constraint_type
    FROM
        information_schema.columns c
    LEFT JOIN
        information_schema.key_column_usage kcu
        ON kcu.table_schema = c.table_schema
        AND kcu.table_name = c.table_name
        AND kcu.column_name = c.column_name
    LEFT JOIN
        information_schema.table_constraints tc
        ON tc.constraint_name = kcu.constraint_name
        AND tc.table_schema = kcu.table_schema
        AND tc.table_name = kcu.table_name
        AND tc.constraint_type IN ('PRIMARY KEY', 'FOREIGN KEY')
    WHERE
        c.table_schema = 'public'
    ORDER BY
        c.table_name, c.ordinal_position
    ;
    """
    
    with engine.connect() as conexao:
        resultado = conexao.execute(text(query))
        colunas_tabelas = resultado.fetchall()
    
    return colunas_tabelas

def gerar_prompt_schema():
    dados = obter_schema_banco()
    tabelas = {}
    for row in dados:
        tabela = row[0]
        coluna = row[1]
        tipo_dado = row[2]
        constraint = row[3]
        
        if tabela not in tabelas:
            tabelas[tabela] = []
        tabelas[tabela].append((coluna, tipo_dado, constraint))
        
    schema_md = "Esquema do Banco de Dados PostgreSQL (Olist):\n\n"
    for tabela, colunas in tabelas.items():
        schema_md += f"Tabela: {tabela}\n"
        for col, tipo, const in colunas:
            detalhe = f" [{const}]" if const else ""
            schema_md += f"  - {col} ({tipo}){detalhe}\n"
        schema_md += "\n"
        
    return schema_md

if __name__=='__main__':
    print(gerar_prompt_schema())