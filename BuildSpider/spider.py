# coding=utf-8
'''
Author: 54fire
Email: 54fireljw@gmail.com
Data: 9:03 PM
'''

import re
import requests
from multiprocessing import Pool
import time
from config import *

# input 公司名称
# output 公司的对应数字标识
def get_company_code(company_name):
    data = {"complexname": company_name}
    url = "http://jzsc.mohurd.gov.cn/dataservice/query/comp/list"
    res = requests.post(url,headers=headers,data=data)
    pattarn = re.compile(r'.*?/compDetail/(\d+)">.*?')
    if res.status_code == 200:
        code = re.findall(pattarn, res.text)
        if code:
            return code[0]
        else:
            print(company_name,url)
            return None
    else:
        print(company_name,url)
        return None


def get_html(company_code):
    url = "http://jzsc.mohurd.gov.cn/dataservice/query/comp/compPerformanceListSys/" + company_code
    res = requests.get(url,headers=headers)
    if res.status_code == 200:
        return res.text
    return None


def get_more_html(company_code,data):
    url = "http://jzsc.mohurd.gov.cn/dataservice/query/comp/compPerformanceListSys/" + company_code
    res = requests.post(url,headers=headers,data=data)
    if res.status_code == 200:
        return res.text
    return None


def get_project_tt_and_pc(html):
    pattarn = re.compile(r'.*?{pg.*?tt:(\d+),pn.*?pc:(\d+),.*?')
    code = re.findall(pattarn, html)
    print(code)
    if code:
        return code[0]
    return None


def write_dict_file(name,dicts):
    with open(name + ".csv", 'a', encoding="utf-8") as f:
        for dict in dicts:
            f.write(dicts[dict].replace(',',' ') + ',')
        f.write('\n')


def get_project_name_and_class(company,html):
    pattarn = re.compile(r'<tr>.*?<td data-header="项目名称".*?(\d+).*?>(.*?)</a></td>.*?<td data-header="项目类别">(.*?)</td>.*?</tr>', re.S)
    tmp = re.findall(pattarn, html)
    for i in tmp:
        project = {}
        project["company"] = company
        project["url"] = "http://jzsc.mohurd.gov.cn/dataservice/query/project/projectDetail/" + i[0]
        project["title"] = i[1]
        project["class"] = i[2]
        write_dict_file(company+"source",project)
        if CONDITIONS:
            if i[2] in CONDITIONS:
                write_dict_file(company,project)
        else:
            write_dict_file(company,project)


def main(company):
    html = get_company_code(company)
    with open(company + '.csv','w') as f:
        f.close()
    with open(company + 'source.csv','w') as f:
        f.close()
    if html:
        ht = get_html(html)
        h = get_project_tt_and_pc(ht)
        get_project_name_and_class(company,ht)
        if h:
            tt = int(h[0])
            pc = int(h[1])
            for i in range(2,pc + 1):
                data = {"$total": tt,"$reload": 0,"$pg": i,"$pgsz": 25}
                ht = get_more_html(html,data)
                get_project_name_and_class(company,ht)


if __name__ == '__main__':
    start = time.time()
    datas = []
    pool = Pool()
    pool.map(main, COMPANYS)
    stop = time.time()
    print(stop - start)