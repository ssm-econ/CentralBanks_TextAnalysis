#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 19:34:48 2022

@author: shreeyeshmenon
"""

import PyPDF2
import os
import re

path='/Users/shreeyeshmenon/Desktop/MPC_Analysis/MPC Minutes/Korea'

os.chdir(path)

folder=os.listdir(path)
pattern='\([a-zA-Z]*\%[0-9]*\)'

arr=[]

for file in folder:
    filename=file
    datefield=re.search(pattern,filename)
    if datefield!=None:
        
        arr.append(datefield[0])

file=open('Minutes_of_the_Monetary_Policy_Committee_Meeting(March_2013).pdf','rb')

string='(April2019)'
datefield=re.search('\([a-zA-Z]*[0-9]*\)', )

pdfReader = PyPDF2.PdfFileReader(file)
 
# printing number of pages in pdf file
print(pdfReader.numPages)
 
# creating a page object
pageObj = pdfReader.getPage(1)
 
# extracting text from page
print(pageObj.extract_text())
 
# closing the pdf file object
pdfFileObj.close()