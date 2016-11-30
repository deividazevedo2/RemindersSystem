#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import TestConection

USER = TestConection.USERNAME
PASSWORD = TestConection.PASSWORD

#"SELECT r.pname as resolution, p.pkey as project, ja.actionbody as jiraaction " \
#"FROM jiraissue i, resolution r, project p, jiraaction ja " \
#"WHERE i.resolution = r.id  AND i.project = p.id AND ja.issueid = i.id " \
#"AND i.issuenum = % s AND p.pkey = '%s' ORDER BY ja.created DESC" % (issue_num, project_key)

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

def JSQL_get_comment_of_tc(issue_num):
    sql_query = "SELECT ja.actionbody " \
                "FROM jiraaction ja " \
                "JOIN jiraissue ji ON ja.issueid = ji.id " \
                "WHERE ja.actiontype = 'comment' AND ji.issuenum = %s AND ROWNUM = 1" \
                "ORDER BY ja.created DESC" % (issue_num)

    data = json.dumps({"real_time": 1,
                       #"jira": "dalek",
                       "sql": sql_query})

    server_request = '%s/%s/%s/%s' % ('http://jsql.mot.com/rest', 'query/', USER, PASSWORD)

    return requests.post(server_request, data=data).json()

#mexendo nesse método.. estou alterando algumas coisas pra ver se consigo capturar os comentários...
# O método que foi passado pra gente nao está capturando nenhum comentário do issue..
def JSQL_get_comment_of_tc2(issuenum):
    sql_query = "SELECT ja.actionbody, ja.author " \
                "FROM jiraaction ja " \
                "JOIN jiraissue ji ON ja.issueid = ji.id " \
                "WHERE ja.actiontype = 'comment' AND ji.issuenum = % s " \
                "ORDER BY ja.created DESC" % (issuenum)

    data = json.dumps({"real_time": 1,
                       #"jira": "dalek",
                       "sql": sql_query})

    server_request = '%s/%s/%s/%s' % ('http://jsql.mot.com/rest', 'query/', USER, PASSWORD)

    return requests.post(server_request, data=data).json()

def JSQL_get_cr_informations2(project_key, issue_num):
    sql_query = "SELECT ja.actionbody " \
                "FROM jiraaction ja, jiraissue i, project p " \
                "JOIN jiraissue ji ON ja.issueid = ji.id " \
                "WHERE ja.actiontype = 'comment' " \
                "AND i.project = p.id " \
                "AND ji.issuenum = '%s' " \
                "AND p.pkey = '%s' " \
                "AND ROWNUM = 1 " \
                "ORDER BY ja.created DESC" % (project_key, issue_num)

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
    dic = select_all_data('deivid')
    lista = []
    print dic

    #for elemento in dic:

    # dic = JSQL_get_cr_informations('IKSWN','11775')
    # cont = 1
    # for list in dic:
    #     lista = list
    #     if lista.get('AUTHOR') != 'deivid':
    #         AnaliseDeComentariosBancoDeDados.analise(lista.get('JIRAACTION').upper())
    #     else:
    #         break

        #print lista.get('ACTIONBODY').upper()
    #print dic
    #JSQL_get_tc_custom_fields("IKSWN-10092")