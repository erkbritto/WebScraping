# 📌 Projeto de Automação e Armazenamento de Dados

## 📖 Sobre o Projeto
Este projeto automatiza o download de um arquivo **XLSX** a partir de um site, processa os dados contidos nele e os armazena em um banco de dados **MySQL**. Ele utiliza:

- **Selenium** para interagir com a web e baixar o arquivo.
- **Pandas** para manipulação dos dados.
- **MySQL Connector** para inseri-los no banco de dados.
- **Tkinter** para uma interface gráfica amigável, permitindo monitoramento e controle do processo.

O projeto também inclui um **sistema de cancelamento**, possibilitando a interrupção da automação a qualquer momento, e um **mecanismo de logs** para acompanhamento detalhado das operações.

---

## 🚀 Funcionalidades
✅ **Automatização Web**: O Selenium acessa o site e baixa automaticamente o arquivo XLSX.

✅ **Processamento de Dados**: Os dados são organizados e preparados para inserção no banco.

✅ **Banco de Dados**: Criação de tabelas dinâmicas e armazenamento eficiente no **MySQL**.

✅ **Interface Gráfica (GUI)**: Monitoramento do processo e opções de controle.

✅ **Geração de Logs**: Registro detalhado de todas as operações.

✅ **Sistema de Cancelamento**: Possibilidade de interromper a automação.

---

## 📁 Estrutura do Projeto
```
WEBSCRAPING/
├── about/                          # Informações sobre o projeto
├── database/                       # Arquivos relacionados ao banco de dados
│   ├── conexao/                    # Conexão com o MySQL
│   │   └── MySQLConnection.py      # Classe de conexão MySQL
│   └── consultas/                  # Consultas e manipulação do banco
│       └── insert.py               # Script de inserção de dados
├── download/                       # Arquivos baixados
│   └── dados_emergy_*.xlsx         # Planilhas XLSX
├── logs/                           # Registros de execução
│   └── automation_log.log          # Arquivo de log principal
├── interface/                      # Interface gráfica
│   └── app_interface.py            # Tkinter GUI
├── scripts/                        # Scripts principais
│   ├── main.py                     # Script de automação
│   └── logging_config.py           # Configuração de logs
├── .env                            # Variáveis de ambiente
├── requirements.txt                # Dependências do projeto
├── README.md                       # Documentação
└── Diagrama WebScraping.drawio.png # Diagrama do fluxo
```

---

## 🔧 Tecnologias Utilizadas
- **Python 3.x**
- **Selenium** → Automação web
- **Pandas** → Manipulação de dados
- **MySQL Connector** → Comunicação com o banco
- **dotenv** → Gerenciamento de variáveis de ambiente
- **WebDriver Manager** → Controle do ChromeDriver
- **openpyxl** → Manipulação de arquivos Excel
- **Tkinter** → Interface gráfica
- **Threading** → Execução em segundo plano
- **Logging** → Geração de logs detalhados

---

## ⚙️ Configuração do Ambiente
### 1️⃣ Clonar o repositório
```sh
git clone https://github.com/seu-usuario/webscraping.git
cd webscraping
```

### 2️⃣ Criar e ativar um ambiente virtual (opcional)
```sh
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3️⃣ Instalar as dependências
```sh
pip install -r requirements.txt
```

### 4️⃣ Configurar o arquivo `.env`
Crie um arquivo `.env` na raiz do projeto e adicione:
```
DB_HOST=seu_host
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=seu_banco_de_dados
DB_PORT=sua_porta
```

---

## 🚀 Como Executar o Projeto
### 1️⃣ Executar a Interface Gráfica
```sh
python interface/app_interface.py
```

### 2️⃣ Iniciar a Automação
- A interface terá um botão "Iniciar Automação".
- O Selenium abrirá o navegador e fará o download do arquivo XLSX.
- O arquivo será salvo na pasta `download/`.
- Os dados serão processados e inseridos no **MySQL**.

### 3️⃣ Acompanhar o Progresso
- A interface mostrará logs em tempo real e uma barra de progresso.
- Se necessário, clique em "Cancelar" para interromper a execução.

### 4️⃣ Visualizar Logs
- Clique em "Gerar Logs" na interface.
- O relatório será salvo no arquivo `logs/automation_log.log`.

---

## 📊 Banco de Dados
As tabelas são criadas dinamicamente com base nas abas do arquivo XLSX. Os dados são sanitizados antes da inserção para evitar erros com caracteres inválidos.

---

## 📞 Contato
📩 **Email:** erickbritto060@gmail.com  
🐙 **GitHub:** [erkbritto](https://github.com/erkbritto/WebScraping)  
💼 **LinkedIn:** [erkbritto](https://www.linkedin.com/in/erkbritto/)  
📸 **Instagram:** [erkbritto](https://www.instagram.com/erkbritto/)

