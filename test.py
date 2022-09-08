import re
from sys import path
from pathlib import Path
import glob

import pandas as pd

from extraction.CleanText.CleanText import Cleaner
from extraction.ExtracText.ExtracText import Extract

file_list = glob.glob('CVs/*')
contents = []
title = []
Email = []
number = []
for filename in file_list:

        # text = pdf_extract_text (filename)
        text = Extract.extract_text(filename)
        texte = Cleaner.clean_text(text)
        contents.append(texte)
        email = (re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', str(text)))
        Email.append(' '.join([str(elem) for elem in email]))
        number.append(Extract.extract_number(text))
        # liste.append(text)
        title.append(Path(filename).stem)

data = pd.DataFrame(contents, index=None)
data['Candidates'] = pd.DataFrame(title)
data['Emails'] = pd.DataFrame(Email)
data['Phone_number'] = pd.DataFrame(number)
data['Resumes'] = pd.DataFrame(contents)

data = data.drop(columns=0, axis=0)

data.to_csv('data_test.csv')

df = pd.read_csv('data_test.csv')
df = df.drop(columns="Unnamed: 0", axis=0)
print(df)
