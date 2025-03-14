import os
import mysql.connector
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

class MySqlConnection:
    def __init__(self):
        self.conn = None

    def conectar(self):
        """Estabelece conexão com o banco de dados."""
        try:
            self.conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
                port=int(os.getenv("DB_PORT")),
                auth_plugin='mysql_native_password',
                charset='utf8mb4',
                collation='utf8mb4_general_ci',
                connection_timeout=30
            )
            print("Conectado ao banco de dados com sucesso!")
            return self.conn
        except mysql.connector.Error as err:
            print(f"Erro ao conectar ao banco de dados: {err}")
            return None

    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()
            print("Conexão com o banco de dados fechada.")


if __name__ == "__main__":
    conexao = MySqlConnection()
    if conexao.conectar():
        print("Conexão bem-sucedida!")
    else:
        print("Falha na conexão.")
        conexao.fechar_conexao()
    