from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logging_config import logger
from database.consultas.insert import inserir_dados
import os
import time
import shutil
from threading import Event

# Variável de cancelamento
cancel_event = Event()

def is_file_in_use(file_path):
    """Verifica se o arquivo está em uso por outro processo."""
    logger.debug(f"Verificando se o arquivo {file_path} está em uso...")
    try:
        # Tenta renomear o arquivo para si mesmo como uma verificação mais robusta
        os.rename(file_path, file_path)
        logger.debug(f"Arquivo {file_path} está livre para uso.")
        return False
    except (IOError, OSError):
        logger.debug(f"Arquivo {file_path} está em uso por outro processo.")
        return True

def wait_until_file_is_free(file_path, max_attempts=60, wait_interval=5):
    """Aguarda até que o arquivo não esteja mais em uso."""
    attempts = 0
    while is_file_in_use(file_path) and attempts < max_attempts:
        logger.info(f"Aguardando o arquivo {file_path} ser liberado... (Tentativa {attempts + 1}/{max_attempts})")
        time.sleep(wait_interval)
        attempts += 1
    if attempts >= max_attempts:
        logger.error(f"❌ Não foi possível liberar o arquivo {file_path} após {max_attempts} tentativas.")
        raise Exception(f"Arquivo {file_path} ainda está em uso após {max_attempts} tentativas.")

def clean_download_directory(download_dir):
    """Remove todos os arquivos no diretório de download."""
    logger.info(f"🗑️ Limpando o diretório '{download_dir}' antes do download...")
    logger.debug(f"Arquivos no diretório antes da limpeza: {os.listdir(download_dir)}")
    for file in os.listdir(download_dir):
        file_path = os.path.join(download_dir, file)
        try:
            logger.debug(f"Tentando remover arquivo: {file_path}")
            wait_until_file_is_free(file_path)
            os.remove(file_path)
            logger.info(f"🗑️ Arquivo {file_path} removido.")
        except Exception as e:
            logger.error(f"❌ Erro ao remover arquivo {file_path}: {e}")
            raise
    logger.debug(f"Arquivos no diretório após a limpeza: {os.listdir(download_dir)}")

def wait_for_download(download_dir, initial_files, timeout=60):
    """Aguarda até que o download seja concluído e o arquivo .xlsx ou .xls esteja presente."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        current_files = set(os.listdir(download_dir))
        new_files = current_files - initial_files
        for file in new_files:
            if file.endswith((".xlsx", ".xls")) and not file.endswith(".crdownload"):
                return os.path.join(download_dir, file)
        # Verifica se há arquivos temporários (.crdownload) e aguarda
        if any(file.endswith(".crdownload") for file in current_files):
            logger.debug("Arquivo temporário (.crdownload) detectado, aguardando conclusão do download...")
        time.sleep(1)
    raise Exception(f"Timeout: Nenhum arquivo .xlsx ou .xls foi baixado após {timeout} segundos.")

def main():
    try:
        logger.info("=== Início da Automação ===")
        logger.info("--- Início do Web Scraping ---")
        logger.info("Configurando opções do Chrome...")
        options = Options()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-extensions')
        options.add_argument("--headless")  # Modo headless para não abrir janela
        logger.debug("Opções do Chrome configuradas: ignore-certificate-errors, disable-popup-blocking, start-maximized, disable-extensions, headless.")

        # Configura o diretório de download
        download_dir = r"download"
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            logger.info(f"📁 Diretório '{download_dir}' criado.")
        else:
            logger.info(f"📁 Diretório '{download_dir}' já existe.")

        # Limpa o diretório de download antes de iniciar o download
        clean_download_directory(download_dir)

        prefs = {
            "download.default_directory": os.path.abspath(download_dir),
            "download.prompt_for_download": False,
            "directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        logger.debug(f"Configurações de download definidas: {prefs}")

        # Configura o driver do navegador
        logger.info("Inicializando o ChromeDriver...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        logger.debug("ChromeDriver inicializado com sucesso.")

        # Acessa a página
        url = "https://www.epa.gov/water-research/uev-library#access"
        logger.info(f"🌐 Acessando site: {url}")
        driver.get(url)

        # Verifica se o cancelamento foi solicitado
        if cancel_event.is_set():
            logger.warning("⚠️ Cancelamento solicitado durante o acesso ao site.")
            driver.quit()
            return

        # Espera até que o link de download esteja visível e clica nele
        link_xpath = '//*[@id="main"]/div/div[1]/div[2]/div[1]/article/div[2]/div/p[11]/span[2]/a'
        logger.info("🔗 Aguardando link de download...")
        link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, link_xpath)))
        logger.info("🔗 Link de download encontrado, clicando...")
        link.click()

        # Aguarda o download ser concluído
        logger.info("⏳ Aguardando conclusão do download...")
        initial_files = set(os.listdir(download_dir))
        downloaded_file = wait_for_download(download_dir, initial_files, timeout=60)

        # Renomeia o arquivo baixado
        logger.info("📂 Verificando arquivos baixados...")
        if downloaded_file:
            # Aguarda até que o arquivo baixado não esteja em uso
            logger.debug(f"Aguardando liberação do arquivo baixado: {downloaded_file}")
            wait_until_file_is_free(downloaded_file)

            # Gera o nome do arquivo com a data e hora atual
            timestamp = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
            new_filename = f"dados_emergy_{timestamp}.xlsx"
            new_path = os.path.join(download_dir, new_filename)

            # Log para confirmar o nome gerado
            logger.debug(f"Nome do arquivo gerado: {new_filename}")

            # Renomeia o arquivo baixado
            try:
                logger.debug(f"Renomeando {downloaded_file} para {new_path}")
                os.rename(downloaded_file, new_path)
                logger.info(f"📥 Arquivo baixado e renomeado para: {new_path}")
            except Exception as e:
                logger.error(f"❌ Erro ao renomear o arquivo {downloaded_file} para {new_path}: {e}")
                raise
        else:
            logger.error("❌ Nenhum arquivo .xlsx ou .xls foi encontrado para renomear.")
            raise Exception("Nenhum arquivo .xlsx ou .xls foi encontrado para renomear.")

        # Fechar o navegador
        logger.info("🌐 Fechando navegador...")
        time.sleep(2)  # Aguarda 2 segundos para garantir que o download esteja concluído
        driver.quit()

        # Verifica se o cancelamento foi solicitado antes de prosseguir
        if cancel_event.is_set():
            logger.warning("⚠️ Cancelamento solicitado após download.")
            return

        # Inserir dados no banco
        logger.info("--- Início da Inserção no MySQL ---")
        inserir_dados(download_dir)

    except Exception as e:
        logger.error(f"❌ Erro no main(): {str(e)}")
        raise
    finally:
        logger.info("=== Fim da Automação ===")