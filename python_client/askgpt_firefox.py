#@Autor: Felipe Frechiani de Oliveira
#Este programa acessa o site do chatgpt e faz uma pergunta e captura a resposta por meio de um servidor do selenium.
#Somente funcionou usando o firefox com o chrome não funcionou.  

from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs





# Função para fazer uma pergunta ao ChatGPT
def ask_gpt(question):

    # Configurações do Selenium para se conectar a um serviço Selenium remoto
    selenium_host = 'selenium'  # Atualize com o endereço IP ou o nome do host do seu serviço Selenium remoto
    selenium_port = '4444'  # Atualize com a porta em que o serviço Selenium remoto está sendo executado
    # URL da página do ChatGPT
    url = "https://chat.openai.com/"
    print("Accessando url do chatgpt:" + url)
    print("Usando o broswer firefox...")
    # Configuração do WebDriver remoto
    webdriver_remote_url = f"http://{selenium_host}:{selenium_port}/wd/hub"
    print("Roda do selenium:" + webdriver_remote_url)
    firefox_options = Options()
    browser = webdriver.Remote(webdriver_remote_url, options=firefox_options)

    # Abre a página do ChatGPT
    try:   

        browser.get(url)
        print("URL da pagina:" + browser.current_url)
        print("Titulo da pagina:" + browser.title)
        time.sleep(1)  # Espera 3 segundos para garantir que a página esteja carregada
        # Insere a pergunta no campo de entrada
        if browser is not None:       
            input_field = browser.find_element(By.ID , "prompt-textarea")
            #print(input_field)
            actions = ActionChains(browser)
            # Clica no botão
            actions.click(input_field).perform()
            input_field.send_keys(question)
            # Clica no botão de enviar
            submit_button = browser.find_element(By.XPATH , '//button[@data-testid="send-button"]')
            time.sleep(1)  # Espera 5 segundos para a resposta ser gerada
            browser.save_screenshot("tela_antes_da_resposta.png")
            submit_button.click()
            print("aguardando resposta")
            # Aguarda a resposta do ChatGPT
            time.sleep(4)  # Espera 5 segundos para a resposta ser gerada
            browser.save_screenshot("tela_depois_da_resposta.png")
            # Obtém a resposta
            response = browser.find_element(By.XPATH ,'//div[@data-message-author-role="assistant"]').text
            browser.quit()  
            return response
    except NoSuchElementException:
        print("Elemento não encontrado na página.")   
        
         
    

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_params = parse_qs(post_data.decode('utf-8'))

        if 'question' in post_params:
            question = post_params['question'][0]
            response = ask_gpt(question)  # Suponha que get_gpt_response seja sua função para interagir com o ChatGPT
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'response': response}).encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Bad Request')

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()
    
    
    
    

if __name__ == "__main__":
    run()




