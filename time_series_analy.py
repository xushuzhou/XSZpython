# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 09:53:53 2017
a
@author: xushuzhou
"""

import os
import matplotlib.pylab as plt
import numpy as np
import datetime

import psycopg2
#import pyhs2 as ph
import sys
import pandas as pd
"""
'调用postgresql数据库'
"""
def Getfile(path):
     fp = open(path,"rb")
     content=fp.readlines()
     fp.close()
     return content
#            
def PutFile1(filename,strr):
    fileN = filename
    fp = open(fileN,"ab+")
    fp.write(strr.encode('utf8'))
    fp.close
def OutPutFile(filename,strr):
    fileN = filename+'.txt'
    fp = open(fileN,"ab+")
    fp.write(strr)
    fp.close    
"""
'调用postgresql数据库'
"""
def conn_db(db_conf) :
    try :
        db = psycopg2.connect(host=db_conf["server"], user=db_conf["username"], password=db_conf["password"],database= db_conf["dbname"], port=db_conf["port"])
    except Exception,e:
        print e
        db = None
    return db
    
def close_db(db):
    if db :
        db.close()


def exec_sql(db,sql) :

    res=()
    try :
        # db = conn_db(db_conf)
        cursor = db.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        db.commit()
        cursor.close()
    except:
        res = ()

    return res

def exec_sql_param(db,sql) :
	  #db=conn_db()
	  cursor = db.cursor()
	  cursor.execute(sql)
	  db.commit()
	  cursor.close()


def executemany_sql_param(db,sql,param) :
    #param￡oêy?Yμ?×éo?áD±í
    # db=conn_db()
    cursor = db.cursor()
    cursor.executemany(sql,param)
    db.commit()
    cursor.close()
    
def if_exists_data(db,sql):
    try :
        # db = conn_db()
        cursor = db.cursor()
        n=cursor.execute(sql)
        if n==0 :
            return False
        else:
            return True
    except:
        return False
def ConntectDB():
   # select*from(select *,RANDOM() as rnk from fact_b2c_crawl_sent_weibo_bolg)a  where rnk<=0.2;
   db_conf={'username': 'bm_repo', 'password': 'bluemoon2016#', 'dbname': 'crawl', 'server': '192.168.39.1','port':"5432"}
   #db_ora={'username': 'bm_repo', 'password': 'bluemoon2016#', 'dbname': 'crawl', 'server': '192.168.39.1','port':"5432"}
   db=conn_db(db_conf)
   #sql="select*from(select *,RANDOM() as rnk from fact_b2c_crawl_sent_weibo_bolg where key_value='à???áá ?′' )a  where rnk<=0.2"

   return db
def Select_DB(sql):
   db=ConntectDB()
   #
   res = exec_sql(db,sql)
   
   close_db(db)
   """
   Data=[]
   temp=""
   for i in range(0,len(res)):
       temp=str(res[i][0])+"^~"+res[i][1]+"^~"+res[i][2]+"^~"+res[i][3].replace("\n","").replace("\t","")+"\n"
       #print  temp     

       Data.append(temp)
   """    
   return res
   
def Insert_DB(sql):
   #á′?óêy?Y?a
   db=ConntectDB()
   #
   try:
       exec_sql_param(db,sql)
   except Exception as err:
       print err
   
   
   close_db(db)        
"""
'调用postgresql数据库'
"""

"""
'调用hive数据库'
"""
def hive_connect(database):
    hconn=ph.connect(host='192.168.39.3',port=10000,authMechanism="PLAIN",user='hive', password='',database=database)
    return hconn
    
def hive_select(sql,database):
    hconn=hive_connect(database)
    cur=hconn.cursor()
    cur.execute(sql)    
    temp=cur.fetch()
    hconn.close()
    return temp

"""调用数据库*************************************"""


def get_data_pandas(sql):

    r_data=Select_DB(sql)
    
    print type(r_data)
    
    
#计算误差代码   
def calculate_H_error(test_sample,test_predict):
    error_sqrt=np.power(np.sum((np.array(test_sample)-np.array(test_predict))*(np.array(test_sample)-np.array(test_predict)))/len(test_sample),0.5)
    return error_sqrt
#模型计算的核心代码
def HoltWinters(series_data,alpha=0.1,beta=0.7,gamma=0.5,cycle=12):
    #模型出处https://www.otexts.org/fpp/7/5

    train_sample=series_data
    test_sample=[]
    test_sample=series_data[(len(train_sample)-cycle):len(train_sample)]
     
    #seasonal=[]
    #水平趋势,初始值计算
    level=[train_sample[0]]
    #trend=[0]
    
    #print trend
    #增长趋势 短区间，初始值计算
    trend_temp=0
    for i in range(0,cycle):
        #print (train_sample[cycle+i]-train_sample[i])/cycle
        trend_temp=trend_temp+(train_sample[cycle+i]-train_sample[i])/cycle
        
    trend= [trend_temp/cycle] 
    #print trend
    #初始化前  cycle 的数据
    seasonal=[]
    for j in range(0,cycle):
        seasonal.append(train_sample[j]-(level[0]-(j+1-1)/trend[0]/2))
    #print seasonal
    #计算水平趋势level
    for k in range(0,len(train_sample)):
        
        #print seasonal[k]
        level.append(alpha*(train_sample[k]-seasonal[k])+(1-alpha)*(level[k]+trend[k]))
        trend.append((beta*(level[k+1]-level[k])+(1-beta)*trend[k]))
        seasonal.append(gamma*(train_sample[k]-level[k+1])+(1-gamma)*seasonal[k])
    #print seasonal
     
    #用一个周期的数据作模型误差计算    
    t=len(seasonal)-cycle
    #print t
    #取最后一个测试    
    test_level_start=level[len(level)-1-len(test_sample)]  
    test_trend_start=trend[len(trend)-1-len(test_sample)]
   
    test_predict=[]
    #print test_level_start,test_trend_start
    for i in range(1,len(test_sample)+1):
        test_predict.append(test_level_start+i*test_trend_start+seasonal[t+i-1-cycle])
    """
    x=list(np.arange(len(test_predict)))
    plt.plot(x,test_sample,linestyle='--',color='red') 
    plt.plot(x,test_predict,linestyle='--',color='blue')
    #print len(test_sample),len(test_predict)
    """
    error_sqrt=calculate_H_error(test_sample,test_predict)
    
    #print error_sqrt
    return level,trend,seasonal,error_sqrt,test_predict

def algorithm_optimize(paymant,step=0.02,cycle=12):
    #HoltWinters 算法默认以0.02步长为优化策略
    level=[]
    trend=[]
    seasonal=[]
    test_predict=[]
    error_sqrt=0
    flag=0
    
    alpha_ret=0
    beta_ret=0
    gamma_ret=0
    
    alpha=0
    beta=0
    gamma=0
    
    while(alpha<1) :
        alpha=alpha+step
        beta=0
        while(beta<1) :
            beta=beta+step
            gamma=0
            while(gamma<1) :            
                gamma=gamma+step
                level_temp,trend_temp,seasonal_temp,error_sqrt_temp,test_predict_temp=HoltWinters(paymant,alpha,beta,gamma,cycle)
                if flag==0 :
                    error_sqrt=error_sqrt_temp
                else:
                    if error_sqrt>error_sqrt_temp:
                        level=level_temp
                        trend=trend_temp
                        seasonal=seasonal_temp
                        error_sqrt=error_sqrt_temp
                        alpha_ret=alpha
                        beta_ret=beta
                        gamma_ret=gamma
                        test_predict=test_predict_temp
                        
                #print alpha,beta,gamma,error_sqrt                
                flag=1
    test_sample=paymant[(len(paymant)-12):len(paymant)]
    """
    x=list(np.arange(len(test_predict)))
    #plt.plot(x,paymant,linestyle='--',color='red')
    plt.plot(x,test_sample,linestyle='--',color='red') 
    plt.plot(x,test_predict,linestyle='--',color='blue')
    """
    return level,trend,seasonal,error_sqrt,alpha_ret,beta_ret,gamma_ret

def predict(level,trend,seasonal,TK,cycle=12):

    test_level_start=level[len(level)-1]
    test_trend_start=trend[len(trend)-1]
    predict_rt=[]
    #计算季节性的起点
    s_t=len(seasonal)
    for i in range(1,TK+1):
        predict_rt.append(test_level_start+i*test_trend_start+seasonal[s_t+i-1-cycle]) #减1是因为列表从0开始
       
    return predict_rt


def main_sun(sql,platform,category):
 
    #连接数据库
    connection_object=ConntectDB()            
#get_data_pandas(sql)    
    train_sample=pd.read_sql(sql, connection_object)    
    train_sample= train_sample.sort_values('datadate')
    train_sample=train_sample[train_sample.datadate>201412]
    #train_sample=train_sample[train_sample.datadate<201707]
    
#print df
    paymant=list(train_sample['paymant'])
    import numpy as np
    paymant=np.array(paymant)

    paymant=paymant
    paymant=list(paymant)
    #print train_sample
    
    #return 0
    #计算最好平滑系数
    level,trend,seasonal,error_sqrt,alpha,beta,gamma=algorithm_optimize(paymant,step=0.02,cycle=12)
    level,trend,seasonal,error_sqrt,test_predict_temp=HoltWinters(paymant,alpha,beta,gamma)
    

    predictd=predict(level,trend,seasonal,6,12)
  
    
    forecast_info='level:'+str(level)+'&trend:'+str(trend)+'&seasonal:'+str(seasonal)
    forecast_info=forecast_info+'&alpha:'+str(alpha)+'&beta:'+str(beta)+'&gamma:'+str(gamma)
    #计算月份
    maxdate=train_sample.datadate.max()
    month_index=maxdate
    
    #删除需要更新的数据，重新预测更新    
    del_sql='delete from fact_b2c_time_series_analy_mon  where datamon>'+str(month_index)+' and category=\''+category+'\' and platform=\''+platform+'\' and index=\'交易额\''
    print del_sql
    Insert_DB(del_sql)
    #更新插入数据库
    for i in range(0,len(predictd)):
        if month_index%100 == 12:
            month_index=(month_index/100+1)*100+1
        else :
            month_index=month_index+1
        in_sql='insert into fact_b2c_time_series_analy_mon values('+str(month_index)+',\''+category+'\',\''+platform+'\',\''+'交易额'+'\','+str(predictd[i])+','\
        +str(error_sqrt)+',\''+str(forecast_info)+'\')'
        Insert_DB(in_sql)
        OutPutFile('forecast_time_series',in_sql+'\n')
        #print in_sql
    
    #print predictd
#补充样本数据
def Update_sample():
	  lastdaysagos = (datetime.datetime.now() - datetime.timedelta(days = 30))
	  print lastdaysagos
	  lastmoonth=str(lastdaysagos)[0:7].replace('-','')
	  lastmoonth=lastmoonth[0:4]+'/'+lastmoonth[4:7]
	  sql='insert into fact_sycm_time_series_sample(datadate,platform,category,index,original_value) \
	      select\
         cast(replace(datadate,\'/\',\'\') as int) ,typesource,ptype,\'tradeIndex\', \
         case when tradeindex<=2999 then exp(0.0648*ln(tradeindex)*ln(tradeindex)+0.5487*ln(tradeindex)-1.7049) \
             when tradeindex>2999 and tradeindex<=4999 then exp(0.0603*ln(tradeindex)*ln(tradeindex)+0.5984*ln(tradeindex)-1.8338) \
             when tradeindex>4999 and tradeindex<=19999 then exp(0.0285*ln(tradeindex)*ln(tradeindex)+1.1014*ln(tradeindex)-3.8206)\
             when tradeindex>19999  then exp(0.01415*ln(tradeindex)*ln(tradeindex)+1.399*ln(tradeindex)-5.3649)\
           end\
        from fact_b2c_crawl_tmall_industry_index_month \
          where datadate=\''+lastmoonth+'\' \
          '
	  print sql
	  Insert_DB(sql)
Update_sample()

#分品类预测
i=0
platform=['全网']
category=['洗手液','洗洁精','马桶清洁剂/洁厕剂','衣物柔顺剂','消毒液','洗衣液','漂白剂','多用途清洁剂','地面清洁剂','油污清洁剂','宝宝洗手液','衣领净','彩漂','洁瓷剂','宝宝洗衣液','玻璃清洁剂']
print len(category)

for p in range(0,len(platform)):
	for i in range(0,len(category)):
         sql='select  \
              datadate, \
              original_value as paymant \
              from fact_sycm_time_series_sample \
              where platform=\''+platform[p]+'\' and category=\''+category[i]+'\' and index=\'tradeIndex\' order by 1 asc'
         print sql
         main_sun(sql,platform[p],category[i]) 
         OutPutFile('sql.txt',sql)

#全网求和预测        
platform=['全网']
for p in range(0,len(platform)):	
        sql='select  \
              datadate, \
              sum(original_value) as paymant \
              from fact_sycm_time_series_sample \
              where platform=\''+platform[p]+'\' and index=\'tradeIndex\' \
              group by  datadate order by 1 asc'
        print sql
        main_sun(sql,platform[p],'all') 
        OutPutFile('sql.txt',sql)
          
#main_sun()   
"""
#print paymant
#print df
###holt_winters 指数
#第一个一次平滑值，
#S_first[0]=df[df.datadate==201501]['paymant']

