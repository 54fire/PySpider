# coding=utf-8

'''
Author: 54fire
Email: 54fireljw@gmail.com
Data: 10:02 PM
'''
from config import *
import requests
from multiprocessing import Pool
import time
from ProjectDetail import *
import json


def get_project_detail(url):
    res = requests.get(url,headers=headers)
    time.sleep(1)
    if  res.status_code == 200:
        return res.text
    else:
        print(url)
        return None


def open_file(company):
    with open(company+".csv",'r',encoding='utf-8') as f:
        datas = f.readlines()
        f.close()
        return datas


def main(data):
    start = time.time()
    data = data.strip().split(',')
    html = get_project_detail(data[1])
    project_detail = projectDetail(html)
    project_detail.html_to_xpath()
    project = project_detail.get_project()
    ztb = ['',]
    tab = ['',]
    if project[2] > '0':
        ztb = project_detail.get_ztb_table()
        # for z in ztb:
            # html = get_project_detail(z[-1])
            # ztbinfo = TenderInfo(html)
            # ztbinfo.get_detail_info()
    if project[3] > '0':
        tab = project_detail.get_jgysba_table()
        # for t in tab:
            # html = get_project_detail(t[-1])
            # jgfinishinfo = baFinishInfo(html)
            # jgfinishinfo.get_detail_info()
    xiangmu = [data[0],data[2],data[1],project[0],project[1],ztb,tab]
    s = json.dumps(xiangmu,ensure_ascii=False)
    print(s)
    with open(data[0]+'.txt','a',encoding='utf-8') as f:
        f.write(s + '\n')
    # print(data,project,'\n',ztb,'\n',tab)
    end1 = time.time()
    print(end1-start)



if __name__ == '__main__':
    start = time.time()
    pool = Pool()
    for company in COMPANYS:
        datas = open_file(company)
        pool.map(main, datas)
    stop = time.time()
    print(stop - start)
