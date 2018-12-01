'''
ZOOMSTAR CLASS

what is drawn in the zoomstars depends on "type" array that is formed in the main method
graphs are saved in "graphs" folder
@author: Kadri Umbleja
'''

import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as clrs
import numbers
import math
from PIL import Image
from matplotlib.offsetbox import (OffsetImage,AnnotationBbox)


ylim=1 #normalized data
datapoints=4 #how many points shown of axis
font_s=8
max_color_intensity=1 #how strong colors will be used
map_name='copper' #color map to be used

class Radar(object):

    def __init__(self, fig, titles,nrf,objects,colors, labels=None, rect=None):
        if rect is None:
            rect = [0.05, 0.05, 0.95, 0.95]    
        self.n = len(titles)
        self.angles = [a if a <=360. else a - 360. for a in np.arange(90, 90+360, 360.0/self.n)]
        self.angle=abs(self.angles[0]-self.angles[1])
        self.angles2 = [a if a <=360. else a - 360. for a in np.arange(90, 90+360, 360.0/(self.n*2))]
        self.axes = [fig.add_axes(rect, projection="polar", label="axes%d" % i) 
                         for i in range(self.n)]
    
        self.ax = self.axes[0]
        self.nrf=nrf
        self.objects=objects
        self.colors=colors
        self.ax.set_thetagrids(self.angles, labels=titles, fontsize=font_s, weight="bold", color="black")
    
        for ax in self.axes[1:]:
            ax.patch.set_visible(False)
            ax.grid("off")
            ax.xaxis.set_visible(False)
            self.ax.yaxis.grid(False)
    
        for ax, angle in zip(self.axes, self.angles):
            ax.set_rgrids(range(1, 10), labels="", angle=angle, fontsize=font_s)
            ax.spines["polar"].set_visible(False)
            ax.set_ylim(0, ylim)  
            ax.xaxis.grid(True,color='black',linestyle='-')
            ax.patch.set_facecolor('none')
    
    def get_angle(self):
        return self.angle
    
    def setTitle(self,title,color):
        self.ax.set_title(title, size=11, color=color, y=1.1)
        
    def plot(self, values,values2, i,*args, **kw):
        self.ax.set_title(self.objects[i], size=11, color=self.colors[i], y=1.1)
        angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
        values = np.r_[values, values[0]]
        values2 = np.r_[values2, values2[0]]
        self.ax.plot(angle, values, *args, **kw)
        self.ax.plot(angle, values2, *args, **kw)

        self.ax.fill_between(angle, values, values2,color=self.colors[i])
        
    def plot_point(self,i,values, *args, **kw):
        angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
        self.ax.plot(angle[i], modValue(values), *args, **kw)
        
    def AddText(self,i, y, s):
        angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
        self.ax.text(angle[i], modValue(y), s, fontsize=font_s)
    
    def plot_filled_line(self,i,x1,x2,y1,y2,e,al=0.1,color=None):
        if(color is None):
            color=self.colors[e]
        angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
        
        a=[angle[i],angle[i+1]]    
        v1=[modValue(x1),modValue(x2)]
        v2=[modValue(y1),modValue(y2)]
        self.ax.fill_between(a, v1, v2,facecolor=color, alpha=al)
    
        
    def plot_lines_for_fill(self,i,x1,x2,y1,y2, *args, **kw):
        angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
        
        a=[angle[i],angle[i+1]]    
        v1=[modValue(x1),modValue(x2)]
        v2=[modValue(y1),modValue(y2)]
        self.ax.plot(a, v1, *args, **kw)
        self.ax.plot(a, v2, *args, **kw)

        
    def plot_int_to_categoryEQ(self,i,x1,y1,m,direction,*args, **kw):
        angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
        angle2 = np.deg2rad(np.r_[self.angles2, self.angles2[0]])
        v1=[modValue(x1),m]
        v2=[modValue(y1),m]
        a=[angle[i],angle2[(i*2+direction)%(self.nrf*2)]]
        self.ax.fill_between(a, v1, v2, *args, **kw)
        
        
    def plot_line_half(self,i,x1,x2,m,direction, *args, **kw):
        angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
        angle2 = np.deg2rad(np.r_[self.angles2, self.angles2[0]])
        
        a=[angle[i],angle2[(i*2+direction)%(self.nrf*2)]]   
        v1=[modValue(x1),m]
        v2=[modValue(x2),m]
        self.ax.fill_between(a, v1, v2, *args, **kw)
    def plot_line(self,i,x1,x2, *args, **kw):
        angle = np.deg2rad(np.r_[self.angles, self.angles[0]])

        a=[angle[i],angle[(i+1)%(self.nrf)]]   
        v1=[modValue(x1),modValue(x2)]
        self.ax.plot(a, v1, *args, **kw)

