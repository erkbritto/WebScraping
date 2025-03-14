📌 Projeto de Automação e Armazenamento de Dados 📖 Sobre o Projeto Este projeto tem como objetivo automatizar o download de um arquivo XLSX a partir de um site, processar seus dados e armazená-los em um banco de dados MySQL. Ele utiliza Selenium para interagir com a web, Pandas para manipulação dos dados e MySQL Connector para armazená-los de forma eficiente.

Além disso, foi desenvolvida uma interface gráfica com Tkinter, permitindo o monitoramento em tempo real do processo e a geração de logs organizados. O projeto também inclui um sistema de cancelamento, que permite interromper a automação a qualquer momento.

🚀 Funcionalidades Automação Web: O Selenium acessa o site e baixa automaticamente o arquivo XLSX.

Processamento de Dados: Os dados da planilha são organizados e preparados para inserção no banco de dados.

Banco de Dados: Criação de tabelas dinâmicas e inserção dos dados no MySQL.

Interface Gráfica (GUI): Exibição do progresso da automação, botões para iniciar, cancelar e gerar logs.

Geração de Logs: Registro de todas as operações para acompanhamento e depuração.

Cancelamento: Permite interromper a automação a qualquer momento.

📁 Estrutura do Projeto WEBSCRAPING/ ├── about/ # Informações sobre o projeto ├── database/ # Arquivos relacionados ao banco de dados │ ├── conexao/ # Conexão com o banco de dados │ │ └── MySQLConnection.py # Classe para gerenciar a conexão MySQL │ └── consultas/ # Consultas e operações no banco de dados │ └── insert.py # Script para inserir dados no MySQL ├── download/ # Arquivos baixados pelo web scraping │ └── dados_emergy_*.xlsx # Arquivos Excel baixados ├── logs/ # Logs gerados durante a execução │ └── automation_log.log # Arquivo de log principal ├── interface/ # Interface gráfica do projeto │ └── app_interface.py # Interface gráfica usando Tkinter ├── scripts/ # Scripts principais do projeto │ ├── main.py # Script principal de web scraping │ └── logging_config.py # Configuração do sistema de logs ├── .env # Variáveis de ambiente (credenciais do banco de dados) ├── requirements.txt # Dependências do projeto ├── README.md # Documentação do projeto └── Diagrama WebScraping.drawio.png # Diagrama de fluxo do projeto 🔧 Tecnologias Utilizadas Python 3.x

Selenium → Automação web

Pandas → Manipulação de dados

MySQL Connector → Comunicação com o banco de dados

dotenv → Gerenciamento de variáveis de ambiente

WebDriver Manager → Gerenciamento do ChromeDriver

openpyxl → Manipulação de arquivos Excel

Tkinter → Interface gráfica para interação com o usuário

Threading → Execução de tarefas em segundo plano

Logging → Geração de logs detalhados

⚙️ Configuração do Ambiente 1️⃣ Clonar o repositório git clone https://github.com/seu-usuario/webscraping.git cd webscraping

2️⃣ Criar e ativar um ambiente virtual (opcional) python -m venv venv source venv/bin/activate # Linux/Mac venv\Scripts\activate # Windows

3️⃣ Instalar as dependências pip install -r requirements.txt

4️⃣ Configurar o arquivo .env Crie um arquivo .env na raiz do projeto e adicione as credenciais do banco de dados:

DB_HOST=seu_host DB_USER=seu_usuario DB_PASSWORD=sua_senha DB_NAME=seu_banco_de_dados DB_PORT=sua_porta

🚀 Como Executar o Projeto

Executar a Interface Gráfica python interface/app_interface.py

Na interface, clique em "Iniciar Automação" O Selenium abrirá o navegador (em modo headless, se configurado), acessará o site e fará o download do arquivo XLSX.

O arquivo será salvo na pasta download/.

O script processará os dados e os armazenará nas tabelas correspondentes no banco de dados MySQL.

Acompanhe o Progresso A interface gráfica exibirá logs em tempo real e uma barra de progresso.
Caso necessário, clique em "Cancelar" para interromper a automação.

Para visualizar os logs, clique em "Gerar Logs" Um relatório completo das operações será exibido no arquivo automation_log.log.
📊 Banco de Dados O projeto cria automaticamente as tabelas no banco de dados com base nas abas da planilha XLSX e insere os dados de forma dinâmica. As tabelas são nomeadas de acordo com as abas do arquivo Excel, e os dados são limpos para evitar problemas com caracteres inválidos.

📞 Contato Caso tenha dúvidas ou sugestões, entre em contato:

Email: erickbritto060@gmail.com

GitHub: https://github.com/erkbritto/WebScraping

LinkedIn: https://www.linkedin.com/in/erkbritto/

instagram: https://www.instagram.com/erkbritto/
