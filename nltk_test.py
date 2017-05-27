from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re

porter = PorterStemmer()
stop = set(stopwords.words('english'))
sentence = "this is not a foo no bar sentence https://www.google.com analysis the running"
sentence = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', sentence)
last_is_neg = ''
for word in sentence.lower().split():
    if word == 'not' or word == 'no':
        last_is_neg = word
    if word not in stop:
        word = porter.stem(word)
        if last_is_neg != '':
            word = last_is_neg + '_' + word
            last_is_neg = ''
        print word
