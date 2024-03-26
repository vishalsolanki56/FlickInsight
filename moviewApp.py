# -*- coding: utf-8 -*-
"""MovieReviewApp.ipynb
Original file is located at
    https://colab.research.google.com/drive/1HtAc4I_pMKgcYahR6oXTrKflff9HMurJ
#Text Summarize (spacy)
"""
from review_scraper import scrape_movie_reviews
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from openai import OpenAI
import spacy
#from spellchecker import SpellChecker
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#from indexer import DictionaryIndex
import re
# Initializing the OpenAI client
client = OpenAI(api_key='---your openai API key---')


def textrank_summarize(text, ratio):
    print("TextRank Method Started");
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(sentences)
    values = cosine_similarity(X)

    scores = Counter()
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                scores[i] += values[i, j]

    top_sentences = [sentences[index] for index, score in scores.most_common(int(len(sentences) * ratio))]
    summary = ' '.join(top_sentences)
    print("TextRank Method Ended");
    return summary


def text_preprocess(text):
    print("Text Preprocess Method Started")
    # Remove newline characters
    text = re.sub(r'\n', ' ', text)

    # Limit total text length to 2200 words
    text = ' '.join(text.split()[:2500])

    print("Text Preprocess Method Ended")
    return text


def generate_summary(text):
    print("Generate Summary Method Started");
    prompt = text + "\n\n\n" + "Summarize the above text like you're giving a movie review, in 4-5 sentences and in simple language"
    completion = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=150,
        temperature=0.5,
        n=1
    )
    print("Generate Summary Method Ended");
    return completion.choices[0].text.strip()


"""#Sentiment Score (VADER)"""

def get_sentiment_score(text):
    print("Get Sentiment Score Method Started");
    # Initialize VADER sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Analyze sentiment
    sentiment_scores = analyzer.polarity_scores(text)

    # Extract the compound sentiment score
    compound_score = sentiment_scores['compound']

    # Map the compound score to a scale of 0 to 10
    sentiment_score_out_of_10 = (compound_score + 1) * 5
    print("Get Sentiment Score Method Eneded");
    return sentiment_score_out_of_10


# Function call

# scrape_movie_reviews("Killer of the Flower Moon")
#
# file_path = 'movie_review.txt'
# with open(file_path, 'r', encoding='utf-8') as file:
#     text = file.read()
#
# textrank_summary = textrank_summarize(text, 0.7)
#
# # Preprocess the text
# preprocessed_text = text_preprocess(textrank_summary)
#
# # Function call for summary and Sentiment Score
# summary = generate_summary(preprocessed_text)
# sentiment_score = get_sentiment_score(summary)
#
# print("\n Movie Review:", summary)
#print("\n Sentiment score out of 10:", sentiment_score)
