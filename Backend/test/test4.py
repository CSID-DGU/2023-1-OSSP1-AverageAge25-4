import gensim

corpus = [
    ['I', 'love', 'coding'],
    ['Machine', 'learning', 'is', 'fascinating'],
    ['Python', 'is', 'popular', 'for', 'data', 'science'],
    # Add more sentences here...
]

model = gensim.models.Word2Vec(sentences=corpus, size=100, window=5, min_count=1, workers=4)

model.save("trained_model.bin")

model1 = gensim.models.Word2Vec.load("trained_model.bin")

# Additional corpus to append
additional_corpus = [
    ['He', 'plays', 'guitar'],
    ['Mother', 'love', 'traveling','Father'],
    # Add more sentences here...
]

# Update the vocabulary with the additional corpus
model1.build_vocab(additional_corpus, update=True)

# Train the model with the updated corpus
model1.train(additional_corpus, total_examples=model.corpus_count, epochs=model.epochs)

# Save the updated model
model1.save("updated2_model.bin")
model2 = gensim.models.Word2Vec.load("updated2_model.bin")

a = model2.wv.most_similar("Father")

print(a)