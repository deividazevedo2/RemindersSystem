#!/usr/bin/env python
# -*- coding: utf-8 -*-
import AnaliseDeComentarios, string

#comentario com caractere especial q da problema quando eh convertido
comentario = 'first.！dfeufhewf?'

#pattern = '?'
#s = AnaliseDeComentarios.BoyerMooreHorspool(pattern.upper(), comentario.upper())

arq = open('words.txt', 'r')
palavras = arq.readlines()

comecar = 0

for linha in palavras:

    c = 0
    pos = 0
    texto = comentario.upper()[pos:len(comentario)]
    pattern = linha.strip().upper()

    while c < len(comentario):

        s = AnaliseDeComentarios.BoyerMooreHorspool(pattern.upper(), texto)

        if s > -1:
            print 'Pattern \"' + pattern + '\" found at position', s + pos

            pos += s + len(pattern) + 1
            texto = comentario.upper()[pos:len(comentario)]
        c += 1

    comecar += 1

def find(str, ch):
    indice = 0
    lista = []
    while indice < len(str):
        if str[indice] == ch:
            lista.append(indice)
        indice = indice + 1
    return lista

def verifica_coreid(texto, core):

    coreIdInicio = '['
    coreIdFim = ']'

    # verificar se o coreId eh igual
    if len(find(texto, coreIdInicio)) != 0:
        listaabre = find(texto, coreIdInicio)
        listafecha = find(texto, coreIdFim)

        tamanho = len(listaabre)
        contador = 0
        while len(listaabre) > contador:
            coreId = texto[listaabre[contador]+2:listafecha[contador]]
            #texto = ' '.join(texto.split(coreId))
            contador +=1
            if (core == coreId):
                return True
        return False

if __name__ == '__main__':

    lista = [1, 2, 3, 4, 5]
    print lista.__contains__(6)

    # listaabre = []
    # listafecha = []
    #
    # texto = "fdnoi [~deivid][~emenezes][~joao] dsgs "
    # #rint texto.__contains__('[~')
    # print verifica_coreid(texto, 'joao')

    # abre = '{'
    # fecha = '}'
    #
    # if find(texto,"{") != -1:
    #     print 'entrou no if'
    #     listaabre = find(texto,abre)
    #     print len(listaabre)-1
    #
    #     listafecha = find(texto, fecha)
    #     print listaabre, listafecha
    #
    #     tamanho = len(listaabre)
    #     contador = 0
    #     while len(listaabre) > 0:
    #
    #         excluir = texto[listaabre[contador]:listafecha[contador+1]+1]
    #         texto = ' '.join(texto.split(excluir))
    #         tamanho -= 2;
    #         listaabre = find(texto, abre)
    #         listafecha = find(texto, fecha)
    #         print texto

