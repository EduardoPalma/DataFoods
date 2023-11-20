from nltk import PorterStemmer

stemmer = PorterStemmer()


def stemmer_porter(doc_):
    text_stemmer = [stemmer.stem(token.text) for token in doc_]
    return " ".join(text_stemmer)


def lemmatizer(doc_):
    text_lemma = [token.lemma_ for token in doc_]
    return " ".join(text_lemma)
