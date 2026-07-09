# Processo automatizado de configuração de notícias

O seguinte pojeto trata da execução e configuração de forma automatizada das notícias da Home Notícias do Sistema Universa. 




## Como usar

1. A configuração inicial é realizada de forma manual em um ambiente e após isso são adicionadas as credenciais de configuração no arquivo .env para que o processo seja realizado para os demais ambientes.
2. Através do streamlit.io, será executado o script criado através da URL https://suporte-noticias.streamlit.app/
3. No formulário disponibilizado pelo Streamlit serão informados os dados necessários para a execução do processo. Essas informações serão armazenadas temporariamente e utilizadas durante a execução da automação.
4. Na própria página de preenchimento do formulário será executada a automação em segundo plano. Durante a execução, serão exibidas capturas de tela (prints) das etapas realizadas em cada ambiente, permitindo o acompanhamento do processo em tempo real.
5. Caso ocorra algum erro durante a execução, será possível identificá-lo por meio das capturas de tela (prints) exibidas ao longo do processo. Dessa forma, será possível verificar em qual ambiente a automação falhou e realizar, se necessário, a configuração manual da notícia.
   


## Configurações

A automação é executada em segundo plano devido às limitações do Streamlit Community Cloud, que não permite a abertura e a interação direta com uma janela do navegador para o usuário. Dessa forma, o processo é realizado internamente no servidor, enquanto a página exibe as capturas de tela (prints) das etapas executadas, permitindo acompanhar o andamento da automação e identificar eventuais falhas.


**Atenção!**

Antes de iniciar a execução do processo, verifique se a versão do navegador Google Chrome instalada em seu computador é compatível com a versão definida no arquivo noticias.py. O trecho abaixo indica onde, no script, pode ser verificada a versão do Google Chrome que está sendo utilizada no momento:

```
navegador = uc.Chrome(
        version_main=150,  # versão do Chromium do Streamlit Cloud
        options=options
    )
```
