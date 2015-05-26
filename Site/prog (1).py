# -*- coding: utf-8 -*-
import re, codecs, json


letters = {u'ӝ':u'ж',u'ӟ':u'з',u'ӥ':u'и',u'ӧ':u'о',u'ӵ':u'ч'}
letters2 = {u'ж':u'ӝ',u'з':u'ӟ',u'и':u'ӥ',u'о':u'ӧ',u'ч':u'ӵ'}
a = []
b = []
n = 0
bgt = codecs.open("stat2.txt", "w", "utf-8-sig")
ng = []
bg = []
tg = []
qg = []
bgc = {}
states = ('Yes', 'No')

yy = 0
yn = 0
ny = 0
nn = 0
topwords = []
pretopwords = {}
diacritics = [u'ӝ',u'ӟ',u'ӥ',u'ӧ',u'ӵ']
posdiacr = [u'ж',u'з',u'и',u'о',u'ч']
start_probability startprobabilityw = 0
startprobabilitys = 0
test = codecs.open("utest+.txt", "w", "utf-8-sig")
tgt = codecs.open('tg.txt', 'w', 'utf-8-sig')
qgt = codecs.open('4g.txt', 'w', 'utf-8-sig')
numbr = 0
#АНАЛИЗ ДАМПА ВИКИПЕДИИИ (DONE НУЖНО ТОЛЬКО 2.3.4.5 ГРАММЫ ЗАПИХНУТЬ В ОДНУ ФУНКЦИЮ)
def cleaning(filename):
    global a
    f = codecs.open(filename, 'r', 'utf-8-sig')
    for line in f:
        line = line.lower()
        k = re.findall(u'[А-Яа-яӜӝӞӟӤӥӦӧӴӵ\-]+',line)
        for i in k:
            if i != u'википедия':
                a.append('#'+i+'$')


cleaning('udmwiki.txt')

def topword(mass):
    for i in mass:
        for letter in i:
                if letter in diacritics and i not in pretopwords:
                    pretopwords[i] = 1
                if i in pretopwords:
                    pretopwords[i] += 1
                    if pretopwords[i] == 500 and i not in topwords:
                        topwords.append(i)

#ПРОСМОТРЕТЬ НА ПРАВИЛЬНОСТЬ ОБРАБОТКИ!!!!
    for q in topwords:
        for qq in q:
            if qq in posdiacr:
                q2 = q.replace(qq, letters2[qq])
                if q2 in mass:
                    topwords.remove(q)




def ngramm(ct,number):
    global bg,ng,tg
    stat = codecs.open("stat3.txt", "w", "utf-8-sig")
    for word in ct:
        for s in word:
            ng.append(s)

    if number == 2:
        for y in range(1,len(ng)):
            if ng[y-1]+ng[y] != '$#':
                bg.append(ng[y-1] + ng[y])

    if number == 3:
        for y in range(2,len(ng)):
            if '#$' not in ng[y-2]+ng[y-1]+ng[y] and '$#' not in ng[y-2]+ng[y-1]+ng[y]:
                tg.append(ng[y-2] + ng[y-1]+ ng[y])


    if number == 4:
        for y in range(3,len(ng)):
            qg.append(ng[y-3] + ng[y-2]+ ng[y-1] + ng[y])
    stat.close()
ngramm(a,2)
ngramm(a,3)






def analysis(mass):
    global bgc, startprobabilityw, startprobabilitys, yn,yy,ny,nn
    for i in mass:
        if i in bgc:
            bgc[i] += 1
        else:
            bgc[i] = 1
    for t in bgc:
        bgc[t] = bgc[t]/float(len(mass))
        if t[0]== u'#' and t[1] not in diacritics:
            startprobabilitys += 1
        if t[0] == u'#' and t[1] in diacritics:
            startprobabilityw += 1
        if t[0] in diacritics and t[1] not in diacritics:
            yn += 1
        if t[0] in diacritics and t[1] in diacritics:
            yy += 1
        if t [0] not in diacritics and t[1] in diacritics:
            yn += 1
        if t[0] not in diacritics and t[1] not in diacritics:
            nn += 1
    nyyn = yn+nn+yy+ny
    nn = nn/nyyn
    yn = yn/nyyn
    ny = ny/nyyn
    yy = yy/nyyn
            
    startprobabilitys = startprobabilitys/(startprobabilitys+startprobabilityw)
    startprobabilityw = startprobabilityw/(startprobabilitys+startprobabilityw)



    return bgc

