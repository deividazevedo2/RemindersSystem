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

if __name__ == '__main__':

    #msg = "Do you want to continue?"
    #msgbox('Testing with EasyGUI')

    # msg = "Enter logon information"
    # title = "Demo of multpasswordbox"
    # fieldNames = ["Server ID", "User ID", "Password"]
    # fieldValues = []  # we start with blanks for the values
    #
    # passwordbox(msg='Enter your password.', title=' ', default='')

    coreId = enterbox("Enter with your Lenovo Core ID")
    msgbox("Searching requests for CRs opened by " + coreId + ". \nPlease, look at the console!")

    # coreId = 'deivid'

    dic = select_all_data(coreId)
    lista = []
    unique = [x for x in dic if x not in lista and (lista.append(x) or True)]

    print 'Este usuario tem ', len(unique), ' CRs abertas!'

    for valor in unique:

        cr = JSQL_get_cr_informations(valor.get('PROJECT'), valor.get('ISSUENUM'))
        link = valor.get('PROJECT')+'-'+valor.get('ISSUENUM')

        print 'ANALISANDO... \nCR: ', link

        request = 0
        notrequest = 0

        for comment in cr:
            listaDeRelevancias = []
            if comment.get('AUTHOR') != coreId:
                resultado = AnaliseDeComentariosBancoDeDados.analise(comment.get('JIRAACTION').upper(), coreId,
                                                                     listaDeRelevancias)
                print resultado
                if AnaliseDeComentariosBancoDeDados.analisando_prioridades(resultado):
                    if AnaliseDeComentariosBancoDeDados.mencionou_usuario(resultado):
                        request+=5
                    request+=1
                else:
                    notrequest+=1

                print 'requests: ', request
                print 'notrequests: ', notrequest

            else:
                break

            #print comment.get('ACTIONBODY').upper()

        if request > notrequest:
            print 'REQUEST ENCONTRADO: https://idart.mot.com/browse/' + link
        else:
            print 'NAO TEM REQUEST'
    # for elemento in unique:
    #
    #     dic = JSQL_get_cr_informations(unique.get(''),'11775')
    #     cont = 1
    #     for list in dic:
    #         lista = list
    #         if lista.get('AUTHOR') != 'deivid':
    #             AnaliseDeComentariosBancoDeDados.analise(lista.get('JIRAACTION').upper())
    #         else:
    #             break
    #
    #         print lista.get('ACTIONBODY').upper()
    #     print dic
    #     JSQL_get_tc_custom_fields("IKSWN-10092")