import re
import psycopg2

def abrir_arquivo(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        # Se falhar com utf-8, tenta latin1
        with open(caminho, "r", encoding="latin1") as f:
            return f.read()

def limpar_texto(texto):
    # Remove caracteres inválidos para UTF-8
    return texto.encode('utf-8', 'ignore').decode('utf-8')

# Caminho do arquivo com os dados
caminho_arquivo = "C:\\Users\\vinicius\\Desktop\\ETL_VLANS\\dados_vlan.txt"

# Lê o conteúdo do arquivo, tentando utf-8 e latin1
raw_text = abrir_arquivo(caminho_arquivo)

# Extração com regex
vlan_match = re.search(r'Logical interface .+\.(\d+)', raw_text)
description_match = re.search(r'Description:\s*(.+)', raw_text)
destinations_ipv6 = re.findall(r'Destination:\s*([a-fA-F0-9:]+/\d+)', raw_text)

# Validação
if vlan_match and description_match and len(destinations_ipv6) >= 2:
    vlanid = int(vlan_match.group(1))
    nome_description = limpar_texto(description_match.group(1).strip())
    destination1 = destinations_ipv6[-2]
    destination2 = destinations_ipv6[-1]
else:
    raise ValueError("Não foi possível extrair todos os campos necessários do arquivo.")

# Conexão com o PostgreSQL local
conn = psycopg2.connect(
    dbname="vlans",
    user="eng",     
    password="223355",   
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Inserção ou atualização dos dados
cur.execute("""
INSERT INTO vlan (vlanid, nome_description, destination1, destination2)
VALUES (%s, %s, %s, %s)
ON CONFLICT (vlanid) DO UPDATE
SET nome_description = EXCLUDED.nome_description,
    destination1 = EXCLUDED.destination1,
    destination2 = EXCLUDED.destination2;
""", (vlanid, nome_description, destination1, destination2))

# Commit e encerramento
conn.commit()
cur.close()
conn.close()

print("Dados extraídos do arquivo e inseridos com sucesso no banco.")
