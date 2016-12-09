#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import TestConection
import AnaliseDeComentariosBancoDeDados

from easygui import *

USER = TestConection.USERNAME
PASSWORD = TestConection.PASSWORD

# Este método realiza a busca de informações de uma CR. Utiliza as informações da tabela
def JSQL_get_cr_informations(project_key, issue_num):
    sql_query = "SELECT p.pkey as project, ja.actionbody as jiraaction, ja.author as author " \
                "FROM jiraissue i, project p, jiraaction ja " \
                "WHERE i.project = p.id AND ja.issueid = i.id " \
                "AND i.issuenum = % s AND p.pkey = '%s' ORDER BY ja.created DESC" % (issue_num, project_key)

    data = json.dumps({
        "real_time": 1,
        "sql": sql_query})

    server_request = '%s/%s/%s/%s' % ('http://jsql.mot.com/rest', 'query/', USER, PASSWORD)

    return requests.post(server_request, data=data).json()

# este metodo faz a captura do status, projeto e numero da issue, para que possamos
# utilizar os outros metodos sabendo destas informações iniciais. Tudo de um determinado
# usuario o qual esta sendo passado como parâmetro. Além disso, são listadas apenas CRs
# cujo status eh diferente de Closed, pois estas nao importam para o sistema de lembretes
# que esta sendo desenvolvido.
def select_all_data(user):
    sql_query = "SELECT p.pkey as project, i.issuenum as issuenum, s.pname as status " \
                "FROM jiraissue i, project p, jiraaction ja, issuestatus s " \
                "WHERE i.project = p.id AND ja.issueid = i.id " \
                "AND i.issuestatus = s.id AND s.pname != 'Closed' " \
                "AND i.reporter = '% s' ORDER BY ja.created DESC" % (user)

    data = json.dumps({
        "real_time": 1,
        "sql": sql_query})

    server_request = '%s/%s/%s/%s' % ('http://jsql.mot.com/rest', 'query/', USER, PASSWORD)

    return requests.post(server_request, data=data).json()

def verifica(coreId):

    dic = select_all_data(coreId)
    lista = []
    unique = [x for x in dic if x not in lista and (lista.append(x) or True)]

    print 'The User has ', len(unique), ' opened CRs!'

    for valor in unique:

        cr = JSQL_get_cr_informations(valor.get('PROJECT'), valor.get('ISSUENUM'))
        link = valor.get('PROJECT') + '-' + valor.get('ISSUENUM')

        print 'ANALYSING... \nCR: ', link

        request = 0
        notrequest = 0

        for comment in cr:
            listaDeRelevancias = []
            if comment.get('AUTHOR') != coreId:
                resultado = AnaliseDeComentariosBancoDeDados.analise(comment.get('JIRAACTION').upper(), coreId,
                                                                     listaDeRelevancias)
                # print resultado
                if AnaliseDeComentariosBancoDeDados.analisando_prioridades(resultado):
                    if AnaliseDeComentariosBancoDeDados.mencionou_usuario(resultado):
                        request += 5
                    request += 1
                else:
                    notrequest += 1

            else:
                break
        # print 'request ',request
        # print 'notrequest ', notrequest

        if request >= notrequest and (request != 0):
            print 'REQUEST FOUND AT: https://idart.mot.com/browse/' + link
        else:
            print 'REQUEST NOT FOUND'

def search_requests():

    coreId = enterbox("Enter with your Lenovo Core ID")
    msgbox("Searching requests for CRs opened by " + coreId + ". \nPlease, look at the console!")

    verifica(coreId)