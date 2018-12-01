'''
Class for handeling symbolic data
SymbolicObject consists of Histograms
*there are methods for both SymbolicObject and Histogram that are not needed for current task
@author: Kadri Umbleja
'''


import math
from scipy import cluster
from main.Zoomstar import modValue

def apply_permutation(lst, p):
    return [lst[x] for x in p]

def apply_permutationM(lst, p):
    res=[]
    for each_item in lst:
       res.append(apply_permutation(each_item, p)) 
    return res

        
def pureness(aList,nrf,l=[],mode=0):
    if(len(l)==0):
        for i in range(nrf):
            l.append(1)
        
    cnt=0
    avg_features=[0 for y in range( nrf )]    
    for i in range(nrf):
        if(l[i]==1):
            cnt+=1
    for i in range(len(aList)):
        features=[0 for y in range( nrf )]
        for j in range(len(aList)):
            if(i!=j):
                for n in range(nrf):
                    if(l[n]==1):
                        if(Histogram(aList[i].histograms[n].join(aList[j].histograms[n],1,1)).getSize()==0):
                            features[n]+=0
                        else:
                            features[n]+=Histogram(aList[i].histograms[n].meet(aList[j].histograms[n])).getSize()/Histogram(aList[i].histograms[n].join(aList[j].histograms[n],1,1)).getSize()
        if mode==0 :
            print(aList[i].getName(), end=' ')
            for n in range(nrf):
                print(str(features[n]/(len(aList)-1)), end=' ')
            print()
        else:
            for n in range(nrf):
                avg_features[n]+=(features[n]/(len(aList)-1))                             
    if(mode==1):
        for n in range(nrf):
            avg_features[n]/=len(aList)
        return   avg_features

#r=0 returns diss and structure
#r1 returns the list
def HCC(aList2,nrf,nre,till,mode=0,Fmin=[],Fmax=[],l=[],r=0):
    aList=[]
    for i in range(nre):
        aList.append(SymbolicObject(aList2[i].hist,aList2[i].name,aList2[i].types,id=aList2[i].id))
            
    
    featue_len=[]
    if(len(Fmin)==0):
        for i in range(nrf):
            Fmin.append(0)
    if(len(Fmax)==0):
        for i in range(nrf):
            Fmax.append(1)
    if(len(l)==0):
        for i in range(nrf):
            l.append(1)
    cnt=0        
    for i in range(nrf):
        featue_len.append(Fmax[i]-Fmin[i])
        if(l[i]==1):
            cnt+=1
    last=0
    diss=[ [ 0 for y in range( nre ) ] for x in range( nre ) ]
    
    while(len(aList)>till):
        curMin=float("inf")
        minj=-1
        mini=-1
        minW =None
        curr_size=len(aList)
#         print("Current size:"+str(curr_size))
        for i in range(curr_size):
            for j in range(curr_size):
                if(i>j):
                    if(mode==0): #hstogram method
                        b = aList[i].combine(aList[j])
                        sum = b.calcCompactness(l,cnt);
                        if(curMin >sum):
                            curMin=sum
                            minW=b
                            mini=i
                            minj=j
                    elif(mode==4): #ichino method
                        b = aList[i].combineR(aList[j])
                        sum=b.get_avg_Span(l)
                        if(curMin >sum):
                            curMin=sum
                            minW=b
                            mini=i
                            minj=j
#         print(curMin)
#         print(minW.getName())
        print(str(curMin)+","+minW.getName())
#         print(str(curMin)+","+str(nre-1),end=",")
        for i in range(len(aList[mini].list)):
            for j in range(len(aList[minj].list)):
                k = aList[mini].list[i].id;
                m = aList[minj].list[j].id;
                diss[k][m]=curMin
                diss[m][k]=curMin
        aList.append(minW)
        aList.pop(mini)
        aList.pop(minj)
#     print(aList[0].getName())
#     print(diss)
    if(r==0):
        return diss,aList[0].getName()
    elif(r==1):
        return aList
#     print(diss)
#     print(aList[0].getName())

