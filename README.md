# Programa de Atualização de Planilha de Controle de Backups

Este é um programa Python que foi projetado para automatizar a atualização de uma planilha do Google Sheets que rastreia os backups controlados de clientes. O programa é capaz de ler informações sobre clientes, nomes de backups e datas/horas de backups de uma planilha e, em seguida, atualiza essas informações com base nos backups detectados em um servidor remoto.

## Requisitos:

  Python 3.11 ou superior instalado no sistema.  
  API do google sheets ativada
  
    https://developers.google.com/sheets/api/quickstart/python?hl=pt-br
    
  Bibliotecas googleapiclient, google_auth_oauthlib, google.oauth2 instaladas. Isso pode ser feito usando o seguinte comando:

    pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

## Configuração Inicial:

  Certifique-se de ter um arquivo client_secret.json que contém as informações de autenticação do Google API. Esse arquivo é necessário para autenticar o acesso à planilha.
  Execute o programa uma vez para autenticar e gerar o arquivo token.json que será usado para autenticação futura.

## Funcionalidades Principais:

  Leitura de informações de clientes, nomes de backups e datas/horas de backups de uma planilha no Google Sheets.
  Verificação de backups em um servidor remoto usando um caminho de rede.
  Atualização das informações de backups detectados na planilha.

## Instruções de Uso:

  Coloque o arquivo client_secret.json na mesma pasta que o programa.
  Execute o programa usando o comando:

    > python nome_do_programa.py

  O programa iniciará a autenticação e, se necessário, abrirá um navegador para autorização.
  Após a autorização, o programa lerá as informações da planilha e iniciará o processo de atualização.
  O programa aguardará por 5 segundos entre cada atualização para evitar problemas de sobrecarga.

## Avisos e Considerações:

  Certifique-se de que o servidor remoto e os caminhos de rede mencionados no programa estejam acessíveis e configurados corretamente.
  Este programa foi projetado para um caso de uso específico. Se você deseja usá-lo para outros fins, pode ser necessário fazer ajustes nas configurações, caminhos e lógica.
  Mantenha suas credenciais de API seguras e não compartilhe o arquivo client_secret.json publicamente.
