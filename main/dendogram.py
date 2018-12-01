'''
Class for drawing dendrograms based on dissimilarity matrix
@author: Kadri Umbleja
'''

import scipy as sp
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform



def drawDendowithDiss(diss,objects):
    

    diss=sp.array(diss)
    linkage_matrix = linkage(squareform(diss), "complete")
    dendrogram(linkage_matrix, labels=objects,leaf_rotation=90.,leaf_font_size=8.,color_threshold=0, above_threshold_color='black')
    plt.subplots_adjust(bottom=0.3)
    plt.savefig('graphs/dendo.png', format='png', dpi=300)
    plt.show()