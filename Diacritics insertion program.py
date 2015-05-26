# -*- coding: utf-8 -*-
import re, codecs, json
letters = {u'ӝ':u'ж',u'ӟ':u'з',u'ӥ':u'и',u'ӧ':u'о',u'ӵ':u'ч'}
letters2 = {u'ж':u'ӝ',u'з':u'ӟ',u'и':u'ӥ',u'о':u'ӧ',u'ч':u'ӵ'}
path = {}
a = []
z = []
n = 0
bgt = codecs.open("stat2.txt", "w", "utf-8-sig")
ng = []
bg = []
tg = []
qg = []
allowednum = ['2','3','4']
bgc = {}
original = []
change = []
ngra = {}
topwords = {}
pretopwords = {}
diacritics = [u'ӝ',u'ӟ',u'ӥ',u'ӧ',u'ӵ']
posdiacr = [u'ж',u'з',u'и',u'о',u'ч']
startprobability = {}
number = raw_input(u'Введите длинну n-грамм:')
if number not in allowednum:
    print u'Введена неверная длинна n-грамм'
    exit()
filename = raw_input(u'Введите название файла (с указанием формата), который вы хотите обработать: ')
newfilename = raw_input(u'Введите название файла (с указанием формата), в который вы хотите записать обработанный текст: ')

#Подсчет статистики
def cleaning(filename,mass):
    f = codecs.open(filename, 'r', 'utf-8-sig')
    for line in f:
        line = line.lower()
        k = re.findall(u'[А-Яа-яӜӝӞӟӤӥӦӧӴӵё\-]+',line)
        for i in k:
            if i != u'википедия':
                mass.append('#'+i+'$')





cleaning('udmwiki.txt',a)

def topword(mass):
    for i in mass:
        for letter in i:
                if letter in diacritics and i not in pretopwords:
                    pretopwords[i] = 1
                if i in pretopwords:
                    pretopwords[i] += 1
                    if pretopwords[i] == 750 and i not in topwords:
                        topwords[transform(i)] = i
                if len(i) <= 3 and transform(i) not in topwords:
                    topwords[transform(i)] = i

    for q in topwords:
        for qq in q:
            if qq in posdiacr:
                q2 = q.replace(qq, letters2[qq])
                if q2 in mass:
                    topwords[q] =  q


def ngramm(number):
    global ng,a
    for word in a:
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
        if len(ng)> 3:
            for y in range(3,len(ng)):
                qg.append(ng[y-3] + ng[y-2]+ ng[y-1]+ng[y])




ngramm(int(number))


def transform(ngramm):
    for i in ngramm:
        if i in letters:
            ngramm =  re.sub(i,letters[i],ngramm)

    return ngramm



def analysis(mass):
    print u'Начало подсчета статистики'
    global bgc, startprobability, diacritics,  letters, bg, transition_probability,ngra, tg
    whith = 0
    for i in mass:
        if i in bgc:
            bgc[i] += 1
        if i not in bgc:
            bgc[i] = 1
        if '#' in i:
            whith += 1
    for y1 in bgc:
        w = bgc[y1]
        for y2 in bgc:
            if y1[0:-1] == y2[0:-1]:
                w +=bgc[y2]
        ngra[y1] = w/float(len(bgc))


    for t in bgc:
        bgc[t] = bgc[t]/float(len(mass))

    for ngramm in mass:
        if '#' == ngramm[0]:
            startprobability[ngramm] = bgc[ngramm]/(whith/float(len(mass)))
        if '#' != ngramm[0]:
            startprobability[ngramm] = 0
    print u'Подсчет статистики закончен. Пожалуйста, ожидайте конца обработки текста'


if number == '2':
    analysis(bg)
if number == '3':
    analysis(tg)
if number == '4':
    analysis(qg)

f = codecs.open('ngrams_freq.txt', 'w', 'utf-8')
f.write(u'\r\n'.join(k + u'\t' + str(bgc[k]) for k in sorted(bgc, key=lambda x: -bgc[x])))
f.close()



topword(a)

#АНАЛИЗ ЗАГРУЖАЕМОГО ФАЙЛА.

