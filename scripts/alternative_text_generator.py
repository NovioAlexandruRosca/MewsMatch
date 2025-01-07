import re
import string
import random
import nltk
import langid
import requests
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

english_pronouns = r'\b(I|you|he|she|it|we|they|me|him|her|us|them|my|your|his|her|its|our|their)\b'
romanian_pronouns = r'\b(eu|tu|el|ea|noi|voi|ei|ele|mă|te|îl|o|ne|vă|îi|le|al meu|al tău|al lui|al ei|pe|din|la|în|despre|pentru|da|nu|de|cu|si|şi|ar|dar|așa|lui)\b'


def get_word_definition(word):
    url = f"https://dexonline.ro/definitie/{word}"

    response = requests.get(url)
    synonyms_list = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        tab_2_div = soup.find('div', id='tab_2')
        if tab_2_div:

            divs = soup.find_all('div', class_='tree-body')

            for div in divs:
                li_elements = div.find_all('li', class_='type-meaning depth-0')

                for li in li_elements:
                    meaning_relations = li.find_all('div', class_='meaning-relations')

                    for meaning_div in meaning_relations:

                        tag_groups = meaning_div.find_all('span', class_='tag-group')

                        for tag_group in tag_groups:
                            text_muted = tag_group.find('span', class_='text-muted')

                            if text_muted and 'sinonime' in text_muted.get_text().lower():
                                synonyms = tag_group.find_all('span', class_='badge-relation')

                                for synonym in synonyms:
                                    link = synonym.find('a')
                                    if link:
                                        synonyms_list.append(link.get_text())
                                    else:
                                        synonyms_list.append(synonym.get_text())

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    return synonyms_list[:1]


def get_synonym(word, checked_words=None):
    if checked_words is None:
        checked_words = set()
    if word.lower() in checked_words:
        return word

    synonyms = wn.synsets(word)
    if synonyms:
        filtered_synonyms = [
            lemma.name() for lemma in synonyms[0].lemmas()
            if lemma.name().lower() != word.lower()
        ]
        filtered_synonyms = [syn for syn in filtered_synonyms if syn.lower() != word.lower()]
        if filtered_synonyms:
            return random.choice(filtered_synonyms)

    return word


def get_hypernym(word, checked_words=None):
    if checked_words is None:
        checked_words = set()
    if word.lower() in checked_words:
        return word

    synonyms = wn.synsets(word)
    if synonyms:
        hypernyms = synonyms[0].hypernyms()
        if hypernyms:
            return hypernyms[0].lemmas()[0].name()

    return word


def get_negated_antonym(word, checked_words=None):
    if checked_words is None:
        checked_words = set()
    if word.lower() in checked_words:
        return word

    synonyms = wn.synsets(word)
    if synonyms:
        antonyms = [ant for lemma in synonyms[0].lemmas() for ant in lemma.antonyms()]
        if antonyms:
            return f"not {antonyms[0].name()}"

    return word


def generate_alternative_text(text, language, replacement_percentage=0.2):
    words = nltk.word_tokenize(text)
    total_words = len(words)
    num_replacements = int(total_words * replacement_percentage)

    words_to_replace = random.sample([word for word in words if
                                      word not in string.punctuation and not re.match(english_pronouns,
                                                                                      word) and not re.match(
                                          romanian_pronouns, word)], num_replacements)

    modified_words = []
    checked_words = set()

    for word in words:
        if word not in string.punctuation and not re.match(english_pronouns, word) and not re.match(romanian_pronouns,
                                                                                                    word):
            if word in words_to_replace:
                if language == "en":
                    original_word = word
                    modified_word = word
                    attempt = 0

                    while modified_word.lower() == original_word.lower() and attempt < 5:
                        replacement_type = random.choice([get_synonym, get_hypernym, get_negated_antonym])
                        modified_word = replacement_type(word, checked_words)
                        attempt += 1

                    if modified_word.lower() != original_word.lower():
                        checked_words.add(modified_word.lower())
                        modified_words.append(modified_word)
                        print(f"Base word: {word} Modified word: {modified_word}")
                    else:
                        modified_words.append(word)
                else:
                    possible_syn = get_word_definition(word)
                    if possible_syn and num_replacements > 0:
                        syn = random.choice(possible_syn)
                        modified_words.append(syn.strip())
                        num_replacements -= 1
                        print(f"Base word: {word} | Modified word: {syn} | Words Left: {num_replacements}")
                    else:
                        modified_words.append(word)

            else:
                modified_words.append(word)
        else:
            modified_words.append(word)

    return ' '.join(modified_words)


with open("../data/nlp_text", "r", encoding="utf-8") as file:
    content = file.read()

language, confidence = langid.classify(content)
print(f"The detected language is: {language} (Confidence: {confidence})")

alternative_text = generate_alternative_text(content, language)

output_path = f"../data/nlp_{language}_alternative_text.txt"

with open(output_path, "w", encoding="utf-8") as text_file:
    text_file.write(alternative_text)
