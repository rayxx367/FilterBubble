import os, re, nltk
import pandas as pd
import numpy as np
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from sklearn import preprocessing
from sklearn.utils import shuffle


def clean_data_from_text(text, remove_stopwords=True, stemming=True, extract_noun=False):
    """
    Take the raw text as input
    Return the text with cleaned texts appended in the new column "text"
    When extract_noun = True, a new column "noun" will also be appended, which consists of only nouns
    """

    # print "Cleaning the data"
    # Strip the whitespaces
    text = text.strip()
    # Remove all non-alphabet characters
    text = text.replace(r"[^a-zA-Z\s-]", r"")

    if (remove_stopwords == True) or (stemming == True) or (extract_noun == True):

        # Split the sentences into words
        # print "Tokenizing the words"
        text = nltk.word_tokenize(text)

        # if extract_noun == True:
        #     print "Tagging parts-of-speech"
        #     df["noun"] = df["title"] + df["description"]
        #     df["noun"] = df["noun"].apply(lambda x: [word[0] for word in nltk.pos_tag(x)
        #                                                 if word[1] in {"NN", "NNS", "NNP", "NNPS"}])
        #     df["noun"] = df["noun"].apply(lambda x: " ".join(x))

        if remove_stopwords == True:
            # Convert stop words to sets as sets have constant look-up time and thus faster
            stops = set(stopwords.words("english"))
            # print "Removing stop words"
            text = [word for word in text if word not in stops]

        if stemming == True:
            # Initialize the Snowball stemmer
            stemmer = SnowballStemmer("english")
            # print "Stemming English words"
            text = [stemmer.stem(word) for word in text]

        text = " ".join(text)

    return text


def clean_data(df, remove_stopwords=True, stemming=True, extract_noun=False):
    """
    Take the raw pandas dataframe as input
    Return the dataframe with cleaned texts appended in the new column "text"
    When extract_noun = True, a new column "noun" will also be appended, which consists of only nouns
    """

    print ("Shuffling the data")
    df = shuffle(df)

    print ("Cleaning the data")
    # Drop the unwanted columns and keep the rest for training
    df = df.drop(["Serial Number", "Unnamed: 7", "link", "Date", "Source"], axis=1)
    df.columns = map(str.lower, df.columns)

    # Strip the whitespaces
    for col in df.columns:
        df[col] = df[col].apply(str.strip)

    # Remove all non-alphabet characters
    df["title"] = df["title"].str.replace(r"[^a-zA-Z\s-]", r"")
    df["description"] = df["description"].str.replace(r"[^a-zA-Z\s-]", r"")

    if (remove_stopwords == True) or (stemming == True) or (extract_noun == True):

        # Split the sentences into words
        print ("Tokenizing the words")
        df["title"] = df["title"].apply(nltk.word_tokenize)
        df["description"] = df["description"].apply(nltk.word_tokenize)

        # Regular expression tokenizer. Disabled as performance is similar to nltk.word_tokenizer
        # pat = r"\b[a-z0-9_\-\.]+[a-z][a-z0-9_\-\.]+\b"
        # df["title"] = df["title"].apply(lambda x: nltk.regexp_tokenize(x, pat))
        # df["description"] = df["description"].apply(lambda x: nltk.regexp_tokenize(x, pat))

        # Combine news titles and content into one column
        df["text"] = df["title"] + df["description"]

        if extract_noun == True:
            print ("Tagging parts-of-speech")
            df["noun"] = df["title"] + df["description"]
            df["noun"] = df["noun"].apply(lambda x: [word[0] for word in nltk.pos_tag(x)
                                                        if word[1] in {"NN", "NNS", "NNP", "NNPS"}])
            df["noun"] = df["noun"].apply(lambda x: " ".join(x))

        if remove_stopwords == True:
            # Convert stop words to sets as sets have constant look-up time and thus faster
            stops = set(stopwords.words("english"))
            print ("Removing stop words")
            df["text"] = df["text"].apply(lambda x: [word for word in x if word not in stops])

        if stemming == True:
            # Initialize the Snowball stemmer
            stemmer = SnowballStemmer("english")
            print ("Stemming English words")
            df["text"] = df["text"].apply(lambda x: [stemmer.stem(word) for word in x])

            # Lemmatization is currently not applied
            # lemmatizer = WordNetLemmatizer()
            # df["text"] = df["text"].apply(lambda x: [lemmatizer.lemmatize(word) for word in x])

        df["text"] = df["text"].apply(lambda x: " ".join(x))

    else:
        df["text"] = df["title"] + " " + df["description"]

    return df
