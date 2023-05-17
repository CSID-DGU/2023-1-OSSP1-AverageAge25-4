def trainModel():
    model = gensim.models.Word2Vec.load(mode_path)
    model.build_vocab(tokenized(), update=True)
    model.train(tokenized(), total_examples=model.corpus_count, epochs=model.epochs)
    model.save(model_path)
