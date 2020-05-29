import pandas as pd
import numpy as np
import re
import dateparser
from collections import Counter
import matplotlib.pyplot as plt
plt.style.use('ggplot') 

def read_file(file):
    '''Reads Whatsapp text file into a list of strings''' 

    x = open(file,'r', encoding = 'utf-8') #Opens the text file into variable x but the variable cannot be explored yet
    y = x.read() #By now it becomes a huge chunk of string that we need to separate line by line
    content = y.splitlines() #The splitline method converts the chunk of string into a list of strings
    return content

chat = read_file('Power Bi Developers.txt')
print(len(chat))


join = [line for line in chat if  "joined using this" in line]
print(join)