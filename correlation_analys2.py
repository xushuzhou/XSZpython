# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 14:05:36 2017

@author: xushuzhou

"""

import psycopg2
import sys
import impala.dbapi as im
#import const
import copy as cp
from copy import deepcopy
#数据库连接，与hive连接
"""
'调用impala
"""
def impala_connect():
    hconn=im.connect(host='192.168.39.6',port=21050,user='hive', password='',database='default')
    #a=im.connect()
    return hconn
    
def impala_select(sql):
    hconn=impala_connect()
    cur=hconn.cursor()
    cur.execute(sql)    
    temp=cur.fetchall()
    hconn.close()
    return temp

#获取每个项集的事物数
def OutPutFile(filename,strr):
    fileN = filename+'.txt'
    fp = open(fileN,"ab+")
    fp.write(strr)
    fp.close
def get_item_sets(start_date,end_date):

    sql='select\
         b.product_code,\
         count(distinct b.buyer_nick),\
         sum(b.pay_price) as pay_price\
         from(select \
         buyer_nick,\
         count(distinct product_code) as buytypecnt,\
         sum(cast(pn.pay_price as float) ) as pay_price\
          from o_ord_mall_unit_order o \
         left outer join o_ord_mall_unit_order_native n on n.order_id=o.order_id\
        join o_ord_mall_unit_product_native pn on pn.order_id=o.order_id\
        where ((substr(o.order_id,1,1)<=\'9\'and o.order_status is not   null)\
               or\
               (o.order_status is  null and n.order_type in (\'original\',\'import\')\
                 and (substr(o.order_id,1,1) NOT LIKE \'S\' AND substr(o.order_id,1,1) NOT LIKE \'C\' )\
                 and (case when o.order_source=\'tmall_gongxiao\' then  5 else \
                     length(substr(o.order_id,instr(o.order_id,\'-\')+1,5)) end )>3 \
               ))\
        and o.order_source=\'tmall\'\
        and to_date(o.pay_time) between \''+start_date+'\'  and \''+end_date+'\'\
        and is_present=\'0\'\
        group by buyer_nick\
        )  a \
        join (\
        select \
        buyer_nick,\
        product_code,\
        sum(cast(pn.pay_price as float)) as pay_price\
         from o_ord_mall_unit_order o \
        left outer join o_ord_mall_unit_order_native n on n.order_id=o.order_id\
        join o_ord_mall_unit_product_native pn on pn.order_id=o.order_id\
        where ((substr(o.order_id,1,1)<=\'9\'and o.order_status is not   null)\
               or\
               (o.order_status is  null and n.order_type in (\'original\',\'import\')\
                 and (substr(o.order_id,1,1) NOT LIKE \'S\' AND substr(o.order_id,1,1) NOT LIKE \'C\' )\
                 and (case when o.order_source=\'tmall_gongxiao\' then  5 else \
                     length(substr(o.order_id,instr(o.order_id,\'-\')+1,5)) end )>3 \
               ))\
        and o.order_source=\'tmall\'\
        and to_date(o.pay_time) between \''+start_date+'\'  and \''+end_date+'\'\
        and is_present=\'0\'\
        group by buyer_nick,\
        product_code\
        ) b on a.buyer_nick=b.buyer_nick and a.buytypecnt>1\
        group by \
        b.product_code\
        order by 2 desc'        
    return impala_select(sql)
    
def get_affair_sets(start_date,end_date):
    sql='select\
      b.buyer_nick,\
      group_concat(product_code,\'&\') as product_code,\
      sum(b.pay_price) as pay_price\
      from(select \
      buyer_nick,\
      count(distinct product_code) as buytypecnt,\
      sum(cast(pn.pay_price as float) ) as pay_price\
       from o_ord_mall_unit_order o \
      left outer join o_ord_mall_unit_order_native n on n.order_id=o.order_id\
      join o_ord_mall_unit_product_native pn on pn.order_id=o.order_id\
      where ((substr(o.order_id,1,1)<=\'9\'and o.order_status is not   null)\
             or\
             (o.order_status is  null and n.order_type in (\'original\',\'import\')\
               and (substr(o.order_id,1,1) NOT LIKE \'S\' AND substr(o.order_id,1,1) NOT LIKE \'C\' )\
               and (case when o.order_source=\'tmall_gongxiao\' then  5 else \
                   length(substr(o.order_id,instr(o.order_id,\'-\')+1,5)) end )>3 \
             ))\
      and o.order_source=\'tmall\'\
      and to_date(o.pay_time) between \''+start_date+'\'  and \''+end_date+'\'\
      and is_present=\'0\'\
      group by buyer_nick\
      )  a \
      join (\
      select \
      buyer_nick,\
      product_code,\
      sum(cast(pn.pay_price as float)) as pay_price\
       from o_ord_mall_unit_order o \
      left outer join o_ord_mall_unit_order_native n on n.order_id=o.order_id\
      join o_ord_mall_unit_product_native pn on pn.order_id=o.order_id\
      where ((substr(o.order_id,1,1)<=\'9\'and o.order_status is not   null)\
             or\
             (o.order_status is  null and n.order_type in (\'original\',\'import\')\
               and (substr(o.order_id,1,1) NOT LIKE \'S\' AND substr(o.order_id,1,1) NOT LIKE \'C\' )\
               and (case when o.order_source=\'tmall_gongxiao\' then  5 else \
                   length(substr(o.order_id,instr(o.order_id,\'-\')+1,5)) end )>3 \
             ))\
      and o.order_source=\'tmall\'\
      and to_date(o.pay_time) between \''+start_date+'\'  and \''+end_date+'\'\
      and is_present=\'0\'\
      group by buyer_nick,\
      product_code\
      ) b on a.buyer_nick=b.buyer_nick and a.buytypecnt>1\
      group by \
      b.buyer_nick'
    print sql
    return impala_select(sql)

#获取item的排序   
def get_item_rank(item_rank,item):
	  itemInfo=item_rank.get(item)
	  return itemInfo
#递归访问字典,遍历字典,遍历树枝,并将一节点增加到树枝上
def const_Node(branchTree,key,NodeItem): #branchTree字典
	  for item,vlue in branchTree.items():
	  	  ##print vlue[0],len(vlue[0])
	  	  if len(vlue[0]) ==0:#列表第一个值子字典
	  	  	  branchTree[item][0]={key:NodeItem} #构造出新的一个树叶
	  	  else:
	  	  	  ##print branchTree[item][0]
	  	  	  branchTree_temp=const_Node(branchTree[item][0],key,NodeItem)
	  	  	  branchTree[item][0]=branchTree_temp
	  ##print branchTree
	  return branchTree
#构造树枝	  
def const_branchTree(Node):
    temp=[]
    branchTree={}
    for i in range(0,len(Node)):
  	   if i==0:#构造第一个树根节点
             temp=[]
             temp.append({}) #son
             temp.append(1) #affairNum
             itemInfo=[]
             itemInfo.append(Node[i][0])
             itemInfo.append(Node[i][1])
             itemInfo.append(Node[i][3])
             temp.append(itemInfo)
             branchTree[Node[i][2]]=temp
  	   else:
             temp=[]
             temp.append({})#son
             temp.append(1) #affairNum
             itemInfo=[]
             itemInfo.append(Node[i][0])
             itemInfo.append(Node[i][1])
             itemInfo.append(Node[i][3])
             temp.append(itemInfo) #itemInfo
    	        #递归构造树枝
             ##print branchTree,temp
             branchTree=const_Node(branchTree,Node[i][2],temp) 	   
    return branchTree
#压缩树branchTree,是列表
def compress_Tree(branchTreeValue,Node):
	  ##print type(Node),len(Node)
	  if len(Node)==0: #当超节点被压缩完时就返回
	  	  return branchTreeValue
	  if get_item_rank(branchTreeValue[0],Node[0][2])==None:
	  	  branchTreeValue[0][Node[0][2]]=const_branchTree(Node)[Node[0][2]]
	  else:
	  	  branchTreeValue[0][Node[0][2]][1]=branchTreeValue[0][Node[0][2]][1]+1
	  	  #将该节点的子枝继续和节点node匹配 看是否相同
	  	  branchTreeValue[0][Node[0][2]]=compress_Tree(branchTreeValue[0][Node[0][2]],Node[1:len(Node)])
	  	  
	  return branchTreeValue	   		  
def FP_growth(affair_data,item_rank):
    
    #将事物数据集合压缩成一个树  
    #书的节点，子节点用列表，数据字典{编码1:[{},'affairNum','itemInfo'],编码2:[{},'affairNum','itemRank']}
    #根节点
    affairTree={'root':'FT-growth','rootson':{}}
    branchTree={}   #单一树枝
    #print len(affair_data)
    for i in range(0,len(affair_data)):
    	  #遍历一个事务的所有项，对项进行排序，并构造树
    	   Node=[]
    	   j=0
    	   for j in range(0,len(affair_data[i][1].split('&'))):
        	  #获取每个项的数据信息
        	  temp=[]
        	 
        	  #temp=get_item_rank(item_rank,affair_data[i][1].split('&')[j])
        	  temp=cp.deepcopy(item_rank[affair_data[i][1].split('&')[j]])
        	  #temp2=temp 
        	  ##print affair_data[i][1].split('&')[j],item_rank.get(affair_data[i][1].split('&')[j])
        	  temp.append(affair_data[i][1].split('&')[j])
        	  temp.append(j)
        	  Node.append(temp)        	          	  
        	  #节点1：商品的购买家数，第二是销售额，第三是商品编码，第四是排序编码
        	  #对事务中的项进行排序
        	  for loop in range(0,j):
        	  	  if Node[j][0]> Node[loop][0]:
        	  	  	   temp_tail=Node[j]
        	  	  	   temp_loop=loop
    	  	  	  	   for loop2 in range(j,loop,-1):
        	  	  	  		  #temp2=Node[loop2]        #倒序置换	，插值排序  	  	  	  	         	  	  	  	  	  
        	  	  	  		  Node[loop2]=Node[loop2-1]
        	  	  	  		  Node[loop2][3]=loop2
    	  	  	  	   Node[loop]=temp_tail
    	  	  	  	   Node[loop][3]=loop
    	  	  ##print Node	  
    	  	  ##print item_rank.get(affair_data[i][1].split('&')[j])
    	   #print Node
    	   #OutPutFile('FP_growth',str(Node)+'\n')
    	   """    	   
    	   if i>10:
         	   break
         """

         #开始造树，将新的节点压缩到fp树种，现在找树种寻找相同的父节点，如果
         #在根节点找到一样的节点则沿着这个树枝进行搜索，否则新建树枝，形成一个新的树枝
         #树的节点，子节点用列表，数据字典{编码1:[{},'affairNum','itemInfo'],编码2:[{},'affairNum','itemRank']}
    	   if len(affairTree['rootson'])==0:
        	   #当根节点为空时构造第一个 树枝
        	   branchTree=const_branchTree(Node)        	  
        	   affairTree['rootson'][Node[0][2]]=branchTree[Node[0][2]]  
        	   ##print i,affairTree  
    	   else:
        	  #这时候树枝的根节点，寻找预支相似的母节点，如果有相同的节点则进行压缩
        	  #否则进行压缩
        	  temp_root=get_item_rank(affairTree['rootson'],Node[0][2])
        	  if temp_root== None:
        	  	  branchTree=const_branchTree(Node)
        	  	  affairTree['rootson'][Node[0][2]]=branchTree[Node[0][2]]
        	  else:
        	  	  #遍历树进行压压缩
        	  	  ##print 'aaaaa',affairTree['rootson'][Node[0][2]],'++++',Node[1:len(Node)]
        	  	  affairTree['rootson'][Node[0][2]][1]=affairTree['rootson'][Node[0][2]][1]+1
        	  	  #如果能查到在根部找到相同的节点，则传递值进行压缩新的节点到树枝        	  	  
        	  	  branchTreeValue=compress_Tree(affairTree['rootson'][Node[0][2]],Node[1:len(Node)])
        	  	  affairTree['rootson'][Node[0][2]]=branchTreeValue
        	  ##print i,affairTree
        	  #OutPutFile('FP_growth',str(i)+str(affairTree)+'\n')
    return affairTree 
"""
def Rank_Items_List(item_dict):
	  ItemsRankList=[]
	  temp=[]
	  for item,value in item_dict:
	  	  temp=[]
	  	  temp.append(item)
	  	  temp.append(value[0])
	  	  temp.append(value[1])	  	  
        ItemsRankList.append(temp)
        for i in range(0,len(ItemsRankList)):
        	  if temp[1]<ItemsRankList[i][1]:        	  	 
        	     temp_tail=temp
        	     for loop in range(len(ItemsRankList),i,-1):
        	     	   ItemsRankList[loop]=ItemsRankList[loop-1]
        	  ItemsRankList[loop]   	  
    return  ItemsRankList     	
