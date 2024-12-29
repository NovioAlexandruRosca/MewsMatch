# from langdetect import detect
import json
import spacy
import re
import langid
from collections import Counter
import nltk
nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")

with open("../data/nlp_text", "r", encoding="utf-8") as file:
    content = file.read()
    # print(content)

# language = detect(content)
# print(f"The detected language is: {language}")

language, confidence = langid.classify(content)
print(f"The detected language is: {language} (Confidence: {confidence})") #Preferam asta

##############################

num_chars = len(content) # nr caractere

text = content.lower()
words = re.findall(r'\b\w+\b', text)
word_count = Counter(words)

num_words = len(words) #nr cuvinte

inverse_proportion = {word: num_words / count for word, count in word_count.items()}
inverse_proportion = sorted(inverse_proportion.items(), key=lambda x: x[1])

ttr = len(word_count) / len(words)
hapax_legomena = [word for word, count in word_count.items() if count == 1]
hapax_dislegomena = [word for word, count in word_count.items() if count == 2]
word_lengths = [len(word) for word in words]
avg_word_length = sum(word_lengths) / len(words)
short_words = [word for word in words if len(word) <= 3]
long_words = [word for word in words if len(word) >= 7]


doc = nlp(text)

# Sentence length metrics
sentences = list(doc.sents)
num_sentences = len(sentences)

# Average sentence length
sentence_lengths = [len([token.text for token in sentence if not token.is_punct]) for sentence in sentences]
avg_sentence_length = sum(sentence_lengths) / num_sentences if num_sentences else 0

# Sentence length variance
variance_sentence_length = sum((x - avg_sentence_length) ** 2 for x in sentence_lengths) / num_sentences if num_sentences else 0

# Part of Speech distribution
pos_tags = [token.pos_ for token in doc]
pos_counts = {pos: pos_tags.count(pos) for pos in set(pos_tags)}

punctuation_marks = [token.text for token in doc if token.is_punct]
punctuation_counts = {punctuation: punctuation_marks.count(punctuation) for punctuation in set(punctuation_marks)}



word_count = word_count.most_common()
########################################

data = {
    "language": {
        "detected_language": language,
    },
    "statistics": {
        "num_chars": num_chars,
        "num_words": num_words,
        "num_sentences": num_sentences,
    },
    "word_frequencies": dict(word_count),
    "inverse_proportions": dict(inverse_proportion),
    "lexical_features": {
            "type_token_ratio": ttr,
            "hapax_legomena_count": len(hapax_legomena),
            "hapax_dislegomena_count": len(hapax_dislegomena),
            "average_word_length": avg_word_length,
            "short_words_count": len(short_words),
            "long_words_count": len(long_words),
        },
    "syntactic_features": {
            "num_sentences": num_sentences,
            "avg_sentence_length": avg_sentence_length,
            "variance_sentence_length": variance_sentence_length,
            "pos_distribution": pos_counts,
            "punctuation_usage": punctuation_counts
        }
}


###################################################

tokens = nltk.word_tokenize(content)

filtered_tokens = ([token for token in tokens if any(c.isalpha() for c in token)])

token_lengths = [len(token) for token in filtered_tokens]
federalist_by_author_length_distributions = nltk.FreqDist(token_lengths)
federalist_by_author_length_distributions.plot(15,title="Length of words frequency")

output_path = "../data/nlp_styleometrics_analysis.json"
with open(output_path, "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)
