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
        os.chmod(LOG_DIR, 0o775)  # Tenta ajustar permissões
        print(f"Permissões ajustadas para {LOG_DIR}.")
    except PermissionError:
        print(f"Erro: Não foi possível ajustar as permissões de {LOG_DIR}. Execute como administrador ou ajuste manualmente.")
else:
    print(f"Permissões de escrita confirmadas para {LOG_DIR}.")

# Testar escrita no arquivo manualmente
try:
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write("Teste inicial de escrita no arquivo de log.\n")
    print(f"Teste de escrita bem-sucedido: {LOG_FILE} foi criado ou sobrescrito.")
except Exception as e:
    print(f"Erro ao testar escrita no arquivo {LOG_FILE}: {e}")

# Criar um logger personalizado
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Garante que o logger aceite logs de nível DEBUG

# Evitar propagação para o logger raiz
logger.propagate = False

# Configurar o FileHandler
file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8', mode='w')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(
    fmt='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

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

# Configurar o ConsoleHandler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Console mostra DEBUG e acima
console_handler.setFormatter(ColoredFormatter())
logger.addHandler(console_handler)

# Handler personalizado para a interface
class InterfaceHandler(logging.Handler):
    def __init__(self, log_text):
        super().__init__()
        self.log_text = log_text
        self.setLevel(logging.INFO)  # Interface mostra apenas INFO e acima
        self.formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

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
            # Exibir diretamente na interface
            if self.log_text is not None:
                self.log_text.config(state=tk.NORMAL)
                self.log_text.insert(tk.END, msg + "\n", tag)
                self.log_text.config(state=tk.DISABLED)
                self.log_text.yview(tk.END)
        except Exception as e:
            print(f"Erro no InterfaceHandler: {e}")

# Função para configurar o logger com o handler da interface
def setup_logger(log_text):
    interface_handler = InterfaceHandler(log_text)
    logger.addHandler(interface_handler)
    return logger

# Função para exibir logs na interface (usada diretamente em alguns casos)
def log_to_interface(message, tag="info", log_text=None):
    # Mapeia a tag para um nível de logging
    level_map = {
        "info": logging.INFO,
        "success": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR
    }
    level = level_map.get(tag, logging.INFO)
    
    # Registra a mensagem usando o logger
    logger.log(level, message)
    
    # Forçar o flush do FileHandler
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.flush()

# Adicionar log para confirmar que o FileHandler foi configurado
logger.info(f"FileHandler configurado para escrever em {LOG_FILE}.")

# Expor o logger e LOG_FILE para outros módulos
__all__ = ['logger', 'log_to_interface', 'LOG_FILE', 'setup_logger']