#!/usr/bin/env python
# coding: utf-8

# In[100]:


"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""


# In[101]:


import sys
from json import loads
from re import sub

columnSeparator = "|"

itemsSeen = set()
catsSeen = set()
bidsSeen = set()
personsSeen=set()
        
# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}


# In[102]:


"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'


# In[103]:


"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

    


# In[104]:


"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]


# In[105]:


"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)


# In[106]:


"""
escaping qutation marks
"""
def transformString(string):
    if string==None: return "\"NULL\""
    string= string.strip()
    
    quotation_line= "\""
    for s in string:
        quotation_line+=s
        if s=="\"": quotation_line+="\""
    
    quotation_line+="\""
    return quotation_line


# In[107]:


"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f, open('item.dat', 'a') as itemtb, open('category.dat','a') as categorytb, open('bidInfo.dat','a') as bidtb, open('person.dat','a') as persontb:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        global itemsSeen
        global catsSeen
        global bidsSeen
        global personsSeen

        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            #item table 
            itemstr= item['ItemID']+"|" +transformString(item['Name']) +"|"+ transformDollar(item['Currently'])+"|"
            if(not 'Buy_Price' in item.keys()): itemstr+="NULL"+"|"
            else: itemstr+=transformString(item['Buy_Price'])+"|"
                
            itemstr+=transformDollar(item['First_Bid'])+"|"+item['Number_of_Bids']+"|"
            itemstr+=transformDttm(item['Started'])+"|"+transformDttm(item['Ends'])+"|"
            itemstr+=transformString(item['Seller']['UserID'])+"|"+transformString(item['Description'])
            
            if(itemstr not in itemsSeen):
                itemsSeen.add(itemstr)
                itemstr+='\n'
                itemtb.write(itemstr)
            
            
            # category table 
            for c in item['Category']:
                catstr = item['ItemID']+"|"+transformString(c)
                if(catstr not in catsSeen):
                    catsSeen.add(catstr)
                    catstr = str(len(catsSeen))+"|"+catstr+"\n"
                    categorytb.write(catstr)
                
                
            # seller info > person 
            pstr=transformString(item['Seller']['UserID'])
            pstr+="|"+item['Seller']['Rating']+"|"
            
            if(pstr not in personsSeen):
                personsSeen.add(pstr)
                if(not 'Location' in item.keys()): pstr+= "\"NULL\""+"|"
                else: pstr+= transformString(item['Location'])+"|"

                if(not 'Country' in item.keys()): pstr+= "\"NULL\""+'\n'
                else: pstr+= transformString(item['Country'])+"\n"
                        
                persontb.write(pstr)
            
            
            
            # bid information table 
            # bidder - person 
            if(item['Bids']!=None):
                for b in item['Bids']:
                    # bid info
                    bstr= item['ItemID']+"|"+transformString(b['Bid']['Bidder']['UserID'])+"|"+transformDollar(b['Bid']['Amount']) +"|"+ transformDttm(b['Bid']['Time'])                  
                    if(bstr not in bidsSeen):
                        bidsSeen.add(bstr)
                        bstr = str(len(bidsSeen))+"|"+bstr+"\n"
                        bidtb.write(bstr)

                    # bidder
                    pstr= transformString(b['Bid']['Bidder']['UserID'])+"|"+b['Bid']['Bidder']['Rating']+"|"

                    
                    
                    
                    if(pstr not in personsSeen):
                        personsSeen.add(pstr)
                        
                        if(not 'Location' in b['Bid']['Bidder'].keys()): pstr+= 'NULL'+"|"
                        else: pstr+= transformString(b['Bid']['Bidder']['Location'])+"|"

                        if(not 'Country' in b['Bid']['Bidder'].keys()): pstr+= 'NULL'+'\n'
                        else: pstr+= transformString(b['Bid']['Bidder']['Country'])+"\n"
                        
                        persontb.write(pstr)
        
        itemtb.close()
        categorytb.close()
        bidtb.close()
        persontb.close()


# In[108]:


"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)
#     main([0,"items-0.json"])


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




