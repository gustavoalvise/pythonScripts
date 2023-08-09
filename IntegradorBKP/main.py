from __future__ import print_function
import os.path
import os
import datetime
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from ftplib import FTP

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Obter informações de data e hora da modificação do arquivo ou pasta
def obter_data_mod_arquivo(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        data_mod_timestamp = os.path.getmtime(caminho_arquivo)
        data_mod = datetime.datetime.fromtimestamp(data_mod_timestamp)
        return data_mod
    else: 
        return None

# Obter o arquivo mais recente dentro de uma pasta

def obter_arquivo_mais_recente(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        arquivos = os.listdir(caminho_arquivo)
        arquivos = [arquivo for arquivo in arquivos if os.path.isfile(os.path.join(caminho_arquivo, arquivo))]
        data_mod_arquivos = [(arquivo, os.path.getmtime(os.path.join(caminho_arquivo, arquivo))) for arquivo in arquivos]
        arquivo_mais_recente = max(data_mod_arquivos, key=lambda x: x[1])[0]
        return arquivo_mais_recente
    else: 
        return None

def main():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Loga o usuário caso exista uma "token.json"
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            #Caso o token esteja expirado, faz um refresh nele
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Salva as credenciais para a proxima vez
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    
    # Leitura de nomes de clientes
    
    planilha_nome = 'BKP Controlado!B:B'
    result = service.spreadsheets().values().get(
    spreadsheetId='1g9wP0Imt7cU4PGK-Y98qBaQykfBb6G97jojSVlH_NWc', range=planilha_nome).execute()
    vetor_clientes_raw = result.get('values', [])
    vetor_clientes = [value[0] for value in vetor_clientes_raw if value] # Limpeza dos valores
    # print(vetor_clientes)

    # Leitura dos nomes dos backups

    planilha_bkp = 'BKP Controlado!J:J'
    result = service.spreadsheets().values().get(
    spreadsheetId='1g9wP0Imt7cU4PGK-Y98qBaQykfBb6G97jojSVlH_NWc', range=planilha_bkp).execute()
    vetor_bkp_raw = result.get('values', [])
    vetor_bkp = [value[0] for value in vetor_bkp_raw if value] # Limpeza dos valores
    # print(vetor_bkp)

    # Leitura das data/hora dos backups

    planilha_dh = 'BKP Controlado!K:K'
    result = service.spreadsheets().values().get(
    spreadsheetId='1g9wP0Imt7cU4PGK-Y98qBaQykfBb6G97jojSVlH_NWc', range=planilha_dh).execute()
    vetor_dh = result.get('values', [])
    # print(vetor_dh)


    # Criando a estutura de FTP

    # ftp = FTP('')  # Conecta ao servidor FTP
    # ftp.login(user='', passwd='')  # Autenticação FTP
    # ftp.cwd(caminho_pasta)  # Muda para a pasta do cliente    


    # Criando o loop de atualização da planilha

    for index, cliente in enumerate(vetor_clientes):
        time.sleep(5)
        caminho_pasta = f'//192.168.1.211/ftp/{cliente}/'       
        try:
            data_backup_delphi = obter_data_mod_arquivo(caminho_pasta + 'Bkp$implesDelphi')
            data_backup_web = obter_data_mod_arquivo(caminho_pasta + 'Bkp$implesWeb')
            data_backup_nfe = obter_data_mod_arquivo(caminho_pasta + 'BkpXML-Nfe')
        except:
            data_backup_delphi = None
            data_backup_web = None
            data_backup_nfe = None
        
        if obter_arquivo_mais_recente(caminho_pasta + 'Bkp$implesDelphi') != None:
            arquivo_busca_delphi = obter_arquivo_mais_recente(caminho_pasta + 'Bkp$implesDelphi') # Obtem o nome do arquivo
            # print(f'{arquivo_busca_delphi}')
            if vetor_bkp[index].split()[0] == arquivo_busca_delphi.split()[0]: # Pega a primeira parte do vetor
                values={'values':[[arquivo_busca_delphi]]}
                request = service.spreadsheets().values().update(
                    spreadsheetId='1g9wP0Imt7cU4PGK-Y98qBaQykfBb6G97jojSVlH_NWc', 
                    range=f'BKP Controlado!J{index+1}',
                    valueInputOption='RAW',
                    body=values
                ).execute()
                data_backup_delphi = data_backup_delphi.strftime('%d/%m/%Y %H:%M:%S') #Transofrma a string em data/hora
                values={'values':[[data_backup_delphi]]}
                request = service.spreadsheets().values().update(
                    spreadsheetId='1g9wP0Imt7cU4PGK-Y98qBaQykfBb6G97jojSVlH_NWc', 
                    range=f'BKP Controlado!K{index+1}',
                    valueInputOption='RAW',
                    body=values
                ).execute()

        if obter_arquivo_mais_recente(caminho_pasta + 'Bkp$implesWeb') != None:
            arquivo_busca_web = obter_arquivo_mais_recente(caminho_pasta + 'Bkp$implesWeb')
            if vetor_bkp[index].split()[0] == arquivo_busca_web.split()[0]:
                values={'values':[[arquivo_busca_web]]}
                request = service.spreadsheets().values().update(
                    spreadsheetId='1g9wP0Imt7cU4PGK-Y98qBaQykfBb6G97jojSVlH_NWc', 
                    range=f'BKP Controlado!J{index+1}',
                    valueInputOption='RAW',
                    body=values
                ).execute()
                data_backup_web = data_backup_web.strftime('%d/%m/%Y %H:%M:%S')
                values={'values':[[data_backup_web]]}
                request = service.spreadsheets().values().update(
                    spreadsheetId='1g9wP0Imt7cU4PGK-Y98qBaQykfBb6G97jojSVlH_NWc', 
                    range=f'BKP Controlado!K{index+1}',
                    valueInputOption='RAW',
                    body=values
                ).execute()

        if obter_arquivo_mais_recente(caminho_pasta + 'BkpXML-Nfe') != None:
            arquivo_busca_nfe = obter_arquivo_mais_recente(caminho_pasta + 'BkpXML-Nfe')
            if vetor_bkp[index].split()[0] == arquivo_busca_nfe.split()[0]:
                values={'values':[[arquivo_busca_nfe]]}
                request = service.spreadsheets().values().update(
                    spreadsheetId='1g9wP0Imt7cU4PGK-Y98qBaQykfBb6G97jojSVlH_NWc', 
                    range=f'BKP Controlado!J{index+1}',
                    valueInputOption='RAW',
                    body=values
                ).execute()
                data_backup_nfe = data_backup_nfe.strftime('%d/%m/%Y %H:%M:%S')
                values={'values':[[data_backup_nfe]]}
                request = service.spreadsheets().values().update(
                    spreadsheetId='1g9wP0Imt7cU4PGK-Y98qBaQykfBb6G97jojSVlH_NWc', 
                    range=f'BKP Controlado!K{index+1}',
                    valueInputOption='RAW',
                    body=values
                ).execute()

        
        # print(f'''
        #        Cliente: {cliente}
        #        Data Backup Delphi: {data_backup_delphi}
        #        Data Backup Web: {data_backup_web}
        #        Data Backup XML: {data_backup_nfe}
        #        ''')
        

if __name__ == '__main__':
    main()