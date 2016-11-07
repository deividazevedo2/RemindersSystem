#!/usr/bin/env python
# -*- coding: utf-8 -*-
import AnaliseDeComentarios

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


print s