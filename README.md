# **Automatização de processos**

Este repositório armazena processos de configuração e testes automatizados realizados pelo Suporte.


## Pré-requisitos

Antes de rodar este projeto, você precisa ter instalado:

- [Git](https://git-scm.com/) (para clonar o repositório)
- [Python 3.12](https://www.python.org/downloads/) (ou outra versão necessária)
- Bibliotecas necessárias:
  ```bash
  pip install streamlit
  pip install selenium
  pip install requests
  pip install -r requirements.txt
  ```
- Editor de código


## Instalação e execução

Configurar o git para o usuário ao qual irá realizar a clonagem do repositório:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seuemail@exemplo.com"
```

Criar um repositório local

```bash
git init
```

Acessar pasta criada:

```bash
cd C:\caminho\da\pasta\do\git
```

Clonar repositório já criado:

```bash
git clone https://github.com/usuario/repositorio.git
```


Acesse a pasta do processo que quer executar:

```bash
cd C:\caminho\da\pasta\do\processo
```


Caso sejam realizadas atualizações nos arquivos, realize o commit pelo powershell com os seguintes comandos:

```bash
git add.
git commit -m “Informação do commit”
git push origin main
```


## Estrutura de Pastas

```
SUPORTE/
├── .github/workflows/ # Workflows do GitHub Actions (CI/CD, automação de testes e deploy)
│ ├── python-package.yml
│ └── selenium.yml
├── configurar_noticias/ # Scripts ou módulos para configuração e gerenciamento de notícias
│ ├── README Noticias.md # Processo de execução da automatização
│ ├── dados_formulario.env # Formulário para preenchimento dos dados da notícia a ser configurada
│ ├── noticias.py
│ └── urls.json # URL's dos ambientes em que será realizado o processo
├── tests/ # Testes automatizados da aplicação
│ └── test_app.py
├── README.md # Este arquivo, com informações sobre o projeto
└── requirements.txt # Lista de dependências do Python para instalar com pip
```