def printSummary(aList,titles):
    for i in range(len(aList)):
        print(aList[i].getName())
        for j in range(len(titles)):
            print(titles[j],end=" ")
            for k in range(aList[i].getHistogram(j).nrofBins):
                if(aList[i].getHistogram(j).get_data(k)>0.2):
                    print("["+str(aList[i].getHistogram(j).get_start(k))+","+str(aList[i].getHistogram(j).get_end(k))+"]"+str(round(aList[i].getHistogram(j).get_start(k),3))+";", end=" ")
            print()

#mode decides if empty bins are ignored or not Usually they would be discarded but sometimes it may be desired to keep them
def normalize(X,objects,titles,type,mode=0,Fmin=None,Fmax=None):
    nre= len(X)
    nrf = len(titles)
    aList=[]
    for i in range(nre):
        aList.append(SymbolicObject(X[i],objects[i],type,id=i))


    if(Fmin is None or len(Fmin)==0):
        Fmin=[float("inf") for i in range(nrf)]
        for j in range(nrf):
            for i in range(nre):
                if(mode==0):
                    if(aList[i].getHistogram(j).get_nonZeroS()<Fmin[j]):
                        Fmin[j]=aList[i].getHistogram(j).get_nonZeroS()
                elif(mode==1):
                    if(aList[i].getHistogram(j).start[0]<Fmin[j]):
                        Fmin[j]=aList[i].getHistogram(j).start[0]

    if(Fmax is None or len(Fmax)==0):
        Fmax=[float("-inf") for i in range(nrf)]
        for j in range(nrf):
            for i in range(nre):
                if(mode==0):
                    if(aList[i].getHistogram(j).get_nonZeroE()>Fmax[j]):
                        Fmax[j]=aList[i].getHistogram(j).get_nonZeroE()
                elif(mode==1):
                    if(aList[i].getHistogram(j).end[aList[i].getHistogram(j).nrofBins-1]>Fmax[j]):
                        Fmax[j]=aList[i].getHistogram(j).end[aList[i].getHistogram(j).nrofBins-1]

    aList2=[]

    for i in range(nre):
        aList2.append(SymbolicObject(X[i],objects[i],type,Fmin,Fmax,id=i))
        
    return aList2,Fmin,Fmax

