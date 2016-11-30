#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import AnaliseDeComentariosBancoDeDados
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


if __name__ == '__main__':
    # dic = JSQL_get_comment_of_tc2("14334")
    dic = JSQL_get_cr_informations('IKSWN','11775')
    print dic
    cont = 1
    for list in dic:
        if list.get('AUTHOR') != 'deivid':
            AnaliseDeComentariosBancoDeDados.analise(list.get('JIRAACTION').upper())
        else:
            break

        #print lista.get('ACTIONBODY').upper()
    #print dic
    #JSQL_get_tc_custom_fields("IKSWN-10092")