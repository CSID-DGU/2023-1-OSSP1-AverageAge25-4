import gensim
from gensim.models import Word2Vec

# Load the pre-trained model
model = gensim.models.Word2Vec.load('ko.bin')

# Additional corpus to append
additional_corpus = [
    ['수강신청', '학사', '개념'],
    ['인생', '우리', '하늘'],
    ['수강신청','낭만','인생'],
    ['수강신청','그래도','다시'],

    # Add more sentences here...
]

# Update the vocabulary with the additional corpus
model.build_vocab(additional_corpus, update=True)

# Train the model with the updated corpus
model.train(additional_corpus, total_examples=model.corpus_count, epochs=model.epochs)

# Save the updated model
model.save("ko_updated.bin")
