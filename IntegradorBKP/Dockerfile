# Use a imagem base com suporte ao Python
FROM python:3.11.4

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos necessários para o diretório de trabalho
COPY main.py .
COPY client_secret.json .
COPY token.json .

# Instale as dependências do seu código (API)
RUN pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Atualizando para utilizar o FTP
VOLUME [ "/app/ftp_share" ]

# Execute o seu código quando o contêiner for iniciado
CMD [ "python", "main.py" ]