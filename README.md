# Projeto de Qualidade do Ar: Impacto Social e Análise de Dados

Este projeto demonstra um pipeline completo de dados, desde a ingestão via API até a transformação, orquestração com Apache Airflow, controle de versão com Git, e visualização com Power BI. O foco principal é a análise de dados de qualidade do ar, com potencial para insights sobre impacto social e ambiental.

## 1. Visão Geral do Projeto

O objetivo deste projeto é coletar, processar e analisar dados de qualidade do ar de diversas cidades ao redor do mundo. A qualidade do ar é um fator crítico para a saúde pública e o meio ambiente, e a análise desses dados pode revelar tendências, identificar áreas de preocupação e informar políticas públicas. Este projeto serve como um exemplo prático de um pipeline de dados de ponta a ponta, ideal para portfólio, utilizando tecnologias modernas de dados.

## 2. Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:

```
projeto_qualidade_ar/
├── .env
├── README.md
├── dags/
│   └── air_quality_dag.py
├── data/
│   ├── raw/
│   └── processed/
├── docker/
│   └── docker-compose.yml
├── docs/
├── src/
│   ├── ingestao/
│   │   └── ingest_data.py
│   ├── transformacao/
│   │   └── transform_data.py
│   └── utils/
└── .gitignore (a ser criado)
```

*   `.env`: Variáveis de ambiente para o Docker Compose.
*   `README.md`: Documentação detalhada do projeto.
*   `dags/`: Contém os DAGs do Apache Airflow para orquestração.
*   `data/`: Armazena os dados brutos (`raw/`) e processados (`processed/`).
*   `docker/`: Contém o arquivo `docker-compose.yml` para configurar o ambiente Airflow.
*   `docs/`: Documentação adicional do projeto (opcional).
*   `src/`: Código fonte dos scripts Python.
    *   `ingestao/`: Script para ingestão de dados da API.
    *   `transformacao/`: Script para limpeza e transformação de dados.
    *   `utils/`: Módulos utilitários (se necessário).
*   `.gitignore`: Arquivo para ignorar arquivos e diretórios no Git.

## 3. Seleção e Acesso à Fonte de Dados (API)

Para este projeto, utilizamos a API do World Air Quality Index (AQICN) para coletar dados de qualidade do ar. Esta API fornece informações em tempo real e históricas sobre diversos poluentes em cidades ao redor do mundo. A escolha desta API se alinha ao foco do projeto em impacto social, permitindo a análise de dados relevantes para a saúde pública.

