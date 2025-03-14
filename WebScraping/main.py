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
        with open(file_path, 'a'):
            logger.debug(f"Arquivo {file_path} está livre para uso.")
            return False
    except IOError:
        logger.debug(f"Arquivo {file_path} está em uso por outro processo.")
        return True

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
        WebDriverWait(driver, 30).until(lambda d: any(f.endswith(".xlsx") for f in os.listdir(download_dir)))

        # Renomeia o arquivo baixado e sobrescreve se necessário
        logger.info("📂 Verificando arquivos baixados...")
        for file in os.listdir(download_dir):
            if file.endswith(".xlsx") and file != "emcf-database-for-ica-508-compliant.xlsx":
                old_path = os.path.join(download_dir, file)
                new_filename = f"dados_emergy_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.xlsx"
                new_path = os.path.join(download_dir, new_filename)

                # Aguarda até que o arquivo não esteja em uso
                while is_file_in_use(old_path):
                    logger.info(f"Aguardando o arquivo {old_path} ser liberado...")
                    time.sleep(1)

                # Remove o arquivo anterior com o mesmo nome, se existir
                if os.path.exists(new_path):
                    os.remove(new_path)
                    logger.info(f"🗑️ Arquivo anterior {new_path} removido para sobrepor.")

                os.rename(old_path, new_path)
                logger.info(f"📥 Arquivo baixado e renomeado para: {new_path}")
                break

        # Fechar o navegador
        logger.info("🌐 Fechando navegador...")
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

if __name__ == "__main__":
    main()