"""    	    
def Trav_Tree(affairTree,ItemNode,Freq=[]):
	  temp=[]
	  for item,value in affairTree.items():
	  	  temp_ret=[]
	  	  #print item,value
	  	  Freq.append({item:value[1]})
	  	  #print Freq
	  	  if item == ItemNode :	#当访问到节点就保存该枝	  	
	  	  	 if len(Freq)>1:  #当是第一个根节点时就直接返回，不需要保存
	  	  	    temp.extend(deepcopy([Freq]))
	  	  	    #print 'aaaaaaaaaaaaaaaaass',temp
	  	  	 del Freq[len(Freq)-1]  #这地方只要相等就会删掉	  	 
	  	  	 continue
	  	  	 #return [Freq]
	  	  else:
	  	  	 if len(value[0])!=0:#如果还有子节点 继续访问
	  	  	 	  temp_ret=Trav_Tree(value[0],ItemNode,Freq)  	  	    
	  	  	 if len(value[0])==0: #对于访问到叶子节点 不做处理，这一步代码可以不写
	         	  del Freq[len(Freq)-1]
	         	  continue
	  	  if len(temp_ret)>0:
                    temp.extend(temp_ret) #这地方只是对返回的组合进行处理
	  	  del Freq[len(Freq)-1]
	  #print 'temp',temp
	  
	  return temp
#构造频繁结合集	
def const_comb_sets2(UNGather,SGSetLength,itemNode):
    maxlength=0
    ##print UNGather
    UNGather_temp=[]
    for i in range(0,len(UNGather)):    	      	  
    	  for j in range(i+1,len(UNGather)):
            temp=[]
            flag=0
            ##print UNGather[j]
            #只选择包含有itemNode的组合
            if len(UNGather[i])==1  :#用于第一次递归
            	  if UNGather[i].keys()[0]==itemNode or UNGather[j].keys()[0]==itemNode:
                     temp.extend([UNGather[i]])
                     temp.extend([UNGather[j]])
                     ##print 'dddddddd'
            else:
                temp.extend(UNGather[i])
                temp.extend(UNGather[j])            	   

            #对组合里面的元素去重
            ##print 'aaaaatemp',temp
            temp2=[]
            for k in range(0,len(temp)):
    	  	      #设置标志位剔除不包含挖掘节点的频繁结合
    	  	      
    	  	      if temp[k].keys()[0]==itemNode:
    	  	      	   flag=1
    	  	      if temp[k] not in temp2: #去重
    	  	      #if temp2.index([temp[k]])<0:
        	  	      temp2.append(temp[k])
            ##print 'aaaaa',temp2
            temp2.sort()
            #剔除不包含挖掘节点的频繁结合
            if flag==0:
            	   continue
            #统计列表中最大项，等于原始单项集合长度减一时统计
            #print len(temp2),maxlength
            if len(temp2)>maxlength:
            	   maxlength=len(temp2)
            if temp2 not in UNGather_temp:
                UNGather_temp.append(temp2)
    #如果结合没有达到大的长度就继续组合
    ##print UNGather_temp
     
    """
    UNGather_temp2=[]
    #去重并且
    for l in range(0,len(UNGather_temp)):
    	  if UNGather_temp[l] not in  UNGather_temp2:
    	  	  UNGather_temp2.append(UNGather_temp[l])
    """
    #判断是否还要继续递归
    #print 'UNGather_temp2',SGSetLength,maxlength,UNGather_temp
    #return
    if (maxlength>4 or (SGSetLength-1)<maxlength) and len(UNGather)>1:
    	  #print 'xxxxxxxxxxxx'
    	  return UNGather_temp
    else:
    	  #print 'ddddddddd',SGSetLength,maxlength
    	  UNGather_temp.extend(const_comb_sets2(UNGather_temp,SGSetLength,itemNode)) 
    ##print UNGather_temp2
    return UNGather_temp 
#挖掘频繁项
    
def MIN_Freq(FreqSetsList,item_rank,itemNode):
     
     tempFreqSetsList=deepcopy(FreqSetsList)
     UNGather=[]
     UNGatherNodeNum=[]
     for i in range(0,len(FreqSetsList)):
     	   #d对于树枝过长的进行裁剪
         for j in range(0,len(FreqSetsList[i])):
             ##print FreqSetsList[i][j]
             if len(UNGather)==0:
             	   tempvalue=item_rank.get(FreqSetsList[i][j].keys()[0])[0]
             	   #if tempvalue>10:
             	   UNGather.append({FreqSetsList[i][j].keys()[0]:tempvalue})
             	   #tempNode=deepcopy()
             	   UNGatherNodeNum.append({FreqSetsList[i][j].keys()[0]:1})
             else:
             	   
                 flag=0
                 for k in range(0,len(UNGatherNodeNum)):
                 
                     if UNGatherNodeNum[k].keys()[0]==FreqSetsList[i][j].keys()[0]:
                         UNGatherNodeNum[k][UNGatherNodeNum[k].keys()[0]]=UNGatherNodeNum[k][UNGatherNodeNum[k].keys()[0]]+1 #+FreqSetsList[i][j][FreqSetsList[i][j].keys()[0]]
                         ##print UNGather[k].values()[0]
                         flag=1
                         break
                     ##print UNGather[k].keys()[0],FreqSetsList[i][j].keys()[0]
                 if flag==0:
                 	   UNGatherNodeNum.append({FreqSetsList[i][j].keys()[0]:1})
                 #获取节点的事物数
                 tempvalue=item_rank.get(FreqSetsList[i][j].keys()[0])[0]
                 if {FreqSetsList[i][j].keys()[0]:tempvalue} not in UNGather:
                     UNGather.append({FreqSetsList[i][j].keys()[0]:tempvalue})
     #对频繁项节点排序
     UNGatherNodeNum_temp=[]
     for item in UNGatherNodeNum:
     	    UNGatherNodeNum_temp.append(item)
     	    ##print item
     	    for loop in range(0,len(UNGatherNodeNum_temp)):
     	    	  if item.values()[0]>UNGatherNodeNum_temp[loop].values()[0]:
     	    	     temp=item
     	    	     for loop2 in range(len(UNGatherNodeNum_temp)-1,loop,-1):
     	    	     	   UNGatherNodeNum_temp[loop2]=UNGatherNodeNum_temp[loop2-1]
     	    	     UNGatherNodeNum_temp[loop]=temp
     	    	     break
     #如果整个树低于20则返回,可以根据需求修改提高阈值

     if UNGatherNodeNum_temp[0].values()[0]<minSupportNum:
     	    return []
     #如果大于基础某个值，则将频繁项大于20的项传递给排列组合函数组合
     UNGatherNodeNum=deepcopy(UNGatherNodeNum_temp)
     UNGatherNodeNum_temp=[]
     UNGather=[]
     for p in range(0, len(UNGatherNodeNum)):
     	   #print UNGatherNodeNum[p]
     	   if UNGatherNodeNum[p].values()[0]>minSupportNum:
     	   	     UNGatherNodeNum_temp.append(UNGatherNodeNum[p])
     	   	     tempvalue=item_rank.get(UNGatherNodeNum[p].keys()[0])[0]
     	   	     UNGather.append({UNGatherNodeNum[p].keys()[0]:tempvalue})
     
     #print 'UNGather',itemNode,UNGather
     #print 'UNGatherNodeNum_temp',UNGatherNodeNum_temp
     #如果频繁度过低则返回
     if len(UNGather)<2:
     	  return 
     UNGatherSets=const_comb_sets2(UNGather,len(UNGather),itemNode)              
	   ###开始统计频繁项集
     FreqMinSets=[]
     for US in range(0,len(UNGatherSets)):	  
        comeq=0 #统计有相等的组合数
        FreqNUM=0  	#统计频繁数   
        for FR in range(0,len(tempFreqSetsList)):	
            flaglength=0  
            flagitemNode=0 	   	                          	   	
            ##print   UNGatherSets[US], tempFreqSetsList[FR]
            for it  in UNGatherSets[US]:	                 	   	    	  
                for ifr in range(0,len(tempFreqSetsList[FR])):	
                    ##print it, tempFreqSetsList[FR][ifr]  	   	    	   	  
                    if it.keys()[0]==tempFreqSetsList[FR][ifr].keys()[0]:	   	   	    	   	   	   
                         flaglength=flaglength+1	   	   	    	   	   
                    if tempFreqSetsList[FR][ifr].keys()[0]==itemNode:	   	   	    	   	   	   
                         flagitemNode=tempFreqSetsList[FR][ifr].values()[0]  
            #查找到结合
            ##print 'flaglength',flaglength,flagitemNode
            if flaglength==len(UNGatherSets[US]) and 	flagitemNode>0:
            	  comeq=comeq+1
            	  FreqNUM=FreqNUM+flagitemNode
        if comeq>0 and FreqNUM>1:
              	  #{'Item':,'FreqSet':,'Freqlength':,'FreqNUM':}   
                   tempd={}                
                   tempd['ItemNode']= itemNode
                   tempd['FreqSet']= UNGatherSets[US]
                   tempd['Freqlength']= len(UNGatherSets[US])
                   tempd['FreqNUM']= FreqNUM
                   #print 'tempd',tempd
                   OutPutFile('FP_growth2','tempd,'+str(tempd)+'\n')
                   FreqMinSets.extend([tempd])
	   
     return FreqMinSets 
	   	  
def MIN_Tree(affairTree,item_rank,item_list):
	  for i in range(len(item_list)-1,-1,-1):#从支持度数最小的开始挖掘
	  	  FreqSetsList=Trav_Tree(affairTree['rootson'],item_list[i][0])
	  	  #print item_list[i][0]
	  	  #若没有则返回
	  	  if len(FreqSetsList)==0:
	  	  	   continue
	  	  """
	  	  for j in range(0,len(FreqSetsList)):
	  	  	  #print j,item_list[i][0],FreqSetsList[j]
	  	  	  OutPutFile('FP_growth2',str(j)+','+str(FreqSetsList[j])+'\n')
	  	  """	  
	  	  FreqMinSets=MIN_Freq(FreqSetsList,item_rank,item_list[i][0])
	  	  OutPutFile('FP_growth2',str(FreqMinSets)+'\n')
	  	  ##print i,item_rank[i],temp
	  	  

#************配置参数***********************
#最新支持数量
minSupportNum=20
#累计统计多少天的数据
statistics_days=0 #累计统计几天的数据
#*******************************************
import time
import datetime
#************统计时间计算*****************
now = datetime.datetime.now()
to_day = now.strftime("%Y-%m-%d")
loop=0
day_list=[]
while(loop<=statistics_days):
	  DayAgo = (datetime.datetime.now() - datetime.timedelta(days = loop))
	  DayAgo = DayAgo.strftime("%Y-%m-%d")
	  day_list.append([to_day,DayAgo])
	  loop=loop+1
#************统计时间计算*****************	  
#day_list=[['2017-06-30','2017-06-01']]
#******************获取样本，并计算*****************
for i in range(0,len(day_list)):
     item_rank={}
     item_list=[]
     temp=[]
     #print day_list[i]
     for item in get_item_sets(day_list[i][1],day_list[i][0]):
         temp=[]
         item_rank[item[0]]=[item[1],item[2]]
         temp.append(item[0])
         temp.append(item[1])
         temp.append(item[2])
         item_list.append(temp)         
     affairTree=FP_growth(get_affair_sets(day_list[i][1],day_list[i][0]),item_rank)
     print get_affair_sets(day_list[i][1],day_list[i][0])
     MIN_Tree(affairTree,item_rank,item_list)
#******************获取样本，并计算*****************
    
##print item_rank    
##print  get_item_rank(item_rank,834543)   
"""    
for i in get_item_sets():
	if i[1]>10:
		 #print i
