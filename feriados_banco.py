from dbconnect import Conexao


connect = Conexao()
conn = connect.conecta()
cursor = conn.cursor()

data = '2024-02-13'             # formato AAAA-MM-DD
nome_do_feriado = 'Carnaval'     # nome do feriado

try:
    query = "INSERT INTO CAD_FERIADOS VALUES (?, ?, 1,1)"
    valores = (data, nome_do_feriado)
    cursor.execute(query, valores)

    conn.commit()

    print("Registro inserido com sucesso!")

except Exception as e:
    conn.rollback()
    print(f"Erro ao inserir registro: {str(e)}")

finally:
    cursor.close()
    conn.close()