class SymbolicObject(object):
    def __init__(self,hist,name,types=[],Fmin=[],Fmax=[],id=0,nr=1,A = None,B = None,C=[],cluster=0,l=[]):
        self.name=name
        self.hist=hist
        self.id=id
        self.nr=nr
        self.list=[]
        self.types=types
        self.histograms=[]
        self.cluster=cluster
        self.l=l
        self.A=A
        self.B=B
        self.Fmin=Fmin
        self.Fmax=Fmax
        if(A is not None and B is not None):
            self.list.extend(A.getList())        
            self.list.extend(B.getList())
            self.nr=A.getNr()+B.getNr() 

        if(len(self.list)==0):
            self.list.append(self)
        abi=hist.split("},")
        self.nrf=len(abi)
        if not types:
            for i in range (self.nrf):
                types.append(0)
        normalize=1
        if not Fmin:
            normalize=0
            for i in range (self.nrf):
                Fmin.append(0)
                Fmax.append(1)
        if(len(C)==0):
            for i in range(self.nrf):
                C.append(1)
        self.C=C
        for i in range (self.nrf):
            self.histograms.append(Histogram(abi[i],id,e=0,type=types[i],nr=self.nr,Fmin=Fmin[i],Fmax=Fmax[i]))
        if(normalize==1):
            self.hist=""
            for n in range(self.nrf):
                self.hist+=self.histograms[n].getHist()+","
            self.hist=self.hist[:-1]
        
    def set_cluster(self,cluster):
        self.cluster=cluster
    def get_cluster(self):
        return self.cluster            
            
    def getList(self):
        return self.list;
    def getNr(self):
        return self.nr;
    def getHist(self):
        return self.hist;
    def getHistRounded(self,nrR=0):
        sttr=""
        for i in range(self.nrf):
            sttr+=self.histograms[i].getHistRounded(nrR)+","
        return sttr[:-1]
    def getName(self):
        return self.name;
    def getHistogram(self,nr):
        if nr<self.nrf:
            return self.histograms[nr]
        else:
            return None
    def getThinness(self,f1,f2,quantiles=[]):
        if(len(quantiles)==0):
            quantiles=[0,0.1,0.25,0.5,0.75,0.9,1]
        sum=0
        for i in range(len(quantiles)-1):
            p11=self.getHistogram(f1).get_quantile(quantiles[i])
            p12=self.getHistogram(f1).get_quantile(quantiles[i+1])
            p21=self.getHistogram(f2).get_quantile(quantiles[i])
            p22=self.getHistogram(f2).get_quantile(quantiles[i+1])
            sum+=(p12-p11)*(p22-p21)
        return sum
    def get_avg_Size(self):
        a=0
        for i in range(self.nrf):
            a+=self.histograms[i].getSize()
        return a/self.nrf
    def get_pure(self):
        for i in range(self.nrf):
            if(self.types[i]==0):
                if(self.histograms[i].getHist()=="{[0,0]0"):
                    return 0
            elif(self.types[i]==1):
                cnt=0
                for j in range(len(self.histograms[i].data)):
                    cnt+=self.histograms[i].data[j]
                if(cnt==0):
                    return 0
        return 1
    def get_avg_Span(self,l=None):
        if(l==None):
            l=[]
            for i in range(self.nrf):
                l.append(1)
        a=0
        cnt=0
        for i in range(self.nrf):
            if(l[i]==1):
                a+=self.histograms[i].getSpan()
                cnt+=1
        return a/cnt
    def get_avg_compactnessR(self,l=None):
        if(l==None or l==[]):
            l=[]
            for i in range(self.nrf):
                l.append(1)

        cnt=0
        a=0
        for i in range(self.nrf):
            if(l[i]==1):
                a+=self.histograms[i].compactnessR()
                cnt+=1
        return a/cnt
    def get_avg_compactness(self):
        a=0
        for i in range(self.nrf):
            a+=self.histograms[i].get_compactness()
        return a/self.nrf
    def calcCompactness(self,l=[],cnt=0):

        if(len(l)==0):
            for i in range(self.nrf):
                l.append(1)
            cnt=0        
            for i in range(self.nrf):
                if(l[i]==1):
                    cnt+=1
        if(cnt==0):
            for i in range(self.nrf):
                if(l[i]==1):
                    cnt+=1
        total=0
        for i in range(len(self.list)):
            a=self.list[i]
            sum=0
            for j in range(self.nrf):
                if(l[j]==1):
                    sum+=self.histograms[j].dissimilarity(a.histograms[j])
            total+=sum
        return  total/(self.nr*cnt)
    def meetR_relaxedPureness(self,H):
        cnt=0
        nrl=0
        for i in range(self.nrf):
                if(self.getHistogram(i).meetR_relaxedPureness(H.getHistogram(i))!=0):
                    cnt+=1
        if(cnt<self.nrf):
            return 0
        return 1
    def meetR_Pureness(self,H):
        
        cnt=0

        for i in range(self.nrf):
            if(self.getHistogram(i).meetR_Pureness(H.getHistogram(i))!=0):
                cnt+=1

        if(cnt<self.nrf):
            return 0
        return 1
    def meet_relaxedPureness(self,H):
        
        cnt=0
        for i in range(self.nrf):
            cnt+=self.getHistogram(i).meet_relaxedPureness(H.getHistogram(i))
        if(cnt<self.nrf):
            return 0
        return 1
            
    def meetR(self,H):
        meet=""
        name="("+self.getName()+"-"+H.getName()+")"
        for i in range(self.nrf):
            meet+=self.getHistogram(i).meetR(H.getHistogram(i))+","
        return SymbolicObject(meet[:-1],name,self.types,cluster=self.cluster)
    def meet(self,H):
        meet=""
        name="("+self.getName()+"-"+H.getName()+")"
        for i in range(self.nrf):
            meet+=self.getHistogram(i).meet(H.getHistogram(i))+","
        return SymbolicObject(meet[:-1],name,self.types,cluster=self.cluster)
    
    def joinR(self,H):
        join=""
        name="("+self.getName()+"-"+H.getName()+")"
        for i in range(self.nrf):
            join+=self.getHistogram(i).joinR(H.getHistogram(i))+","
        ll=[]
        return SymbolicObject(join[:-1],name,self.types,cluster=self.cluster,l=ll)
    
    def join(self,H):
        join=""
        name="("+self.getName()+"-"+H.getName()+")"
        for i in range(self.nrf):
            join+=self.getHistogram(i).join(H.getHistogram(i))+","
        return SymbolicObject(join[:-1],name,self.types,cluster=self.cluster)
        
    def compactnessR(self):
        comp=0
        for i in range(self.nrf):
            comp+=self.getHistogram(i).compactnessR()
        return comp/self.nrf
    def compactness(self):
        comp=0
        for i in range(self.nrf):
            comp+=self.getHistogram(i).compactness()
        return comp/self.nrf
    
    def purenessR(self,H):
        comp=0
        for i in range(self.nrf):
            comp+=self.getHistogram(i).purenessR(H.getHistogram(i))
        return comp/self.nrf
    
    def mergeFeatures(self,p,q):
        name=self.getName()
        nH=""
        
        CC=[]
        for i in range(self.nrf):
            if(i!=p and i!=q):
                nH+=self.getHistogram(i).getHist()+","
                CC.append(self.C[i])
        nH+=self.getHistogram(p).join(self.getHistogram(q),nr1=self.C[p],nr2=self.C[q])
        CC.append(self.C[p]+self.C[q])
        return SymbolicObject( nH[:-1],name,C=CC)
    
    def mergeFeaturesByAvg(self,p,q,quantiles):  
        name=self.getName()
        nH=""  
        CC=[]
        for i in range(self.nrf):
            if(i!=p and i!=q):
                nH+=self.getHistogram(i).getHist()+","
                CC.append(self.C[i])
        nH+=self.getHistogram(p).mergeByAvg(self.getHistogram(q),quantiles,nr1=1,nr2=1)
        CC.append(self.C[p]+self.C[q])
        return SymbolicObject( nH[:-1],name,C=CC)
    
    def combineByAvg(self,O,quantiles):  
        name="("+str(self.getName())+"-"+str(O.getName())+")"
        nH=""  

        for i in range(self.nrf):
            nH+=self.getHistogram(i).mergeByAvg(O.getHistogram(i),quantiles,nr1=1,nr2=1)+","

        return SymbolicObject( nH[:-1],name,self.types,A = self,B = O)
    
    def combine(self,O):
        name="("+str(self.getName())+"-"+str(O.getName())+")"
        nH=""
        
        for i in range(self.nrf):
            nH+=self.getHistogram(i).join(O.getHistogram(i))+","
        
        return SymbolicObject( nH[:-1],name,self.types,A = self,B = O)
    
    def combineR(self,O):
        name="("+self.getName()+"-"+O.getName()+")"
        nH=""
        for i in range(self.nrf):
            s1=self.getHistogram(i)
            s2=O.getHistogram(i)
            nH+=s1.joinR(s2)+","
        
        return SymbolicObject( nH[:-1],name,self.types,A = self,B = O,cluster=self.cluster)
    def assymetricDissimilarity(self,H,l=[]):
        if(l==[]):
            for i in range(self.nrf):
                l.append(1)
        sum=0
        sum2=0

        for i in range(self.nrf):
            if(l[i]==1):
                sum+=H.getHistogram(i).getSpan()


        join=self.joinR(H)

        for i in range(self.nrf):
            if(l[i]==1):
                sum2+=join.getHistogram(i).getSpan()
        
   
        return sum/sum2
    def purenessR2(self,H,l=[]):
        if(l==[]):
            for i in range(self.nrf):
                l.append(1)
        sum=0
        sum2=0

        meet=self.meetR(H)
        for i in range(self.nrf):
            if(l[i]==1):
                sum+=meet.getHistogram(i).getSpan()


        join=self.joinR(H)

        for i in range(self.nrf):
            if(l[i]==1):
                sum2+=join.getHistogram(i).getSpan()
        
   
        return sum/sum2
    