**API Utilizada**: [AQICN - World Air Quality Index](https://aqicn.org/api/pt/)

Para acessar a API, é necessário um token de acesso. O processo de obtenção do token envolve o registro de um e-mail no site da AQICN. Uma vez obtido, o token é utilizado nos scripts de ingestão de dados para autenticação.

## 4. Ingestão de Dados via API

A ingestão de dados é realizada por um script Python (`src/ingestao/ingest_data.py`) que se conecta à API do AQICN, coleta os dados de qualidade do ar para cidades específicas e os salva em formato JSON no diretório `data/raw`.

**Tecnologias**: Python, `requests` library.

## 5. Transformação de Dados (ETL/ELT) com Pandas e SQL

Após a ingestão, os dados brutos são transformados para um formato mais limpo e estruturado, adequado para análise. Este processo envolve:

*   **Limpeza de Dados**: Tratamento de valores ausentes, remoção de duplicatas e correção de inconsistências.
*   **Enriquecimento de Dados**: Extração de informações adicionais (ex: data, hora) a partir de campos existentes.
*   **Normalização**: Padronização de nomes de cidades e outros campos textuais.

O script `src/transformacao/transform_data.py` utiliza a biblioteca Pandas para realizar essas operações. Os dados transformados são salvos em formato CSV no diretório `data/processed`.

**Tecnologias**: Python, Pandas.

## 6. Automação do Workflow com Apache Airflow

Para automatizar o processo de ingestão e transformação de dados, utilizaremos o Apache Airflow. O Airflow é uma plataforma para programar, orquestrar e monitorar workflows de dados. Ele nos permitirá definir as dependências entre as tarefas (ingestão e transformação) e agendá-las para execução automática.

### Estrutura do DAG

O DAG (Directed Acyclic Graph) será responsável por:
1.  **Ingerir dados**: Executar o script `ingest_data.py` para coletar novos dados da API.
2.  **Transformar dados**: Executar o script `transform_data.py` para limpar e transformar os dados brutos.

### Configuração do Ambiente Airflow

Para rodar o Airflow localmente, você pode usar Docker ou instalá-lo diretamente. Recomenda-se o uso de Docker para um ambiente isolado e consistente.

### Configuração e Execução do Airflow com Docker Compose

1.  **Pré-requisitos**: Certifique-se de ter o Docker e o Docker Compose instalados em sua máquina.

2.  **Navegue até o diretório do projeto**: Abra seu terminal e navegue até o diretório raiz do projeto `projeto_qualidade_ar`.

    ```bash
    cd /home/ubuntu/projeto_qualidade_ar
    ```

3.  **Crie o arquivo `.env`**: Este arquivo contém variáveis de ambiente necessárias para o Airflow. Já foi criado para você, mas verifique seu conteúdo:

    ```bash
    cat .env
    ```

    Conteúdo esperado:
    ```
    AIRFLOW_UID=50000
    _AIRFLOW_WWW_USER_USERNAME=airflow
    _AIRFLOW_WWW_USER_PASSWORD=airflow
    ```

4.  **Inicialize o ambiente Airflow**: Use o Docker Compose para construir as imagens e iniciar os serviços do Airflow.

    ```bash
    docker compose -f docker/docker-compose.yml up airflow-init
    ```

    Este comando inicializará o banco de dados do Airflow e criará o usuário padrão. Aguarde a conclusão.

5.  **Inicie os serviços do Airflow**: Após a inicialização, você pode iniciar todos os serviços do Airflow em segundo plano.

    ```bash
    docker compose -f docker/docker-compose.yml up -d
    ```

    Isso iniciará o webserver, scheduler e worker do Airflow.

6.  **Acesse a UI do Airflow**: Abra seu navegador e acesse `http://localhost:8080`. Use as credenciais `airflow` para usuário e `airflow` para senha (definidas no arquivo `.env`).

7.  **Ative o DAG**: Na interface do Airflow, procure pelo DAG `air_quality_etl_dag` e ative-o. Você pode acionar uma execução manual para testar o pipeline.

### Verificação dos Dados Processados

Após a execução bem-sucedida do DAG, os dados transformados serão salvos no diretório `data/processed` dentro do seu projeto. Você pode verificar os arquivos CSV gerados lá.

```bash
ls -l data/processed
```

Com o Airflow configurado, o pipeline de ingestão e transformação de dados está automatizado. A próxima etapa é configurar o controle de versão com Git para gerenciar o código do projeto.

## 7. Controle de Versão com Git

O controle de versão é essencial para gerenciar o código do projeto, rastrear alterações e colaborar com outros desenvolvedores. Utilizaremos o Git para isso, e o GitHub como repositório remoto.

### Inicializando o Repositório Git

1.  **Navegue até o diretório raiz do projeto**: Se você ainda não estiver lá, navegue até o diretório `projeto_qualidade_ar`.

    ```bash
    cd /home/ubuntu/projeto_qualidade_ar
    ```

2.  **Inicialize o repositório Git**: Este comando cria um novo repositório Git vazio ou reinicializa um existente.

    ```bash
    git init
    ```

3.  **Adicione os arquivos ao staging area**: Adicione todos os arquivos do projeto ao staging area para o primeiro commit.

    ```bash
    git add .
    ```

4.  **Faça o primeiro commit**: Registre as alterações no histórico do repositório.

    ```bash
    git commit -m "Initial commit: Setup project structure, data ingestion, transformation, and Airflow DAG"
    ```

### Conectando ao GitHub (Repositório Remoto)

1.  **Crie um novo repositório no GitHub**: Vá para o GitHub e crie um novo repositório vazio (não inicialize com README, .gitignore ou licença).

2.  **Adicione o repositório remoto**: Conecte seu repositório local ao repositório remoto no GitHub. Substitua `<YOUR_GITHUB_USERNAME>` e `<YOUR_REPOSITORY_NAME>` pelos seus dados.

    ```bash
    git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPOSITORY_NAME>.git
    ```

3.  **Renomeie a branch principal (opcional, mas recomendado)**:

    ```bash
    git branch -M main
    ```

4.  **Envie o código para o GitHub**: Faça o push do seu código local para o repositório remoto.

    ```bash
    git push -u origin main
    ```

Agora seu projeto está versionado e disponível no GitHub. A próxima fase será a apresentação dos dados com Power BI.

## 8. Apresentação do Projeto com Power BI

Após a ingestão e transformação dos dados, a próxima etapa é visualizá-los e apresentá-los de forma significativa. O Power BI é uma ferramenta poderosa para criar dashboards interativos e relatórios que comunicam insights de dados de forma eficaz.

### Carregando os Dados no Power BI

1.  **Abra o Power BI Desktop**: Inicie o aplicativo Power BI Desktop em sua máquina.

2.  **Obtenha Dados**: Na tela inicial ou na guia 'Página Inicial', clique em 'Obter Dados'.

3.  **Selecione a Fonte de Dados**: Escolha 'Texto/CSV' e navegue até o diretório `data/processed` do seu projeto. Selecione o arquivo CSV mais recente gerado pelo script de transformação (ex: `air_quality_processed_YYYYMMDDHHMMSS.csv`).

4.  **Carregue os Dados**: O Power BI exibirá uma prévia dos dados. Clique em 'Carregar' para importar os dados para o modelo de dados do Power BI.

### Criando Visualizações e Dashboards

Com os dados carregados, você pode começar a criar visualizações e dashboards para explorar a qualidade do ar. Algumas ideias de visualizações incluem:

*   **Gráficos de Linha**: Tendências de poluentes (PM2.5, PM10, NO2, etc.) ao longo do tempo.
*   **Gráficos de Barras**: Níveis médios de poluentes por cidade ou por hora do dia.
*   **Mapas**: Visualização da qualidade do ar em diferentes cidades (se os dados de localização forem suficientes).
*   **Cartões**: Exibição de KPIs (Key Performance Indicators) como o AQI médio ou máximo.
*   **Tabelas**: Detalhes dos dados brutos e transformados.

### Publicando e Compartilhando

Após criar seu relatório e dashboard, você pode publicá-lo no serviço do Power BI para compartilhar com outras pessoas. Isso exigirá uma conta do Power BI.

Esta seção do projeto demonstra sua capacidade de não apenas processar dados, mas também de apresentá-los de forma clara e impactante, o que é crucial para qualquer projeto de dados.




## 9. Containerização com Docker

Para garantir que o ambiente de desenvolvimento e execução do projeto seja consistente e reproduzível, utilizaremos o Docker. A containerização empacota o aplicativo e todas as suas dependências em um contêiner isolado, garantindo que ele funcione de forma idêntica em qualquer ambiente.

### Dockerfile para o Projeto

Embora o Airflow já esteja containerizado via `docker-compose.yml`, é uma boa prática ter um `Dockerfile` para a aplicação principal (os scripts Python de ingestão e transformação). Isso permite que o pipeline seja executado independentemente do Airflow, se necessário, ou como parte de um serviço maior.

Um `Dockerfile` básico para os scripts Python pode ser:

```dockerfile
# Use uma imagem base Python
FROM python:3.9-slim-buster

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar os arquivos de requisitos e instalar as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação
COPY . .

# Definir variáveis de ambiente (se necessário, por exemplo, para o token da API)
ENV API_TOKEN="your_api_token_here" # Substitua pelo seu token real ou use secrets do Docker

# Comando para executar o script de ingestão (exemplo)
CMD ["python", "src/ingestao/ingest_data.py"]
```

### Construindo e Executando a Imagem Docker

1.  **Crie um arquivo `requirements.txt`**: Liste todas as dependências Python do seu projeto.

    ```bash
    pip freeze > requirements.txt
    ```

2.  **Construa a imagem Docker**: No diretório raiz do projeto, execute:

    ```bash
    docker build -t air-quality-pipeline .
    ```

3.  **Execute o contêiner**: Você pode executar um script específico ou entrar no contêiner interativamente.

    ```bash
    docker run --name air-quality-container -v $(pwd)/data:/app/data air-quality-pipeline python src/ingestao/ingest_data.py
    ```

    O volume (`-v`) é importante para que os dados gerados dentro do contêiner sejam persistidos no seu sistema de arquivos local.

### Benefícios da Containerização

*   **Portabilidade**: O aplicativo funciona da mesma forma em qualquer ambiente que tenha Docker.
*   **Isolamento**: As dependências do projeto são isoladas do sistema host, evitando conflitos.
*   **Reproducibilidade**: Garante que outros desenvolvedores ou sistemas possam configurar e executar o projeto exatamente como pretendido.

Esta etapa finaliza a parte de infraestrutura do projeto, tornando-o robusto e fácil de implantar.




## 10. Entrega do Projeto

Este projeto é um exemplo completo de um pipeline de dados, ideal para ser incluído em um portfólio. Ele demonstra proficiência em diversas ferramentas e tecnologias essenciais para um engenheiro de dados ou cientista de dados.

### Como Usar Este Projeto

1.  **Clone o Repositório**: Obtenha o código do projeto do GitHub.

    ```bash
    git clone https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPOSITORY_NAME>.git
    cd <YOUR_REPOSITORY_NAME>
    ```

2.  **Obtenha seu Token da API AQICN**: Siga as instruções na seção "Seleção e Acesso à Fonte de Dados (API)" para obter seu próprio token e atualize o arquivo `src/ingestao/ingest_data.py` com seu token.

3.  **Configure e Inicie o Airflow**: Siga as instruções na seção "Automação do Workflow com Apache Airflow" para configurar e iniciar o ambiente Airflow via Docker Compose.

4.  **Execute o Pipeline**: Ative o DAG `air_quality_etl_dag` na UI do Airflow para iniciar a ingestão e transformação dos dados.

5.  **Analise os Dados no Power BI**: Carregue os dados processados no Power BI Desktop conforme as instruções na seção "Apresentação do Projeto com Power BI" e crie suas próprias visualizações.

### Próximos Passos e Melhorias

*   **Integração com Banco de Dados**: Em vez de salvar em CSV, os dados processados poderiam ser carregados em um banco de dados (ex: PostgreSQL, MySQL) para análises mais complexas e persistência.
*   **Monitoramento e Alertas**: Implementar monitoramento de performance do pipeline e alertas para falhas.
*   **Mais Fontes de Dados**: Integrar dados de outras APIs ou fontes para enriquecer a análise.
*   **Modelagem de Dados**: Criar um modelo de dados mais robusto (ex: esquema estrela) para otimizar a análise no Power BI.
*   **Dashboards Avançados**: Desenvolver dashboards mais complexos e interativos no Power BI, explorando diferentes aspectos da qualidade do ar e seu impacto.

Este projeto oferece uma base sólida para expandir e aprofundar seus conhecimentos em engenharia de dados e análise, com um foco significativo em dados de impacto social.


