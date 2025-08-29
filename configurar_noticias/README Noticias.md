# Processo automatizado de configuração de notícias

O seguinte pojeto trata da execução e configuração de forma automatizada das notícias da Home Notícias do Sistema Universa. 




## Como usar

1. A configuração inicial é realizada de forma manual em um ambiente e após isso são adicionadas as credenciais de configuração no arquivo .env para que o processo seja realizado para os demais ambientes.
2. Atualize os dados do arquivo dados_formulario.env.
3. No powershell execute o seguinte comando:
   ```
   streamlit run noticias.py
   ```
4. Será aberta uma guia do navegador para que sejam informados os dados de login, preencha-os.
5. Depois de preenchido selecione o botão para executar o processo e aguarde um momento, as urls começaram a serem abertas e a configuração será iniciada.
   


## Configurações

Este projeto utiliza variáveis de ambiente para armazenar informações das configurações das notícias. Com os seguintes dados:

```env
TITULO = titulonoticia
HTML = htmldanoticia
DATA_INICIO = datainicionoticia
DATA_FIM = datafimnoticia
```
