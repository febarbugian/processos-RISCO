import os as os
import requests
import json
import pandas as pd
import time
from dotenv import dotenv_values


class APILine():
    def __init__(self):
        config = dotenv_values(".env")
        self.username = config['LINE_USER']
        self.password = config['LINE_PW']
        self.broker_code = config['LINE_BROKER']
        self.category_code = config['LINE_CATEGORY']
        self.url = 'https://api.line.bvmfnet.com.br/api/v1.0/' ##cert 'https://api.line.trd.cert.bvmfnet.com.br/api/v1.0/'
        self.url_token = 'https://api.line.bvmfnet.com.br/api/oauth/token' ##cert 'https://api.line.trd.cert.bvmfnet.com.br/api/oauth/token'
        self.token = None
        self.account = None
        self.document = None

    def auth(self):
        r = requests.get(self.url + 'token/authorization')
        authheader = r.json()['header']

        header = {'Authorization' : "Basic "+authheader,
                'content-type': 'application/x-www-form-urlencoded'
                }
        
        params = {'grant_type': 'password',
                'username': self.username, 
                'password' : self.password, 
                'brokerCode': self.broker_code,
                'categoryCode': self.category_code
                }
        
        t = requests.post(self.url_token,headers=header,data=params)
        
        if t.status_code == 200:
            token = t.json()
            self.token = token['access_token']
        else:
            print(f'Erro na solicitação: {t.status_code} - {t.text}')

    def consultaAccount(self, cd_cliente):
        time.sleep(1)
        url = self.url + 'account'

        params = {
            'accountCode': cd_cliente
        }

        headers = {
            'Authorization': 'Bearer '+ self.token,  
        }

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            accounts = response.json()
            print(accounts)
            for account in accounts:
                self.account = account
                return self.account
        else:
            print(f'Erro na solicitação: {response.status_code} - {response.text}')

    def consultaDocumento(self, documento):
        time.sleep(1)
        url = self.url + 'document'

        params = {
            'documentCode': documento
        }

        headers = {
            'Authorization': 'Bearer '+ self.token,  
        }

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            documents = response.json()
            print(documents)
            for document in documents:
                self.document = document
                return self.account
        else:
            print(f'Erro na solicitação: {response.status_code} - {response.text}')

    def isBlockedAccount(self, valor):
        time.sleep(1)
        AccId = str(self.account['id'])
        url = self.url + 'account/' + AccId

        data = {
            "isBlocked": valor
            # "isProtected": True
            #"profileId": 42 
        }

        headers = {
            'Authorization': 'Bearer '+ self.token,
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json=data, headers=headers)
        
        conta = str(self.account['code'])

        if response.status_code == 200:
            print(f'Conta {conta} atualizada com sucesso.')
        elif response.status_code == 201:
            print("Conta criada com sucesso.")
        else:
            print(f'Erro na solicitação: {response.status_code} - {response.text}')

    def consultaLimiteMercadosConta(self):
        time.sleep(1) 
        AccId = str(self.account['id'])

        url = self.url + 'account/' +AccId +'/lmt/mkta'
        
        params = {
            'accId': AccId
        }

        headers = {
            'Authorization': 'Bearer '+ self.token,  
        }

        response = requests.get(url,params=params, headers=headers)

        if response.status_code == 200:
            limite_conta = response.json()
            return limite_conta
        else:
            print(f'Erro na solicitação: {response.status_code} - {response.text}')

    def consultaLimiteConta(self):
        time.sleep(1) 
        AccId = str(self.account['id'])

        url = self.url + 'account/' +AccId +'/lmt'
        
        params = {
            'accId': AccId
        }

        headers = {
            'Authorization': 'Bearer '+ self.token,  
        }

        response = requests.get(url,params=params, headers=headers)

        if response.status_code == 200:
            limite_conta = response.json()
            return limite_conta
        else:
            print(f'Erro na solicitação: {response.status_code} - {response.text}')

if __name__ == '__main__':
    cd_cliente = 14348
    api_line = APILine()
    api_line.auth()
    api_line.consultaAccount(cd_cliente)