analysis(bg)
analysis(tg)
f = codecs.open('trigrams_freq.txt', 'w', 'utf-8')
f.write(u'\r\n'.join(k + u'\t' + str(bgc[k]) for k in sorted(bgc, key=lambda x: -bgc[x])))
f.close()
#analysis(qg)


def probability(mass):
    for y in sorted(mass):
        for e in y:
            if e in diacritics:
                y2 = y.replace(e, letters[e])
                if y2 in bgc:
                    bgt.write(y + u':' +  str(bgc[y]) + '\r\n'+ y2 + u':' + str(bgc[y2]) + '\r\n' + '\r\n')
                if y2 not in bgc:
                    bgc[y2] = 0
            else:
                bgt.write(y + u':' +  str(bgc[y]) + '\r\n')
    bgt.close()

probability(bgc)
topword(a)

#АНАЛИЗ ЗАГРУЖАЕМОГО ФАЙЛА.
def wordch(word):
    word = re.sub(u'\$','',word)
    word = word+' '
    word = re.sub('\r\n ','\r\n',word)
    word = re.sub('#','',word)
    return word

def an(filename, mass, numbers):
    global yy,ny,yn,nn,startprobabilityw,startprobabilitys
    f1 = codecs.open(filename, 'r', 'utf-8-sig')
    f2 = codecs.open('reworked.txt','w','utf-8-sig')

    if numbers==2:
        for line in f1:
            for word in line.split(' '):
                word = u'#'+word +u'$ '
                word = re.sub(u'([А-Яа-яӜӝӞӟӤӥӦӧӴӵ])([^А-Яа-яӜӝӞӟӤӥӦӧӴӵ]+)\$',r'\1$\2',word)
                k = 1
                k1 = 1
                k2 = 1
                transition_probability = []
                start_probability = 0
                if word[1] in posdiacr:
                    k = max[startprobabilitys*mass[word[0]+word[1]],startprobabilityw*mass[word[0]+letters2[word[1]]]]
                    print k
                else:
                    k = startprobabilitys*mass[word[0]+word[1]]
                for number in range(1,len(word)-1):
                    if word[number].lower() + word[number+1].lower() in mass:
                        print '1'
                        print k
                        if word[number].lower() in posdiacr and word[number] != '#' and word[number-1].lower()+letters2[word[number].lower()] + word[number+1] in mass:
                            print '2'
                            if letters2[word[number].lower()] + word[number+1] in bgc and word[number+1].lower() + letters2[word[number].lower()]in bgc:
                                k1 = k*mass[word[number].lower() + word[number+1].lower()]*((mass[word[number-1].lower()+word[number].lower() + word[number+1].lower()])/mass[word[number-1].lower()+word[number].lower()])
                                k2 = k*mass[letters2[word[number].lower()] + word[number+1].lower()]*((mass[word[number-1].lower()+letters2[word[number].lower()] + word[number+1].lower()])/mass[word[number-1].lower()+word[number].lower()])
                                print k1,k2,'da'
                                if k1>k2:
                                    k=k*k1
                                    f2.write(word[number])
                                if k2>k1:
                                    k=k1
                                    f2.write(letters2[word[number]])
                                    print 'ppdfsdf', word
                        else:
                            f2.write(word[number])
                    else:
                        if number == len(word)-2 and '\r\n' not in word:
                            f2.write(' ')
                            print k
                        if word[number] !='#' and word[number]!='$':
                            f2.write(word[number])
        f2.close()
        print 'ofsdfs'
        print k