"""
#Node=[[3286, 302966.5904598236, '80000244', 0], [2181, 97683.13784646988, '10001018', 1], [1362, 107667.6963596344, '10000939', 2]]

"""
#FreqSetsList=Trav_Tree(affairTree['rootson'],'10000936')
#print  get_item_sets()
#for i in range(0,len(FreqSetsList)):
#         print 'aaaaa',i,FreqSetsList[i]
#for i in affairTree['rootson']:
#	   #print i,affairTree['rootson'][i]
	   #OutPutFile('FP_growth2',str(i)+','+str(affairTree['rootson'][i])+'\n')
#import json
##print json.dumps(affairTree)

##用于测试遍历各种树枝类型
testrootson1='{"rootson": {"10000403": [{"10000711": [{}, 1, [326, 1064.963302910328, 1]]}, 1, [855, 65802.6887550354, 0]], "10000937": [{"10001018": [{}, 1, [2181, 97683.13784646988, 1]]}, 1, [2363, 184202.77228927612, 0]], "10000936": [{"10001018": [{}, 1, [2181, 97683.13784646988, 1]]}, 1, [4016, 368150.38353538513, 0]], "80000087": [{"10001017": [{}, 1, [189, 10628.700351715088, 1]]}, 1, [305, 18240.05435180664, 0]], "10000846": [{"10001018": [{"10000939": [{"10001033": [{"10001032": [{"10000346": [{}, 1, [708, 16176.839259147644, 5]]}, 1, [823, 41076.697174072266, 4]]}, 1, [1162, 42228.86979866028, 3]]}, 1, [1362, 107667.6963596344, 2]]}, 1, [2181, 97683.13784646988, 1]]}, 1, [2716, 227308.2946472168, 0]], "80000244": [{"10000937": [{"10000744": [{"10001024": [{}, 1, [460, 26741.60032272339, 3]]}, 1, [1487, 11624.160913158208, 2]]}, 1, [2363, 184202.77228927612, 1]], "10001027": [{}, 1, [1772, 263672.50091552734, 1]], "10001018": [{"10000939": [{}, 1, [1362, 107667.6963596344, 2]]}, 2, [2181, 97683.13784646988, 1]]}, 4, [3286, 302966.5904598236, 0]], "10001018": [{"10000847": [{}, 1, [1363, 110336.95314216614, 1]]}, 1, [2181, 97683.13784646988, 0]], "10000679": [{"10000743": [{}, 1, [825, 6598.683988511562, 1]]}, 1, [1505, 26662.451779603958, 0]]}, "root": "FT-growth"}'
#testrootson1='{"rootson": {"10000403": [{"10001018": [{}, 1, [825, 6598.683988511562, 1]],"10000711": [{"10001018": [{}, 1, [825, 6598.683988511562, 1]],"10000679": [{"10000743": [{"10001018": [{}, 1, [825, 6598.683988511562, 1]]}, 1, [825, 6598.683988511562, 1]]}, 1, [1505, 26662.451779603958, 0]]}, 1, [326, 1064.963302910328, 1]]}, 1, [855, 65802.6887550354, 0]]}, "root": "FT-growth"}'
testrootson1='{"rootson": {"10000403": [{"10001018": [{"10000679": [{}, 1, [825, 6598.683988511562, 1]]}, 1, [825, 6598.683988511562, 1]],"10000711": [{"10001018": [{}, 1, [825, 6598.683988511562, 1]],"10000679": [{"10000743": [{"10001018": [{}, 1, [825, 6598.683988511562, 1]]}, 1, [825, 6598.683988511562, 1]]}, 1, [1505, 26662.451779603958, 0]]}, 2, [326, 1064.963302910328, 1]]}, 1, [855, 65802.6887550354, 0]]}, "root": "FT-growth"}'

FreqSetsList=[[{'80000244': 3053}, {'10000744': 175}, {'10000743': 10}, {'80000164': 1}]\
,[{'10000403': 379}, {'10000595': 34}, {'80000164': 1}]\
,[{'10001028': 81}, {'10000711': 2}, {'10000067': 1}, {'80000164': 1}]\
,[{'80000731': 14}, {'80000164': 1}]\
,[{'10000936': 3868}, {'10000744': 108}, {'10000847': 5}, {'10000940': 1}, {'10001033': 1}, {'10001034': 1}, {'80000682': 1}, {'10001024': 1}, {'10000711': 1}, {'10001037': 1}, {'80000550': 1}, {'10000741': 1}, {'80000684': 1}, {'10000094': 1}, {'80000164': 1}]]





##print affairTree
#branchTree=const_branchTree(Node)
##print branchTree
#compress_Tree()

#if item_rank[10001018] !=None:


for i in get_affair_sets():
	#print i
"""	