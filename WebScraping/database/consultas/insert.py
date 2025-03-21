import os
import pandas as pd
from database.conexao.MySqlConnection import MySqlConnection
from logging_config import logger
import threading
import unicodedata
from threading import Event

# Variável de cancelamento global
cancel_event = Event()

def criar_diretorio():
    diretorio_download = "download"
    if not os.path.exists(diretorio_download):
        os.makedirs(diretorio_download)
        logger.info(f"📁 Diretório '{diretorio_download}' criado.")
    return diretorio_download

def limpar_texto(texto):
    """Remove ou substitui caracteres problemáticos para o MySQL."""
    if pd.isna(texto):
        return ""
    if not isinstance(texto, str):
        texto = str(texto)
    # Normaliza o texto para decompor caracteres Unicode
    texto = unicodedata.normalize('NFKD', texto)
    # Substitui caracteres problemáticos (como ➪) por um espaço ou remove
    texto = ''.join(c for c in texto if ord(c) < 0x10000)  # Remove caracteres fora do BMP
    return texto.strip()

def criar_tabela(nome_tabela, df):
    global cancel_event
    if cancel_event.is_set():
        raise Exception("Cancelamento solicitado.")
    conexao = MySqlConnection()
    try:
        logger.info(f"Conectando ao MySQL para criar tabela `{nome_tabela}`...")
        conn = conexao.conectar()
        if conn:
            cursor = conn.cursor()
            colunas_sql = []
            
            for col in df.columns:
                colunas_sql.append(f"`{col}` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            
            query = f"""
                CREATE TABLE IF NOT EXISTS `{nome_tabela}` (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    {', '.join(colunas_sql)}
                ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
            """
            logger.info(f"Executando query para criar tabela `{nome_tabela}`...")
            cursor.execute(query)
            conn.commit()
            cursor.close()
            logger.info(f"✅ Tabela `{nome_tabela}` criada/verificada com sucesso!")
    except Exception as e:
        logger.error(f"❌ Erro ao criar/verificar a tabela `{nome_tabela}`: {e}")
        raise
    finally:
        conexao.fechar_conexao()

def inserir_dados(diretorio_download):
    global cancel_event
    try:
        if not os.path.exists(diretorio_download):
            os.makedirs(diretorio_download)
            logger.info(f"📁 Diretório '{diretorio_download}' criado.")

        arquivos = [f for f in os.listdir(diretorio_download) if os.path.isfile(os.path.join(diretorio_download, f))]
        
        if not arquivos:
            logger.warning("❌ Nenhum arquivo encontrado no diretório!")
            return
        
        xlsx_path = os.path.join(diretorio_download, arquivos[0])
        logger.info(f"📂 Arquivo encontrado: {xlsx_path}")
        
        conexao = MySqlConnection()
        conn = None
        try:
            logger.info("Conectando ao MySQL para inserção de dados...")
            conn = conexao.conectar()
            
            if conn:
                logger.info(f"Lendo arquivo Excel: {xlsx_path}")
                # Usa pd.ExcelFile com um contexto para garantir que o arquivo seja fechado
                with pd.ExcelFile(xlsx_path) as xls:
                    logger.info(f"Abas encontradas no arquivo Excel: {xls.sheet_names}")
                    for aba in xls.sheet_names:
                        if cancel_event.is_set():
                            logger.warning("⚠️ Cancelamento solicitado durante a leitura da aba.")
                            raise Exception("Cancelamento solicitado.")
                        logger.info(f"📋 Processando aba: {aba}")
                        df = pd.read_excel(xls, sheet_name=aba, dtype=str)
                        logger.info(f"Linhas lidas na aba {aba}: {len(df)}")
                        
                        if df.empty:
                            logger.warning(f"⚠️ Aba {aba} está vazia, ignorando...")
                            continue
                        
                        # Limpar os dados antes de inserir
                        logger.debug(f"Limpando dados da aba `{aba}` para evitar caracteres inválidos...")
                        for col in df.columns:
                            df[col] = df[col].apply(limpar_texto)
                        
                        nome_tabela = aba.replace(" ", "_").lower()
                        criar_tabela(nome_tabela, df)
                        
                        cursor = conn.cursor()
                        colunas = ", ".join([f"`{col}`" for col in df.columns])
                        valores = ", ".join(["%s"] * len(df.columns))
                        query = f"INSERT INTO `{nome_tabela}` ({colunas}) VALUES ({valores})"
                        
                        logger.info(f"Inserindo {len(df)} linhas na tabela `{nome_tabela}`...")
                        for i, row in df.iterrows():
                            if cancel_event.is_set():
                                logger.warning(f"⚠️ Cancelamento solicitado na linha {i+1}.")
                                raise Exception("Cancelamento solicitado.")
                            data = tuple(row.fillna("").values)
                            logger.debug(f"Dados {i+1} sendo inseridos: {data}")
                            try:
                                cursor.execute(query, data)
                                logger.debug(f"Dados {i+1} inseridos com sucesso.")
                            except Exception as e:
                                logger.error(f"❌ Erro ao inserir dados {i+1}: {e}")
                                logger.error(f"Valores problemáticos: {data}")
                                raise
                        conn.commit()
                        cursor.close()
                        logger.info(f"✅ {len(df)} linhas inseridas na tabela `{nome_tabela}` com sucesso!")
                        # Libera o DataFrame da memória
                        del df
                
        except Exception as e:
            logger.error(f"❌ Erro ao processar o arquivo: {e}")
            raise
        finally:
            if conn:
                conn.close()
            conexao.fechar_conexao()
    except Exception as e:
        logger.error(f"❌ Erro em inserir_dados(): {str(e)}")
        raise

if __name__ == "__main__":
    diretorio_download = criar_diretorio()