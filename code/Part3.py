# Janani Kalyanam
# May 11, 2017

import os, sys
import numpy as np
import scipy as sp
from sklearn import preprocessing
import sklearn.mixture
import operator

def applyModelNumerical():
    '''
        TERMINOLOGY:

        1. "data point" refers to the features extracted from a single XML file.
        2. "data point with missing covariates" means that the XML file had empty fields for some
        of the features I was interested in.

        MY IDEA:

        After the feature extraction in part-2, I found that many data points have missing co-variates :(
        In this analysis, I chose to skip the data points that have missing co-variates. 

        That said, I wanted to retain as many data points as possible.  Which means, I have to be
        careful about the co-variates (or the columns) I choose to analyze.  They must be both
        dense enough & also "useful" (or) interpretable by me.  

        So, I tried (manually) some combination of columns based on how empty they were, and based on whether
        I could interpret the meaning of the column.  From this manual experimentation, I 
        chose the following 5 features: gross-receipt, employee-count, volunteer-count, TotRev, TotExpenses.
        This resulted in ~ 300 data points (from a total of 1000 that I downloaded).

        I plan to go the unsupervised route for now.  Based on these features, I want to cluster the data
        and see what types of organizations fall under the same cluster.  This will give insights about the
        general landscape of what types of non-profits are out there.  

        I want apply Gaussian Mixture Model (as an unsupervised model) on the 300 data points.  Once we learn the GMM model,
        we can maybe see what type of data is grouped together.  (REMARK: Think of GMM as a "sophisticated" version
        of k-means clustering.  A GMM is a generalization of k-means clustering; a GMM with identity covariance
        reduces to k-means.)

    '''
    # Load numeric data into np matrix;
    D = np.genfromtxt('features_numeric.txt',dtype='float',delimiter=',',usecols=range(35)[1:]);

    # Skip the rows with missing data.  I choose specific features to do analysis.
    # My features are gross-receipt[0], employee-ct[3], volunteer-ct[4], TotRev[15], TotExpenses[25]

    # Obtain numpy array with no empty elements.
    M = D[~np.isnan(D[:,[0,3,4,15,25]]).any(axis=1)];
    M = M[:,[0,3,4,15,25]]; # Now M has no empty elements

    M_scaled = preprocessing.scale(M); # Make the co-variates 0-mean, unit variance
    
    # CREATING GMM INSTANCE
    # For this I would crossvalidate over n_components and covariance_type
    # and find the model that gives the best likelihood score
    Likelihood_score = []; # Store the likelihood score, and pick the model that yields best score
    for n_comps in range(8)[1:]:
        for t in ['diag','full']:
            GMM_instance = sklearn.mixture.GMM(n_components = n_comps, covariance_type = t, );
            myFit = GMM_instance.fit(M_scaled)
            Likelihood_score.append((t,n_comps,GMM_instance.bic(M_scaled)));
            print(t + ' ' + str(n_comps) + ' ' + str(GMM_instance.bic(M_scaled)));

    best = sorted(Likelihood_score, key = lambda x: x[-1])[0]; # Pick the parameters for best model

    # Train on best model
    GMM_instance = sklearn.mixture.GMM(n_components = best[1], covariance_type = best[0]);
    GMM_instance.fit(M_scaled); 
    
    # Predict.
    cluster_labels = GMM_instance.predict(M_scaled);

    print(cluster_labels)

    # REMARK:  For x-validation, I wouldn't necessarily choose the "best" model.  I'll choose the one
    # beyond which there are not significant increments in likelihood scores.

def applyModelTextual():
    
    '''
        I plan to use topic modeling on the mission statements and interpret the topics.

        As a result of running the code in this module, below are my conclusions:

        I ran topic modeling with K = 3 (I just chose the number "3".  I also tried it with other
        larger numbers, like 5,7,9.  But, the topics began to get repeated - possibly means than a lower
        K would suffice).  

        I used the "Biterm Topic Model" which specializes
        in finding topics from short text lengths.  I cloned the code form the repo here:
        https://github.com/xiaohuiyan/BTM

        Some of the top words in each topic are:
        TOPIC1 = provide, people, organization, financial, area, opportunity, support
        TOPIC2 = public, education, school, student, organization, achievement, activities
        TOPIC3 = support, health, care, communities, funds, social, economic, people, access

        I see a clear separation of themes here.

        TOPIC1 is about providing financial support to (possibly low income?) people.
        TOPIC2 is about non profits for education
        TOPIC3 is about non profits for health care, maybe espcially for people with lower social
                and economic conditions.
        
    '''

    # get the descriptions, remove punctuation (I focus only on periods here), remove stop words
    desc = map(lambda x: map(lambda y: y.lower(), x.strip().split(',')[-1].split(' ')), open('features_nonNumeric.txt','r').readlines())
    desc = map(lambda y: map(lambda x: x.replace('.',''), y), desc);
    stopwords = map(lambda x: x.strip(), open('stopwords.txt','r').readlines());
    desc = map(lambda x: list(set(x).difference(set(stopwords))), desc)


    ######## create the vocab
    vocab = dict();   
    for each_desc in desc:
        for each_word in each_desc:
            if each_word == '':
                continue;
            #print each
            if each_word in vocab.keys():
                vocab[each_word] += 1;
            else:
                vocab[each_word] = 1;

    ####### write the vocab in a file
    fout_vocab = open('vocab.txt','w');
    vocab_sorted = sorted(vocab.items(), key = operator.itemgetter(1),reverse=True);

    i = 0;
    for each in vocab_sorted:
        fout_vocab.write(str(i) + '\t' + str(each[0]) + '\n')# + ' ' + str(each[1]) + '\n');
        i += 1;
    fout_vocab.close()    
    
    ######## Create Input according to topic model format
    fout_input = open('topic_model_input.txt','w');
    vocab_list = map(lambda x: x[0], vocab_sorted);
    for each_desc in desc:
        input_line = '';
        for each_word in each_desc:
            if each_word == '':
                continue;
            if(each_word in vocab_list):
                input_line += str(vocab_list.index(each_word)) + ' ';
        if(input_line == ''):
            continue;
        fout_input.write(input_line + '\n');

    #### Now run the topic model.
    #### I installed the "Biterm topic model" by Yan et al (presented at WWW 2013).
    #### This topic model specializes in extracting topics from short texts.
    
    # example run
    # /mnt/spare/users/janani/Research/Ebola/btm-v0.3/batch/btm est 3 1421 1 0.01 100 10 topic_model_input.txt out/
    # /mnt/spare/users/janani/Research/Ebola/btm-v0.3/batch/btm inf sum_b 3 topic_model_input.txt out/
    
            
if __name__ == '__main__':

   #applyModelNumerical(); 
    applyModelTextual()
