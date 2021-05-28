import pandas as pd
import datetime


def main(target_company,stop_days):
    #获取工作日日期
    start_date = input('请以 mm/dd/yyyy 的格式输入需要分析的新闻的起始日期:')
    end_date = input('请以 mm/dd/yyyy 的格式输入需要分析的新闻的结束日期:')

    workdays = pd.bdate_range(start_date, end_date)
    #print(workdays.date) #获取日期列表

    trading_days = list(workdays.date)
    
    trading_days = [str(i) for i in trading_days if i not in stop_days]
    #print(trading_days)

    daily_factor = pd.read_csv('daily_factor.tsv',sep='\t',header=None)

    company_list = []
    date_list = []
    F_iT = []

    for company in target_company:
        company_info = daily_factor.loc[daily_factor[1] == company]
        #print(company_info)
        for trade_date in trading_days:
            d1 = datetime.datetime.strptime(trade_date,'%Y-%m-%d')
            delta = datetime.timedelta(days=31)
            n_days = d1 - delta
            #print(str(n_days))
            #break
            companydate_info = company_info.loc[(company_info[0] >= str(n_days) )&(company_info[0] <= trade_date)]
            nrow = companydate_info.shape[0]
            f_iT = 0
            company_list.append(company)
            date_list.append(trade_date)
            if nrow != 0:
                for index in range(0,nrow):
                    d2 = datetime.datetime.strptime(companydate_info.iloc[index,0],'%Y-%m-%d')
                    day = d1-d2
                    day = int(day.days) 
                    wt = (30-day)/30 #带有时间衰减的权重，没新闻的天数默认得分为0
                    #print(day,wt,nrow)
                    f_iT += wt*float(companydate_info.iloc[index,2])
            F_iT.append(f_iT)

    emotion_factor = pd.DataFrame({'date':date_list,'company':company_list,'F_iT':F_iT})
    emotion_factor.to_csv("emotion_factor.tsv",index=False,encoding='utf-8',sep='\t')
    return