'''
Main class for calling methods. 
Uncomment method desired to perform it under "CallMethod"
@author: Kadri Umbleja
'''

import numpy as np
from main.Common import Histogram,SymbolicObject,normalize
import main.Zoomstar as star
import main.ShapeEncoding as se
import main.classicalPCA as cp
from main.MicroHCC import MHCC
from main.dendogram import drawDendowithDiss

# zoomstar_conf indicates what is included in graph 
#0 - 1-span, 2-color intensity , 3- quantiles
#1 - 1-plot eq interval
#2 - 1- plot median line with 100% color intensity 2-median with black color
#3 - 1- axis texts are includes, 0 - not included

def callMethod(X,objects,titles,type,cat,bins,Fmin,Fmax,norm_mode):
    nre= len(X)
    nrf = len(titles)
    
    aList2,Fmin,Fmax=normalize(X,objects,titles,type,mode=norm_mode,Fmin=Fmin,Fmax=Fmax)
    
    quantiles=[x*0.1 for x in range(11)] #quantiles from 0%, 10%...90%,100%
    nrq=len(quantiles)
    
    
#DRAW ZOOMSTARS:
    hues=[] #if different colors are desired for all objects, values from 0 to 1 should be assigned for every object. Empty list is replaced with 0.5 in method

    #QUANTILE ZOOMSTARS
    zoomstar_conf=[3,0,1,1]
    
    #EQUIVALENT INTERVAL ZOOMSTARS
#     zoomstar_conf=[1,1,1,1]
    
    #EQUIVALENT INTERVAL ZOOMSTARS (for interval without extra span)
#     zoomstar_conf=[0,1,1,1]

    #COLOR INTENSITY ZOOMSTARS
#     zoomstar_conf=[2,0,2,1]
    
    #single  zoomstar
    object_nr=0
    star.drawZoomStar(aList2,nrf,nre,objects,titles,zoomstar_conf,Fmin,Fmax,object_nr,hues=hues,labels=cat,quantiles=quantiles)
    #all zoomstars
#     cols=5 #how many zoomstars is a row
#     star.drawZoomStar(aList2,nrf,nre,objects,titles,zoomstar_conf,Fmin,Fmax,cols=cols,hues=hues,labels=cat,quantiles=quantiles)
    
    
#SCATTER PLOT OF PCA
#     D=[]
#     for i in range(nre):
#         abi=[]
#         for j in range(nrf):
#             abi.append(aList2[i].getHistogram(j).get_median())
#         D.append(abi)
#     #PERFORM PCA AND GET POINTS
#     P=cp.getPCAPoints(D,nre,nrf,titles,objects,type)  
#     star.drawScatterPlot(aList2,nrf,nre,objects,titles,type,Fmin,Fmax,P,quantiles,hues=hues,labels=cat)


#SHAPE ENCODING
#     new_order=[x for x in range(nre)] #for reordering objects
#     se.drawShapeCoding(aList2,objects,titles,bins,new_order)
   
   
#DENDROGRAM DRAWING
#fs is for feature selection
#     fs=[1 for x in range(nrf)] #all features included
#     diss=MHCC(aList2,nre,nrf,objects,quantiles,fs=fs)
#     drawDendowithDiss(diss,objects) 
    
    
if __name__ == '__main__':
    cat=[]
    bins=[]
    Fmin=[]
    Fmax=[]
    
#OILS DATASET
#     objects=['Linsead','Perilla','Cotton','Sesame','Camellia','Olive','Beef','Hog']
#     titles = ['Specific Gravity','Freezing Point','Iodine Value','Saponification value','Major Fatty Acids']
#     type=[0,0,0,0,1]
#     X = np.loadtxt("data/oils.txt", dtype='str', delimiter='\n')
#     cat=[[],[],[],[],["L", "Ln", "O", "P", "M","S","A","C","Lu"]]
#     bins=[10,10,10,10,9]
#     norm_mode=0


#HARDWOOD DATASET
    objects=['ACER_EAST','ACER_WEST','ALNUS_EAST','ALNUS_WEST','FRAXINUS_EAST','FRAXINUS_WEST','JUGLANS_EAST','JUGLANS_WEST','QUERCUS_EAST','QUERCUS_WEST']
    titles=['ANNT','JANT','JULT','ANNP','JANP','JULP','GDC5','MITM']
    type=[0,0,0,0,0,0,0,0,0]
    X = np.loadtxt("data/hardwood.txt", dtype='str', delimiter='\n')
    norm_mode=0

#STATES TEMPERATURE DATASET
#     objects=['Alabama','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New_Hampshire','New_Jersey','New_Mexico','New_York','North_Carolina','North_Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode_Island','South_Carolina','South_Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West_Virginia','Wisconsin','Wyoming']
#     titles=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
#     type=[0,0,0,0,0,0,0,0,0,0,0,0]
#     X = np.loadtxt("data/states.txt", dtype='str', delimiter='\n')
#     norm_mode=1

