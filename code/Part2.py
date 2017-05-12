# Janani Kalyanam
# May 11, 2017
# Start time: 2:30 PM; End time: 4 PM

import os, sys
import json
import xml.etree.ElementTree as ET 
import glob

def featureExtraction_numeric():
    '''
        I spent some time looking at the IRS990 PDF on this link: https://www.irs.gov/pub/irs-pdf/f990.pdf
        to understand what information it could potentially have.

        This part extracts some numeric features.  

        Remark:  After the successful completion of this module, I learnt that most features are
        empty for most organization!  :( 

        Some other quick notes:

        (1) Gross receipts.  Important number.  This tells us how much the non-profit made
            that year.  An interesting problem would be to see what can most accurately predict
            gross receipt.

        (2) Extract simple numeric features like 
            the size of the non-profit (based on employees and volunteers), expenses, etc.


    '''

    list_of_files = glob.glob('../data/2017_forms/*');

    # I made a list of features which made sense to me.  These are all numeric features.
    fields = map(lambda x: x.strip(), open('numeric_tags.txt','r').readlines());

    # Each line in the output file will be the features for each non-profit.
    fout = open('features_numeric.txt','w');

    for f in list_of_files:
        print(f)
        tree = ET.parse(f);
        root = tree.getroot();

        # Reminder: root[1][0] is the Element "IRS990"

        # First write the unique ID of the non-profit (easy to backtrack during debugging);
        to_write = f.split('/')[-1];

        for field in fields:
            M = root[1][0].find(field);
            if(M == None):
                to_write = to_write + ',';
            else:
                to_write = to_write + ',' + str(M.text);


        fout.write(to_write + '\n');

    fout.close();

def featureExtraction_nonNumeric():



    list_of_files = glob.glob('../data/2017_forms/*');

    # Each line in the output file will be the features for each non-profit.
    fout = open('features_nonNumeric.txt','w');

    for f in list_of_files:
        print(f)
        tree = ET.parse(f);
        root = tree.getroot();

        # Reminder: root[1][0] is the Element "IRS990"

        # First write the unique ID of the non-profit (easy to backtrack during debugging);
        to_write = f.split('/')[-1];

        # Gross receipt amount
        M = root[1][0].find('{http://www.irs.gov/efile}GrossReceiptsAmt');
        if(M == None):
            to_write = to_write + ',';
        else:
            to_write = to_write + ',' + str(M.text);

        # STATE of non-profit.  Do non-profits in "richer" states have higher gross receipts? 
        M = root[1][0].find('{http://www.irs.gov/efile}USAddress');
        if(M == None):
            to_write = to_write + ',';
        else:
            M = M.find('{http://www.irs.gov/efile}StateAbbreviationCd');
            if(M == None):
                to_write = to_write + ',';
            else:
                to_write = to_write + ',' + str(M.text);

        # MISSION
        M = root[1][0].find('{http://www.irs.gov/efile}MissionDesc');
        
        if(M == None):
            to_write = to_write + ',';
        else:
            to_write = to_write + ',' + str(M.text);

        fout.write(to_write + '\n');

    fout.close();


if __name__ == '__main__':

    featureExtraction_numeric();
    #featureExtraction_nonNumeric();