paymant=list(df['paymant'])
alpha=0.9
for i in range(1,len(paymant)):
    #print paymant[i-1],S_first[i-1]
    S_first[i]=alpha*paymant[i-1]+(1-alpha)*S_first[i-1]

##三次平滑
#初始值
#平滑系数
alpha=0.1088
beta=0.4
gamma=0.0027


level=[paymant[0]]
trend=[paymant[1]-paymant[0]]
seasonal=[0]

for i in range(1,len(paymant)):
    ##季节处理
    if i<12:
        seasonal_temp=0
    else:
        seasonal_temp=seasonal[i-12]
    #print paymant[i],seasonal_temp,level[i-1],trend[i-1]
    level.append(alpha*(paymant[i]-seasonal_temp)+(1-alpha)*(level[i-1]+trend[i-1]))
    trend.append(beta*(level[i]-level[i-1])+(1-beta)*trend[i-1])

    seasonal.append(gamma*(paymant[i]-level[i])+(1-gamma)*seasonal_temp)
    #print level[i],trend[i],seasonal[i]
print paymant
import numpy as np
import matplotlib.pyplot as plt
x=list(np.arange(len(level)))
#plt.plot(x,paymant,linestyle='--',color='red')
plt.plot(x,level,linestyle='--',color='red') 
plt.plot(x,trend,linestyle='--',color='blue')
plt.plot(x,seasonal,linestyle='--',color='black')

   
#print    trend 
p_data=paymant
#print paymant
#print seasonal[len(seasonal)+12-12]
for k in range(1,12):
    p_data.append(level[len(level)-1]+trend[len(trend)-1]*k+seasonal[len(seasonal)+k-12])
    print seasonal[len(seasonal)+k-12]
#print p_data
#print p_data
#print df[1]
import numpy as np
x=list(np.arange(len(level)))
#df['sort']=x
#print x
import matplotlib.pyplot as plt

#plt.plot(df['sort'],df['paymant'],linestyle='--',color='green')    


plt.plot(x,level,linestyle='--',color='red') 
plt.plot(x,trend,linestyle='--',color='blue')
plt.plot(x,seasonal,linestyle='--',color='black')
#plt.plot(x,paymant,linestyle='--',color='red')  

#plt.plot(x,p_data,linestyle='-',color='blue')
#plt.xticks(df['sort'],df[df.datadate>201501]['datadate'])  
#pl.plot(df['datadate'],df['paymant'])

#print df  
#fig = plt.figure()
#fig,ax = plt.subplots()

#plt.xticks(df['datadate'])    
#plt.grid()     
"""    