def algorithm(filename,number,newfilename):
    global states,startprobability,z,bgc, topwords, original, change
    f_result = codecs.open(newfilename,'w','utf-8-sig')
    f = codecs.open(filename, 'r', 'utf-8-sig')
    for line in f:
        k = re.findall(u'[А-Яа-яӜӝӞӟӤӥӦӧӴӵ\-]+',line)
        for word in k:
                original.append(word)


    cleaning(filename,z)
    if number == 2:
        for zz in z:
            if zz in topwords:
                f_result.write(zz+' ')
            if zz not in topwords and len(zz) >3:
                let = 0
                obs = []
                states = []
                transition_probability = {}
                while zz[let] != '$':
                    obs.append(zz[let].lower()+zz[let+1].lower())
                    states.append(zz[let].lower()+zz[let+1].lower())
                    if zz[let+1].lower() in posdiacr:
                        states.append(zz[let].lower()+letters2[zz[let+1].lower()])
                    if zz[let].lower() in posdiacr:
                        states.append(letters2[zz[let].lower()] +zz[let+1])

                    for x1 in states:
                        pretransition_probability = {}
                        for x2 in states:
                            if x1[-1] == x2[0] and x1 in bgc and x2 in bgc:
                                pretransition_probability[x2] = bgc[x1]/ngra[x1]
                            else:
                                pretransition_probability[x2] = 0
                        transition_probability[x1] = pretransition_probability
                    let += 1

                viterbi(obs,states,startprobability,transition_probability,f_result,number)



    if number == 3:
        for zz in z:
            if zz in topwords:
                f_result.write(zz)
            if zz not in topwords and len(zz) >3:
                let = 1
                obs = []
                states = []
                transition_probability = {}
                while zz[let] != '$':
                    obs.append(zz[let-1].lower()+zz[let].lower()+zz[let+1].lower())
                    states.append(zz[let-1].lower()+zz[let].lower()+zz[let+1].lower())
                    if zz[let+1].lower() in posdiacr:
                        states.append(zz[let-1].lower()+zz[let].lower()+letters2[zz[let+1].lower()])
                    if zz[let].lower() in posdiacr:
                        states.append(zz[let-1].lower()+letters2[zz[let].lower()]+zz[let+1].lower())
                    if zz[let-1].lower() in posdiacr:
                        states.append(letters2[zz[let-1].lower()]+zz[let].lower()+zz[let+1].lower())

                    for x1 in states:
                        pretransition_probability = {}
                        for x2 in states:
                            if x1[-2] == x2[0] and x1 in bgc and x2 in bgc:
                                pretransition_probability[x2] = bgc[x1]/ngra[x1]
                            else:
                                pretransition_probability[x2] = 0

                        transition_probability[x1] = pretransition_probability
                    let += 1
                viterbi(obs,states,startprobability,transition_probability,f_result,number)
    if number == 4:
       for zz in z:
            if zz in topwords or len(zz)<= 3:
                f_result.write(zz)
            if zz not in topwords and len(zz)>3:
                let = 2
                obs = []
                states = []
                transition_probability = {}
                while zz[let] != '$':
                    obs.append(zz[let-2].lower()+zz[let-1].lower()+zz[let].lower()+zz[let+1].lower())
                    states.append(zz[let-2].lower()+zz[let-1].lower()+zz[let].lower()+zz[let+1].lower())
                    if zz[let+1].lower() in posdiacr:
                        states.append(zz[let-2].lower()+zz[let-1].lower()+zz[let].lower()+letters2[zz[let+1].lower()])
                    if zz[let] in posdiacr:
                        states.append(zz[let-2].lower()+zz[let-1].lower()+letters2[zz[let].lower()]+zz[let+1].lower())
                    if zz[let-1] in posdiacr:
                        states.append(zz[let-2].lower()+letters2[zz[let-1].lower()]+zz[let].lower()+zz[let+1].lower())
                    if zz[let-2].lower() in posdiacr:
                        states.append(letters2[zz[let-2].lower()]+zz[let-1].lower()+zz[let].lower()+zz[let+1].lower())
                    for x1 in states:
                        pretransition_probability = {}
                        for x2 in states:
                            if x1[1] == x2[0] and x1 in bgc and x2 in bgc:
                                pretransition_probability[x2] = bgc[x1]/ngra[x1]
                            else:
                                pretransition_probability[x2] = 0
                        transition_probability[x1] = pretransition_probability
                    let += 1
                viterbi(obs,states,startprobability,transition_probability,f_result,number)
    f_result.close()
    f_result = codecs.open(newfilename,'r','utf-8-sig')
    for line in f_result:
        k = re.findall(u'[А-Яа-яӜӝӞӟӤӥӦӧӴӵ\-]+',line)
        for word in k:
               change.append(word)


def viterbi(obs, states, start_p, trans_p, file, number):
    V = [{}]
    path = {}
    n = 0
    for y in states:
        if obs[0] == transform(y):
            emit_p = 1
        if obs[0] != transform(y):
            emit_p = 0
        if y not in bgc:
            start_p[y] = 0
        V[0][y] = start_p[y] * emit_p
        path[y] = [y]

    for t in range(1, len(obs)):
        V.append({})
        newpath = {}

        for y in states:
            if obs[t] == transform(y):
                emit_p = 1
            if obs[t] != transform(y):
                emit_p = 0
            (prob, state) = max((V[t-1][y0] * trans_p[y0][y] * emit_p, y0) for y0 in states)
            V[t][y] = prob
            newpath[y] = path[state] + [y]
        path = newpath


    if len(obs) != 1:
        n = t
    (prob, state) = max((V[n][y], y) for y in states)


    for qwe in range(1,len(path[state]),number):
        file.write(path[state][qwe])
    file.write(' ')






algorithm(filename,int(number),'text_r.txt')

def createMapFile(new_data, filename, map_file):
    ii = 0
    f = codecs.open(filename, 'r', 'utf-8-sig')
    y = 0
    f2 = codecs.open(map_file,'w','utf-8-sig')
    for line in f:
        k = re.findall(u'[А-Яа-яӜӝӞӟӤӥӦӧӴӵё\-]+',line)
        for num in range(0,len(k)):
            for ii in range(0,len(new_data)):
                if k[num] == transform(new_data[ii]).capitalize():
                    line=line.replace(k[num],new_data[ii].capitalize(),1)
                if k[num] == transform(new_data[ii]).upper():
                    line=line.replace(k[num],new_data[ii].upper(),1)
                if k[num] == transform(new_data[ii]).lower():
                    line=line.replace(k[num],new_data[ii],1)


        f2.write(line)


    f2.close()



createMapFile(change,filename,newfilename)

print u'Обработка текста завершена'