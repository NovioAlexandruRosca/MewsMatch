import json
import spacy
import re
import langid
from collections import Counter
import nltk
import yake
import google.generativeai as genai
from googletrans import Translator
from transformers import GPT2LMHeadModel, GPT2Tokenizer


nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")
#nlp = spacy.load("ro_core_news_sm")

with open("../data/english_nlp_text", "r", encoding="utf-8") as file:
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


#extract keywords from text
def extract_keywords(text, num_keywords=10, language="ro", duplication_threshold=0.9):
    kw_extractor = yake.KeywordExtractor(lan=language, n=1, top=num_keywords,dedupLim=duplication_threshold)
    keywords = kw_extractor.extract_keywords(text)
    return [kw[0] for kw in keywords]


keywords = extract_keywords(content, language=language)


def genereate_sentences(keywords, content, language="ro", type_of_generation=1):
    sentence = []

    if type_of_generation == 1:
        genai.configure(api_key="AIzaSyB4lrryXp_acVm7ANCfunAdDfXFupLEHwY")
        generation_config = {
            "temperature" : 0.7,
            "max_output_tokens" : 50
        }
        model = genai.GenerativeModel("gemini-1.5-flash")

        for keyword in keywords:
            keyword_sentence = find_sentence_with_keyword(keyword, content)
            # prompt = f"Generează o propoziție folosind cuvantul: {keyword}, în care cuvântul dat să aibă același sens ca în propoziția: {keyword_sentence}"
            prompt = (f"Create a new sentence in the {language} language using the word: {keyword},"
                      f" where the given word has a similar meaning with its appearance in the following sentence: {keyword_sentence}")
            response = model.generate_content(prompt)
            sentence.append(response.text)
    else:
        model_name = "gpt2"
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        model = GPT2LMHeadModel.from_pretrained(model_name)

        translator = Translator()

        for keyword in keywords:
            if language == "ro":
                keyword = translator.translate(keyword, src="ro", dest="en").text

            input_ids = tokenizer.encode(keyword, return_tensors="pt")

            output = model.generate(
                input_ids,
                max_length=10,
                num_return_sequences=1,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                do_sample=True
            )

            generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

            if language == "ro":
                generated_text = translator.translate(generated_text, src="en", dest="ro").text

            sentence.append(generated_text)

    return sentence


def find_sentence_with_keyword(keyword, content):
    sentences = re.split(r'[.!?]\s*', content)
    for sentence in sentences:
        if re.search(rf'\b{keyword}\b', sentence, re.IGNORECASE):
            return sentence.strip()
    return None


keyword_sentences = genereate_sentences(keywords, content, language=language, type_of_generation=2)

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
        },
    "keywords": {
        "extracted_keywords": keywords,
        "generated_sentences": keyword_sentences
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