def modValue(x):
    extra_space=0.2
    return (x+extra_space)/(1+extra_space)
    
def fig2data ( fig ):
    """
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    # draw the renderer
    fig.canvas.draw ( )
 
    # Get the RGBA buffer from the figure
    w,h = fig.canvas.get_width_height()
    buf = np.fromstring ( fig.canvas.tostring_argb(), dtype=np.uint8 )
    buf.shape = ( w, h,4 )
 
    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll ( buf, 3, axis = 2 )
    return buf

def fig2img ( fig ):
    """
    @brief Convert a Matplotlib figure to a PIL Image in RGBA format and return it
    @param fig a matplotlib figure
    @return a Python Imaging Library ( PIL ) image
    """
    # put the figure pixmap into a numpy array
    buf = fig2data ( fig )
    w, h, d = buf.shape
    return Image.frombytes( "RGBA", ( w ,h ), buf.tostring( ) )

#P-PCA points
def drawScatterPlot(aList2,nrf,nre,objects,titles,type,Fmin,Fmax,P,quantiles,hues=[],labels=[]):


    if(labels is None or len(labels)==0):
        labels=[]
        for i in range(nrf):
            ll=[]
            ll.append(Fmin[i])
            ll.append(Fmax[i])
            labels.append(ll)
    else:
        for i in range(nrf):
            if(len(labels[i])==0):
                ll=[]
                ll.append(Fmin[i])
                ll.append(Fmax[i])
                labels[i]=ll
    
    
    fig = plt.figure(figsize=(15, 8))
    ax1 = fig.add_subplot(111)
    
    for i in range(nre):
        xy = [P[0][i],P[1][i]]
        arr =drawZoomStar(aList2,nrf,nre,objects,titles,[3,0,1,1],Fmin,Fmax,quantiles=quantiles,obj_nr=i,hues=hues,labels=labels,mode=1)
    #     arr =z.eqZoomStar(X,i,titles,objects,color,labels,type,1)
        im = OffsetImage(fig2img (arr), zoom=0.10)
        plt.close(arr)
    
        im.image.axes = ax1
    
        ab = AnnotationBbox(im, xy, xybox=(0,0),boxcoords="offset points")
        ab.patch.set(edgecolor='white', alpha=0)
        ax1.add_artist(ab)
    
    ax1.scatter(P[0], P[1])
    ax1.set_xlabel("PC1")
    ax1.set_ylabel("PC2")
    for i, txt in enumerate(objects):
        ax1.annotate(txt, (P[0][i],P[1][i]))
    
    fig.savefig('graphs/PCA_scatter.pdf', format='pdf', dpi=300)
    pl.show()
    

# type indicates what is included in graph 
#0 - 1-span, 2-color intensity , 3- quantiles
#1 - 1-plot eq interval
#2 - 1- plot median line with 100% color intensity 2-median with black color
#3 - 1- axis texts are includes, 0 - not included
def plotFeature(histogram,nextH,radar,colors,i,nrf,quantiles=[],type=[0,0,0,0]):
    
    global max_color_intensity
    r_max=max_color_intensity
       
    
    if(type[0]==2): #color intensity
        
        #different between different symbolic objects        
        if(histogram.type==0):
            if(nextH.type==0):
                x1=histogram.get_nonZeroS()
                x2=nextH.get_nonZeroS()
                y1=histogram.get_nonZeroE()
                y2=nextH.get_nonZeroE()
                radar.plot_filled_line(i,x1,x2,y1,y2,histogram.e,max_color_intensity,color=colors[histogram.e])
           #next is category
            elif(nextH.type==1):
                m=histogram.get_m(nextH,radar.get_angle())
    
                radar.plot_int_to_categoryEQ(i,histogram.get_nonZeroS(),histogram.get_nonZeroE(),m,1,facecolor=colors[histogram.e], alpha=max_color_intensity)
                for j in range(nextH.getNrofBins()):
                    if nextH.get_data(j)>0:
    
                        radar.plot_line_half((i+1)%nrf,nextH.get_start(j),nextH.get_end(j),m,-1,facecolor=colors[histogram.e], alpha=max_color_intensity*nextH.get_data(j)) 
    #                 i am category
        elif(histogram.type==1):
            #next is interval
            if(nextH.type==0):
                m=histogram.get_m(nextH,radar.get_angle())
                radar.plot_int_to_categoryEQ((i+1)%nrf,nextH.get_nonZeroS(),nextH.get_nonZeroE(),m,-1,facecolor=colors[nextH.e], alpha=max_color_intensity)
    
    
                for j in range(histogram.getNrofBins()):
                    if histogram.get_data(j)>0:
                        radar.plot_line_half(i,histogram.get_start(j),histogram.get_end(j),m,1,facecolor=colors[histogram.e], alpha=max_color_intensity*histogram.get_data(j))  
            
            #next is also category
            if(nextH.type==1):
                m=histogram.get_m(nextH,radar.get_angle())
                for j in range(histogram.getNrofBins()):
                    if histogram.get_data(j)>0:
                        radar.plot_line_half(i,histogram.get_start(j),histogram.get_end(j),m,1,facecolor=colors[histogram.e], alpha=max_color_intensity*histogram.get_data(j)) 
                        
    
                for j in range(nextH.getNrofBins()):
                    if nextH.get_data(j)>0:
                        radar.plot_line_half((i+1)%nrf,nextH.get_start(j),nextH.get_end(j),m,-1,facecolor=colors[histogram.e], alpha=max_color_intensity*nextH.get_data(j)) 
#         max_color_intensity=r_max
    elif(type[0]==1): #span       
        
        #I am interval
        if(histogram.type==0):
            #next is also interval
            if(nextH.type==0):
                radar.plot_filled_line(i,histogram.get_nonZeroS(),nextH.get_nonZeroS(),
                                        histogram.get_nonZeroE(),nextH.get_nonZeroE(),histogram.e, al=0.4, color=colors[histogram.e])
            #next is category
            elif(nextH.type==1):
                m=histogram.get_m(nextH,radar.get_angle())
                radar.plot_int_to_categoryEQ(i,histogram.get_nonZeroS(),histogram.get_nonZeroE(),m,1,facecolor=colors[histogram.e], alpha=0.4)
                

                for j in range(nextH.getNrofBins()):
                    if nextH.get_data(j)==1:
                        radar.plot_line_half((i+1)%nrf,nextH.get_start(j),nextH.get_end(j),m,-1,facecolor=colors[histogram.e], alpha=0.4) 
        #i am category
        elif(histogram.type==1):
            #next is interval
            if(nextH.type==0):
                m=histogram.get_m(nextH,radar.get_angle())

                radar.plot_int_to_categoryEQ((i+1)%nrf,nextH.get_nonZeroS(),nextH.get_nonZeroE(),m,-1, facecolor=colors[histogram.e], alpha=0.4)

                for j in range(histogram.getNrofBins()):
                    if histogram.get_data(j)==1:
                        radar.plot_line_half(i,histogram.get_start(j),histogram.get_end(j),m,1,facecolor=colors[histogram.e], alpha=0.4)  
            
            #next is also category
            if(nextH.type==1):
                m=histogram.get_m(nextH,radar.get_angle())
#                 radar.plot_int_to_categoryEQ(nextH.i,nextH.get_nonZeroS(),nextH.get_nonZeroE(),m,-1, color=colors[self.e], alpha=0.4)
                

                for j in range(histogram.getNrofBins()):
                    if histogram.get_data(j)==1:
                        radar.plot_line_half(i,histogram.get_start(j),histogram.get_end(j),m,1, color=colors[histogram.e], alpha=0.4) 
                        
#                 radar.plot_int_to_categoryEQ(self.i,self.get_nonZeroS(),self.get_nonZeroE(),m,1,color=colors[self.e], alpha=0.4)

                for j in range(nextH.getNrofBins()):
                    if nextH.get_data(j)==1:
                        radar.plot_line_half((i+1)%nrf,nextH.get_start(j),nextH.get_end(j),m,-1,color=colors[histogram.e], alpha=0.4) 
    elif(type[0]==3): #quantile zoomstar
        #quantiles
        nr_of_quantiles=len(quantiles)
        color_modi=(1-0.2)/(nr_of_quantiles-1)
        for j in range(nr_of_quantiles-1):
            x1=histogram.get_quantile(quantiles[j])
            x2=nextH.get_quantile(quantiles[j])
            y1=histogram.get_quantile(quantiles[j+1])
            y2=nextH.get_quantile(quantiles[j+1])
            
            radar.plot_filled_line(i,x1,x2,y1,y2,histogram.e,al=(0.2+color_modi*j),color=colors[histogram.i])
            
    if(type[1]==1): #plot equivalent interval       
        c1=histogram.get_compactness(1)
        c2=nextH.get_compactness(1)
        m1=histogram.get_median(histogram.type)
        m2=nextH.get_median(nextH.get_type())
    
        x1=max(m1-c1/2,0)
        x2=max(m2-c2/2,0)
        y1=min(m1+c1/2,1)
        y2=min(m2+c2/2,1)
        radar.plot_filled_line(i,x1,x2,y1,y2,histogram.e,0.6,color=colors[histogram.i])
    
    if(type[2]==1): #median with 100% intensity
        m1=histogram.get_median(histogram.type)
        m2=nextH.get_median(nextH.get_type())
        radar.plot_line(i,m1,m2,"-", lw=1, color=colors[histogram.i], alpha=1)
    elif(type[2]==2): #median with black
        m1=histogram.get_median(histogram.type)
        m2=nextH.get_median(nextH.get_type())
        radar.plot_line(i,m1,m2,"-", lw=1, color='black', alpha=1)
        

    
def drawZoomStar(aList,nrf,nre,objects,titles,type,Fmin,Fmax,obj_nr=None,hues=[],quantiles=[],new_order=[],cols=None,labels=[],mode=0):
    if(len(hues)==0):
        hues=[0.5 for x in range(nre)]
        
   
    labels,colors,titles=ZoomStarInitalize(nrf,nre,titles,Fmin,Fmax,hues,new_order,labels)
    
    if(obj_nr is None):
        if(cols is None):
            cols=nre
        fig=drawZoomStarPlot(aList,nrf,nre,objects,titles,type,colors,labels,cols,quantiles)
    else:
        fig=drawZoomStarSingle(aList,nrf,obj_nr,titles,objects,colors,labels,quantiles,type)
  
    if(mode==0):
        plt.savefig('graphs/zoomstar.pdf', format='pdf', dpi=300, bbox_inches = "tight")
        pl.show()
    elif(mode==1):
        return fig

def ZoomStarInitalize(nrf,nre,titles,Fmin,Fmax,hues,new_order=[],labels=None): 
    if(labels is None or len(labels)==0):
        labels=[]
        for i in range(nrf):
            ll=[]
            ll.append(Fmin[i])
            ll.append(Fmax[i])
            labels.append(ll)
    else:
        for i in range(nrf):
            if(len(labels[i])==0):
                ll=[]
                ll.append(Fmin[i])
                ll.append(Fmax[i])
                labels[i]=ll
    
    jet = cm = plt.get_cmap(map_name) 
    cNorm  = clrs.Normalize(vmin=0, vmax=1)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
    colors =[]
    for e in range(nre):
        colors.append(scalarMap.to_rgba(hues[e]))

    if  new_order:
        labels=apply_permutation(labels,new_order)
        titles=apply_permutation(titles,new_order)
    return labels,colors,titles


def drawZoomStarPlot(aList,nrf,nre,objects,titles,type,colors,labels,cols,quantiles):
    rows=math.ceil(nre/cols)
    fig = pl.figure(figsize=(5*cols,5*rows)) 
    
    marginw=0.03
    marginh=0.02
    width=(1-cols*marginw)/cols
    height=(1-rows*marginh)/rows   
       
    for e in range(nre):

        
        row=math.floor(e/rows)
        col=(e-row*rows)
        
        histograms=[]
        
        #rectangle x0, y0, width, height
        radar = Radar(fig, titles,nrf,objects,colors,labels,rect=[row*width+marginh*(row), col*height+marginw*(col),width,height])
        radar.setTitle(objects[e],colors[e])
            
        for i in range(len(labels)):
            if(np.size(labels[i])!=2 or isinstance(labels[i][0], numbers.Number)==False):
                kord=ylim/(np.size(labels[i]))
                for j in range(np.size(labels[i])):
                    radar.plot_point(i,kord*(j),'ro',color="black", alpha=0.4,markersize=2);
                    radar.AddText(i, kord*(j)+kord/2, labels[i][j])
            else:
                kord=(labels[i][1]-labels[i][0])/datapoints
                kord2=ylim/(datapoints)
                for j in range(datapoints+1):
                    if j>=0:
                        radar.plot_point(i,kord2*(j),'ro',color="black", alpha=0.4,markersize=2);
                        if(abs(labels[i][0]+kord*j)<1):
                            radar.AddText(i, kord2*(j), round(labels[i][0]+kord*j,2))
                        else:
                            radar.AddText(i, kord2*(j), round(labels[i][0]+kord*j))
                           

           
        for i in range(nrf):
            histograms.append(aList[e].getHistogram(i))
           
           
        for i in range(nrf):
            plotFeature(histograms[i],histograms[(i+1)%nrf],radar,colors,i,nrf,quantiles,type=type)   
        e=e+1               
                    
                    
def drawZoomStarSingle(aList2,nrf,e,titles,objects,colors,labels,quantiles,type):
    fig = plt.figure(figsize=(8, 8)) 

    fig.patch.set_facecolor('none')
        
    histograms=[]
    
    if(type[3]==0):
        for i in range(len(titles)):
            titles[i]=""
        
    radar = Radar(fig, titles,nrf,objects,colors)
    if(type[3]==1):
        radar.setTitle(objects[e],colors[e])
            

        for i in range(len(labels)):
            if(np.size(labels[i])!=2 or isinstance(labels[i][0], numbers.Number)==False):
                kord=ylim/(np.size(labels[i]))
                for j in range(np.size(labels[i])):
                    radar.plot_point(i,kord*(j),'ro',color="black", alpha=0.4,markersize=2);
                    radar.AddText(i, kord*(j)+kord/2, labels[i][j])
            else:
                kord=(labels[i][1]-labels[i][0])/datapoints
                kord2=ylim/(datapoints)
                for j in range(datapoints+1):
                        if j>=0:
                            radar.plot_point(i,kord2*(j),'ro',color="black", alpha=0.4,markersize=2);
                            if(abs(labels[i][0]+kord*j)<1):
                                radar.AddText(i, kord2*(j), round(labels[i][0]+kord*j,2))
                            else:
                                radar.AddText(i, kord2*(j), round(labels[i][0]+kord*j))
           
    for i in range(nrf):
        histograms.append(aList2[e].getHistogram(i))

    for i in range(nrf):
        plotFeature(histograms[i],histograms[(i+1)%nrf],radar,colors,i,nrf,quantiles,type=type)
               
    return fig


def apply_permutation(lst, p):
    return [lst[x] for x in p]
