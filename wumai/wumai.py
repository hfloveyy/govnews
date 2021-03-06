from time import time

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
#from sklearn.datasets import fetch_20newsgroups

n_samples = 2000
n_features = 1000

n_topics = 1

n_top_words = 20
cut = []

score = []
topics = []

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        for i in topic.argsort()[:-n_top_words - 1:-1]:
            score.append(str(topic[i]))
            topics.append(feature_names[i])
            #print("score:" + str(topic[i]))
            #print("topic:"+ feature_names[i])
            #print("\n")


        #print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))


def load_stop_words(path = 'stop_words.txt'):
    with open(path,'r',encoding="gbk") as f:
        for line in f:
            content = line.strip()
            stop_words.append(content)

def load_data(path = 'cut.txt'):
    with open(path,'r',encoding="gbk") as f:
        cut = f.readlines()
    return cut
# Load the 20 newsgroups dataset and vectorize it. We use a few heuristics
# to filter out useless terms early on: the posts are stripped of headers,
# footers and quoted replies, and common English words, words occurring in
# only one document or in at least 95% of the documents are removed.

print("Loading dataset...")
t0 = time()
#dataset = fetch_20newsgroups(shuffle=True, random_state=1,
#                             remove=('headers', 'footers', 'quotes'))

data_samples = load_data()

print("done in %0.3fs." % (time() - t0))

# Use tf-idf features for NMF.
print("Extracting tf-idf features for NMF...")
tfidf_vectorizer = TfidfVectorizer(max_df=2, min_df=0.95)
t0 = time()
tfidf = tfidf_vectorizer.fit_transform(data_samples)
print("done in %0.3fs." % (time() - t0))

# Use tf (raw term count) features for LDA.
print("Extracting tf features for LDA...")
tf_vectorizer = CountVectorizer(max_df=2, min_df=0.95, max_features=n_features)
t0 = time()
tf = tf_vectorizer.fit_transform(data_samples)
print("done in %0.3fs." % (time() - t0))

'''
# Fit the NMF model
print("Fitting the NMF model with tf-idf features,"
      "n_samples=%d and n_features=%d..."
      % (n_samples, n_features))
t0 = time()


nmf = NMF(n_components=n_topics, random_state=1, alpha=.1, l1_ratio=.5).fit(tfidf)

print("done in %0.3fs." % (time() - t0))

print("\nTopics in NMF model:")
tfidf_feature_names = tfidf_vectorizer.get_feature_names()
print_top_words(nmf, tfidf_feature_names, n_top_words)

print("Fitting LDA models with tf features, n_samples=%d and n_features=%d..."
      % (n_samples, n_features))


'''
#LDA模型
lda = LatentDirichletAllocation(n_components=n_topics, max_iter=5,
                                learning_method='online', learning_offset=50.,
                                random_state=0)
t0 = time()
lda.fit(tf)
print("done in %0.3fs." % (time() - t0))

print("\nTopics in LDA model:")
tf_feature_names = tf_vectorizer.get_feature_names()



print_top_words(lda, tf_feature_names, n_top_words)


print(topics)

import plotly.offline as py
import plotly.graph_objs as go



data = [go.Bar(
            x = topics,
            #x=['发展','中国','经济','企业','合作','改革','国家','创新','增长','建设','工作','推进','李克强','总理','服务','推动','我国','投资','加强','问题'],
            y = score
    )]
layout = go.Layout(
    xaxis=dict(tickangle=-45),
    barmode='group',
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='govnews.html')

