import logging
import os
import tkinter as tk
from colorama import init

# Inicializar colorama para cores no console
init()

# Configurar diretórios e arquivos de log
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "automation_log.log")
os.makedirs(LOG_DIR, exist_ok=True)

# Verificar e corrigir permissões do diretório e arquivo
if not os.access(LOG_DIR, os.W_OK):
    print(f"Erro: Sem permissão de escrita no diretório {LOG_DIR}. Tentando ajustar...")
    try:
        os.chmod(LOG_DIR, 0o775)  # Tenta ajustar permissões (pode exigir privilégios de administrador)
    except PermissionError:
        print(f"Erro: Não foi possível ajustar as permissões de {LOG_DIR}. Execute como administrador ou ajuste manualmente.")

# Configuração personalizada de logging
logging.basicConfig(
    level=logging.DEBUG,  # Captura todos os logs (DEBUG e acima)
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8', mode='w'),  # 'w' para sobrescrever em vez de 'a'
        logging.StreamHandler()  # Para exibir no console
    ]
)

# Criar um logger personalizado
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Garante que o logger aceite logs de nível DEBUG

# Adicionar emojis e cores ao console
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[96m',    # Ciano
        'INFO': '\033[94m',     # Azul
        'WARNING': '\033[93m',  # Amarelo
        'ERROR': '\033[91m',    # Vermelho
        'SUCCESS': '\033[92m',  # Verde
        'RESET': '\033[0m'      # Resetar cor
    }

    def format(self, record):
        levelname = record.levelname
        if levelname not in self.COLORS:
            levelname = 'INFO'
        emoji = {
            'DEBUG': '🐞',
            'INFO': 'ℹ️',
            'WARNING': '⚠️',
            'ERROR': '❌',
            'SUCCESS': '✅'
        }.get(levelname, 'ℹ️')
        message = super().format(record)
        return f"{self.COLORS[levelname]}{emoji} {message}{self.COLORS['RESET']}"

# Aplicar o formatador colorido ao handler do console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Console mostra DEBUG e acima
console_handler.setFormatter(ColoredFormatter())
logger.addHandler(console_handler)

# Remover handlers padrão para evitar duplicação
for handler in logging.root.handlers[:]:
    if isinstance(handler, logging.StreamHandler) and handler != console_handler:
        logging.root.removeHandler(handler)

# Handler personalizado para a interface
class InterfaceHandler(logging.Handler):
    def __init__(self, log_text):
        super().__init__()
        self.log_text = log_text
        self.setLevel(logging.INFO)  # Interface mostra apenas INFO e acima

    def emit(self, record):
        try:
            msg = self.format(record)
            tag = {
                'DEBUG': 'info',
                'INFO': 'info',
                'WARNING': 'warning',
                'ERROR': 'error',
                'SUCCESS': 'success'
            }.get(record.levelname, 'info')
            log_to_interface(msg, tag, self.log_text)
        except Exception as e:
            print(f"Erro no InterfaceHandler: {e}")

# Função para configurar o logger com o handler da interface
def setup_logger(log_text):
    interface_handler = InterfaceHandler(log_text)
    logger.addHandler(interface_handler)
    return logger

# Função para exibir logs na interface
def log_to_interface(message, tag="info", log_text=None):
    if log_text is not None:
        try:
            log_text.config(state=tk.NORMAL)
            log_text.insert(tk.END, message + "\n", tag)
            log_text.config(state=tk.DISABLED)
            log_text.yview(tk.END)
        except Exception as e:
            print(f"Erro ao exibir log na interface: {e}")

# Expor o logger e LOG_FILE para outros módulos
__all__ = ['logger', 'log_to_interface', 'LOG_FILE', 'setup_logger']