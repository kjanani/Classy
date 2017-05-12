# Janani Kalyanam
# Start time:  May 10, Wed, 1:30 PM
# End time: May 10, Wed, 2:30 PM.

# I answer part one using to two functions.

### Function #1 #############################
# dataDownload() --> primarily downloads data.

### Function #2 ############################
# loadParse() --> In this function, I show some examples of how I would
# load and parse the xml files.  This is my first time with xml format; 
# I used the ElementTree API in python to load (and parse) the files.
# I used an example xml file to play around with the python API.  I also looked at
# the actual PDF of an IRS990 form.  I went back and forth between the python API and
# the IRS990 PDF form to gain a basic understanding of what is present in these files.
# I show some examples in the function loadParse().

######################################################################################

import os, sys
import json
import xml.etree.ElementTree as ET

def dataDownload(): 
    '''
        (1) Download the list of 2016 forms (so, need index_2017.json).
        (2) Download some actual forms 2016.
    '''

    # (1)
    # Get 2017 list and save it in ../data/
    #os.system('wget --directory-prefix ../data/ \
    #        https://s3.amazonaws.com/irs-form-990/index_2017.json');

    json_data = open('../data/index_2017.json').read();
    data = json.loads(json_data);

    # (2)
    # Download first 100 IRS filings and save them in ../data/2017_forms
    # os.system('mkdir ../data/2017_forms');
    for i in range(1000):
        os.system('wget --directory-prefix ../data/2017_forms/ ' + data['Filings2017'][i]['URL']);


def loadParse():

    '''
        Some examples of loading and parsing the files.        
        I would use python's xml API.  This is my first time parsing XML, 
        but seems straightforward with python.
    '''
    
    # Load an example XML file
    tree = ET.parse('../data/2017_forms/201612449349301061_public.xml');
    root = tree.getroot();
    print('root: ' + root.tag);

    # It seems to me that a lot of the information about the non-profit is
    # in root[1][0].  That seems to be where the actual IRS990 begins.

    print('IRS990: ' + root[1][0].tag);

    # Print all children of IRS990
    for child in root[1][0]:
        print('IRS990 TAG: ' + child.tag);


if __name__ == '__main__':

    dataDownload();
    #loadParse();
