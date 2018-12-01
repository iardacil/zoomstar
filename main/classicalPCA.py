'''
Class for performing PCA
'''

from sklearn.decomposition import PCA as sklearnPCA
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import scale
import matplotlib.patches as patches
import matplotlib.lines as lines    


def getPCAPoints(D,nre,nrf,titles,objects,type):
    return mainMethod(D,nre,nrf,titles,objects,type,1)

#mode=0: draw graph
#mode=1: return center points
def mainMethod(D,nre,nrf,titles,objects,type,mode=0):

    n_samples = nre
    n_features = nrf
    n=objects

    
    
    # P = np.loadtxt("points.txt", dtype='d', delimiter=',')
    # X=np.append(D, P, axis=0)
    X=D
    sd=np.std(X, axis=0)
    mu2 = np.mean(X, axis=0)
    # pointsN-=mu2
    # pointsN/=sd
    # X_std = StandardScaler().fit_transform(X)
    
    X=scale(X)
    # print(X)
    # P-=mu2
    # P/=sd
    D-=mu2
    D/=sd


    
    
    pca = sklearnPCA(n_components=n_features)
    newX = pca.fit_transform(X)
    # W=pca.transform(P)
    D2=pca.transform(D)
    print(pca.components_)
    
    if(mode==0):
        plot_results(X,pca,newX,n_samples,n_features,n)
        plt.savefig('graphs/classical.png')
        plt.show()
    elif(mode==1):
        res=[]
        for j in range(2):
            abi=[]
            for i in range(nre):
                abi.append(newX[i][j])
            res.append(abi)
        return res

def plot_results(X_scaled, pca,newX,n_samples,n_features,n,ncomp=2):
    conf=2   
    fig, ax = plt.subplots(2, 2, figsize=(16*conf, 10*conf))

    imp1=0
    imp2=2
    pperelem=1
    
##original
    ax[0, 0].scatter(X_scaled[:,imp1],X_scaled[:,imp2])
#     ax[0, 0].scatter(P[:,imp1],P[:,imp2])
#     for i in range(0,n_samples):
#         len1=P[i*2,imp1]
#         len2=P[i*2,imp2]
#         len3=P[i*2+1,imp1]
#         len4=P[i*2+1,imp2]
# #         print(len1)
# #         print(len2)
#         ax[0, 0].add_patch(
#         patches.Rectangle(
#             (len1, len2),
#             (len3-len1),
#             (len4-len2),
#             fill=False      # remove background
#             )
#         )
        
    ax[0, 1].scatter(newX[:,0],newX[:,1])
#     ax[0, 1].scatter(W[:,imp1],W[:,imp2])
# #      PCA
#     for i in range(0,n_samples):
#         len1=W[i*2,imp1]
#         len2=W[i*2,imp2]
#         len3=W[i*2+1,imp1]
#         len4=W[i*2+1,imp2]
#         ax[0, 1].add_patch(
#         patches.Rectangle(
#             (len1, len2),
#             (len3-len1),
#             (len4-len2),
#             fill=False      # remove background
#             )
#         )
#      
    for i, txt in enumerate(n):
        ax[0, 0].annotate(txt, (X_scaled[i*pperelem,imp1],X_scaled[i*pperelem,imp2]))
#         ax[1, 0].annotate(txt, (Y[i*pperelem,imp1],Y[i*pperelem,imp2]))   
        ax[0, 1].annotate(txt, (newX[i*pperelem,0],newX[i*pperelem,1]))   
     
    index = np.arange(2, n_features+2)
    bar_width=1/n_features
 
#     print(pca.components_)


#     l1 = lines.Line2D([pca.components_[0,0]*4, pca.components_[1,0]*4], [pca.components_[0,0]*4, pca.components_[1,0]*4], transform=ax[0, 0].transFigure, figure=ax[0, 0])                              
#     l2 = lines.Line2D([pca.components_[0,1]*4, pca.components_[1,1]*4], [pca.components_[0,1]*4, pca.components_[1,1]*4], transform=ax[0, 0].transFigure, figure=ax[0, 0]) 
#
   
#     ax[0, 0].lines.extend([l1, l2])
    
#     l1 = lines.Line2D([pca.components_[0,0]*4, pca.components_[1,0]*4], [pca.components_[0,0]*4, pca.components_[1,0]*4],
#                     lw=1, color='black', axes=ax[0, 0])   
    l2 = lines.Line2D([pca.components_[0,0]*-8,pca.components_[0,0]*8],[pca.components_[1,0]*-8,pca.components_[1,0]*8],
                    lw=1, color='black', axes=ax[0, 0])
    l1 = lines.Line2D([pca.components_[0,1]*-8,pca.components_[0,1]*8],[pca.components_[1,1]*-8,pca.components_[1,1]*8],
                    lw=1, color='black', axes=ax[0, 0])
    l3 = lines.Line2D([-8,8],[0,0],
                    lw=1, color='grey', axes=ax[0, 0])
    l4 = lines.Line2D([0,0],[-4,4],
                    lw=1, color='grey', axes=ax[0, 0])

   
#     ax[0, 0].add_line(l1)
    ax[0, 0].add_line(l1)
    ax[0, 0].add_line(l2)
    ax[0, 0].add_line(l3)
    ax[0, 0].add_line(l4)
    
    l3 = lines.Line2D([-8,8],[0,0],
                    lw=1, color='black', axes=ax[0, 1])
    l4 = lines.Line2D([0,0],[-4,4],
                    lw=1, color='black', axes=ax[0, 1])
    ax[0, 1].add_line(l3)
    ax[0, 1].add_line(l4)
#     plt.show()

#     print(pca.explained_variance_)
    
#     ax[0, 1].plot(np.arange(1, ncomp+1), pca.explained_variance_ratio_)
    rect =ax[1, 1].bar(index, pca.explained_variance_ratio_, bar_width,color='b')
    ax[1, 1].set_xlim(1, n_features+2)
    ax[1, 1].set_ylim(0, None)
    ax[0, 1].set_ylim([-4,4])
    ax[0, 1].set_xlim([-4,4])
    ax[0, 0].set_ylim([-2,2])
    ax[0, 0].set_xlim([-2,2])
    ax[1, 0].set_ylim([-2,2])
    ax[1, 0].set_xlim([-2,2])
    
    labels=['PC %s' %i for i in range(1,(n_features+1))]
    plt.xticks(index, labels)
    
         
    def autolabel(rects):
        i=0
        for rect in rects:
            height = rect.get_height()
            ax[1, 1].text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%.2f' % pca.explained_variance_ratio_[i],
                    ha='center', va='bottom')
            i=i+1
  
    autolabel(rect)
 
 
#     ax[0, 0].xaxis.set_major_formatter(plt.NullFormatter())
#     ax[0, 1].xaxis.set_major_formatter(plt.NullFormatter())
#     ax[1, 1].xaxis.set_major_formatter(plt.NullFormatter())
#     ax[1, 0].xaxis.set_major_formatter(plt.NullFormatter())
     
    ax[0, 0].set_title('Input Data')
    ax[0, 1].set_title('First {0} Principal Vectors'.format(ncomp))
    ax[1, 0].set_title('Reconstructed Data ({0} components)'.format(ncomp))
    ax[1, 1].set_title('PCA variance ratio')
    ax[1, 1].set_xlabel('principal vector')
    ax[1, 1].set_ylabel('proportion of total variance')
     
    fig.suptitle('PCA', fontsize=16)

