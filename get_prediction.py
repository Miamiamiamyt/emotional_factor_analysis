import os
import pandas as pd
 
 
def main():
    path = "predict_emotion/"
    pd_all = pd.read_csv(os.path.join(path, "test_results.tsv") ,sep='\t',header=None)
    pd_info = pd.read_csv("test.tsv",sep='\t',header=None)
    company = pd_info[2]
    date = pd_info[3]
    company = company[1:]
    date = date[1:]
 
    prediction = []
    ind = []
    count = 0
 
    for index in pd_all.index:
        negative_score = pd_all.loc[index].values[0]
        neutral_score = pd_all.loc[index].values[1]
        positive_score = pd_all.loc[index].values[2]

        count += 1
        ind.append(count)

        if max(neutral_score, positive_score, negative_score) == neutral_score:
            # data.append(pd.DataFrame([index, "neutral"],columns=['id','polarity']),ignore_index=True)
            prediction.append(0)
        elif max(neutral_score, positive_score, negative_score) == positive_score:
            #data.append(pd.DataFrame([index, "positive"],columns=['id','polarity']),ignore_index=True)
            prediction.append(1)
        else:
            #data.append(pd.DataFrame([index, "negative"],columns=['id','polarity']),ignore_index=True)
            prediction.append(-1)
        #print(negative_score, positive_score, negative_score)
 
    #print(ind)
    data= pd.DataFrame({'index':ind,'date':date,'company':company,'prediction':prediction})
    data.to_csv(os.path.join(path, "final_prediction.tsv"),index=False,  encoding='utf-8',sep='\t')
    #print(data)
    return