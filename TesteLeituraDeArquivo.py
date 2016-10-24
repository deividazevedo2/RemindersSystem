from AlgoritmoDeBoyerMoore import string_search

def BoyerMooreHorspool(pattern, text):
    m = len(pattern)
    n = len(text)
    if m > n: return -1
    skip = []
    for k in range(256): skip.append(m)
    for k in range(m - 1): skip[ord(pattern[k])] = m - k - 1
    skip = tuple(skip)
    k = m - 1
    while k < n:
        j = m - 1; i = k
        while j >= 0 and text[i] == pattern[j]:
            j -= 1; i -= 1
        if j == -1: return i + 1
        k += skip[ord(text[k])]
    return -1

if __name__ == '__main__':

    arq = open('words.txt', 'r')
    texto = arq.readlines()
    cont = 0

    comment = 'Hi, Deivid Lima! Can you verify if issue is reproducible in Nexus 6? If yes, can you collect bugreport and attach to this CR? Thanks and regards'

    for linha in texto:
        palavra = linha.strip().upper()
        s = BoyerMooreHorspool(palavra, comment.upper())
        cont += 1

        print 'pattern', linha.upper()
        print 'text', comment.upper()

        if s > -1:
            print 'Pattern \"' + linha + '\" found at position',s

    arq.close()

#    text = "this is the string to search in"
#    pattern = "the wrong"
#    s = BoyerMooreHorspool(pattern, text)
#    print 'Text:',text
#    print 'Pattern:',pattern