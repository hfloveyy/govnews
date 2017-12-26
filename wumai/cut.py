#!/usr/bin/env python  
# -*- coding:utf-8 -*-
import jieba
import csv 
import re
import xlrd

r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+' 
stop_words = []
text = []
title = []
contents = []

def load_stop_words(path = 'stop_words.txt'):
    with open(path,'r',encoding="gbk") as f:
        for line in f:
            content = line.strip()
            stop_words.append(content)

def load_data(path = '1.csv'):
    with open(path,newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            text.append(row[0])
            text.append(row[2])
        #    print(' '.join(row))
        return text

def load_xls_data(path = 'data.xlsx'):
    data = xlrd.open_workbook(path)
    table = data.sheets()[1] 
    title = table.col_values(0)
    contents = table.col_values(2) 
    #print(title)
    text = title + contents

    text = [re.sub(r, '', line.strip().replace(u'\u3000', u'').replace('\r','').replace('\n','').replace('\t','')) for line in text ]
    #print(text)
    return text
text = load_xls_data()
#load_data()

load_stop_words()
print(text)
lcut = jieba.lcut(''.join(text))
print(lcut)
cut = [x for x in lcut if x not in stop_words]

with open('cut.txt', 'wt') as f:
    print(cut, file=f)

'''
with open('1.csv','r') as f:
    for line in f:
        print(line)
'''