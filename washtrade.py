import numpy as np
import datetime as dt
import csv

position=[]
f1new=[]
buy=[]
sell=[]
matched_pairs=[]
signed=[]

dp=3;
dv=30;
dti=10; 


class order:
    def __init__(self,trader_id,time,price,volume):
        self.trader=trader_id
        self.time=time
        self.price=price
        self.volume=volume
        
        
#a=order(1,dt.datetime.now(),125,500)
#
#b=order(-2,dt.datetime.now(),124.2,490)
#
#c=order(2,dt.datetime.now(),125.5,490)
#
#d=order(-1,dt.datetime.now(),125,500)
#a=order()
        
a=order(-1,dt.datetime.now(),125,1450)
b=order(2,dt.datetime.now(),125.01,1500)
c=order(-2,dt.datetime.now(),124.95,1500)
d=order(3,dt.datetime.now(),125.01,1450)
e=order(-5,dt.datetime.now(),124.90,200)
f=order(3,dt.datetime.now(),124.90,235)
g=order(-3,dt.datetime.now(),125,1450)
h=order(4,dt.datetime.now(),125.01,1500)
i=order(-3,dt .datetime.now(),124.80,250)
j=order(6,dt.datetime.now(),124.70,350)
k=order(-4,dt.datetime.now(),125.01,1450)
l=order(1,dt.datetime.now(),125.01,1450)
m=order(-6,dt.datetime.now(),124.80,200)
n=order(5,dt.datetime.now(),124.50,550)

position.append(a)
position.append(b)
position.append(c)
position.append(d)
position.append(e)
position.append(f)
position.append(g)
position.append(h)
position.append(i)
position.append(j)
position.append(k)
position.append(l)
position.append(m)
position.append(n)
 
    
def wash_trade_detection(position):
    matched_pairs=list()
    tm=list()
    for i in range(len(position)):
        
        if position[i].trader>0:
            buy.append(position[i])
            matched_pairs=coarse_detect(matched_pairs,position[i],sell);
        else:
            sell.append(position[i])
            matched_pairs=coarse_detect(matched_pairs,position[i],buy);
        ss=np.size(matched_pairs)
        if ss>0:
            cc=0
    
            if len(tm)<=0:
                for i in matched_pairs:
                    tm.append(i)
            else:        
            
                for i in matched_pairs:
                    cc=0
                    for j in range(len(tm)):
                        if (tm[j].trader==i.trader) and (tm[j].time==i.time) and (tm[j].price==i.price) and  (tm[j].volume==i.volume):
                            
                            break;
                        else:
                            cc+=1
                         
                    if cc==len(tm):
                        tm.append(i)
            print 'tm is',tm
            fine_detect(tm);

def coarse_detect(qq,order,queue):
    if len(queue)==0:
       return qq;
    #print 'Coarse for the order',order.trader,order.volume
    qtp=[]
    if (order.trader>0):
        for i in range(len(queue)):
            if (queue[i].price<=order.price) and ((abs(queue[i].price)-order.price)<=dp):
                qtp.append(queue[i])
    else:
        for i in range(len(queue)):
            if (queue[i].price>=order.price) and ((abs(queue[i].price)-order.price)<=dp):
                qtp.append(queue[i])
    
    if(len(qtp)==0):
        return qtp;
            
    if(len(qtp)>0):
 
        
        print '\nVolume Matching for the order : ',order.trader,order.volume
        temp=volume_match(qtp,order)
        print 'output of vol_match',temp
        tempo=[]
        
        for i in range(len(temp)):
            for j in range(len(qtp)):
                if temp[i]==qtp[j].volume:
                    tempo.append(qtp[i])
        tempo.append(order)
        return tempo



def opt(n,vk,q,dv,sn):
    
    if len(q)==0:
        print 'Not Possible'
        return
    
    if n>=0:
        print 'Incoming element',q[n],'CAP->',vk,'subset->',sn;
  
    if abs(vk)<=dv:
         
        with open("volume.csv",'a') as towrite:
            csvwriter=csv.writer(towrite)
            csvwriter.writerow(sn);
        

    if n<0:
        return 0;
    
    if ((q[n])-vk)>dv:
        return opt(n-1,vk,q,dv,sn);
    
    else:
        sn.append(q[n])
        print(sn)
        opt(n-1,vk-q[n],q,dv,sn);
        del(sn[len(sn)-1])
        print(sn)
        opt(n-1,vk,q,dv,sn);
        
def ck1(q,val):
    q.append(val)
    s=0
    for i in range(len(q)):
       s+=abs(q[i])
    
    if s/len(q) == s/2:
        del(q[len(q)-1])
        return 0
    else:
        del(q[len(q)-1])
        return 1        
f1new=[-1,2,-2,3,-3,4,-4,1]
def volume_match(matched_pairs,order):
    vk=order.volume
    sn=[]
    q=[]
    l=[]
    ct=-1
    new=[]
    n=len(matched_pairs)
    for i in range(n):
        q.append(matched_pairs[i].volume)
    
    print('Going for opt is',q,'length',n,'vol',vk)
    f=open("volume.csv","w+")
    f.close()
    
    opt(n-1,vk,q,dv,sn)
    
    with open("volume.csv",'r') as toread:
        csvreader=csv.reader(toread)
        for row in csvreader:
            if row not in l:
                l.append(row)
    for i in range(len(l)):
        print(l[i])
    
    for i in l:
        ct+=1
        for j in range(len(i)):
            l[ct][j]=int(l[ct][j])
    for i in range(len(l)):
        print(l[i])    
        
    for i in l:
        for j in i:
            new.append(j)
   
    for i in range(len(new)):
        print(new[i])
    
    
    
    return new;


    
def fine_detect(orders):        
    cyc=[]
    n=len(orders)
    sign=[]
    ct=-1
    for i in range(len(orders)):
        sign.append(orders[i].trader)
    for i in range(len(sign)):
        print(sign[i])
    tot=0
    fnew=[]  
    t=[]  
    f=open("wash.csv","w+")
    f.close()
    washed_away(n,tot,sign,t)   
    with open("wash.csv",'r') as toread:
        csvreader=csv.reader(toread)
        for row in csvreader:
            if row not in cyc:
                cyc.append(row)
    for i in range(len(cyc)):
        print(cyc[i])
    for i in cyc:
        ct+=1
        for j in range(len(i)):
            cyc[ct][j]=int(cyc[ct][j])
    for i in range(len(cyc)):
        print(cyc[i])    
    for i in cyc:
        for j in i:
            fnew.append(j)
    for i in range(len(fnew)):
        print(fnew[i])
    if len(fnew)>0:
        print 'Wash Trade happened',f1new
    else:
        print 'No wash Trade'
    


def washed_away(n,tot,q,fn):
    print 'Incoming Wash ',n,tot,q,fn
    if n<1:
        return;
    if q[n-1]+tot ==0 and ck1(fn,q[n-1]):
        fn.append(q[n-1])
        with open("wash.csv",'a') as towrite:
            csvwriter=csv.writer(towrite)
            csvwriter.writerow(fn);
        del(fn[len(fn)-1])
        return;
        
    else:
        fn.append(q[n-1])
        washed_away(n-1,tot+q[n-1],q,fn)
        del(fn[len(fn)-1])
        washed_away(n-1,tot,q,fn)
        

wash_trade_detection(position)