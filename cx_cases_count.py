import pandas as pd
import os
from collections import Counter
from pprint import pprint
import sys


def fileinfo(dataset):
    statuslist = []

    #allcases info
    for i in dataset["Status"]:
        statuslist.append(i)

    allcases = Counter(statuslist)
    pprint(allcases)

    #total parts cases in Que
    partscases = (statuslist.count("Parts Review") +
                  statuslist.count("TAG/CUSTOMER MISMATCH") +
                  statuslist.count("Complete Care"))

    print(f"""
    
    there are {partscases} in parts
    
    """)
    #filter out pend cases only
    dataset2 = dataset[dataset.Status == "Pending Supervisor"]

    listofbulk = []

    for i in dataset2["Dell Internal Notes"]:
        if "bulk" in i.lower():
            listofbulk.append(i)

    bulk = pprint(listofbulk)

    print (str(bulk) + '\n bulk list \n\n') 

def clean_file(filename):

    #file name 
    data = pd.read_csv(filename)

    #making a softcopy of data
    dataset = data.copy()

    ##cleaning up the dataset
    #replaceing empty / blank cells with "N/A" cells
    dataset.fillna("N/A", inplace=True)

    #colums removed from dataset
    removecolums = ['Start Timestamp', 'Locked By', 'Locked Timestamp']
    dataset = dataset.drop(columns=removecolums)

    #removing rows from dataset as per column name "Status"
    dataset = dataset[dataset.Status != "N/A"]
    fileinfo(dataset)

    #removing rows from dataset as per column name "Pending Supervisor" and "AlsoShipReview" 
    dataset = dataset[dataset.Status != "Pending Supervisor"]
    dataset = dataset[dataset.Status != "AlsoShipReview"]

    filecustumer = []


    for i in dataset["Service Provider Name"]:
        filecustumer.append(i)

    filecustumer.sort()
    custcasescount = str(pprint(Counter(filecustumer)))
    print (custcasescount)
    dataset = dataset.to_csv("finalfile.csv")

filename = sys.argv[-1]

clean_file(filename)


