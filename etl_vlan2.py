import re
import psycopg2

def abrir_arquivo(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(caminho, "r", encoding="latin1") as f:
            return f.read()

def limpar_texto(texto):
    return texto.encode('utf-8', 'ignore').decode('utf-8')

# Caminho do arquivo grande
caminho_arquivo = r"C:\Users\vinicius\Desktop\ETL_VLANS\interfaces.txt"
raw_text = abrir_arquivo(caminho_arquivo)

# Separa blocos por interfaces (cada bloco começa com 'Logical interface')
# Divide corretamente por blocos de interface
blocos = re.findall(r'(Logical interface .+?)(?=Logical interface |\Z)', raw_text, re.DOTALL)

#verifica quantas interfaces foram encontradas
print(f"🔍 {len(blocos)} blocos de interface encontrados no arquivo.")


# Conecta ao banco uma única vez
conn = psycopg2.connect(
    dbname="vlans",
    user="eng",
    password="223355",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

cont_sucesso = 0
cont_erro = 0

for bloco in blocos:
    try:
        vlan_match = re.search(r'Logical interface .+\.(\d+)', bloco)
        description_match = re.search(r'Description:\s*(.+)', bloco)
        destinations_ipv6 = re.findall(r'Destination:\s*([a-fA-F0-9:]+/\d+)', bloco)

        if vlan_match and description_match and len(destinations_ipv6) >= 2:
            vlanid = int(vlan_match.group(1))
            nome_description = limpar_texto(description_match.group(1).strip())
            destination1 = destinations_ipv6[-2]
            destination2 = destinations_ipv6[-1]

            cur.execute("""
                INSERT INTO vlan (vlanid, nome_description, destination1, destination2)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (vlanid) DO UPDATE
                SET nome_description = EXCLUDED.nome_description,
                    destination1 = EXCLUDED.destination1,
                    destination2 = EXCLUDED.destination2;
            """, (vlanid, nome_description, destination1, destination2))

            cont_sucesso += 1
        else:
            cont_erro += 1

    except Exception as e:
        print(f"Erro ao processar bloco:\n{e}\n")
        cont_erro += 1

conn.commit()
cur.close()
conn.close()

print(f"✅ {cont_sucesso} blocos inseridos com sucesso.")
if cont_erro:
    print(f"⚠️ {cont_erro} blocos com erro.")
