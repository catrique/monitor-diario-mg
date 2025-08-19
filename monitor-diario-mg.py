import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import date
import fitz
import urllib.parse

def get_diario_data(day, month, year, is_extraordinary=False):
    base_url = "https://www.diariomunicipal.com.br/amm-mg"
    
    with requests.Session() as s:
        try:
            response_get = s.get(base_url + '/')
            response_get.raise_for_status()
            
            soup = BeautifulSoup(response_get.text, 'html.parser')
            token_element = soup.find('input', {'name': 'calendar[_token]'})
            if not token_element:
                print("Erro: Não foi possível encontrar o token de segurança na página.")
                return None, None
            
            token = token_element.get('value')

            endpoint = "/materia/calendario/extra" if is_extraordinary else "/materia/calendario"
            url_post = base_url + endpoint
            
            payload = {
                'calendar[day]': str(day),
                'calendar[month]': str(month),
                'calendar[year]': str(year),
                'calendar[_token]': token
            }
            
            headers = {
                'Referer': base_url + '/',
                'Accept': 'application/json, text/javascript, */*; q=0.01'
            }

            response_post = s.post(url_post, data=payload, headers=headers)
            response_post.raise_for_status()
            
            data = response_post.json()
            
            if not data.get('edicao'):
                print(f"Nenhum diário encontrado para a data {day}/{month}/{year}.")
                return None, None

            url_arquivos = data['url_arquivos']
            link_diario = data['edicao'][0]['link_diario']
            
            final_pdf_url = f"{url_arquivos}{link_diario}.pdf"
            
            filename = data['edicao'][0]['ds_controle']
            
            return final_pdf_url, filename

        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            if 'response_post' in locals():
                print("Conteúdo da resposta para depuração:", response_post.text)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Erro ao processar a resposta JSON: {e}")
            if 'response_post' in locals():
                print("Conteúdo da resposta para depuração:", response_post.text)
    
    return None, None

def download_pdf(url, filename):
    if not url or not filename:
        print("URL ou nome do arquivo inválido. O download não pode ser feito.")
        return

    try:
        pdf_response = requests.get(url, stream=True)
        pdf_response.raise_for_status()

        if 'application/pdf' not in pdf_response.headers.get('Content-Type', ''):
            print("AVISO: O servidor não retornou um arquivo PDF.")
            print("Conteúdo da Resposta do Servidor:", pdf_response.text)
            filepath = os.path.join(os.getcwd(), filename.replace('.pdf', '.html'))
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(pdf_response.text)
            return
            
        filepath = os.path.join(os.getcwd(), filename)
        
        with open(filepath, 'wb') as f:
            for chunk in pdf_response.iter_content(chunk_size=8192):
                f.write(chunk)
        return filepath
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o arquivo: {e}")
        return None

def send_whatsapp_callmebot(api_key, phone_number, message):
    try:
        encoded_message = urllib.parse.quote(message)
        url = f"https://api.callmebot.com/whatsapp.php?phone={phone_number}&text={encoded_message}&apikey={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar mensagem via Callmebot para {phone_number}: {e}")

def search_names_in_pdf(filepath, pessoas_para_buscar, message_type, pdf_url):
    if not filepath or not os.path.exists(filepath):
        print(f"Erro: O arquivo {filepath} não foi encontrado.")
        return

    try:
        document = fitz.open(filepath)
        
        for pessoa in pessoas_para_buscar:
            name_to_search = pessoa['name']
            phone_number = pessoa['phone']
            api_key = pessoa['api_key']

            found = False
            for page_number in range(len(document)):
                page = document.load_page(page_number)
                text = page.get_text()
                
                if name_to_search.lower() in text.lower():
                    message = f"Olá! O nome '{name_to_search}' foi encontrado no {message_type} na página {page_number + 1}.\n\nPara baixar o PDF, acesse: {pdf_url}"
                    send_whatsapp_callmebot(api_key, phone_number, message)
                    found = True
                    break
            
            if not found:
                message = f"Olá! O nome '{name_to_search}' infelizmente seu nome não está no diário de hoje"
                send_whatsapp_callmebot(api_key, phone_number, message)
            
    except Exception as e:
        print(f"Erro ao ler o arquivo PDF: {e}")

if __name__ == "__main__":
    hoje = date.today()
    dia = hoje.day
    mes = hoje.month
    ano = hoje.year
    data_formatada = hoje.strftime("%d-%m-%Y")
    
    pessoas_para_buscar = [
        {
            'name': 'nome que deseja buscar no diário',
            'phone': 'seu telefone',
            'api_key': 'sua api_key'
        },
        {
            'name': 'nome que deseja buscar no diário',
            'phone': 'seu telefone',
            'api_key': 'sua api_key'
        }
    ]

    url_pdf_oficial, filename_oficial = get_diario_data(day=dia, month=mes, year=ano, is_extraordinary=False)
    
    filepath_oficial = None
    if url_pdf_oficial:
        novo_nome_oficial = f"diario_oficial_{data_formatada}.pdf"
        filepath_oficial = download_pdf(url_pdf_oficial, novo_nome_oficial)

    url_pdf_extra, filename_extra = get_diario_data(day=dia, month=mes, year=ano, is_extraordinary=True)
    
    filepath_extra = None
    if url_pdf_extra:
        novo_nome_extra = f"diario_extra_{data_formatada}.pdf"
        filepath_extra = download_pdf(url_pdf_extra, novo_nome_extra)
    
    if filepath_oficial:
        search_names_in_pdf(filepath_oficial, pessoas_para_buscar, "diário oficial", url_pdf_oficial)
    else:
        print("Não foi possível buscar nomes no diário ordinário pois o arquivo não foi baixado.")
    
    if filepath_extra:
        search_names_in_pdf(filepath_extra, pessoas_para_buscar, "diário extraordinário", url_pdf_extra)
    else:
        print("Não foi possível buscar nomes no diário extraordinário pois o arquivo não foi baixado.")