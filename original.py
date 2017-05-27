#coding: utf-8

from sklearn.datasets import fetch_20newsgroups
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np

from sklearn.linear_model import SGDClassifier
from sklearn import metrics


categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']

#twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)
directory = 'release_1.0'
twenty_train = load_files(directory, description=None, load_content=True, shuffle=True, encoding='utf-8', decode_error='ignore', random_state=42)

#print "1"
#print(len(twenty_train.data))

#print "2"
#print("\n".join(twenty_train.data[0].split("\n")[:3]))

#print "3"
#print(twenty_train.target_names[twenty_train.target[0]])

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train.data)
#print "4"
#print X_train_counts.shape

# CountVectorizersuporta as contagens de n-gramas de palavras ou caracteres consecutivos.
# Uma vez instalado, o vectorizer construiu um dicionario de indices de recursos:
#print "5"
#print count_vect.vocabulary_.get(u'algorithm')
#O valor do indice de uma palavra no vocabulario esta ligada a sua frequencia no
# corpus de treinamento por completo.

#print "6"
#print X_train_counts

#Para evitar estes potenciais discrepancias, basta dividir o numero de ocorrencias
# de cada palavra em um documento pelo numero total de palavras no documento:
# esses novos recursos sao chamados tfpara o termo Frequencies.
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
#print "7"
#print X_train_tfidf.shape

clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)

docs_new = [
    'Update jQuery to v1.12.2.',
    'Ports 16d710217667879c6a79b3df25fd565fcc89cb34 to v3',
    'Update htmlmin options.',
    'Updated SRI hashes in docs for CDN links',
    'Make hound fail on violations',
    'Add Wall of Browser Bugs entry for #18228',
    'ci skip'
]
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, twenty_train.target_names[category]))

text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB()),
])

text_clf = text_clf.fit(twenty_train.data, twenty_train.target)


# AVALIANDO O DESEMPENHO
twenty_test = twenty_train
docs_test = twenty_test.data
predicted = text_clf.predict(docs_test)
print "Usando Naive Bayes, a precisão é de:"
print np.mean(predicted == twenty_test.target)

text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42)),
])

_ = text_clf.fit(twenty_train.data, twenty_train.target)
predicted = text_clf.predict(docs_test)
print "Usando SGDClassifier, a precisão é de:"
print np.mean(predicted == twenty_test.target)

print(metrics.classification_report(twenty_test.target, predicted, target_names=twenty_test.target_names))
print(metrics.confusion_matrix(twenty_test.target, predicted))