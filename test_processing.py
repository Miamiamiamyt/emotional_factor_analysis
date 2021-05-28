import pandas as pd
import xlrd
from sklearn.utils import shuffle
import re

def cut_sent(para):
    para = re.sub('([；。？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")

def main(date,company,title,content):
    label = []
    text = []
    set_type = []
    #count = 0
    nrows = len(date)
    for i in range(nrows):
        label.append(0)
        #print(count)
        #count += 1
        title[i] = title[i].replace("\n", "")
        title[i] = title[i].replace("\r", "")
        title[i] = title[i].replace("\t", "")
        content[i] = content[i].replace("\t", "")
        content[i] = content[i].replace("\n", "")
        content[i] = content[i].replace("\r", "")

        para = cut_sent(content[i])
        cleaned_content = ''
        for cut in para:
            if '投资者提问' in cut:
                #print(cut)
                cleaned_content += cut
            
        if cleaned_content == '':
            text.append(title[i])
        else:
            text.append(cleaned_content)
        #set_type.append('train')
    #print(text[0])

    test = pd.DataFrame({'label':label, 'text':text, 'company':company, 'date':date})
    test.to_csv("test.tsv", index=False,  encoding='utf-8',sep='\t')

    return
