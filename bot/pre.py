# -*- coding: utf-8 -*-

import mechanicalsoup
import time
import requests
import webbrowser
from .utils import response

BASE_URL = 'https://pre.ufcg.edu.br:8443/ControleAcademicoOnline'
KEYWORD = 'Realizar matricula'


browser = mechanicalsoup.StatefulBrowser(
    soup_config={'features': 'lxml'},
    raise_on_404=True,
    user_agent='Mozilla/5.0 (X11;U; '
               'Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615Fedora/3.0.1-1.fc9 Firefox/3.0.1',)


def authenticate(enrolment, password):
    if is_logged():
        logout()
    browser.open(BASE_URL)
    browser.select_form('form[action="Controlador"]')
    browser['login'] = enrolment
    browser['senha'] = password
    browser.submit_selected()


def is_logged():
    # Se for a primeira visita o valor é None, logo retorna false.
    return browser.get_url()


def logout():
    logout_url = '{base_url}/Controlador?command=SairDoSistema'.format(base_url=BASE_URL)
    browser.open(logout_url)


def is_enrolment_released(itens):
    enrolment_released = False
    for item in itens:
        if KEYWORD in item.text:
            enrolment_released = True
    return enrolment_released


def parse_html():
    dropdown_menu = browser.get_current_page().find('ul', {'aria-labelledby': 'alunoMatriculas'})
    itens = dropdown_menu.find_all('li')
    return itens


def open_browser():
    # abre a página do controle academico no browser default.
    webbrowser.open_new_tab(BASE_URL)


def start_bot(enrolment, password):
    enrolment_released = False
    while not enrolment_released:
        try:
            authenticate(enrolment, password)
            itens = parse_html()
            enrolment_released = is_enrolment_released(itens)
            response.waiting()
            time.sleep(3)
        except requests.exceptions.HTTPError:
            response.http_error()
        except requests.exceptions.ConnectionError:
            response.connection_error()
        except requests.exceptions.Timeout:
            response.timeout_error()
    response.sucess()
    open_browser()


