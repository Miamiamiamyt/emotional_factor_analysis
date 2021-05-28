import get_news
import test_processing
import get_prediction
import daily_factor
import emotion_factor
import time
import os
import datetime

print('**********舆情因子自动生成系统启动************')
print('任务提示:')
print('每一个任务都需要确保test_company.txt文件的建立和存在')
print('任务说明：')
print('任务1：从爬取新闻开始自动生成舆情因子')
print('任务2：已有新闻数据，从对新闻数据做预测开始自动生成舆情因子')
print('任务3：已有预测数据，直接生成舆情因子')
task = '0'
while (task != '1') and (task != '2') and (task != '3'): 
    task = input('请输入您想实现的任务，用数字1，2，3表示：')
    if (task != '1') and (task != '2') and (task != '3'):
        print('输入任务序号有误，请重新输入：')

#2021年由于节日休市不交易的日期，之后需要每年更新
stop_days = [datetime.date(2021,2,11),datetime.date(2021,2,12),datetime.date(2021,2,15),\
    datetime.date(2021,2,16),datetime.date(2021,2,17),datetime.date(2021,4,5),datetime.date(2021,5,3),\
    datetime.date(2021,5,4),datetime.date(2021,5,5),datetime.date(2021,6,14),datetime.date(2021,9,20),\
    datetime.date(2021,9,21),datetime.date(2021,10,1),datetime.date(2021,10,4),datetime.date(2021,10,5),\
    datetime.date(2021,10,6),datetime.date(2021,10,7)]

if task == '1':
    print('执行任务1：从爬取新闻开始自动生成舆情因子')
    '''
    第一步：先在test_company.txt文件中写入需要分析的目标公司，奇数行是股票代码，偶数行是股票名称
    '''

    '''
    第二步：根据test_company爬取目标公司的新闻
    '''
    date_list = []
    name_list = []
    title_list = []
    content_list = []
    #读取目标公司的股票代码和中文名称
    codes, target_company = get_news.read_txt()
    #注意爬取的新闻的起始日期要比需要计算舆情因子的起始日期早一个月
    get_news.main(codes,target_company,date_list,name_list,content_list,title_list)
    print('新闻已爬取')

    '''
    第三步：进行数据处理，生成test.tsv文件
    '''
    test_processing.main(date_list,name_list,title_list,content_list)

    '''
    第四步:对test.tsv文件的数据进行预测
    '''
    finish = '0'
    while finish == '0':
        command = 'python run_classifier.py --task_name=my --do_predict=true --data_dir=. --vocab_file=./FinBERT_L-12_H-768_A-12_tf/vocab.txt --bert_config_file=./FinBERT_L-12_H-768_A-12_tf/bert_config.json --init_checkpoint=./FinBERT_L-12_H-768_A-12_tf/bert_model.ckpt --max_seq_length=64 --output_dir=./predict_emotion'
        os.system('activate bert')
        os.system(command)
        get_prediction.main()
        print('预测结果已存入predict_emotion/final_prediction.tsv文件中')
        finish = input('若您认为预测结果不理想，请输入0重新预测；若您认为预测结果理想，请输入1进行下一步：')
    '''
    第五步：计算每一天的情绪分数平均值
    '''
    daily_factor.main(target_company)
    '''
    第六步：计算每家企业每天的舆情因子
    '''
    emotion_factor.main(target_company,stop_days)
    print('各家企业每天的舆情因子已生成')

if task == '2':
    print('执行任务2：已有新闻数据test.tsv，从对新闻数据做预测开始自动生成舆情因子')
    codes, target_company = get_news.read_txt()
    '''
    第一步:对test.tsv文件的数据进行预测
    '''
    finish = '0'
    while finish == '0':
        command = 'python run_classifier.py --task_name=my --do_predict=true --data_dir=. --vocab_file=./FinBERT_L-12_H-768_A-12_tf/vocab.txt --bert_config_file=./FinBERT_L-12_H-768_A-12_tf/bert_config.json --init_checkpoint=./FinBERT_L-12_H-768_A-12_tf/bert_model.ckpt --max_seq_length=64 --output_dir=./predict_emotion'
        os.system('activate bert')
        os.system(command)
        get_prediction.main()
        print('预测结果已存入predict_emotion/final_prediction.tsv文件中')
        finish = input('若您认为预测结果不理想，请输入0重新预测；若您认为预测结果理想，请输入1进行下一步：')
    '''
    第二步：计算每一天的情绪分数平均值
    '''
    daily_factor.main(target_company)
    '''
    第三步：计算每家企业每天的舆情因子
    '''
    emotion_factor.main(target_company,stop_days)
    print('各家企业每天的舆情因子已生成')

if task == '3':
    print('执行任务3：已有预测数据，直接生成舆情因子')
    codes, target_company = get_news.read_txt()
    '''
    第一步：计算每一天的情绪分数平均值
    '''
    daily_factor.main(target_company)
    '''
    第二步：计算每家企业每天的舆情因子
    '''
    emotion_factor.main(target_company,stop_days)
    print('各家企业每天的舆情因子已生成')
