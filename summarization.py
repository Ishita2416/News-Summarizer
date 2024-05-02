import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from collections import Counter
import nltk
nltk.download('punkt')

nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# To fetch news articles from a given URL
def fetch_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_text = ''
    for paragraph in soup.find_all('p'):
        article_text += paragraph.text
    return article_text

# Preprocess the text
def preprocess_text(text):
    sentences = sent_tokenize(text)
    tokens = []
    stop_words = set(stopwords.words('english'))
    for sentence in sentences:
        words = word_tokenize(sentence.lower())
        words = [word for word in words if word.isalnum() and word not in stop_words]
        tokens.extend(words)
    return tokens

# Perform POS tagging
def pos_tagging(tokens):
    tagged_tokens = pos_tag(tokens)
    return tagged_tokens

# Extract nouns and adjectives
def extract_nouns_adjectives(tagged_tokens):
    nouns_adjectives = [word for word, pos in tagged_tokens if pos.startswith('NN') or pos.startswith('JJ')]
    return nouns_adjectives

# Function to score sentences based on word frequency
def score_sentences(text):
    tokens = preprocess_text(text)
    tagged_tokens = pos_tagging(tokens)
    nouns_adjectives = extract_nouns_adjectives(tagged_tokens)
    word_freq = Counter(nouns_adjectives)
    max_freq = max(word_freq.values())
    scores = {}
    for sentence in sent_tokenize(text):
        sentence_tokens = preprocess_text(sentence)
        sentence_score = sum(word_freq.get(token, 0) / max_freq for token in sentence_tokens)
        scores[sentence] = sentence_score
    return scores

# Function to generate summary
def generate_summary(text, num_sentences=3):
    scores = score_sentences(text)
    top_sentences = sorted(scores, key=scores.get, reverse=True)[:num_sentences]
    summary = ' '.join(top_sentences) 
    return summary

def summary_generator(url):
    article_text = fetch_article(url)
    summary = generate_summary(article_text)
    return article_text, summary


