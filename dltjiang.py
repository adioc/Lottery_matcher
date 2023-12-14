# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 22:45:54 2023

@author: adioc
"""


import time
from selenium import webdriver
import re


jiezhi = 23152  #截止期次

#path = "/usr/local/chromedriver"
driver = webdriver.Edge()

headers = {'X-Requested-With': 'XMLHttpRequest','User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

url = 'https://www.lottery.gov.cn/dlt/'

driver.get(url)
time.sleep(1) #这是为了让网页能够完全加载出来
res = driver.page_source
driver.close()
#req = res.read().decode('utf-8')
detail = re.findall(r'"qiu-blue qiu-shadow">[0-9]*', res)
detail_0 = re.findall(r'"qiu-yellow qiu-shadow">[0-9]*',res)
qishu = re.findall(r'第[0-9]*期',res)
print(f"距离重买还有{jiezhi- eval(qishu[0][1:6])}期")

huangq = []
lanq = []

for i in detail:
    lanq.append(i.split('>')[1])
for i in detail_0:
    huangq.append(i.split('>')[1])

   
#print(hongq, "lnaqiu", detail_0)
zhu_1 = ['14','15','20',']
zhu_2 = ['06','10','12','22]
zhu_3 = ['02','05','19',]
zhu_4 = ['03','07','27',']
zhu_5 = ['01','11','23','']

'''对于列表a[n]的形式表示的为单个元素,其类型为元组的类型，
而a[n:m] 的类型仍然为列表,对于长度为n的列表，最后一位元素
按列表形式取出的方式为a[n-1,n]'''

#奖等和奖金转换程序
def jiang(a, b):    # a为前区  b为后区
    if b == 1:
        if a< 2:
            return "meiyou",0
        elif a == 2 :
            return 'nine', 5
        elif a == 3:
            return 'eight', 15
        elif a == 4:
            return 'five', 300
        elif a == 5:
            return 'two!!', 100000
        else:
            return 'error!', 0
    elif b == 2:
        if a <= 1:
            
            return 'nine', 5
        elif  a == 2:
            return 'eight', 15
        elif a == 3:
            return 'six', 200
        elif a == 4:
            return 'four', 3000
        elif a == 5:
            return 'yidengjiang!!!', 10000000
        else:
            return 'error', 0
    elif b == 0:
        if a == 3:
            return 'nine', 5
        elif a == 4:
            return 'seven', 100
        elif a == 5:
            return 'three', 10000
        else:
            return 'meiyou',0
    else:
        return 'error',0
        
def duij(a, b):             #a为彩票，b为当期结果
    set_1 = set(a)
    set_2 = set(b)
    same_set = set_1 & set_2
    return len(same_set)

def cundang(qishu, kaij, jieguo, zhongjiang):
    file = open('./data/大乐透.txt', mode= 'a')
    file.write(str(qishu[0])+'开奖：'+str(kaij)+'\t'+str(jieguo)+'\t'+"总金额："+str(zhongjiang)+"\n")
    file.close()
zongjj = 0
jisq = []
for i in range(1,6):
    qian = []
    qian.append(duij(eval(f'zhu_{i}' )[0:5],lanq))
    qian.append(duij(eval(f'zhu_{i}' )[5:7],huangq))
    jisq.append(jiang(qian[0], qian[1])[0])
    zongjj += jiang(qian[0], qian[1])[1]

print('出奖结果：', jisq, '\n' "总金额：", zongjj)
print('本期结果：', lanq, huangq)
print('幸运值+1')
cundang(qishu, lanq+huangq, jisq, zongjj)