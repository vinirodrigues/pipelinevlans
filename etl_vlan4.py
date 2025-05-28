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

# Caminho do arquivo
caminho_arquivo = "C:\\Users\\vinicius\\Desktop\\ETL_VLANS\\dados_vlan.txt"
raw_text = abrir_arquivo(caminho_arquivo)

# Conexão com o banco
conn = psycopg2.connect(
    dbname="vlans",
    user="eng",
    password="223355",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Coleta os vlanid já existentes
cur.execute("SELECT vlanid FROM vlan")
ids_existentes = set(row[0] for row in cur.fetchall())

# Divide os blocos de interface
blocos = re.findall(r'(Logical interface .+?)(?=Logical interface |\Z)', raw_text, re.DOTALL)

print(f"🔍 {len(blocos)} blocos encontrados")
inseridos = 0
erros = 0

for bloco in blocos:
    vlan_match = re.search(r'Logical interface .+\.(\d+)', bloco)
    if not vlan_match:
        erros += 1
        with open("blocos_com_erro.txt", "a", encoding="utf-8") as log:
            log.write("\n\n----- VLAN ID NÃO ENCONTRADO -----\n")
            log.write(bloco)
        continue

    vlanid = int(vlan_match.group(1))

    # Ignora se já foi inserido
    if vlanid in ids_existentes:
        continue

    # Description é opcional
    desc_match = re.search(r'Description:\s*(.+)', bloco)
    nome_description = limpar_texto(desc_match.group(1).strip()) if desc_match else None

    # Destinos obrigatórios
    destinations = re.findall(r'Destination:\s*([a-fA-F0-9.:]+/\d+)', bloco)

    if len(destinations) >= 1:
        destination1 = destinations[-2] if len(destinations) >= 2 else destinations[0]
        destination2 = destinations[-1] if len(destinations) >= 2 else None

        try:
            cur.execute("""
                INSERT INTO vlan (vlanid, nome_description, destination1, destination2)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (vlanid) DO NOTHING;
            """, (vlanid, nome_description, destination1, destination2))
            inseridos += 1
        except Exception as e:
            erros += 1
            with open("blocos_com_erro.txt", "a", encoding="utf-8") as log:
                log.write("\n\n----- ERRO AO INSERIR -----\n")
                log.write(bloco)
    else:
        erros += 1
        with open("blocos_com_erro.txt", "a", encoding="utf-8") as log:
            log.write("\n\n----- DESTINATIONS INCOMPLETOS -----\n")
            log.write(bloco)

# Finaliza conexão
conn.commit()
cur.close()
conn.close()

print(f"✅ {inseridos} novos blocos inseridos.")
print(f"⚠️ {erros} blocos com erro ou incompletos.")
