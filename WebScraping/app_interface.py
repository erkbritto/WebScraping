import os
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter.ttk import Progressbar, Separator
from logging_config import logger, log_to_interface, LOG_FILE, setup_logger
from main import main, cancel_event
import shutil

# Função para limpar todas as pastas __pycache__ no projeto
def clean_pycache_directories():
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                pycache_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(pycache_path)
                except Exception as e:
                    return 0

# Definição das funções antes da criação da interface
def run_automation():
    global cancel_event
    cancel_event.clear()
    progress_bar['value'] = 0
    log_text.config(state=tk.NORMAL)
    log_text.delete(1.0, tk.END)
    logger.debug("Debug: Iniciando run_automation...")
    log_to_interface("🚀 Iniciando automação...", "info", log_text)
    
    # Desativa o botão "Iniciar Automação" e ativa o botão "Cancelar"
    start_btn.config(state=tk.DISABLED)
    cancel_btn.config(state=tk.NORMAL)
    
    def automation_thread():
        global cancel_event
        try:
            logger.info("=== Início da Automação ===")
            progress_bar['value'] = 10
            top.update()  # Forçar atualização da interface
            
            logger.info("Iniciando execução do main()...")
            main()
            
            if not cancel_event.is_set():
                progress_bar['value'] = 100
                top.update()  # Forçar atualização da interface
                log_to_interface("✅ Automação concluída com sucesso!", "success", log_text)
                logger.info("=== Fim da Automação ===")
            else:
                log_to_interface("⚠️ Automação cancelada pelo usuário.", "warning", log_text)
                logger.warning("Automação cancelada pelo usuário.")
        except Exception as e:
            log_to_interface(f"❌ Erro durante a automação: {e}", "error", log_text)
            logger.error(f"Erro durante a automação: {e}")
        finally:
            # Reativa o botão "Iniciar Automação" e desativa o botão "Cancelar"
            start_btn.config(state=tk.NORMAL)
            cancel_btn.config(state=tk.DISABLED)
            log_text.config(state=tk.DISABLED)
            # Limpa as pastas __pycache__ após a automação
            clean_pycache_directories()

    threading.Thread(target=automation_thread, daemon=True).start()

def cancel_automation():
    global cancel_event
    cancel_event.set()  # Define o evento de cancelamento
    log_to_interface("⚠️ Cancelamento solicitado...", "warning", log_text)
    logger.warning("Cancelamento solicitado pelo usuário.")

def generate_logs():
    logger.info(f"Gerando logs a partir do arquivo: {LOG_FILE}")
    if os.path.exists(LOG_FILE):
        logger.info(f"Arquivo de log encontrado: {LOG_FILE}")
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                logger.info(f"Conteúdo do arquivo de log:\n{content}")
            os.system(f"notepad {LOG_FILE}")
        except Exception as e:
            logger.error(f"Erro ao ler o arquivo de log: {e}")
            messagebox.showerror("Erro", f"Não foi possível ler o arquivo de log: {e}")
    else:
        logger.warning("Nenhum arquivo de log foi encontrado!")
        messagebox.showwarning("Aviso", "Nenhum log foi gerado ainda!")

# Criação da interface
top = tk.Tk()
top.title("Automação de Web Scraping")
top.geometry("800x600")
top.configure(bg="#f0f4f8")  # Cor de fundo mais suave

# Título
title_label = tk.Label(top, text="Automação de Coleta de Dados", font=("Helvetica", 18, "bold"), bg="#f0f4f8", fg="#2c3e50")
title_label.pack(pady=15)

# Frame principal
main_frame = tk.Frame(top, bg="#f0f4f8")
main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

# Área de logs com borda estilizada
log_frame = tk.Frame(main_frame, bg="#ffffff", bd=2, relief=tk.SOLID, highlightbackground="#d1d5db", highlightthickness=1)
log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

log_label = tk.Label(log_frame, text="Logs da Automação", font=("Helvetica", 12, "bold"), bg="#ffffff", fg="#2c3e50")
log_label.pack(pady=5)

log_text = scrolledtext.ScrolledText(log_frame, height=20, width=70, state=tk.DISABLED, bg="#f9fafb", font=("Consolas", 10), wrap=tk.WORD, borderwidth=0)
log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Configurar o logger com o handler da interface
setup_logger(log_text)

# Definição de cores para logs na interface
log_text.tag_configure("info", foreground="#1e90ff", font=("Consolas", 10))
log_text.tag_configure("success", foreground="#28a745", font=("Consolas", 10, "bold"))
log_text.tag_configure("error", foreground="#dc3545", font=("Consolas", 10, "bold"))
log_text.tag_configure("warning", foreground="#ffc107", font=("Consolas", 10, "bold"))

# Barra de progresso com label
progress_frame = tk.Frame(main_frame, bg="#f0f4f8")
progress_frame.pack(fill=tk.X, padx=10, pady=5)
progress_label = tk.Label(progress_frame, text="Progresso:", font=("Helvetica", 10, "bold"), bg="#f0f4f8", fg="#2c3e50")
progress_label.pack(anchor="w")
progress_bar = Progressbar(progress_frame, length=600, mode='determinate', style="blue.Horizontal.TProgressbar")
progress_bar.pack(fill=tk.X)

# Botões com estilo
btn_frame = tk.Frame(main_frame, bg="#f0f4f8")
btn_frame.pack(side=tk.RIGHT, anchor="se", padx=10, pady=10)

start_btn = tk.Button(btn_frame, text="Iniciar Automação", command=run_automation, font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", width=18, height=2, relief=tk.FLAT, activebackground="#45a049")
start_btn.pack(pady=5)

cancel_btn = tk.Button(btn_frame, text="Cancelar", command=cancel_automation, font=("Helvetica", 12, "bold"), bg="#F44336", fg="white", width=18, height=2, relief=tk.FLAT, activebackground="#e53935", state=tk.DISABLED)
cancel_btn.pack(pady=5)

log_btn = tk.Button(btn_frame, text="Gerar Logs", command=generate_logs, font=("Helvetica", 12, "bold"), bg="#2196F3", fg="white", width=18, height=2, relief=tk.FLAT, activebackground="#1e88e5")
log_btn.pack(pady=5)

# Separador estilizado
separator = Separator(main_frame, orient="vertical")
separator.pack(side=tk.RIGHT, fill=tk.Y, padx=5)

# Inicia a interface
top.mainloop()