#an2('utest.txt',bgc)

def an3(filename,mass):
    f1 = codecs.open(filename, 'r', 'utf-8-sig')
    f2 = codecs.open('reworked3.2.txt','w','utf-8-sig')
    k = 1
    for line in f1:
        for word in line.split(' '):
            word = u'#'+word +u'$ '
            word = re.sub(u'([А-Яа-яӜӝӞӟӤӥӦӧӴӵ])([^А-Яа-яӜӝӞӟӤӥӦӧӴӵ]+)\$',r'\1$\2',word)

            for number in range(1,len(word)-1):
                if word[number-1].lower()+ word[number].lower() + word[number+1].lower() in mass:
                    if word[number].lower() not in posdiacr:
                        k = k * mass[word[number-1].lower() + word[number].lower() + word[number+1].lower()]
                        if word[number] != '$' and word[number] != '#':
                            f2.write(word[number])

                    if word[number].lower() in posdiacr:
                        #print 'вариант 2'
                        if word[number-1].lower()+letters2[word[number].lower()] + word[number+1] in bgc and letters2[word[number].lower()]+word[number+1].lower() + word[number+2] in bgc:
                            #print 'шаг2'
                            if mass[word[number-1].lower()+word[number].lower()+ word[number+1].lower()]*mass[word[number].lower()+word[number+1].lower()+word[number+2].lower()]\
                                < mass[word[number-1].lower()+letters2[word[number].lower()]+ word[number+1].lower()]*mass[letters2[word[number].lower()]+word[number+1].lower()+word[number+2].lower()]:
                                k = k * mass[word[number-1].lower()+letters2[word[number]].lower() + word[number+1].lower()]
                                f2.write('_'+letters2[word[number].lower()]+'_')
                                print 'замена',word[number],letters2[word[number]],word
                             #re.sub(word[number],'_!'+letters2[word[number]]+'!_',word)
                            #print 'Было сравнение с заменой', mass[words[number].lower()+words[number+1].lower()],mass[words[number].lower()+words[number+1].lower()]
                            if mass[word[number-1].lower()+word[number].lower()+word[number+1].lower()]*mass[word[number].lower()+word[number+1].lower()+ word[number+2].lower()]\
                                > mass[word[number-1].lower()+letters2[word[number].lower()]+word[number+1].lower()]*mass[letters2[word[number].lower()]+word[number+1].lower()+word[number+2].lower()]:
                                k = k * mass[word[number-1].lower()+word[number].lower() + word[number+1].lower()]
                                #re.sub(word[number],'_!'+letters2[word[number]]+'!_',word)
                                f2.write(word[number])
                        else:
                            k = k * mass[word[number-1].lower()+word[number].lower() + word[number+1].lower()]
                            #re.sub(word[number],'_!',word)
                            f2.write(word[number])

                else:
                    if word[number] != '$' and word[number] != '#':
                            f2.write(word[number])
                    k = k*1
                if number == len(word)-2 and '\r\n' not in word:
                    f2.write(' ')

    f2.close()
    print 'Обработка текста окончена'

def viterbi(file, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}

    # Initialize base cases (t == 0)
    for y in states:
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        path[y] = [y]

    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}

        for y in states:
            (prob, state) = max((V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states)
            V[t][y] = prob
            newpath[y] = path[state] + [y]

        # Don't need to remember the old paths
        path = newpath
    n = 0           # if only one element is observed max is sought in the initialization values
    if len(obs) != 1:
        n = t
    print_dptable(V)
    (prob, state) = max((V[n][y], y) for y in states)
    return (prob, path[state])

# Don't study this, it just prints a table of the steps.
def print_dptable(V):
    s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
    for y in V[0]:
        s += "%.5s: " % y
        s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
        s += "\n"
    print(s)

an('utest2.txt',bgc,2)