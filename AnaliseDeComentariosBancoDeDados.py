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
            j -= 1; i -= 1
        if j == -1:
            return i + 1
        k += skip[ord(text[k])]
    return -1


def analise(texto):

    safe_chars = string.ascii_letters + string.digits + ' '
    text = ''.join([char if char in safe_chars else ' ' for char in texto])

    print text

    arq = open('words.txt', 'r')
    palavras = arq.readlines()

    for linha in palavras:

        c = 0
        pos = 0
        texto = text.upper()[pos:len(text)]
        pattern = linha.strip().upper()

        while c < len(text):

            s = BoyerMooreHorspool(pattern.upper(), texto)

            if s > -1:
                print 'Pattern \"' + pattern + '\" found at position', s + pos

                pos += s + len(pattern) + 1
                texto = text.upper()[pos:len(text)]
            c += 1