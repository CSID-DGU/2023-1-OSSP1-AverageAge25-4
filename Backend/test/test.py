
from gensim.models.word2vec import Word2Vec

model0_path = '../model/Kkma_dataset.model'
def getSimKey(model_path, keyword, accuracy):
    model = Word2Vec.load(model_path)
    try:
        similar_words = model.wv.most_similar(keyword, topn=100)
        similar_words = [(word, score) for word, score in similar_words if score >= accuracy]
        return similar_words
    except KeyError:
        print(f"{keyword} is not in vocabulary")

        return []


print(getSimKey(model0_path, "수강신청", 0.8))