#PORTUGAL TIMES DATASET
#     objects=['M / 25_34/WorkDay','M / 55_64/WorkDay','F / 35_54/WorkDay','M / 35_54/WorkDay','M / 55_64/Weekend','F / 55_64/Weekend','F / 65 or more/WorkDay','F / 25_34/WorkDay','M / 65 or more/WorkDay','F / 55_64/WorkDay','F / 35_54/Weekend','M / 35_54/Weekend','M / 15_24/Weekend','M / 65 or more/Weekend','F / 65 or more/Weekend','F / 15_24/WorkDay','M / 15_24/WorkDay','M / 25_34/Weekend','F / 25_34/Weekend','F / 15_24/Weekend']
#     titles=['Region','Diar','Educ','Status','Babies','Children','Adults','CPT','Econ_act','Occupation','Num_Hor','Hurried','Hurried_Often','Hurried_5years','Hurried_3years','Hurried_1year','Reduce','Work_Time','Private_Life_Time','Weekend_Time','Available_time','Fam_Type','Sleep','Eat','Personal_Hig','Prof_Act','Study','Prep_Food','Reparing_House','Clothes_Making_Caring','Gardening_TreatingAnimals','Construction_Repairs','Purchases','Children_Cares','Voluntary_work','Soc_Life','Sports','Games','Read','Television_Video','Route_to_from_work','Sex','Age','Day']
#     type=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1]
#     X = np.loadtxt("data/portugal.txt", dtype='str', delimiter='\n')
#     cat=[['RN','RC','RLVT','RA','Ralg','REA','REM'],['Th','Tu','Su','Mo','We','Fr','Sa'],['Primary','No r/w','Secondary','Higher'],['Married','Single','Widow','Divorvced'],['0','1','2','3','4'],['2','0','1','3','4','5','6'],['2','3','1','4','6','5','7','8','9','10'],['Employee','Housewife','Retired','Other Inactive','Student','Unemployed'],['Construction','Industry','Agriculture','Services','Production of electricity',' gas and water','Dont'],['Skilled workers',' craftsmen','Machine operations','Farmers and skilled agricultural','Middle management and technicians','Professionals and scientists','Services and sales','Administrative and related','Unskilled workers','Directors and executives','Military forces','Don t'],['40_45','45 our more','35_40','15_35','1_15','Don t'],['Yes','No'],['Freq','Sometimes','Everyday'],['The same','More hurried','Less hurried','Don t'],['The same','More hurried','Less hurried','Don t'],['The same','More hurried','Less hurried','Don t'],['Yes','No','Dont'],['Yes but rarely','Never','Yes everyday','Yes sometimes','Yes frequently','Don t'],['Yes sometimes','Yes frequently','Yes everyday','Yes but rarely','Never','Don t'],['Yes but rarely','Yes sometimes','Never','Yes frequently','Don t'],['Rarely','Never','Frequently','Sometimes','Everyday','Don t'],['Married with children','Another type of family','Married without children','Single','Single parent'],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],['F','M'],['15-24','25-34','35-54','55-64','65-'],['Weekend','Weekday']]
#     norm_mode=0

#CITY TEMPERATURE DATASET
#     objects=['Amsterdam','Athens','Bahrain','Bombay','Cairo','Calcutta','Colombo','Copenhagen','Dubai','Frankfurt','Geneva','Hong_Kong','Kuala_Lumpur','Lisbon','London','Madras','Madrid','Manila','Mauritius','Mexico_City','Moscow','Munich','Nairobi','New_Delhi','New_York','Paris','Rome','San_Francisco','Seoul','Singapore','Stockholm','Sydney','Tehran','Tokyo','Toronto','Vienna','Zurich']
#     titles=['jan','feb','mar','apr','may','jun','jul','aug','sept','oct','nov','dec']
#     type=[0,0,0,0,0,0,0,0,0,0,0,0]
#     X = np.loadtxt("data/city.txt", dtype='str', delimiter='\n')
#     norm_mode=0

#ENVIRONMENT DATASET
#     objects=["1241","1242","1441","1442","1641","1642","1741","2241","2242","2441","2442","2641","2642","2741"]
#     titles=["URBANICITY","INCOMELEVEL","EDUCATION","REGIONDEVELOPMENT","CONTROL","SATISFY","INDIVIDUAL","WELFARE","HUMAN","POLITICS","BURDEN ","NOISE ","NATURE ","SEASETC ","MULTI ","WATERWASTE ","VEHICLE"]
#     type=[1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#     X = np.loadtxt("data/environment.txt", dtype='str', delimiter='\n')
#     cat=[[6,4,5,1,3,2],[25,75,50,90,100],[1,3,5,6],[4,3,2,1],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#     Fmin=[0,0,0,0,-723.252 ,-570.567,-826.253,-1117.93,-879.714 ,-491.784,-1466.66,-579.987,-572.77,-747.455,-719.408,-960.767 ,-840.002]
#     Fmax=[6,5,4,4,637.963,855.139,817.586 ,576.222,867.43,767.897,651.622 ,926.595 ,692.682,575.099,552.675,482.79 ,1607.88 ]
#     norm_mode=0
    
    callMethod(X,objects,titles,type,cat,bins=bins,Fmin=Fmin,Fmax=Fmax,norm_mode=norm_mode)