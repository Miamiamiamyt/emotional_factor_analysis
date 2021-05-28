import requests
from bs4 import BeautifulSoup
import csv
import time

def read_txt():
    codes = []
    names = []
    with open("test_company.txt",'r',encoding='utf_8') as f:
        lines = f.readlines()
        for line in lines:
            if (lines.index(line) & 1) == 0:
                codes.append(line.replace("\n", ""))
            else:
                names.append(line.replace("\n", ""))
    f.close()
    return codes,names

def get_paperinfo(url,code,name,date_list,name_list,content_list,title_list,start_date,end_date):
    resp = requests.get(url)
    resp.encoding = resp.apparent_encoding
    #resp.encoding = BeautifulSoup(resp.content, "lxml").original_encoding 
    bs = BeautifulSoup(resp.text,'lxml')
    #title = bs.find_all('h1',class_ = 'main-title')
    title = bs.select('h1.main-title')
    date = bs.select('span.date')
    content = bs.select('div.article > p')
    if not content:
        #print(1)
        content = bs.select('div.article > div > p')
    if not content:
        content = bs.select('div.article > div.article-content-detail > p')
    #print(title[0].text)
    full_content = ''
    for i in content[:-1]:
        #if target_firm in i.text:
        full_content += i.text
        #full_content += '\n' 
    print('***************************************************************')
    if title:
        #print(title[0].text)
        #print(date[0].text)
        #print(full_content)
        if start_date >= date[0].text:
            print("已爬取该企业全部目标日期的新闻")
            return False
        if (date[0].text <= end_date) and (date[0].text != '') and ('年' in date[0].text) and ('月' in date[0].text)and ('日' in date[0].text):
            date_list.append(date[0].text)
            title_list.append(title[0].text)
            content_list.append(full_content)
            name_list.append(name)
            print(date[0].text,name,title[0].text)
        #time.sleep(5)
    print('***************************************************************')
    return True

def main(codes,names,date_list,name_list,content_list,title_list):
    start_date = input('请以 yyyy年mm月dd日 的格式输入爬取新闻的起始日期:')
    end_date = input('请以 yyyy年mm月dd日 的格式输入爬取新闻的结束日期的后一天（因为需要包括结束当天的新闻）:')
    for code in codes:
        i = codes.index(code)
        print(code,'  ',names[i])
        result = True
        for page in range(1,100):
            url = 'http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol={}&Page={}'.format(code,page)
            resp = requests.get(url)
            #resp.encoding = BeautifulSoup(resp.content, "lxml").original_encoding 
            bs = BeautifulSoup(resp.text,'lxml')
            #divlist = bs.find_all('div',class_ = 'datelist')
            url_list = bs.select('div.datelist > ul > a ')
            #print(url_list)
            for url_i in url_list:
                #print(i," {}的第{}页".format(names[i],page))
                result = get_paperinfo(url_i['href'],code,names[i],date_list,name_list,content_list,title_list,start_date,end_date)
                if result == False:
                    break
            #get_paperinfo(url_list[0]['href'])
            if result == False:
                break
        if result == False:
            continue
    return
            