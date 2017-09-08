# coding: utf-8
# Programa escrito por Eric Breno B. dos Santos
# Programa apenas para fins did�ticos
# Recomendado rodar em sistemas linux, � necessario instalar o pacote mechanize e cookielib.
# Para instalar use "sudo apt-get install python-setuptools", "sudo easy_install mechanize",
# "sudo easy_install html2text" e "sudo apt-get install python-bs4"
#
# ########################################################################
# ################### AVISO: PROGRAMA INCABADO ############################
###########################################################################
 
import mechanize, cookielib, time, ssl
import smtplib
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

# Funcao utilizada para sempre reiniciar o browser e nao dar problema ao verificar se houveram mudan�as
# pois o controle academico as vezes buga quando voce esta logado e nao aparece a opcao de realizar matriculas
def logaRetornaBrowser():
    br = mechanize.Browser()
    url = 'https://pre.ufcg.edu.br:8443/ControleAcademicoOnline/'
 
    matric=""
    senha=""
 
    # Prepara para tratar cookies...
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
 
    # Ajusta algumas op��es do navegador...
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
 
    # Pronto! Agora � navegar, acessando a URL usando o m�todo HTTP GET
    br.open(url)
 
    # Se existirem formul�rios, voc� pode selecionar o primeiro (#0), por exemplo...
    br.select_form(nr=0)
 
    # Preencher o formul�rio com os dados de login...
    br.form['login'] = matric
    br.form['senha'] = senha
 
    # Enviar o formul�rio usando o m�todo HTTP POST
    br.submit()
    return br

def avisa_o_maluco(nota):

    email = 'kaio.kassiano.oliveira@gmail.com'
    emails = ['kaio.kassiano.oliveira@gmail.com', 'kaio.kassiano.oliveira@ccc.ufcg.edu.br', 'joserenansl99@gmail.com', 'joao.felipe@ccc.ufcg.edu.br', 'caio.camboim@ccc.ufcg.edu.br', 'adson.silva@ccc.ufcg.edu.br', 'rubensbbatista@gmail.com']
    kaiooo = ['kaio.kassiano.oliveira@gmail.com', 'kaio.kassiano.oliveira@ccc.ufcg.edu.br']
    app = 'acsoloceoiirdqzz'

    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.login(email, app)

    teste2 = 'SAIU A NOTA DA FINAL DE PROB, MIZERA'

    for i in emails:
        print i
        if (i in kaiooo):
            smtp_server.sendmail(email, i, teste2 + ': ' + nota)
        else:
	        smtp_server.sendmail(email, i, teste2)

    smtp_server.quit()
    print('Email sent successfully')

# Faz o parse das informacoes da pagina para poder imprimir no console
def filtraQueOMlkTaDoente(pagina):
    sopa = bs(pagina, "html.parser") # "html.parser" para osx ou windows, "lxml" para linux
    sopa = sopa.findAll('td', attrs={"class": "text-right"})
    parte_que_quero = str(sopa[4]).split()

    return parte_que_quero
 
ultimas_infos = ''
parte_importante = ''
   
first_run = True
   
while 1:   
    print "\n===== Nova requisicao ====="
   
    time.ctime()
    print time.strftime('%X %x %Z')
   
    br = logaRetornaBrowser()
 
    link = "https://pre.ufcg.edu.br:8443/ControleAcademicoOnline/Controlador?command=AlunoTurmaNotas&codigo=1114107&turma=01&periodo=2017.1"
    br.open(link)
    novaPag = br.response().read()
    novaPag += "Terminado com sucesso. Aguarde..."
   
    novo = filtraQueOMlkTaDoente(novaPag)
    print novo
 
    if novo != ultimas_infos and not first_run:
        print "saiu, mizera!"
        print novo
        avisa_o_maluco(novo)
        break
   
    time.sleep(20)
   
    ultimas_infos = novo
    novo = ''
    first_run = False
