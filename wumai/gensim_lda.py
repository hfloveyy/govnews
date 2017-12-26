from gensim.corpora import Dictionary
from gensim.models import LdaModel

train_set = []

def load_data(path = 'cut.txt'):
    with open(path,'r') as f:
        for line in f:
            train_set.append(line.split())


load_data()

#print(train_set)

# 构建训练语料
dictionary = Dictionary(train_set)
corpus = [ dictionary.doc2bow(text) for text in train_set]



# lda模型训练
lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=10)

#lda.print_topic(0)
for index, score in sorted(lda[corpus[0]], key=lambda tup: -1*tup[1]):
    print("Score: {}\t Topic: {}".format(score, lda.print_topic(index, 10)))