from gensim.models import KeyedVectors


# Load the model from the bin file
wv = KeyedVectors.load_word2vec_format('ko.bin', binary=True, encoding='utf-8')

# Load the word vectors from the tsv file
wv.init_sims(replace=True)
wv.vocab.clear()
with open('ko.tsv', 'r', encoding='utf-8') as f:
    for line in f:
        word, *vec = line.rstrip().split('\t')
        vec = [float(v) for v in vec]
        wv.add_vector(word, vec)

# Get the most similar words
similar_words = wv.most_similar('단어')
print(similar_words)