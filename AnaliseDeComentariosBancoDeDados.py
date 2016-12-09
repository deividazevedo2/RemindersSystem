#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string

def BoyerMooreHorspool(pattern, text):
    m = len(pattern)
    n = len(text)
    if m > n:
        return -1
    skip = []
    for k in range(256):
        skip.append(m)
    for k in range(m - 1):
        skip[ord(pattern[k])] = m - k - 1
    skip = tuple(skip)
    k = m - 1
    while k < n:
        j = m - 1; i = k
        while j >= 0 and text[i] == pattern[j]:
            j -= 1;
            i -= 1
        if j == -1:
            return i + 1
        k += skip[ord(text[k])]
    return -1

def find(str, ch):
    indice = 0
    lista = []
    while indice < len(str):
        if str[indice] == ch:
            lista.append(indice)
        indice = indice + 1
    return lista

def reduz_texto(texto):

    abre = '{'
    fecha = '}'


    if len(find(texto, abre)) != 0:

        listaabre = find(texto, abre)
        listafecha = find(texto, fecha)

        tamanho = len(listaabre)
        contador = 0
        while len(listaabre) > 0:
            excluir = texto[listaabre[contador]:listafecha[contador + 1] + 1]
            texto = ' '.join(texto.split(excluir))
            tamanho -= 2;
            listaabre = find(texto, abre)
            listafecha = find(texto, fecha)

            return texto
    else:
        return texto

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
            contador +=1
            if (core == coreId):
                return True
        return False

#contar quantidade de repeticoes
def countPrefix(words, prefix):
    return len([1 for w in words if w.startswith(prefix)])


def analise(texto, coreId, listaDeRelevancias):

    safe_chars = string.ascii_letters + string.digits + ' ' + '?' + '[' + ']' + '~' + '{' + '}'
    text = ''.join([char if char in safe_chars else ' ' for char in texto])

    text = reduz_texto(text)

    arq = open('words.txt', 'r')
    palavras = arq.readlines()

    qtpattern = 0
    valor = 0

    for linha in palavras:

        linhacompleta = linha.strip().split(",")

        c = 0
        pos = 0
        texto = text.upper()[pos:len(text)]
        pattern = linhacompleta[0].upper()

        while c < len(text):

            s = BoyerMooreHorspool(pattern.upper(), texto)

            if s > -1:

                qtpattern += 1
                pos += s + len(pattern) + 1
                texto = text.upper()[pos:len(text)]

                valor = int(linhacompleta[1])

            c += 1

    if text.__contains__('[~'):
        if texto.find(coreId.upper()) > -1:
            listaDeRelevancias.append('MENCIONA O DONO')
        else:
            listaDeRelevancias.append('NAO MENCIONA O DONO')
    else:
        listaDeRelevancias.append('NAO MENCIONA NINGUEM')

    if qtpattern == 1:

        if valor >= 3:
            listaDeRelevancias.append("ALTA RELEVANCIA")
        if valor == 2:
            listaDeRelevancias.append("MEDIA RELEVANCIA")
        if valor == 1:
            listaDeRelevancias.append("POUCA RELEVANCIA")

    if qtpattern >= 2:
        if (qtpattern >= 3) | (qtpattern == 2 and valor != 3) | (qtpattern == 2 and valor == 3):
            listaDeRelevancias.append("ALTA RELEVANCIA")

    condicoes = ['NAO MENCIONA NINGUEM','NAO MENCIONA O DONO', 'MENCIONA O DONO','ALTA RELEVANCIA','MEDIA RELEVANCIA', 'POUCA RELEVANCIA']

    resultado = [countPrefix(listaDeRelevancias, p) for p in condicoes]

    return resultado

def mencionou_usuario(resultado):
    if resultado[2] > 0:
        if resultado[3] == 0:
            return False
        else:
            return True

def analisando_prioridades(resultado):
    if resultado[0] == 0:
        if resultado[2] > 0:
            return True
        else:
            return False
    if resultado[0] > 0:
        if resultado[3] > 0 or resultado[4] > 0:
            return True
        else:
            return False
    if resultado[1] > 0:
        if resultado[2] == 0:
            return False
        else:
            return True
