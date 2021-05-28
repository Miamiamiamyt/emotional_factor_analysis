import os
import pandas as pd
from numpy import *
import datetime

def main(target_company):
    path = "predict_emotion/"
    pd_info = pd.read_csv(os.path.join(path, "final_prediction.tsv") ,sep='\t',header=None)

    company_list = []
    date_list = []
    S_it = []

    for company in target_company:
        company_info = pd_info.loc[pd_info[2] == company]
        date_set = company_info[1]
        date_set = sorted(set(date_set))
        for date in date_set:
            companydate_info = company_info.loc[company_info[1]==date]
            #print(companydate_info)
            s_it = mean([int(i) for i in companydate_info[3]])
            #print(s_it)
            company_list.append(company)
            date_list.append(date[:4]+'-'+date[5:7]+'-'+date[8:10])
            S_it.append(s_it)

    daily_factor = pd.DataFrame({'date':date_list,'company':company_list,'S_it':S_it})
    daily_factor.to_csv("daily_factor.tsv",index=False,encoding='utf-8',sep='\t')
    return