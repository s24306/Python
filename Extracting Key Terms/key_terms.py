import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter
import string

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

file = open("news.xml", "r").read()
soup = BeautifulSoup(file, "xml")
news_tags = soup.find_all('news')
stop_words = list(stopwords.words('english'))
stop_words += list(string.punctuation)
lemmatizer = WordNetLemmatizer()

headlines = []
tf_dataset = []

for i in news_tags:
    title = i.find("value", {"name": "head"})
    text = i.find("value", {"name": "text"})
    tokenized_text = word_tokenize(text.text.lower())
    lemmatized_text = [lemmatizer.lemmatize(w) for w in tokenized_text]
    filtered_text = [w for w in lemmatized_text if w not in stop_words]
    nouns = [w for w in filtered_text if nltk.pos_tag([w])[0][1] == 'NN']
    sorted_counter = sorted(Counter(nouns).items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    string_to_vectorize = ''
    for key in sorted_counter:
        string_to_vectorize += str(key[0] + ' ') * key[1]
    tf_dataset.append(string_to_vectorize)
    headlines.append(title.text + ":")

cv = CountVectorizer(tf_dataset, stop_words=stop_words)
word_count_vector = cv.fit_transform(tf_dataset)

tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
tfidf_transformer.fit(word_count_vector)

df_idf = pd.DataFrame(tfidf_transformer.idf_, index=cv.get_feature_names(), columns=["idf_weights"])
df_idf.sort_values(by=['idf_weights'])

count_vector = cv.transform(tf_dataset)
tf_idf_vector = tfidf_transformer.transform(count_vector)
feature_names = cv.get_feature_names()

for i in range(len(headlines)):
    print(headlines[i])
    df = pd.DataFrame(tf_idf_vector[i].T.todense(), index=feature_names, columns=["tfidf"])
    print(*(df.rename_axis('words').sort_values(by=["tfidf", "words"], ascending=False).index.tolist()[0:5]))
