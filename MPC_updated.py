#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 10:23:19 2018

@author: shreeyeshmenon
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import re

cap_dic=["international capital market", "international market", "global financial condition", "international financial market","global market","global economic conditions","global economic environment","foreign investment","international financial environment","global financial environment","portfolio","foreign capital"]
out_dic=["output", "economic activity", "employment", "economic growth", "production", "domestic demand", "domestic activity","labor market","labour market"]

path='/Users/shreeyeshmenon/Desktop/MPC_Analysis/MPC Minutes/Canada/docs/'
folder=os.listdir(path)
w=open(path+"results.txt",'w')
for file in folder:
    cap_count=0;
    out_count=0;
    filepath=path+str(file)
    f=open(filepath,'r',encoding="latin-1")
    text_str=f.read()
    text_str=text_str.lower()
    for word in cap_dic:
        cap_count=cap_count+text_str.count(word)
    for word in out_dic: 
        out_count=out_count+text_str.count(word)
    tot_count=text_str.count(" ")
    line=file[:-4]+"\t"+str(cap_count)+"\t"+str(out_count)+"\t"+str(tot_count)+"\n"
    print(line)
        
    
