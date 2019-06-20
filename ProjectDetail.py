'''
Author: 54fire
Time:   2019-06-20 12:58
Name:   projectDetail
'''

from lxml import etree

class baFinishInfo():

    def __init__(self,html):
        self.elements = etree.HTML(html)

    def get_detail_info(self):
        data_tables             = self.elements.xpath('//div[@class="plr"]//tbody/tr')
        all_money, all_area     = data_tables[5].xpath('./td/text()')
        act_money, act_area     = data_tables[8].xpath('./td/text()')
        guimo                   = data_tables[9].xpath('./td/text()')[0]
        start_time, end_time    = data_tables[-2].xpath('./td/text()')
        print(all_money,all_area,act_money,act_area,guimo,start_time,end_time)


class TenderInfo():

    def __init__(self,html):
        self.elements = etree.HTML(html)

    def get_detail_info(self):
        data_tables             = self.elements.xpath('//div[@class="plr"]//tbody/tr')
        all_money, all_area     = data_tables[5].xpath('./td/text()')
        act_money, act_area     = data_tables[6].xpath('./td/text()')
        print(all_money,all_area,act_money,act_area)



class projectDetail():

    def __init__(self,html):
        self.html = html

    def html_to_xpath(self):
        elements = etree.HTML(self.html)
        self.ele = elements
        return elements

    def get_project(self):
        names = self.ele.xpath('//dl//dd')
        pro_class = names[5].xpath('./text()')[0]
        pro_use = names[7].xpath('./text()')[0] if len(names[7].xpath('./text()')) > 0 else ''
        ztb = self.ele.xpath('//a[@data-contentid="tab_ztb"]/span/em/text()')[0]
        jgysba = self.ele.xpath('//a[@data-contentid="tab_jgysba"]/span/em/text()')[0]
        ls = (pro_class,pro_use,ztb,jgysba)
        return ls

    def get_ztb_table(self):
        ztbs = self.ele.xpath('//div[@id="tab_ztb"]/table/tbody/tr')
        tab_ztbs = []
        for ztb in ztbs:
            ls = ztb.xpath('./td')
            t1 = ls[4].xpath('./text()')[0]
            t2 = ls[5].xpath('./text()')[0]
            t3 = 'http://jzsc.mohurd.gov.cn' + ls[-1].xpath('./a/@data-url')[0]
            tab_ztb = (t1, t2, t3)
            tab_ztbs.append(tab_ztb)
        return tab_ztbs


    def get_jgysba_table(self):
        jgysbas = self.ele.xpath('//div[@id="tab_jgysba"]/table/tbody/tr')
        tab_jgysbas = []
        for ztb in jgysbas:
            ls = ztb.xpath('./td')
            t1 = ls[3].xpath('./text()')[0]
            t2 = ls[4].xpath('./text()')[0]
            t3 = ls[5].xpath('./text()')[0]
            t4 = ls[6].xpath('./text()')[0]
            t5 = 'http://jzsc.mohurd.gov.cn' + ls[-1].xpath('./a/@data-url')[0]
            tab_jgysba = (t1, t2, t3, t4, t5)
            tab_jgysbas.append(tab_jgysba)
        return tab_jgysbas