class Histogram(object):
   
    def __init__(self, hist,i=0,e=0,type=0,nr=1,Fmin=0,Fmax=1):
        
        self.hist=hist+"}"
        self.splitHist(Fmin,Fmax)
        self.type=type
        self.i=i
        self.e=e
        self.nr=nr
        self.nrofBins=len(self.data)
        
        if(Fmin!=0 or Fmax!=1):
            self.hist="{"
            for n in range(self.nrofBins):
                self.hist+="["+str(self.get_start(n))+","+str(self.get_end(n))+"]"+str(self.get_data(n))+";"
            self.hist=self.hist[:-1]+"}"

    
    def getHist(self):
        return self.hist
    def getHistRounded(self,nrR=0):
        sttr="{"
        for i in range(self.nrofBins):
            sttr+="["+str(round(self.start[i],nrR))+","+str(round(self.end[i],nrR))+"]"+str(round(self.data[i],nrR))+";"
        sttr=sttr[:-1]+"}"
        return sttr
    def getSpan(self):
        
        if(self.type==0):
            if(self.get_nonZeroE()==self.get_nonZeroS()):
                return 0.0000000001
            return self.get_nonZeroE()-self.get_nonZeroS()
        elif(self.type==1):
            return self.getSize()
            
    def getSize(self):
        if(self.nrofBins==0):
            return 0
        elif(self.get_nonZeroS()==self.get_nonZeroE()):
            return 0
        else:
            prob_t=0;
            size=0;
            if(self.type==1):
                for i in range(self.nrofBins):
                    size=size+self.get_data(i)*(self.get_end(i)-self.get_start(i))
            else:
                for i in range(self.nrofBins):
                    prob_t=prob_t+self.get_data(i)
                    size=size+prob_t*(self.get_end(i)-self.get_start(i))
        return size
    def assymetricDissimilarity(self,H):
        if(Histogram(self.joinR(H),self.i,0,self.type,1).getSpan()==0):
            return 0
        return H.getSpan()/Histogram(self.joinR(H),self.i,0,self.type,1).getSpan()
    def assymetricDissimilarity2(self,H):

        return self.getSpan()/Histogram(self.joinR(H),self.i,0,self.type,1).getSpan()
    def inclusionSimilarity(self,H):
        return Histogram(self.meetR(H),self.i,0,self.type,1).getSpan()/H.getSpan()
    def inclusionSimilarity2(self,H):
        return Histogram(self.meetR(H),self.i,0,self.type,1).getSpan()/self.getSpan()
     
    def dissimilarity(self,H):
        return Histogram(self.join(H),self.i).getSize()-Histogram(self.meet(H),self.i).getSize()
    def purenessR(self,H):
        meet=Histogram(self.meetR(H),self.i).getSize()
        join=Histogram(self.joinR(H),self.i).getSize()
        if(join==0):
            return 0
        return meet/join
    def pureness(self,H):
        meet=Histogram(self.meet(H),self.i).getSize()
        join=Histogram(self.join(H),self.i).getSize()
        return meet/join
    def compactnessR(self):
        return self.getSpan()
    def compactness(self):
        return self.get_compactness()
    def meetR_Pureness(self,H):
        meet=Histogram(self.meetR(H))
        if(meet.getHist()!="{[0,0]0}"): #not pure
            return 1
        else:
            return 0
    def meetR_relaxedPureness(self,H):
        meet=Histogram(self.meetR(H))
        if(meet.getHist()!="{[0,0]0}"):
            if(self.getSpan()/2>meet.getSpan() and H.getSpan()/2>meet.getSpan()):
                return 0
        else:
            return 0
        return 1
    def meet_relaxedPureness(self,H):
        meet=Histogram(self.meet(H))
        if(meet.getHist()!="{[0,0]0}"):
            if(self.getSpan()/2>meet.getSize() and H.getSpan()/2>meet.getSize()):
                return 0
        else:
            return 0
        return 1
    def meetR (self, H):
        if(self.type==0):
            if(max(self.get_nonZeroS(), H.get_nonZeroS())<=min(self.get_nonZeroE(), H.get_nonZeroE())):
                if((self.get_nonZeroS()==self.get_nonZeroE() or H.get_nonZeroS()==H.get_nonZeroE()) and ((self.get_nonZeroE() == H.get_nonZeroE()) or (self.get_nonZeroS()== H.get_nonZeroS()))):

                    return "{[0,0]0}"
                else:
                    return "{["+str(max(self.get_nonZeroS(), H.get_nonZeroS()))+","+str(min(self.get_nonZeroE(), H.get_nonZeroE()))+"]1}"
            else:
                return "{[0,0]0}"
        elif(self.type==1):
            sttr="{"
            for i in range(len(self.data)):
                if(self.data[i]==1 and H.data[i]==1):
                    sttr+="["+str(self.start[i])+","+str(self.end[i])+"]1;"
                else:
                    sttr+="["+str(self.start[i])+","+str(self.end[i])+"]0;"
            sttr=sttr[:-1]+"}"
            if(sttr=="}"):
                return "{[0,0]0}"
            else:
                return sttr
    def meet(self,H):
        nSt="{"
        i=0
        j=0
        start_c=min(self.get_start(i),H.get_start(j))
        if(start_c==self.get_start(i)):
            i=i+1
        if(start_c==H.get_start(j)):
            j=j+1
        while(i<=self.getNrofBins() and j<=H.getNrofBins()):
            end_c=min(self.next(i),H.next(j));
            prob=0
            if(self.type==0):
                prob=self.probability_min_uni(i,j,start_c,end_c,H)
            elif(self.type==1): # categorical value
                if(self.get_data(i-1)==1 and H.get_data(j-1)==1):
                    prob=1;
            nSt=nSt+"["+str(start_c)+","+str(end_c)+"]"+str(prob)+";"
            if(end_c==self.next(i)): 
                i=i+1
            if(end_c==H.next(j)):
                j=j+1

            start_c=end_c;
        if(i>self.getNrofBins()):
            while(j<=H.getNrofBins()):
                end_c=H.next(j)
                prob=0;
                nSt=nSt+"["+str(start_c)+","+str(end_c)+"]"+str(prob)+";"
                start_c=end_c; 
                j=j+1
        else:
            while(i<=self.getNrofBins()):
                end_c=self.next(i)
                prob=0;
                nSt=nSt+"["+str(start_c)+","+str(end_c)+"]"+str(prob)+";"
                start_c=end_c; 
                i=i+1
        return nSt[:-1]+"}";
    def joinR (self, H):
        if(self.type==0):
            return "{["+str(min(self.get_nonZeroS(), H.get_nonZeroS()))+","+str(max(self.get_nonZeroE(), H.get_nonZeroE()))+"]1}"
        elif(self.type==1):
            sttr="{"
            for i in range(len(self.data)):
                if(self.data[i]==1 or H.data[i]==1):
                    sttr+="["+str(self.start[i])+","+str(self.end[i])+"]1;"
                else:
                    sttr+="["+str(self.start[i])+","+str(self.end[i])+"]0;"
            sttr=sttr[:-1]+"}"
            if(sttr=="}"):
                return "{[0,0]0}"
            else:
                return sttr
    def mergeByAvg(self,H,quantiles,nr1=1,nr2=1):
        nSt="{"
        la=self.get_quantile(quantiles[0])
        lb=H.get_quantile(quantiles[0])
        for i in range(len(quantiles)-1):
            a=self.get_quantile(quantiles[i+1])
            b=H.get_quantile(quantiles[i+1])
            
            nSt=nSt+"["+str(((la*nr1)+(lb*nr2))/((nr1+nr2)))+","+str(((a*nr1)+(b*nr2))/((nr1+nr2)))+"]"+str((quantiles[i+1]-quantiles[i]))+";"
        return nSt[:-1]+"}";
    
    def join(self,H,nr1=0,nr2=0):
        nSt="{"
        i=0
        j=0
        if(nr1==0):
            nr1=self.nr
        if(nr2==0):
            nr2=H.nr
        start_c=min(self.get_start(i),H.get_start(j))
        if(start_c==self.get_start(i)):
            i=i+1
        if(start_c==H.get_start(j)):
            j=j+1
            
        while(i<=self.getNrofBins() and j<=H.getNrofBins()):
            end_c=min(self.next(i),H.next(j));
            prob=0
            if(self.type==0):
                prob=self.probability_norm_uni(i,j,start_c,end_c,H,nr1,nr2)
            elif(self.type==1): # categorical value
                if(self.get_data(i-1)==1 or H.get_data(j-1)==1):
                    prob=1;
     
            nSt=nSt+"["+str(start_c)+","+str(end_c)+"]"+str(prob)+";"
            if(end_c==self.next(i)): 
                i=i+1
            if(end_c==H.next(j)):
                j=j+1

            start_c=end_c;
        
        if(i>self.getNrofBins()):
            while(j<=H.getNrofBins()):
                end_c=H.next(j)
                prob=self.probability_norm_uni(i,j,start_c,end_c,H,nr1,nr2);
                nSt=nSt+"["+str(start_c)+","+str(end_c)+"]"+str(prob)+";"
                start_c=end_c; 
                j=j+1
        else:
            while(i<=self.getNrofBins()):
                end_c=self.next(i)
                prob=self.probability_norm_uni(i,j,start_c,end_c,H,nr1,nr2);
                nSt=nSt+"["+str(start_c)+","+str(end_c)+"]"+str(prob)+";"
                start_c=end_c; 
                i=i+1
        return nSt[:-1]+"}";
    
    def probability_min_uni(self,i,j,start_c,end_c,H): 
        if(i-1<0 or i>self.getNrofBins()):
            return 0;
        elif(j-1<0 or j>H.getNrofBins()):
             return 0  
        else:
            if(i-1<0):
                return 0
            elif(j-1<0):
                return 0  
            elif(end_c==start_c):
                return 0      
            elif(self.get_end(i-1)>=end_c and self.get_start(i-1)<=start_c and H.get_end(j-1)>=end_c and H.get_start(j-1)<=start_c):
                return min(self.get_data(i-1)*(end_c-start_c)/(self.get_end(i-1)-self.get_start(i-1)),
                        H.get_data(j-1)*(end_c-start_c)/(H.get_end(j-1)-H.get_start(j-1)))
            else:
                return 0;        
    def probability_norm_uni(self,i,j,start_c,end_c,H,nr1,nr2):

        if(i-1<0 or i>self.getNrofBins()): #first has no bins
            if(j-1<0 or j>H.getNrofBins()): #second has no bins
                return 0
            else:
                if(H.get_end(j-1)>=end_c and H.get_start(j-1)<=start_c): #second has a bin
                    if(end_c==start_c):
                        return (nr2*H.get_data(j-1))/(nr1+nr2)
                    else:
                        return ((end_c-start_c)*nr2*H.get_data(j-1)/(H.get_end(j-1)-H.get_start(j-1)))/(nr1+nr2);
                else:
                    return 0
        elif(j-1<0 or j>H.getNrofBins()): #second has no bins
            if(i-1<0 or i>self.getNrofBins()): #first has no bins
                return 0
            else:
                if(self.get_end(i-1)>=end_c and self.get_start(i-1)<=start_c): #second has a bin
                    if(end_c==start_c):
                        return (nr1*self.get_data(i-1))/(nr1+nr2)
                    else:
                        return ((end_c-start_c)*nr1*self.get_data(i-1)/(self.get_end(i-1)-self.get_start(i-1)))/(nr1+nr2);
                else:
                    return 0
        else:
            if(end_c==start_c):
                return 1
            elif(self.get_end(i-1)>=end_c and self.get_start(i-1)<=start_c and H.get_end(j-1)>=end_c and H.get_start(j-1)<=start_c):
                return ((end_c-start_c)*nr1*self.get_data(i-1)/(self.get_end(i-1)-self.get_start(i-1))+(end_c-start_c)*nr2*H.get_data(j-1)/(H.get_end(j-1)-H.get_start(j-1)))/(nr1+nr2);
            elif(self.get_end(i-1)>=end_c and self.get_start(i-1)<=start_c):
                return ((end_c-start_c)*nr1*self.get_data(i-1)/(self.get_end(i-1)-self.get_start(i-1)))/(nr1+nr2);
            elif(H.get_end(j-1)>=end_c and  H.get_start(j-1)<=start_c):
                return ((end_c-start_c)*nr2*H.get_data(j-1)/(H.get_end(j-1)-H.get_start(j-1)))/(nr1+nr2);
            else:
                return 0;
    
    def next(self,index):        
        if(index<self.getNrofBins()): #valid index
            return self.get_start(index)
        elif(index==self.getNrofBins()):
            return self.get_end(self.getNrofBins()-1)
        else:
            return -1

    def splitHist(self,Fmin,Fmax):

        self.data=[]
        self.start=[]
        self.end=[]
        abi=self.hist.replace("{", "").replace("}", "").replace("[","").split(";")
        conf=Fmax-Fmin
        for n in range(len(abi)):
            b=abi[n].split("]")
            c=b[0].split(",")
            self.data.append(float(b[1]))
            if(Fmin==0 and Fmax==1):
                self.start.append(float(c[0]))
                self.end.append(float(c[1]))
            else:
                self.start.append(max(0,(float(c[0])-Fmin)/conf))
                self.end.append(min(1,(float(c[1])-Fmin)/conf))
            
    def getNrofBins(self):
        return self.nrofBins

    def get_nonZeroS(self):
        for i in range(self.nrofBins):
            if(self.data[i]>0):
                return self.start[i]
        return 0;
        
    def get_nonZeroE(self):
        for i in reversed(range(self.nrofBins)):
            if(self.data[i]>0):
                return self.end[i]
        return 0;
    def get_data(self,j):
        return self.data[j]
    def get_start(self,j):
        return self.start[j]
    def get_end(self,j):
        return self.end[j]
    def get_type(self):
        return self.type
    def get_median(self,type=None):
        if(type==None):
            type=self.type
            
        if(type==0):
            total=0
            for i in range(self.nrofBins):
                total+=self.get_data(i)
            if(total==0):
                return 0
            return self.get_quantile(total/2)
        elif(type==1):
            total=0
            for i in range(self.nrofBins):
                total+=self.get_data(i)
            if(total==0):
                return 0
            
            if(total>1): #categorical variable
            
                half1=math.floor(total/2)
                half2=math.ceil(total/2)
                
                if(half1!=half2): #odd nr of categories
                    i=0
                    total=0
                    while total<half1:
                        total+=self.get_data(i)
                        i+=1
                    return (self.get_start(i)+self.get_end(i))/2
                else:
                    i=0
                    total=0
                    while total<half1:
                        total+=self.get_data(i)
                        i+=1
                    return self.get_start(i)
            else: #modal multi valued
                return self.get_quantile(total/2)
    def get_compactness(self,feature_len=1):
        so_far=0
        for i in range(self.nrofBins):
            so_far+=self.get_data(i)*(self.get_end(i)-self.get_start(i))
        return so_far/feature_len
    def print_quantiles(self,quantiles):
        for i in range(len(quantiles)):
            print(self.get_quantile(quantiles[i]),end=" ")
        print()
    def get_eqInterval(self):
        c=self.get_compactness()
        m=self.get_median(self.type)
        min=m-c/2
        max=m+c/2
        if(min<0):
            min=0
            max=c
        return Histogram("{["+str(min)+","+str(max)+"]1")
    def get_quantile(self,perc):
        so_far=0
        tt=0
        if(perc==0):
            return self.get_nonZeroS();
        if(perc==1):
            return self.get_nonZeroE();

        for i in range(self.nrofBins):
            tt=tt+self.get_data(i)

        for i in range(self.nrofBins):
            if so_far+(self.get_data(i)/tt)<perc:
                so_far=so_far+(self.get_data(i)/tt)
            else:
                return (perc-so_far)*(self.get_end(i)-self.get_start(i))/(self.get_data(i)/tt)+self.get_start(i)
        return 0

    def get_cummulative(self,limit):
        so_far=0
        if(limit==0):
            return 0
        for i in range(self.nrofBins):
            if(self.get_end(i)<0):
                so_far=0
            if self.get_end(i)>=limit:
                if(limit<self.get_start(i)):
                    return 0
                return so_far+self.get_data(i)*(limit-self.get_start(i))/(self.get_end(i)-self.get_start(i))
            else:
                so_far=so_far+self.get_data(i)
        return 1
        
    def get_m(self,nextH,angle):
        m1=modValue(self.get_median(self.type))
        m2=modValue(nextH.get_median(nextH.get_type()))
        a=math.sqrt(math.pow(m1, 2)+math.pow(m2, 2)-2*m1*m2*math.cos(math.radians(angle)))
        p=(a+m1+m2)/2
        return math.sqrt((4*m1*m2*p*(p-a))/(math.pow((m1+m2),2)))
    
    
                                
                            