# coding: utf-8
# Programa escrito por Eric Breno B. dos Santos
# Programa apenas para fins didáticos
# Recomendado rodar em sistemas linux, é necessario instalar o pacote mechanize e cookielib.
# Para instalar use "sudo apt-get install python-setuptools", "sudo easy_install mechanize",
# "sudo easy_install html2text" e "sudo apt-get install python-bs4"
#
# ########################################################################
# ################### AVISO: PROGRAMA INCABADO ############################
###########################################################################
 
import mechanize, cookielib, time, ssl
from os import system
from bs4 import BeautifulSoup as bs
 
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context        

# Funcao utilizada para sempre reiniciar o browser e nao dar problema ao verificar se houveram mudanças
# pois o controle academico as vezes buga quando voce esta logado e nao aparece a opcao de realizar matriculas
def logaRetornaBrowser():
    br = mechanize.Browser()
    url = 'https://pre.ufcg.edu.br:8443/ControleAcademicoOnline/'
 
    matric=""
    senha=""
 
    # Prepara para tratar cookies...
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
 
    # Ajusta algumas opções do navegador...
    br.set_handle_equiv(True)
    br.set_handle_gzip(False)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
 
    # Configura o user-agent.
    # Do ponto de vista do servidor, o navegador agora o Firefox.
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11;\
     U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615\
    Fedora/3.0.1-1.fc9 Firefox/3.0.1')]      
 
    # Pronto! Agora é navegar, acessando a URL usando o método HTTP GET
    br.open(url)
 
    # Se existirem formulários, você pode selecionar o primeiro (#0), por exemplo...
    br.select_form(nr=0)
 
    # Preencher o formulário com os dados de login...
    br.form['login'] = matric
    br.form['senha'] = senha
 
    # Enviar o formulário usando o método HTTP POST
    br.submit()
    return br

# Faz o parse das informacoes da pagina para poder imprimir no console
def filtraQueOMlkTaDoente(pagina):
    sopa = bs(pagina, "lxml") # "lxml" para linux, "html.parser" para windows
    sopa = sopa.findAll('li', attrs={"class": "dropdown"})
    parte_que_quero = str(sopa[1]).split()
 
    return "\n".join([p for p in parte_que_quero if "href" in p])
 
ultimas_infos = ''
parte_importante = ''
   
first_run = True
   
while 1:   
    system("clear") # Opcional
   
    time.ctime()
    print time.strftime('%X %x %Z')
   
    br = logaRetornaBrowser()
 
    link = "https://pre.ufcg.edu.br:8443/ControleAcademicoOnline/Controlador"
    br.open(link)
    novaPag = br.response().read()
    novaPag += "Terminado com sucesso. Aguarde..."
   
    novo = filtraQueOMlkTaDoente(novaPag)
    print novo
 
    if novo != ultimas_infos and not first_run:
        print "Algo mudou!"
        print ultimas_infos    
        break
   
    time.sleep(15)
   
    ultimas_infos = novo
    novo = ''
    first_run = False