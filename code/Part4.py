# Janani Kalyanam
# jkalyana@ucsd.edu


import os, sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing

'''
    Vizualizations; some quick ideas.
    
    1)  Use topic modeling to summarize the different types of non-profits based on
        their mission.  I already did this in Part3.py

    2)  Sort and plot the grossReceipts to see what is the distribution of the
        money that the non-profits get.

    3)  Scatter-plots: grossReceipts-vs-numEmployees
                       grossReceipts-vs-numVolunteers
                       grossReceipts-vs-Expenses
                       grossReceipts-vs-Revenue
        Is there a clear correlation?

'''

def makePlots():

    # Get the data, and get the needed columns
    # This part is copied from Part3.py
    D = np.genfromtxt('features_numeric.txt',dtype='float',delimiter=',',usecols=range(35)[1:]);
    M = D[~np.isnan(D[:,[0,3,4,15,25]]).any(axis=1)];
    M = M[:,[0,3,4,15,25]]; # Now M has no empty elements
    M_scaled = preprocessing.scale(M); # Make the co-variates 0-mean, unit variance

    # PLOT_GROSS_RECEIPTS_1
    # Just plot the gross-receipts
    plt.plot(sorted(M[:,0],reverse=True))
    plt.title('Gross Receipts');
    plt.ylabel('Amount in Dollars');
    plt.show()
    
    # PLOT_GROSS_RECEIPTS_1 seemed to follow a "power law".  Many non-profits with low
    # gross-receipts, and very few with extremely high ones.  So, lets do the same
    # plot in a log-log scale to confirm.  (Must get a linear plot in the middle)
    plt.plot(np.log(range(M.shape[0]+1)[1:][:-1]),np.log(sorted(sorted(M[:,0]),reverse=True)[:-1]))
    plt.title('Gross Receipts; log-log scale');

    # OK -- Maybe it's better to plot the CDF. Each point (x,y) in the plot
    # below says that there are y number of non-profits which receive at least
    # a gross receipt of $x
    O = np.ones((M[:,0].shape[0],)); # just a vector of ones
    plt.plot(sorted(M[:,0]),np.cumsum(O));
    plt.xlabel('Gross receipts (sorted)')
    plt.ylabel('#-non-profits');
    plt.title('CDF plot')
    plt.show();
    # Yes, there's definitely a "power law" here.  

    ######### SCATTER PLOTS ###############

    # I tried scatter plots between different co-variates.
    # However, I included the code only for the ones that I thought were interesting.
    # (1) gross_receipts vs num_employees (visually, there didn't seem to be a clear correlation)
    # (2) gross_receipts vs num_volunteers (visually, there didn't seem to be a clear correlation)
    # (3) gross_receipts vs revenue (visually, there was a correlation; but that's maybe expected?
    #       Because gross_receipts = revenue - expenditure)
    # (4) revenue vs expenditure (visually, there was a clear positive correlation.
    #   Organizations that make more also spend more.
    #   THe code for this is below
    plt.scatter(M[:,3],M[:,4]);
    plt.xlabel('revenue')
    plt.ylabel('expenditure')
    plt.show()

    # (5) gross_receipts vs expenditure (visually, there was again a positive correlation;
    #  Organizations that spend more - perhaps on fund raising events, also end up making
    # a net "profit").
    plt.scatter(M[:,0],M[:,4])
    plt.xlabel('gross-receipts')
    plt.ylabel('expenditure')
    plt.show()
    

if __name__ == '__main__':
    makePlots();
