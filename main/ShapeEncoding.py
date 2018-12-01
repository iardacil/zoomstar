'''
Class for drawing ShapeEncoding vizualisation
@author: Kadri Umbleja
'''

import matplotlib.pyplot as plt


class QDraw(object):
    def __init__(self, fig,titles,xlim,ylim,height, rect=None):
        if rect is None:
            rect = [0.05, 0.05, 0.95, 0.95]
        self.n = len(titles)
        self.axes = [fig.add_axes(rect) 
                         for i in range(self.n)]
        self.ax = self.axes[0]
        self.ax.set_ylim(0, ylim)  
        self.ax.set_xlim(0, xlim)  
        self.height=height
        
    def setTitle(self,title,color):
        self.ax.set_title(title, size=11, color=color, y=1.1)
        
    #e is the objects
    #j is the feature
    #k is the bin
    
    def paintSymbol(self,e,j,k,alpha,bins):
        so_far=0
        if(j>0):
            for i in range(j):
                so_far+=bins[i]

          
        a=[so_far+(k),so_far+(k+1)]
       
        v1=[self.height*e,self.height*e]
        v2=[self.height*(e+1),self.height*(e+1)]

        self.ax.fill_between(a, v1, v2,facecolor='black', alpha=alpha)
    def addLineOnly(self,x1,x2,y1,y2):
        v=[x1,x2]
        y=[y1,y2]
        self.ax.plot(y, v, color="black")
    def addObjectNames(self,e,nrf, s):
        self.ax.text(nrf+1,e*self.height+self.height*0.3, s)
    def addFeatureNames(self,j,nre, s):
        self.ax.text(j,nre*self.height+0.1, s,{'ha': 'left', 'va': 'bottom'},rotation=90)
        
def drawShapeCoding(aList,objects,titles,bins=None,new_order=[],new_order2=[]):
    
    nrf=aList[0].nrf
    nre=len(aList)
    
    if(len(new_order)==0):
        for i in range(nre):
            new_order.append(i)
    
    if(len(new_order2)==0):
        for i in range(nrf):
            new_order2.append(i)       

    if(bins is None or len(bins)==0):
        bins=[]
        for j in range(nrf):
            if(aList[0].getHistogram(j).type==0):
                bins.append(10)
            else:
                bins.append(aList[0].getHistogram(j).nrofBins)
    
    print(bins)

    a_s=0.5
    a_s2=0.5
    margin=0.035
    margin2=0.1
    height=1
    
    t_bins=0
    for j in range(nrf):
        t_bins+=bins[j]
    fig = plt.figure(figsize=(24, 8))
    radar = QDraw(fig, titles,t_bins,nre,height, rect=[margin, margin2, a_s, a_s2])
    
        

    for e in range(nre):
        
   
    
        histograms=[]
        for i in range(nrf):
            histograms.append(aList[new_order[e]].getHistogram(new_order2[i]))
            
        
        so_far=0;
        for j in range(nrf):
            nr_of_steps=bins[j]
            for k in range(nr_of_steps):
                st=histograms[j].get_cummulative(k/nr_of_steps)
                en=histograms[j].get_cummulative((k+1)/nr_of_steps)  
                diff=en-st
#                 print(diff)
                radar.paintSymbol(e,j,k,diff,bins)
#                 Y[e][i*10+j]=diff
        e=e+1 
    for e in range(nre): 
        radar.addLineOnly(e*height,e*height,0,t_bins)
        radar.addObjectNames(e,t_bins,objects[new_order[e]])
    so_far=0
    for i in range(nrf):
        radar.addFeatureNames(so_far,nre,titles[new_order2[i]])
        so_far+=bins[i]
        radar.addLineOnly(0,nre*height,so_far,so_far)
        
    
    plt.savefig('graphs/shapeEncoding.pdf', format='pdf', dpi=300, bbox_inches = "tight")
    plt.show() 