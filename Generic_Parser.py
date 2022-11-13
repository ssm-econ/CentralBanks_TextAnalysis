"""
Program to provide generic parsing for all files in a user-specified directory.
The program assumes the input files have been scrubbed,
  i.e., HTML, ASCII-encoded binary, and any other embedded document structures that are not
  intended to be analyzed have been deleted from the file.

Dependencies:
    Python:  MOD_Load_MasterDictionary_v2020.py
    Data:    LoughranMcDonald_MasterDictionary_XXXX.csv

The program outputs:
   1.  File name
   2.  File size (in bytes)
   3.  Number of words (based on LM_MasterDictionary
   4.  Proportion of positive words (use with care - see LM, JAR 2016)
   5.  Proportion of negative words
   6.  Proportion of uncertainty words
   7.  Proportion of litigious words
   8.  Proportion of modal-weak words
   9.  Proportion of modal-moderate words
  10.  Proportion of modal-strong words
  11.  Proportion of constraining words (see Bodnaruk, Loughran and McDonald, JFQA 2015)
  12.  Number of alphanumeric characters (a-z, A-Z)
  13.  Number of digits (0-9)
  14.  Number of numbers (collections of digits)
  15.  Average number of syllables
  16.  Average word length
  17.  Vocabulary (see Loughran-McDonald, JF, 2015)

  ND-SRAF
  McDonald 201606 : updated 201803; 202107
"""

import csv
import glob
import re
import string
import sys
import datetime as dt
sys.path.append(r'/Users/shreeyeshmenon/Desktop/MPC_Analysis')  # Modify to identify path for custom modules
import MOD_Load_MasterDictionary_v2020 as LM
import pandas as pd

# User defined directory for files to be parsed
TARGET_FILES = r'/Users/shreeyeshmenon/Desktop/MPC_Analysis/MPC Minutes/South Africa_Analysis/*.*'
# User defined file pointer to LM dictionary
MASTER_DICTIONARY_FILE = r'/Users/shreeyeshmenon/Desktop/MPC_Analysis/' + \
                         r'LoughranMcDonald_MasterDictionary_2020.csv'
# User defined output file
OUTPUT_FILE = r'/Users/shreeyeshmenon/Desktop/MPC_Analysis/SouthAfrica.txt'
# Setup output
OUTPUT_FIELDS = ['date', 'file size', 'number of words', '% negative', '% positive',
                 '% uncertainty', '% litigious', '% strong modal', '% weak modal',
                 '% constraining', '# of alphabetic', '# of digits',
                 '# of numbers', 'avg # of syllables per word', 'average word length', 'vocabulary']

lm_dictionary = LM.load_masterdictionary(MASTER_DICTIONARY_FILE, print_flag=True)



f_out = open(OUTPUT_FILE, 'w')
database=pd.DataFrame()

file_list = glob.glob(TARGET_FILES)
n_files = 0


def get_data(doc):

    vdictionary = dict()
    _odata = [0] * 16
    total_syllables = 0
    word_length = 0
    
    tokens = re.findall('\w+', doc)  # Note that \w+ splits hyphenated words
    for token in tokens:
        if not token.isdigit() and len(token) > 1 and token in lm_dictionary:
            _odata[2] += 1  # word count
            word_length += len(token)
            if token not in vdictionary:
                vdictionary[token] = 1
            if lm_dictionary[token].negative: _odata[3] += 1
            if lm_dictionary[token].positive: _odata[4] += 1
            if lm_dictionary[token].uncertainty: _odata[5] += 1
            if lm_dictionary[token].litigious: _odata[6] += 1
            if lm_dictionary[token].strong_modal: _odata[7] += 1
            if lm_dictionary[token].weak_modal: _odata[8] += 1
            if lm_dictionary[token].constraining: _odata[9] += 1
            total_syllables += lm_dictionary[token].syllables

    _odata[10] = len(re.findall('[A-Z]', doc))
    _odata[11] = len(re.findall('[0-9]', doc))
    # drop punctuation within numbers for number count
    doc = re.sub('(?!=[0-9])(\.|,)(?=[0-9])', '', doc)
    doc = doc.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    _odata[12] = len(re.findall(r'\b[-+\(]?[$€£]?[-+(]?\d+\)?\b', doc))
    _odata[13] = total_syllables / _odata[2]
    _odata[14] = word_length / _odata[2]
    _odata[15] = len(vdictionary)
    
    # Convert counts to %
    for i in range(3, 10 + 1):
        _odata[i] = (_odata[i] / _odata[2]) * 100
    # Vocabulary
        
    return _odata



for file in file_list:
    n_files += 1
    print(f'{n_files:,} : {file}')
    with open(file, 'r', encoding='UTF-8', errors='ignore') as f_in:
        doc = f_in.read()
    doc = re.sub('(May|MAY)', ' ', doc)  # drop all May month references
    doc = doc.upper()  # for this parse caps aren't informative so shift
    output_data = get_data(doc)
    output_data[0] = pd.to_datetime(file[-11:-4],format="%b%Y")
    output_data[1] = len(doc)
    output_data=pd.Series(output_data)
    database=database.append(output_data.T,ignore_index=True)
        
database.columns=OUTPUT_FIELDS
database.to_csv('/Users/shreeyeshmenon/Desktop/MPC_Analysis/SouthAfrica.csv')



if __name__ == '__main__':
    start = dt.datetime.now()
    print(f'\n\n{start.strftime("%c")}\nPROGRAM NAME: {sys.argv[0]}\n')
    database=main()
    print(f'\n\nRuntime: {(dt.datetime.now()-start)}')
    print(f'\nNormal termination.\n{dt.datetime.now().strftime("%c")}\n')
