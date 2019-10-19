# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 23:30:50 2019

@author: hitsu
"""

import os
directory = 'C:/Users/hitsu/Desktop/senior project/Prototype'

for filename in os.listdir(directory):
    if filename.endswith(".c"):
        path = (directory + '/' + filename)
        file = open(path,'r')
        file_data = file.read()
        print(type(file_data))