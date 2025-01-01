import random
from nltk.corpus import wordnet as wn
import pandas as pd
import nltk

nltk.download('wordnet')

valid_species = [
    "Bengal", "Birman", "British Shorthair", "Chartreux",
    "European", "Maine coon", "Persian", "Ragdoll",
    "Savannah", "Sphynx", "Siamese", "Turkish angora"
]

column_mappings = {
    "Sexe": "Sex",
    "Age": "Age",
    "Nombre": "Number",
    "Logement": "Accommodation",
    "Zone": "Area",
    "Ext": "Ext",
    "Obs": "Obs",
    "Timide": "Shy",
    "Calme": "Calm",
    "Effraye": "Afraid",
    "Intelligent": "Clever",
    "Vigilant": "Vigilant",
    "Perseverant": "Persevering",
    "Affectueux": "Affectionate",
    "Amical": "Friendly",
    "Solitaire": "Lonely",
    "Brutal": "Brutal",
    "Dominant": "Dominant",
    "Agressif": "Aggressive",
    "Impulsif": "Impulsive",
    "Previsible": "Predictable",
    "Distrait": "Distracted",
    "Abondance": "Abundance",
    "PredOiseau": "PredBird",
    "PredMamm": "PredMamm",
    "Race": "Breed"
}

breed_to_code = {
    "Bengal": 5,
    "Birman": 1,
    "British Shorthair": 9,
    "Chartreux": 10,
    "European": 2,
    "Maine Coon": 4,
    "Persian": 7,
    "Ragdoll": 11,
    "Savannah": 6,
    "Sphynx": 13,
    "Siamese": 8,
    "Turkish Angora": 12,
    "No breed": 3,
    "Other": 14,
    "Unknown": -1
}

unchanged_words = {"male", "males", "female", "females"}
for breed in valid_species:
    unchanged_words.add(breed)

df = pd.read_excel('../data/datasets/balanced_outputs/balanced_hybrid.xlsx')
df.rename(columns=column_mappings, inplace=True)

# cat1_species = random.choice(valid_species)
# cat2_species = random.choice(valid_species)

cat1_species = 'Siamese'
cat2_species = 'Turkish Angora'

cat1_code = breed_to_code.get(cat1_species, "Unknown breed")
cat2_code = breed_to_code.get(cat2_species, "Unknown breed")

df_cat1 = df[df['Breed'] == cat1_code]
df_cat2 = df[df['Breed'] == cat2_code]


def get_synonym(word):
    if word in unchanged_words:
        return word

    synonyms = wn.synsets(word)
    if synonyms:
        filtered_synonyms = [
            lemma.name() for lemma in synonyms[0].lemmas()
            if lemma.name().lower() != word.lower()
        ]

        if filtered_synonyms:
            return random.choice(filtered_synonyms)

    return word

def get_hypernym(word):
    if word in unchanged_words:
        return word

    synonyms = wn.synsets(word)
    if synonyms:
        hypernyms = synonyms[0].hypernyms()
        if hypernyms:
            return hypernyms[0].lemmas()[0].name()
    return word

def get_negated_antonym(word):
    if word in unchanged_words:
        return word

    synonyms = wn.synsets(word)
    if synonyms:
        antonyms = [ant for lemma in synonyms[0].lemmas() for ant in lemma.antonyms()]
        if antonyms:
            return f"not {antonyms[0].name()}"
    return word


def generality_words():
    return " " + random.choice(["", "typically", "normally", "commonly", "as a rule", "on the whole", "most of the time", "ordinarily", "in most cases", "in the main", "by and large", "in the usual way", "habitually", "as a general rule", "customarily", "regularly", "in the majority of cases", "broadly speaking", "on average", "in a general sense", "for the most part", "largely", "almost always", "practically", "almost invariably", "frequently", "predominantly", "often", "routinely", "consistently", "in most instances", "at large", "mainly", "more often than not", "in effect", "as a standard practice", "usually speaking", "in common situations", "in everyday situations", "customarily speaking", "as a general tendency"])


def connection_words():
    return random.choice(["and", "but", "also", "as well", "in addition", "furthermore", "moreover", "besides", "likewise", "too", "however", "on the other hand", "yet", "although", "whereas", "nor", "either", "neither", "as well as", "similarly", "in contrast", "on the contrary", "conversely", "while", "even so", "for instance", "for example", "thus", "therefore", "so", "because", "since", "although", "on top of that", "not only... but also", "in comparison", "instead", "still", "nevertheless"])


# def c#at_words():
    #cats, "Adult females"
# "Females of the species"
# "The female population"
# "Female felines"
# "Female individuals"
# "Female cats of the breed"
# "She-cats"
# "Feline females"
#Tomcats
#male memb ers

def count_column_values(df, breed_name):
    column_counts = {"Breed": breed_name}
    columns_dictionary = {}

    for column in df.columns:
        if column != 'Breed':
            value_counts = df[column].value_counts().to_dict()

            total_count = sum(value_counts.values())
            weighted_sum = sum(value * count for value, count in value_counts.items())
            avg = weighted_sum / total_count if total_count > 0 else 0

            columns_dictionary[column] = {
                "counts": value_counts,
                "average": avg
            }

    column_counts['Attributes'] = columns_dictionary
    return column_counts


cat1_data = count_column_values(df_cat1, cat1_species)
cat2_data = count_column_values(df_cat2, cat2_species)

print(cat1_data, cat2_data)

text = ""


def sex_text_generation():
    templates = {
        'male': [
            "there tends to be more {species} male cats than female{generality_words}",
            "the {species} breed has a higher number of males compared to females{generality_words}",
            "it is more common for {species} cats to be male than female{generality_words}",
            "there tends to be {male_percent}% male {species} cats compared to females{generality_words}"
        ],
        'female': [
            "there tends to be more {species} female cats than male{generality_words}",
            "the {species} breed has a higher number of females compared to males{generality_words}",
            "it is more common for {species} cats to be female than male{generality_words}",
            "there tends to be {female_percent}% female {species} cats compared to males{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} are similar in number of males and females{generality_words}",
            "the distribution of males and females in {species1} and {species2} is almost equal{generality_words}",
            "there is a balanced male-to-female ratio in both {species1} and {species2}{generality_words}"
        ],
        'more_female': [
            "there tend to be more female {species1} cats and more male {species2} cats{generality_words}",
            "it is common to find more female {species1} cats and more male {species2} cats{generality_words}"
        ],
        'more_male': [
            "there tend to be more male {species1} cats and more female {species2} cats{generality_words}",
            "it is common to find more male {species1} cats and more female {species2} cats{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_sex = cat1_data['Attributes']['Sex']
    cat2_sex = cat2_data['Attributes']['Sex']

    male_percent1 = round((cat1_sex['counts'][0] / (cat1_sex['counts'][0] + cat1_sex['counts'][1])) * 100, 2)
    female_percent1 = 100 - male_percent1

    male_percent2 = round((cat2_sex['counts'][0] / (cat2_sex['counts'][0] + cat2_sex['counts'][1])) * 100, 2)
    female_percent2 = 100 - male_percent2

    if cat1_sex['average'] < 0.3:
        characteristic1 = random.choice(templates['male']).format(species=cat1_species, generality_words=generality_words(), male_percent=male_percent1)
    elif cat1_sex['average'] > 0.7:
        characteristic1 = random.choice(templates['female']).format(species=cat1_species, generality_words=generality_words(), female_percent=female_percent1)

    if cat2_sex['average'] < 0.3:
        characteristic2 = random.choice(templates['male']).format(species=cat2_species, generality_words=generality_words(), male_percent=male_percent2)
    elif cat2_sex['average'] > 0.7:
        characteristic2 = random.choice(templates['female']).format(species=cat2_species, generality_words=generality_words(), female_percent=female_percent2)

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_sex['average'] - cat2_sex['average']) < 0.3:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_sex['average'] > cat2_sex['average']:
        sentence_parts.append(random.choice(templates['more_female']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['more_male']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def age_text_generation():
    templates = {
        'young': [
            "there tends to be more {species} cats that are less than 1 year old{generality_words}",
            "it is common to find younger {species} cats under 1 year old{generality_words}",
            "the {species} breed has a higher proportion of cats younger than 1 year{generality_words}"
        ],
        'young_adult': [
            "there tends to be more {species} cats between 1 and 2 years old{generality_words}",
            "the {species} breed has a significant number of cats aged 1 to 2 years{generality_words}",
            "many {species} cats are found to be in the 1-2 year age range{generality_words}"
        ],
        'adult': [
            "there tends to be more {species} cats between 2 and 10 years old{generality_words}",
            "most {species} cats are aged between 2 and 10 years{generality_words}",
            "the {species} breed commonly has cats in the 2-10 year age group{generality_words}"
        ],
        'senior': [
            "there tends to be more {species} cats older than 10 years{generality_words}",
            "it is common for {species} cats to be over 10 years old{generality_words}",
            "the {species} breed often has older cats aged above 10 years{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} have a similar average age{generality_words}",
            "the average age of {species1} and {species2} cats is comparable{generality_words}",
            "there is little difference in the average age of {species1} and {species2} cats{generality_words}"
        ],
        'older_younger': [
            "there tend to be older {species1} cats and younger {species2} cats{generality_words}",
            "it is common to find older {species1} cats and younger {species2} cats{generality_words}"
        ],
        'younger_older': [
            "there tend to be older {species2} cats and younger {species1} cats{generality_words}",
            "it is common to find older {species2} cats and younger {species1} cats{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_age = cat1_data['Attributes']['Age']
    cat2_age = cat2_data['Attributes']['Age']

    if cat1_age['average'] < 1:
        characteristic1 = random.choice(templates['young']).format(species=cat1_species, generality_words=generality_words())
    elif 1 <= cat1_age['average'] < 2:
        characteristic1 = random.choice(templates['young_adult']).format(species=cat1_species, generality_words=generality_words())
    elif 2 <= cat1_age['average'] < 10:
        characteristic1 = random.choice(templates['adult']).format(species=cat1_species, generality_words=generality_words())
    else:
        characteristic1 = random.choice(templates['senior']).format(species=cat1_species, generality_words=generality_words())

    if cat2_age['average'] < 1:
        characteristic2 = random.choice(templates['young']).format(species=cat2_species, generality_words=generality_words())
    elif 1 <= cat2_age['average'] < 2:
        characteristic2 = random.choice(templates['young_adult']).format(species=cat2_species, generality_words=generality_words())
    elif 2 <= cat2_age['average'] < 10:
        characteristic2 = random.choice(templates['adult']).format(species=cat2_species, generality_words=generality_words())
    else:
        characteristic2 = random.choice(templates['senior']).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_age['average'] - cat2_age['average']) < 1:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_age['average'] > cat2_age['average']:
        sentence_parts.append(random.choice(templates['older_younger']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['younger_older']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def number_text_generation():
    templates = {
        'one': [
            "there tends to be only 1 {species} cat in an apartment{generality_words}",
            "most apartments house only 1 {species} cat{generality_words}"
        ],
        'two': [
            "there tends to be 2 {species} cats in an apartment{generality_words}",
            "it is common to find 2 {species} cats living in one apartment{generality_words}"
        ],
        'three': [
            "there tends to be 3 {species} cats in an apartment{generality_words}",
            "typically, 3 {species} cats share an apartment{generality_words}"
        ],
        'four': [
            "there tends to be 4 {species} cats in an apartment{generality_words}",
            "4 {species} cats often live together in an apartment{generality_words}"
        ],
        'five': [
            "there tends to be 5 {species} cats in an apartment{generality_words}",
            "it is typical to see 5 {species} cats in a single apartment{generality_words}"
        ],
        'more_than_five': [
            "there tends to be more than 5 {species} cats in an apartment{generality_words}",
            "apartments often house more than 5 {species} cats{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} live in apartments with an equal number of cats{generality_words}",
            "the number of {species1} and {species2} cats in apartments is nearly identical{generality_words}"
        ],
        'more_species1': [
            "there tends to be more {species1} cats than {species2} cats in an apartment{generality_words}",
            "apartments typically house more {species1} cats compared to {species2} cats{generality_words}"
        ],
        'more_species2': [
            "there tends to be more {species2} cats than {species1} cats in an apartment{generality_words}",
            "apartments typically house more {species2} cats compared to {species1} cats{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_number = cat1_data['Attributes']['Number']
    cat2_number = cat2_data['Attributes']['Number']

    if cat1_number['average'] == 1:
        characteristic1 = random.choice(templates['one']).format(species=cat1_species, generality_words=generality_words())
    elif cat1_number['average'] == 2:
        characteristic1 = random.choice(templates['two']).format(species=cat1_species, generality_words=generality_words())
    elif cat1_number['average'] == 3:
        characteristic1 = random.choice(templates['three']).format(species=cat1_species, generality_words=generality_words())
    elif cat1_number['average'] == 4:
        characteristic1 = random.choice(templates['four']).format(species=cat1_species, generality_words=generality_words())
    elif cat1_number['average'] == 5:
        characteristic1 = random.choice(templates['five']).format(species=cat1_species, generality_words=generality_words())
    else:
        characteristic1 = random.choice(templates['more_than_five']).format(species=cat1_species, generality_words=generality_words())

    if cat2_number['average'] == 1:
        characteristic2 = random.choice(templates['one']).format(species=cat2_species, generality_words=generality_words())
    elif cat2_number['average'] == 2:
        characteristic2 = random.choice(templates['two']).format(species=cat2_species, generality_words=generality_words())
    elif cat2_number['average'] == 3:
        characteristic2 = random.choice(templates['three']).format(species=cat2_species, generality_words=generality_words())
    elif cat2_number['average'] == 4:
        characteristic2 = random.choice(templates['four']).format(species=cat2_species, generality_words=generality_words())
    elif cat2_number['average'] == 5:
        characteristic2 = random.choice(templates['five']).format(species=cat2_species, generality_words=generality_words())
    else:
        characteristic2 = random.choice(templates['more_than_five']).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_number['average'] - cat2_number['average']) < 1:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_number['average'] > cat2_number['average']:
        sentence_parts.append(random.choice(templates['more_species1']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['more_species2']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def accommodation_text_generation():
    templates = {
        'apartment_no_balcony': [
            "{species} cats are often found in apartments without balconies{generality_words}",
            "It is common to see {species} cats in apartments that do not have balconies{generality_words}",
            "Apartments without balconies are a typical living arrangement for {species} cats{generality_words}"
        ],
        'apartment_balcony': [
            "{species} cats are often found in apartments with balconies or terraces{generality_words}",
            "Apartments with balconies or terraces tend to house more {species} cats{generality_words}",
            "{species} cats commonly live in apartments with balconies or terraces{generality_words}"
        ],
        'subdivision_house': [
            "Houses in subdivisions are a typical setting for {species} cats{generality_words}",
            "{species} cats are often found in houses within subdivisions{generality_words}",
            "Subdivisions are a common living arrangement for {species} cats{generality_words}"
        ],
        'individual_house': [
            "Individual houses often accommodate {species} cats{generality_words}",
            "{species} cats are frequently found in individual houses{generality_words}",
            "Living in individual houses is typical for {species} cats{generality_words}"
        ],
        'similar': [
            "{species1} and {species2} cats share similar living arrangements{generality_words}",
            "The living arrangements for {species1} and {species2} cats are comparable{generality_words}",
            "{species1} and {species2} cats tend to reside in similar types of accommodations{generality_words}"
        ],
        'different': [
            "{species1} and {species2} cats differ in their preferred living arrangements{generality_words}",
            "The accommodation preferences for {species1} and {species2} cats are distinct{generality_words}",
            "{species1} cats and {species2} cats have different types of accommodations{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_accommodation = cat1_data['Attributes']['Accommodation']
    cat2_accommodation = cat2_data['Attributes']['Accommodation']

    accommodation_map = {1: 'apartment_no_balcony', 2: 'apartment_balcony', 3: 'subdivision_house', 4: 'individual_house'}

    dominant_accommodation1 = max(cat1_accommodation['counts'], key=cat1_accommodation['counts'].get)
    dominant_accommodation2 = max(cat2_accommodation['counts'], key=cat2_accommodation['counts'].get)

    if dominant_accommodation1 in accommodation_map:
        accommodation_type1 = accommodation_map[dominant_accommodation1]
        characteristic1 = random.choice(templates[accommodation_type1]).format(species=cat1_species, generality_words=generality_words())

    if dominant_accommodation2 in accommodation_map:
        accommodation_type2 = accommodation_map[dominant_accommodation2]
        characteristic2 = random.choice(templates[accommodation_type2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if dominant_accommodation1 == dominant_accommodation2:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['different']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def area_text_generation():
    templates = {
        'urban': [
            "{species} cats are commonly found in urban areas{generality_words}",
            "It is typical for {species} cats to reside in urban regions{generality_words}",
            "Urban zones are often home to {species} cats{generality_words}"
        ],
        'periurban': [
            "{species} cats are frequently seen in periurban areas{generality_words}",
            "Periurban regions tend to accommodate many {species} cats{generality_words}",
            "It is common to find {species} cats in periurban areas{generality_words}"
        ],
        'rural': [
            "Rural areas are a typical habitat for {species} cats{generality_words}",
            "{species} cats are often found in rural zones{generality_words}",
            "Living in rural areas is common for {species} cats{generality_words}"
        ],
        'similar': [
            "{species1} and {species2} cats are found in similar types of areas{generality_words}",
            "The areas where {species1} and {species2} cats live are comparable{generality_words}",
            "{species1} and {species2} cats tend to reside in similar zones{generality_words}"
        ],
        'different': [
            "{species1} and {species2} cats live in different types of areas{generality_words}",
            "The area preferences for {species1} and {species2} cats are distinct{generality_words}",
            "{species1} cats and {species2} cats are found in different zones{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_area = cat1_data['Attributes']['Area']
    cat2_area = cat2_data['Attributes']['Area']

    area_map = {1: 'urban', 2: 'rural', 3: 'periurban'}

    dominant_area1 = max(cat1_area['counts'], key=cat1_area['counts'].get)
    dominant_area2 = max(cat2_area['counts'], key=cat2_area['counts'].get)

    if dominant_area1 in area_map:
        area_type1 = area_map[dominant_area1]
        characteristic1 = random.choice(templates[area_type1]).format(species=cat1_species, generality_words=generality_words())

    if dominant_area2 in area_map:
        area_type2 = area_map[dominant_area2]
        characteristic2 = random.choice(templates[area_type2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if dominant_area1 == dominant_area2:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['different']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def exterior_text_generation():
    templates = {
        'none': [
            "{species} cats are mostly indoor cats, spending no time outdoors{generality_words}",
            "It's rare to see {species} cats outside as they spend all their time indoors{generality_words}",
            "{species} cats typically do not go outdoors{generality_words}"
        ],
        'limited': [
            "{species} cats spend limited time outdoors, usually less than an hour a day{generality_words}",
            "Outdoor activity for {species} cats is restricted to less than one hour daily{generality_words}",
            "{species} cats only go outside for brief periods each day{generality_words}"
        ],
        'moderate': [
            "{species} cats enjoy moderate outdoor time, typically between one to five hours daily{generality_words}",
            "On average, {species} cats spend a few hours outdoors every day{generality_words}",
            "{species} cats balance their time between indoors and outdoors, usually staying outside for several hours{generality_words}"
        ],
        'long': [
            "{species} cats spend a significant part of their day outdoors, often more than five hours{generality_words}",
            "Outdoor exploration is a key activity for {species} cats, with them spending over five hours outside daily{generality_words}",
            "{species} cats thrive on long outdoor hours, typically staying out for most of the day{generality_words}"
        ],
        'all_time': [
            "{species} cats are outdoor cats, staying outside almost all the time and coming back only to eat{generality_words}",
            "It's common for {species} cats to spend nearly all their time outdoors, returning just for meals{generality_words}",
            "{species} cats live an outdoor lifestyle, coming indoors just to eat{generality_words}"
        ],
        'similar': [
            "{species1} and {species2} cats have similar outdoor habits{generality_words}",
            "The outdoor activity patterns of {species1} and {species2} cats are comparable{generality_words}",
            "Both {species1} and {species2} cats exhibit similar tendencies when it comes to outdoor time{generality_words}"
        ],
        'different': [
            "{species1} and {species2} cats differ significantly in their outdoor habits{generality_words}",
            "The time spent outdoors by {species1} and {species2} cats varies considerably{generality_words}",
            "Outdoor activity levels are distinct between {species1} and {species2} cats{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_exterior = cat1_data['Attributes']['Ext']
    cat2_exterior = cat2_data['Attributes']['Ext']

    def categorize_outdoor_time(avg):
        if avg <= 0.5:
            return 'none'
        elif avg < 1.5:
            return 'limited'
        elif avg < 2.5:
            return 'moderate'
        elif avg < 3.5:
            return 'long'
        else:
            return 'all_time'

    category1 = categorize_outdoor_time(cat1_exterior['average'])
    category2 = categorize_outdoor_time(cat2_exterior['average'])

    if category1 in templates:
        characteristic1 = random.choice(templates[category1]).format(species=cat1_species, generality_words=generality_words())

    if category2 in templates:
        characteristic2 = random.choice(templates[category2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if category1 == category2:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['different']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def observation_text_generation():
    templates = {
        'none': [
            "{species} cats tend to have very little interaction each day, often spending the day alone with no observation or play{generality_words}",
            "Interaction with {species} cats is minimal, with little to no time dedicated to games or petting{generality_words}",
            "Typically, {species} cats don't require much attention, spending most of their time without observation or care{generality_words}",
            "{species} cats are independent and usually don't engage in any activities such as play or observation during the day{generality_words}",
            "Most of the day, {species} cats are left to themselves, with no involvement in games or observation{generality_words}"
        ],
        'limited': [
            "{species} cats enjoy some attention, but usually only for a short period of time each day, less than an hour{generality_words}",
            "With {species} cats, interaction is kept to a minimum, generally under an hour per day for play or petting{generality_words}",
            "Interaction with {species} cats is limited to brief sessions, often less than one hour each day{generality_words}",
            "While {species} cats appreciate some attention, they typically spend under an hour a day on observation or care activities{generality_words}",
            "{species} cats generally enjoy short moments of play or petting, usually not exceeding an hour per day{generality_words}"
        ],
        'moderate': [
            "{species} cats have a balanced amount of daily interaction, typically spending a few hours each day on observation, games, or care{generality_words}",
            "Moderate interaction is common for {species} cats, with several hours spent on play and petting each day{generality_words}",
            "On average, {species} cats engage in about one to five hours of activity daily, including petting, observation, and play{generality_words}",
            "{species} cats thrive on moderate interaction, enjoying a few hours daily for activities such as play and observation{generality_words}",
            "While {species} cats enjoy some independent time, they usually spend a few hours each day on games and petting{generality_words}"
        ],
        'long': [
            "{species} cats are very social, often spending most of their day interacting with their owners for over five hours{generality_words}",
            "Daily interaction is important for {species} cats, who typically enjoy over five hours of care, play, or observation{generality_words}",
            "{species} cats thrive on long, extended interaction, spending a significant part of their day engaged in activities like observation and petting{generality_words}",
            "Spending the majority of their time with their owners, {species} cats often have more than five hours of observation and care each day{generality_words}",
            "{species} cats are very affectionate, regularly dedicating five or more hours a day to playing, petting, and other activities{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} have similar levels of daily interaction and care{generality_words}",
            "the interaction time with {species1} and {species2} is nearly the same{generality_words}",
            "both {species1} and {species2} cats enjoy comparable amounts of time for games, petting, and observation{generality_words}"
        ],
        'more_interaction': [
            "it is common for {species1} cats to have more interaction time compared to {species2} cats{generality_words}",
            "there tends to be more daily interaction with {species1} than {species2}{generality_words}"
        ],
        'less_interaction': [
            "it is common for {species2} cats to have more interaction time compared to {species1} cats{generality_words}",
            "there tends to be more daily interaction with {species2} than {species1}{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_obs = cat1_data['Attributes']['Obs']
    cat2_obs = cat2_data['Attributes']['Obs']

    def categorize_observation_time(value):
        if value <= 0.5:
            return 'none'
        elif value < 1.5:
            return 'limited'
        elif value < 2.5:
            return 'moderate'
        else:
            return 'long'

    category1 = categorize_observation_time(cat1_obs['average'])
    category2 = categorize_observation_time(cat2_obs['average'])

    if category1 in templates:
        characteristic1 = random.choice(templates[category1]).format(species=cat1_species, generality_words=generality_words())

    if category2 in templates:
        characteristic2 = random.choice(templates[category2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_obs['average'] - cat2_obs['average']) < 1:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_obs['average'] > cat2_obs['average']:
        sentence_parts.append(random.choice(templates['more_interaction']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['less_interaction']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def shyness_text_generation():
    templates = {
        '1': [  # Very shy
            "{species} cats are very shy and tend to avoid interactions with people and other animals{generality_words}",
            "Interaction with {species} cats is difficult, as they are extremely timid and avoid contact{generality_words}",
            "It is common for {species} cats to stay hidden, showing little to no interest in engaging with anyone{generality_words}",
            "Very shy by nature, {species} cats rarely approach people or participate in activities{generality_words}"
        ],
        '2': [  # Shy
            "{species} cats are somewhat shy, often avoiding interactions unless they feel safe{generality_words}",
            "Shyness is typical for {species} cats, as they tend to keep their distance and may take time to warm up{generality_words}",
            "Interaction with {species} cats is usually cautious, as they are shy and prefer to observe from a distance{generality_words}",
            "{species} cats are shy, often hiding when new people or animals are around{generality_words}"
        ],
        '3': [  # Moderate shyness
            "{species} cats are moderately shy, with a balanced level of interaction and independence{generality_words}",
            "While {species} cats can be shy at times, they also enjoy some interaction with people and animals{generality_words}",
            "Moderately shy, {species} cats enjoy some quiet time but will engage when they feel comfortable{generality_words}",
            "{species} cats are moderately shy, preferring to stay near their owners but avoiding too much attention{generality_words}"
        ],
        '4': [  # Not very shy
            "{species} cats are not very shy, and they are generally open to interacting with people and animals{generality_words}",
            "Not particularly shy, {species} cats are often curious and willing to engage with others{generality_words}",
            "{species} cats are typically confident and comfortable around people, showing less shyness in general{generality_words}",
            "Though not overly social, {species} cats are not shy and may seek attention from time to time{generality_words}"
        ],
        '5': [  # Not shy at all
            "{species} cats are very outgoing and confident, showing little to no signs of shyness{generality_words}",
            "Interaction with {species} cats is easy, as they are confident and not shy around people or animals{generality_words}",
            "Very sociable, {species} cats are confident and comfortable with people, showing no signs of shyness{generality_words}",
            "{species} cats are not shy at all, thriving on interaction and engagement with their environment{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} have similar levels of shyness, with neither being particularly shy or outgoing{generality_words}",
            "The shyness level of {species1} and {species2} is quite alike, with both being moderately shy or outgoing{generality_words}",
            "{species1} and {species2} cats share similar levels of shyness, neither being overly shy nor excessively outgoing{generality_words}"
        ],
        'more_shy': [
            "it is common for {species1} cats to be more shy than {species2}, as {species1} tends to avoid interaction more often{generality_words}",
            "Compared to {species2}, {species1} cats are generally shyer, preferring to stay out of sight or avoid contact{generality_words}"
        ],
        'less_shy': [
            "it is common for {species2} cats to be more shy than {species1}, as {species2} tends to avoid people and animals more often{generality_words}",
            "Compared to {species1}, {species2} cats are generally shyer and may be more hesitant to engage{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_shyness = cat1_data['Attributes']['Shy']
    cat2_shyness = cat2_data['Attributes']['Shy']

    def categorize_shyness(value):
        if value <= 1.5:
            return '1'
        elif value < 2.5:
            return '2'
        elif value < 3.5:
            return '3'
        elif value < 4.5:
            return '4'
        else:
            return '5'

    category1 = categorize_shyness(cat1_shyness['average'])
    category2 = categorize_shyness(cat2_shyness['average'])

    if category1 in templates:
        characteristic1 = random.choice(templates[category1]).format(species=cat1_species, generality_words=generality_words())

    if category2 in templates:
        characteristic2 = random.choice(templates[category2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_shyness['average'] - cat2_shyness['average']) < 1:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_shyness['average'] > cat2_shyness['average']:
        sentence_parts.append(random.choice(templates['more_shy']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['less_shy']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def calmness_text_generation():
    templates = {
        '1': [  # Very calm
            "{species} cats are extremely calm, often remaining very relaxed and composed even in new situations{generality_words}",
            "Very calm, {species} cats show little to no signs of anxiety or agitation in most situations{generality_words}",
            "Interaction with {species} cats is easy, as they are remarkably composed and serene in their demeanor{generality_words}",
            "{species} cats are very calm, often lounging peacefully and rarely displaying any signs of stress{generality_words}"
        ],
        '2': [  # Calm
            "{species} cats are generally calm, staying relaxed and composed but with occasional bursts of energy{generality_words}",
            "While {species} cats are calm, they can sometimes show moments of excitement or curiosity{generality_words}",
            "Calm by nature, {species} cats enjoy peaceful moments but will still engage in playful behavior from time to time{generality_words}",
            "{species} cats are calm overall, though they may exhibit brief periods of excitement or play{generality_words}"
        ],
        '3': [  # Moderately calm
            "{species} cats are moderately calm, showing a balance between peacefulness and occasional bursts of activity{generality_words}",
            "Moderately calm, {species} cats can switch between relaxed and playful behaviors depending on the situation{generality_words}",
            "While {species} cats are generally calm, they can be playful and active when the mood strikes{generality_words}",
            "{species} cats are moderately calm, preferring a balance between relaxation and brief playful moments{generality_words}"
        ],
        '4': [  # Not very calm
            "{species} cats are not particularly calm, often showing excitement and energy throughout the day{generality_words}",
            "Not as calm as other breeds, {species} cats tend to be more active and energetic, seeking out play or exploration{generality_words}",
            "{species} cats are not very calm, often moving around energetically and seeking attention and interaction{generality_words}",
            "While {species} cats are not overly frantic, they are more active than calm, often engaging in playful behavior{generality_words}"
        ],
        '5': [  # Very active (Not calm at all)
            "{species} cats are very energetic, rarely sitting still and constantly seeking play or interaction{generality_words}",
            "Very active, {species} cats have high energy levels and rarely remain calm or composed for long{generality_words}",
            "{species} cats are full of energy, always looking for something to do and never showing signs of calmness{generality_words}",
            "{species} cats are highly energetic, constantly moving and engaging with their surroundings, never seeming calm{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} have similar levels of calmness, with neither being overly calm or energetic{generality_words}",
            "The calmness levels of {species1} and {species2} are comparable, with both showing a balance between calmness and activity{generality_words}",
            "{species1} and {species2} cats share similar calmness levels, neither being particularly calm or excessively energetic{generality_words}"
        ],
        'more_calm': [
            "it is common for {species1} cats to be calmer than {species2}, as {species1} tends to be more composed and relaxed{generality_words}",
            "Compared to {species2}, {species1} cats are generally calmer, preferring peaceful moments over active play{generality_words}"
        ],
        'less_calm': [
            "it is common for {species2} cats to be calmer than {species1}, as {species2} tends to remain more composed and relaxed{generality_words}",
            "Compared to {species1}, {species2} cats are generally calmer, often preferring calm over playful activities{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_calm = cat1_data['Attributes']['Calm']
    cat2_calm = cat2_data['Attributes']['Calm']

    def categorize_calmness(value):
        if value <= 1.5:
            return '1'
        elif value < 2.5:
            return '2'
        elif value < 3.5:
            return '3'
        elif value < 4.5:
            return '4'
        else:
            return '5'

    category1 = categorize_calmness(cat1_calm['average'])
    category2 = categorize_calmness(cat2_calm['average'])

    if category1 in templates:
        characteristic1 = random.choice(templates[category1]).format(species=cat1_species, generality_words=generality_words())

    if category2 in templates:
        characteristic2 = random.choice(templates[category2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_calm['average'] - cat2_calm['average']) < 1:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_calm['average'] > cat2_calm['average']:
        sentence_parts.append(random.choice(templates['more_calm']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['less_calm']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def afraid_text_generation():
    templates = {
        '1': [
            "{species} cats are rarely afraid, displaying a calm demeanor most of the time{generality_words}",
            "It's uncommon for {species} cats to be afraid, as they tend to stay confident and composed{generality_words}",
            "{species} cats are generally fearless and rarely show signs of fear or anxiety{generality_words}",
            "{species} cats are known for their bravery and usually don't get scared easily{generality_words}",
            "Fear is not something {species} cats typically experience; they tend to stay calm and composed{generality_words}"
        ],
        '2': [
            "{species} cats show slight signs of fear at times, but it is not common{generality_words}",
            "While {species} cats may be wary in certain situations, they tend to calm down quickly{generality_words}",
            "Occasionally, {species} cats may get scared, but it doesn't last long{generality_words}",
            "{species} cats have a bit of fear but are usually not easily rattled by their environment{generality_words}",
            "Fear is not a major trait of {species} cats, but they may get anxious in certain circumstances{generality_words}"
        ],
        '3': [
            "{species} cats are moderately afraid, sometimes showing signs of nervousness or caution{generality_words}",
            "There is a balanced level of fear in {species} cats; they may get anxious at times but can manage it{generality_words}",
            "{species} cats display moderate fear and may hesitate in unfamiliar situations{generality_words}",
            "{species} cats are fairly cautious and may show mild fear when faced with something unknown{generality_words}",
            "{species} cats can be fearful at times, but they are generally able to manage their emotions{generality_words}"
        ],
        '4': [
            "{species} cats are often afraid and may be nervous around new people or situations{generality_words}",
            "{species} cats tend to be fearful, showing anxiety when faced with unfamiliar surroundings{generality_words}",
            "{species} cats have a high level of fear, becoming easily frightened in certain circumstances{generality_words}",
            "Fear is a common trait in {species} cats, who may get easily spooked or anxious{generality_words}",
            "{species} cats often display signs of fear, especially in stressful or new environments{generality_words}"
        ],
        '5': [
            "{species} cats are extremely afraid, displaying high anxiety and fear in most situations{generality_words}",
            "It is very common for {species} cats to be fearful and anxious throughout their day{generality_words}",
            "{species} cats are highly fearful, showing constant signs of anxiety or distress{generality_words}",
            "{species} cats experience significant fear and tend to avoid situations or people that cause them anxiety{generality_words}",
            "Fear dominates {species} cats' behavior, as they tend to be highly anxious and easily startled{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} show similar levels of fear and anxiety{generality_words}",
            "the fear levels in {species1} and {species2} are quite comparable{generality_words}",
            "{species1} and {species2} cats both experience similar amounts of fear and hesitation{generality_words}"
        ],
        'more_afraid': [
            "{species1} cats tend to be more afraid than {species2} cats{generality_words}",
            "{species1} shows higher fear levels compared to {species2} in similar situations{generality_words}"
        ],
        'less_afraid': [
            "{species2} cats are more afraid than {species1} cats{generality_words}",
            "{species2} shows higher fear levels compared to {species1} in similar situations{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_afraid = cat1_data['Attributes']['Afraid']
    cat2_afraid = cat2_data['Attributes']['Afraid']

    def categorize_afraid(value):
        if value <= 1.5:
            return '1'
        elif value < 2.5:
            return '2'
        elif value < 3.5:
            return '3'
        elif value < 4.5:
            return '4'
        else:
            return '5'

    category1 = categorize_afraid(cat1_afraid['average'])
    category2 = categorize_afraid(cat2_afraid['average'])

    if category1 in templates:
        characteristic1 = random.choice(templates[category1]).format(species=cat1_species, generality_words=generality_words())

    if category2 in templates:
        characteristic2 = random.choice(templates[category2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_afraid['average'] - cat2_afraid['average']) < 1:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_afraid['average'] > cat2_afraid['average']:
        sentence_parts.append(random.choice(templates['more_afraid']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['less_afraid']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def clever_text_generation():
    templates = {
        '1': [
            "{species} cats are not known for their cleverness, often showing limited problem-solving ability{generality_words}",
            "Cleverness is not a dominant trait in {species} cats, as they may struggle with tasks that require thinking{generality_words}",
            "{species} cats typically don't show much cleverness and are not quick to adapt to new challenges{generality_words}",
            "Problem-solving is not a strong point for {species} cats, as they tend to avoid complex tasks{generality_words}",
            "{species} cats may struggle with figuring out puzzles or problems and are not seen as particularly clever{generality_words}"
        ],
        '2': [
            "{species} cats show slight cleverness, occasionally solving simple problems with some effort{generality_words}",
            "Cleverness is present but not dominant in {species} cats, who might solve easy challenges but struggle with more complex ones{generality_words}",
            "While {species} cats can be clever at times, they may not quickly adapt to more difficult tasks{generality_words}",
            "Cleverness is moderate in {species} cats, as they sometimes figure out simple problems or obstacles{generality_words}",
            "{species} cats occasionally show signs of cleverness, but they are not known for their ability to tackle complex challenges{generality_words}"
        ],
        '3': [
            "{species} cats show moderate cleverness, often able to solve problems or navigate challenges with some effort{generality_words}",
            "Cleverness is noticeable in {species} cats, as they can figure out tasks or challenges with relative ease{generality_words}",
            "{species} cats demonstrate a fair amount of cleverness and can be resourceful in overcoming simple obstacles{generality_words}",
            "Moderately clever, {species} cats can adapt and solve problems, though they may need some time or help{generality_words}",
            "Problem-solving is relatively easy for {species} cats, who display moderate levels of cleverness when faced with challenges{generality_words}"
        ],
        '4': [
            "{species} cats are quite clever, often figuring out problems or tasks quickly and efficiently{generality_words}",
            "Cleverness is a strong trait in {species} cats, who can adapt to new challenges and solve problems with ease{generality_words}",
            "With a high level of cleverness, {species} cats are quick thinkers and often solve problems without much difficulty{generality_words}",
            "Problem-solving comes naturally to {species} cats, as they are able to tackle obstacles with impressive cleverness{generality_words}",
            "{species} cats are known for their cleverness, often displaying sharp problem-solving skills in various situations{generality_words}"
        ],
        '5': [
            "{species} cats are extremely clever, often coming up with creative solutions to problems and challenges{generality_words}",
            "Cleverness is one of the most prominent traits in {species} cats, as they can easily overcome complex obstacles{generality_words}",
            "{species} cats are exceptional problem-solvers, consistently displaying remarkable cleverness in various situations{generality_words}",
            "With outstanding cleverness, {species} cats are able to think critically and quickly adapt to challenges{generality_words}",
            "Highly clever, {species} cats are resourceful and skilled at solving problems, even in difficult situations{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} have similar levels of cleverness and problem-solving abilities{generality_words}",
            "the cleverness of {species1} and {species2} cats is nearly identical{generality_words}",
            "{species1} and {species2} cats both display comparable levels of cleverness when solving problems{generality_words}"
        ],
        'more_clever': [
            "{species1} cats tend to be more clever than {species2} cats, showing higher problem-solving abilities{generality_words}",
            "{species1} displays more cleverness than {species2}, often solving problems more easily{generality_words}"
        ],
        'less_clever': [
            "{species2} cats are more clever than {species1} cats, solving problems with greater ease{generality_words}",
            "{species2} shows higher cleverness than {species1}, demonstrating stronger problem-solving abilities{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_clever = cat1_data['Attributes']['Clever']
    cat2_clever = cat2_data['Attributes']['Clever']

    def categorize_cleverness(value):
        if value <= 1.5:
            return '1'
        elif value < 2.5:
            return '2'
        elif value < 3.5:
            return '3'
        elif value < 4.5:
            return '4'
        else:
            return '5'

    category1 = categorize_cleverness(cat1_clever['average'])
    category2 = categorize_cleverness(cat2_clever['average'])

    if category1 in templates:
        characteristic1 = random.choice(templates[category1]).format(species=cat1_species, generality_words=generality_words())

    if category2 in templates:
        characteristic2 = random.choice(templates[category2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_clever['average'] - cat2_clever['average']) < 1:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_clever['average'] > cat2_clever['average']:
        sentence_parts.append(random.choice(templates['more_clever']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['less_clever']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def vigilant_text_generation():
    templates = {
        '1': [
            "{species} cats are not particularly vigilant, often unaware of their surroundings and slow to react to stimuli{generality_words}",
            "{species} cats tend to be less alert, often missing potential dangers or changes in their environment{generality_words}",
            "Vigilance is not a strong trait in {species} cats, as they are typically slow to notice new things or changes around them{generality_words}",
            "Most of the time, {species} cats are not very vigilant, failing to notice movements or sounds in their environment{generality_words}",
            "{species} cats are known for being relatively unaware of their surroundings and often overlook potential threats{generality_words}"
        ],
        '2': [
            "{species} cats show slight vigilance, occasionally noticing changes in their environment but often not reacting quickly{generality_words}",
            "Vigilance is mild in {species} cats, as they may notice some changes but aren't quick to respond to stimuli{generality_words}",
            "{species} cats are somewhat aware of their surroundings, but they typically react slowly to stimuli or changes{generality_words}",
            "While {species} cats may notice some movements or noises, they are not quick to act on them{generality_words}",
            "{species} cats are moderately vigilant, reacting to some changes or sounds but not always immediately{generality_words}"
        ],
        '3': [
            "{species} cats are moderately vigilant, reacting promptly to changes or sounds in their environment{generality_words}",
            "{species} cats are fairly alert, often noticing changes or stimuli and reacting in a timely manner{generality_words}",
            "Vigilance is moderate in {species} cats, who typically react to new situations or noises with some urgency{generality_words}",
            "On average, {species} cats are aware of their surroundings and will act if they perceive a change or threat{generality_words}",
            "With a moderate level of vigilance, {species} cats are able to detect most movements or sounds and react appropriately{generality_words}"
        ],
        '4': [
            "{species} cats are quite vigilant, often noticing even the smallest changes or movements in their environment{generality_words}",
            "{species} cats are highly alert, reacting quickly to any changes or disturbances around them{generality_words}",
            "Vigilance is strong in {species} cats, who are quick to notice and respond to stimuli or threats in their environment{generality_words}",
            "{species} cats demonstrate high vigilance, reacting swiftly to new sounds, movements, or changes in their surroundings{generality_words}",
            "{species} cats are known for their alertness, often spotting potential threats or changes before others do{generality_words}"
        ],
        '5': [
            "{species} cats are exceptionally vigilant, constantly aware of their surroundings and quick to respond to any changes{generality_words}",
            "Vigilance is one of the standout traits in {species} cats, who are always alert and react immediately to stimuli or threats{generality_words}",
            "{species} cats are extremely vigilant, constantly scanning their environment and reacting to even the smallest changes{generality_words}",
            "With an outstanding level of vigilance, {species} cats are always aware of their surroundings and quick to react to changes or movements{generality_words}",
            "{species} cats are highly vigilant, immediately noticing even the smallest shifts in their environment and acting on them{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} have similar levels of vigilance and alertness in their environment{generality_words}",
            "the vigilance of {species1} and {species2} cats is nearly identical, as both react similarly to stimuli{generality_words}",
            "{species1} and {species2} cats both demonstrate comparable levels of alertness and awareness of their surroundings{generality_words}"
        ],
        'more_vigilant': [
            "{species1} cats tend to be more vigilant than {species2} cats, reacting quicker to changes or movements{generality_words}",
            "Vigilance is stronger in {species1} than in {species2}, as {species1} is quicker to react to stimuli{generality_words}"
        ],
        'less_vigilant': [
            "{species2} cats are more vigilant than {species1} cats, reacting faster to environmental changes or stimuli{generality_words}",
            "There is higher vigilance in {species2} than in {species1}, as {species2} cats are quicker to notice and respond to changes{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_vigilant = cat1_data['Attributes']['Vigilant']
    cat2_vigilant = cat2_data['Attributes']['Vigilant']

    def categorize_vigilance(value):
        if value <= 1.5:
            return '1'
        elif value < 2.5:
            return '2'
        elif value < 3.5:
            return '3'
        elif value < 4.5:
            return '4'
        else:
            return '5'

    category1 = categorize_vigilance(cat1_vigilant['average'])
    category2 = categorize_vigilance(cat2_vigilant['average'])

    if category1 in templates:
        characteristic1 = random.choice(templates[category1]).format(species=cat1_species, generality_words=generality_words())

    if category2 in templates:
        characteristic2 = random.choice(templates[category2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_vigilant['average'] - cat2_vigilant['average']) < 1:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_vigilant['average'] > cat2_vigilant['average']:
        sentence_parts.append(random.choice(templates['more_vigilant']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['less_vigilant']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def persevering_text_generation():
    templates = {
        '1': [
            "{species} cats tend to give up quickly when faced with challenges, showing minimal perseverance{generality_words}",
            "{species} cats often struggle to stay persistent, quickly losing interest when tasks become difficult{generality_words}",
            "Perseverance is not a strong trait in {species} cats, who are likely to abandon tasks at the first sign of difficulty{generality_words}",
            "Most of the time, {species} cats do not demonstrate much persistence and will stop trying when things get tough{generality_words}",
            "{species} cats are not known for their perseverance, often quitting when faced with obstacles{generality_words}"
        ],
        '2': [
            "{species} cats show some perseverance, but they are likely to give up if a task takes too long or becomes too challenging{generality_words}",
            "Perseverance is moderate in {species} cats, as they may continue to try but will stop if things become too difficult{generality_words}",
            "{species} cats demonstrate some persistence, but they are prone to abandoning tasks if they don't see quick results{generality_words}",
            "While {species} cats can be persistent, they are likely to quit when faced with sustained challenges or slow progress{generality_words}",
            "{species} cats may persist in a task, but they lack the stamina to continue if it becomes too taxing or prolonged{generality_words}"
        ],
        '3': [
            "{species} cats are fairly persevering, often continuing with tasks even when challenges arise{generality_words}",
            "{species} cats show a decent level of persistence, sticking with a task as long as they believe it will eventually succeed{generality_words}",
            "Moderate perseverance is observed in {species} cats, as they generally continue with tasks despite occasional setbacks{generality_words}",
            "While {species} cats may encounter obstacles, they are usually able to push through and persist until the task is completed{generality_words}",
            "{species} cats tend to show resilience, maintaining persistence through moderate challenges or distractions{generality_words}"
        ],
        '4': [
            "{species} cats are quite persevering, often continuing a task even in the face of significant challenges{generality_words}",
            "{species} cats demonstrate strong perseverance, sticking with difficult tasks and working through obstacles{generality_words}",
            "Perseverance is a notable trait in {species} cats, who are determined to complete tasks regardless of the difficulties{generality_words}",
            "{species} cats show great persistence, often working through challenges and refusing to give up easily{generality_words}",
            "{species} cats are determined and persistent, consistently pushing forward even when tasks become challenging{generality_words}"
        ],
        '5': [
            "{species} cats are extremely persevering, never giving up and continuing to work on tasks no matter how difficult{generality_words}",
            "{species} cats demonstrate exceptional perseverance, always striving to overcome obstacles and never quitting{generality_words}",
            "Perseverance is one of the standout traits of {species} cats, who are unyielding in their efforts despite even the toughest challenges{generality_words}",
            "{species} cats are relentless, continuously pushing through obstacles and showing extraordinary persistence{generality_words}",
            "With unmatched perseverance, {species} cats are always determined to finish tasks, no matter the difficulty{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} show similar levels of perseverance and persistence when faced with challenges{generality_words}",
            "the perseverance levels in {species1} and {species2} cats are comparable, both demonstrating similar levels of determination{generality_words}",
            "{species1} and {species2} cats both persist in the face of challenges with similar levels of persistence and effort{generality_words}"
        ],
        'more_persevering': [
            "{species1} cats tend to be more persevering than {species2} cats, showing greater persistence in difficult situations{generality_words}",
            "{species1} exhibits more perseverance than {species2}, continuing with tasks despite more significant challenges{generality_words}"
        ],
        'less_persevering': [
            "{species2} cats are more persevering than {species1} cats, often showing greater persistence when faced with difficulties{generality_words}",
            "{species2} demonstrates more perseverance than {species1}, as {species2} cats tend to persist longer in challenging tasks{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_persevering = cat1_data['Attributes']['Persevering']
    cat2_persevering = cat2_data['Attributes']['Persevering']

    def categorize_perseverance(value):
        if value <= 1.5:
            return '1'
        elif value < 2.5:
            return '2'
        elif value < 3.5:
            return '3'
        elif value < 4.5:
            return '4'
        else:
            return '5'

    category1 = categorize_perseverance(cat1_persevering['average'])
    category2 = categorize_perseverance(cat2_persevering['average'])

    if category1 in templates:
        characteristic1 = random.choice(templates[category1]).format(species=cat1_species, generality_words=generality_words())

    if category2 in templates:
        characteristic2 = random.choice(templates[category2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_persevering['average'] - cat2_persevering['average']) < 1:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_persevering['average'] > cat2_persevering['average']:
        sentence_parts.append(random.choice(templates['more_persevering']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['less_persevering']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def affectionate_text_generation():
    templates = {
        '1': [
            "{species} cats are not very affectionate, often preferring solitude over companionship{generality_words}",
            "{species} cats are distant and rarely seek out affection from their owners{generality_words}",
            "Affection is not a strong trait of {species} cats, who tend to keep to themselves{generality_words}",
            "{species} cats are independent and usually do not engage in affectionate behaviors{generality_words}",
            "{species} cats often prefer their personal space and do not seek affection from others{generality_words}"
        ],
        '2': [
            "{species} cats show limited affection, occasionally seeking attention but often preferring their own space{generality_words}",
            "While {species} cats may enjoy some affection, they typically don't demand it often{generality_words}",
            "{species} cats are not overly affectionate, but they can be warm when approached on their own terms{generality_words}",
            "Affection from {species} cats is sporadic, with some cats showing interest but not seeking constant interaction{generality_words}",
            "{species} cats can be affectionate at times, though they usually enjoy independence more{generality_words}"
        ],
        '3': [
            "{species} cats display moderate affection, often enjoying interaction but not always seeking it out{generality_words}",
            "Moderate affection is common in {species} cats, as they enjoy cuddles and attention when it is offered{generality_words}",
            "{species} cats appreciate affection, but they do not demand it constantly{generality_words}",
            "Affectionate behaviors are common in {species} cats, though they do not always initiate them{generality_words}",
            "{species} cats enjoy a good balance of affection and independence, seeking attention at times but not excessively{generality_words}"
        ],
        '4': [
            "{species} cats are quite affectionate, often seeking out their owners for attention and interaction{generality_words}",
            "{species} cats thrive on affection, regularly engaging in cuddles and petting with their owners{generality_words}",
            "Affection is important to {species} cats, who enjoy spending time with their owners and being the center of attention{generality_words}",
            "{species} cats are very affectionate, regularly seeking out their owners for companionship and warmth{generality_words}",
            "{species} cats love being close to their owners, often following them around for attention and affection{generality_words}"
        ],
        '5': [
            "{species} cats are extremely affectionate, always seeking attention and companionship from their owners{generality_words}",
            "Affection is a key trait of {species} cats, who constantly seek out petting, cuddles, and interaction{generality_words}",
            "{species} cats are exceptionally affectionate, craving attention and companionship at all times{generality_words}",
            "{species} cats are known for their boundless affection, constantly seeking their owners' attention and love{generality_words}",
            "{species} cats are highly affectionate, regularly showing deep affection and always wanting to be near their owners{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} cats share similar levels of affection and companionship{generality_words}",
            "the affectionate nature of {species1} and {species2} cats is comparable, as both enjoy attention and interaction{generality_words}",
            "{species1} and {species2} cats show similar affection, frequently seeking out companionship from their owners{generality_words}"
        ],
        'more_affectionate': [
            "{species1} cats tend to be more affectionate than {species2} cats, seeking out more attention from their owners{generality_words}",
            "{species1} exhibits more affection than {species2}, often seeking cuddles and attention more frequently{generality_words}"
        ],
        'less_affectionate': [
            "{species2} cats are more affectionate than {species1} cats, often showing more desire for interaction and companionship{generality_words}",
            "{species2} demonstrates more affection than {species1}, frequently seeking attention and warmth from their owners{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_affectionate = cat1_data['Attributes']['Affectionate']
    cat2_affectionate = cat2_data['Attributes']['Affectionate']

    def categorize_affection(value):
        if value <= 1.5:
            return '1'
        elif value < 2.5:
            return '2'
        elif value < 3.5:
            return '3'
        elif value < 4.5:
            return '4'
        else:
            return '5'

    category1 = categorize_affection(cat1_affectionate['average'])
    category2 = categorize_affection(cat2_affectionate['average'])

    if category1 in templates:
        characteristic1 = random.choice(templates[category1]).format(species=cat1_species, generality_words=generality_words())

    if category2 in templates:
        characteristic2 = random.choice(templates[category2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_affectionate['average'] - cat2_affectionate['average']) < 1:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_affectionate['average'] > cat2_affectionate['average']:
        sentence_parts.append(random.choice(templates['more_affectionate']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['less_affectionate']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def friendly_text_generation():
    templates = {
        '1': [
            "{species} cats tend to be quite aloof and unfriendly, often avoiding interaction with others{generality_words}",
            "{species} cats are known for their solitary nature and rarely engage in friendly behaviors{generality_words}",
            "Friendliness is not common among {species} cats, who tend to keep to themselves{generality_words}",
            "{species} cats are distant and do not usually show friendliness toward other people or animals{generality_words}",
            "{species} cats are not typically sociable and prefer to remain in their own space{generality_words}"
        ],
        '2': [
            "{species} cats may show some friendliness but often keep to themselves, engaging minimally with others{generality_words}",
            "While {species} cats can be friendly on occasion, they generally enjoy their solitude{generality_words}",
            "{species} cats may not seek out others, but they can show friendly behavior when approached{generality_words}",
            "Friendliness in {species} cats is limited, as they are often more independent than sociable{generality_words}",
            "{species} cats can be friendly but usually on their own terms, often enjoying time alone{generality_words}"
        ],
        '3': [
            "{species} cats exhibit moderate friendliness, engaging with people and other animals when the situation allows{generality_words}",
            "Friendly behaviors are common in {species} cats, though they can also appreciate some alone time{generality_words}",
            "{species} cats are generally friendly and will engage with others, but they also value their independence{generality_words}",
            "{species} cats enjoy moderate interaction and can be friendly with people and other pets{generality_words}",
            "Friendliness is a common trait in {species} cats, but they may not seek constant attention{generality_words}"
        ],
        '4': [
            "{species} cats are very friendly, regularly seeking interaction with others and forming strong bonds{generality_words}",
            "Friendliness is a strong characteristic of {species} cats, who are often eager to engage with their owners and others{generality_words}",
            "{species} cats are sociable and thrive on interaction, often showing friendly behaviors with both people and pets{generality_words}",
            "{species} cats love being around people and animals, regularly seeking attention and affection{generality_words}",
            "Friendly behaviors are a hallmark of {species} cats, who enjoy socializing and engaging with others{generality_words}"
        ],
        '5': [
            "{species} cats are extremely friendly, always seeking companionship and eager to interact with others{generality_words}",
            "Sociability is a defining trait of {species} cats, who consistently seek out attention and enjoy being around others{generality_words}",
            "{species} cats are known for their exceptional friendliness, constantly engaging with their owners and other pets{generality_words}",
            "Extremely friendly, {species} cats thrive on companionship and eagerly interact with anyone they meet{generality_words}",
            "{species} cats are incredibly sociable, always looking for ways to engage with their owners and other animals{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} cats are similarly friendly and enjoy social interaction{generality_words}",
            "the friendliness of {species1} and {species2} cats is comparable, as both are sociable and enjoy companionship{generality_words}",
            "{species1} and {species2} cats share similar friendly behaviors, often seeking out attention and interaction{generality_words}"
        ],
        'more_friendly': [
            "{species1} cats tend to be more friendly than {species2} cats, seeking more interaction with others{generality_words}",
            "There is generally more friendliness in {species1} than {species2}, as {species1} cats seek out social interaction more{generality_words}"
        ],
        'less_friendly': [
            "{species2} cats are more friendly than {species1} cats, often showing greater sociability and seeking companionship{generality_words}",
            "{species2} exhibits more friendliness than {species1}, regularly seeking out people and animals for social interaction{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_friendly = cat1_data['Attributes']['Friendly']
    cat2_friendly = cat2_data['Attributes']['Friendly']

    def categorize_friendly(value):
        if value <= 1.5:
            return '1'
        elif value < 2.5:
            return '2'
        elif value < 3.5:
            return '3'
        elif value < 4.5:
            return '4'
        else:
            return '5'

    category1 = categorize_friendly(cat1_friendly['average'])
    category2 = categorize_friendly(cat2_friendly['average'])

    if category1 in templates:
        characteristic1 = random.choice(templates[category1]).format(species=cat1_species, generality_words=generality_words())

    if category2 in templates:
        characteristic2 = random.choice(templates[category2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_friendly['average'] - cat2_friendly['average']) < 1:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_friendly['average'] > cat2_friendly['average']:
        sentence_parts.append(random.choice(templates['more_friendly']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['less_friendly']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def lonely_text_generation():
    templates = {
        '1': [
            "{species} cats are very independent and rarely show signs of loneliness, preferring to be alone{generality_words}",
            "{species} cats tend to enjoy their own company and are seldom lonely, even when left alone for long periods{generality_words}",
            "Loneliness is uncommon for {species} cats, who are generally self-sufficient and not affected by solitude{generality_words}",
            "{species} cats are independent creatures and do not exhibit loneliness, even in isolation{generality_words}",
            "Most {species} cats enjoy solitude and do not show signs of loneliness{generality_words}"
        ],
        '2': [
            "{species} cats can tolerate being alone for periods of time but may occasionally show signs of loneliness{generality_words}",
            "While {species} cats are generally independent, they may exhibit mild signs of loneliness if left alone for extended periods{generality_words}",
            "Loneliness is not a major issue for {species} cats, but they may seek some companionship from time to time{generality_words}",
            "{species} cats can handle solitude but might feel lonely during longer periods without interaction{generality_words}",
            "Though independent, {species} cats may occasionally experience mild loneliness when alone{generality_words}"
        ],
        '3': [
            "{species} cats can be moderately affected by loneliness, often seeking attention or companionship when left alone{generality_words}",
            "Moderate loneliness is common for {species} cats, who may occasionally display signs of distress when alone for too long{generality_words}",
            "{species} cats sometimes feel lonely, but they manage on their own, although they may seek company during these times{generality_words}",
            "Loneliness is a moderate concern for {species} cats, who may become withdrawn or seek interaction when left alone{generality_words}",
            "{species} cats are moderately affected by solitude, often becoming lonely and seeking companionship or comfort{generality_words}"
        ],
        '4': [
            "{species} cats tend to feel lonely when left alone, often seeking attention or company from their owners{generality_words}",
            "Loneliness is a significant issue for {species} cats, who may actively seek companionship and show distress when alone{generality_words}",
            "{species} cats thrive on company and often feel lonely when left alone for extended periods{generality_words}",
            "{species} cats are sensitive to loneliness, often becoming anxious or withdrawn when isolated for too long{generality_words}",
            "Feeling lonely is common for {species} cats, who may display clear signs of distress or seek constant attention{generality_words}"
        ],
        '5': [
            "{species} cats are extremely social and cannot tolerate being alone, becoming highly lonely and distressed when isolated{generality_words}",
            "Loneliness is a major issue for {species} cats, who require constant companionship and often show extreme signs of distress when alone{generality_words}",
            "{species} cats are very sensitive to loneliness, and they frequently experience anxiety or depression when left alone{generality_words}",
            "Extreme loneliness is common for {species} cats, who struggle to be alone and need constant companionship to stay happy{generality_words}",
            "{species} cats cannot tolerate being left alone and become highly lonely, often displaying signs of anxiety or sadness{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} cats experience similar levels of loneliness, with neither particularly sensitive to solitude{generality_words}",
            "the loneliness levels of {species1} and {species2} cats are quite similar, with both coping moderately well with being alone{generality_words}",
            "{species1} and {species2} cats share comparable experiences of loneliness, neither being overly affected by solitude{generality_words}"
        ],
        'more_lonely': [
            "{species1} cats tend to experience more loneliness than {species2} cats, showing greater signs of distress when left alone{generality_words}",
            "Loneliness affects {species1} cats more strongly than {species2}, with {species1} becoming more distressed when isolated{generality_words}"
        ],
        'less_lonely': [
            "{species2} cats are less affected by loneliness than {species1}, managing better on their own without showing signs of distress{generality_words}",
            "Loneliness is less of an issue for {species2} than for {species1}, as {species2} can tolerate being alone more easily{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_lonely = cat1_data['Attributes']['Lonely']
    cat2_lonely = cat2_data['Attributes']['Lonely']

    def categorize_loneliness(value):
        if value <= 1.5:
            return '1'
        elif value < 2.5:
            return '2'
        elif value < 3.5:
            return '3'
        elif value < 4.5:
            return '4'
        else:
            return '5'

    category1 = categorize_loneliness(cat1_lonely['average'])
    category2 = categorize_loneliness(cat2_lonely['average'])

    if category1 in templates:
        characteristic1 = random.choice(templates[category1]).format(species=cat1_species, generality_words=generality_words())

    if category2 in templates:
        characteristic2 = random.choice(templates[category2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_lonely['average'] - cat2_lonely['average']) < 1:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_lonely['average'] > cat2_lonely['average']:
        sentence_parts.append(random.choice(templates['more_lonely']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['less_lonely']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def brutal_text_generation():
    templates = {
        '1': [
            "{species} cats are gentle and rarely display any aggressive behavior or brutality{generality_words}",
            "Brutality is uncommon in {species} cats, who are generally calm and peaceful in nature{generality_words}",
            "{species} cats are known for their calm demeanor and are very unlikely to show signs of brutality{generality_words}",
            "Aggression and brutality are not traits associated with {species} cats, who tend to be friendly and non-confrontational{generality_words}",
            "Most {species} cats are mild-mannered and do not engage in brutal behavior{generality_words}"
        ],
        '2': [
            "{species} cats are generally calm but may occasionally display mild aggression or brutish behavior in certain situations{generality_words}",
            "While {species} cats are mostly peaceful, they can sometimes exhibit signs of brutality if provoked or stressed{generality_words}",
            "{species} cats tend to be gentle but may show mild brutality in rare or stressful situations{generality_words}",
            "Brutality is not typical of {species} cats, though they may occasionally display aggression when threatened{generality_words}",
            "On rare occasions, {species} cats may show aggression, though they are generally calm and non-brutal{generality_words}"
        ],
        '3': [
            "{species} cats can be moderately brutal, sometimes showing aggressive tendencies in tense or competitive situations{generality_words}",
            "Moderate brutality is common in {species} cats, who may react aggressively under stress or provocation{generality_words}",
            "{species} cats may show signs of brutality in situations where they feel threatened, though it's not a constant trait{generality_words}",
            "{species} cats occasionally exhibit aggressive or brutal behavior, especially in tense situations or when defending themselves{generality_words}",
            "While {species} cats are usually calm, they can sometimes act brutally when under stress or in a conflict{generality_words}"
        ],
        '4': [
            "{species} cats are prone to showing aggressive or brutal behavior, especially when provoked or threatened{generality_words}",
            "Brutality is a common trait for {species} cats, who may often react with aggression or force in stressful situations{generality_words}",
            "{species} cats are more likely to display brutal behavior, showing signs of aggression when under pressure{generality_words}",
            "{species} cats frequently exhibit brutality in confrontational situations, often reacting aggressively to threats{generality_words}",
            "Aggression and brutality are regular traits of {species} cats, who can be quite forceful when they feel threatened{generality_words}"
        ],
        '5': [
            "{species} cats are extremely brutal and aggressive, often reacting violently to perceived threats or challenges{generality_words}",
            "Brutality defines {species} cats, who are quick to show aggression and forceful behavior in most situations{generality_words}",
            "Extreme brutality is a key trait of {species} cats, who often react with intense aggression and violence{generality_words}",
            "{species} cats are highly brutal, frequently displaying violent tendencies and aggressive behavior in response to stress{generality_words}",
            "Violence and brutality are dominant traits for {species} cats, who often react aggressively in various situations{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} cats exhibit similar levels of brutality, with neither showing extreme aggression{generality_words}",
            "the brutality of {species1} and {species2} cats is comparable, with both displaying occasional aggressive behavior{generality_words}",
            "{species1} and {species2} cats share similar tendencies towards aggression, though neither is excessively brutal{generality_words}"
        ],
        'more_brutal': [
            "{species1} cats tend to be more brutal than {species2} cats, frequently displaying signs of aggression and force{generality_words}",
            "Brutality is more common in {species1} than {species2}, with {species1} often showing more aggression and violence{generality_words}"
        ],
        'less_brutal': [
            "{species2} cats are less brutal than {species1} cats, displaying fewer signs of aggression and violent behavior{generality_words}",
            "Brutality is less common in {species2} compared to {species1}, who tends to be more aggressive{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_brutal = cat1_data['Attributes']['Brutal']
    cat2_brutal = cat2_data['Attributes']['Brutal']

    def categorize_brutality(value):
        if value <= 1.5:
            return '1'
        elif value < 2.5:
            return '2'
        elif value < 3.5:
            return '3'
        elif value < 4.5:
            return '4'
        else:
            return '5'

    category1 = categorize_brutality(cat1_brutal['average'])
    category2 = categorize_brutality(cat2_brutal['average'])

    if category1 in templates:
        characteristic1 = random.choice(templates[category1]).format(species=cat1_species, generality_words=generality_words())

    if category2 in templates:
        characteristic2 = random.choice(templates[category2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_brutal['average'] - cat2_brutal['average']) < 1:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_brutal['average'] > cat2_brutal['average']:
        sentence_parts.append(random.choice(templates['more_brutal']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['less_brutal']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def dominant_text_generation():
    templates = {
        '1': [
            "{species} cats are very passive and unlikely to show dominance in their behavior{generality_words}",
            "Dominance is rare among {species} cats, as they are typically calm and non-confrontational{generality_words}",
            "{species} cats are not known for dominant behavior and prefer to stay passive and cooperative{generality_words}",
            "{species} cats tend to avoid dominance, favoring a more passive and relaxed approach in interactions{generality_words}",
            "Most {species} cats show little to no dominant traits, being gentle and adaptable in their behavior{generality_words}"
        ],
        '2': [
            "{species} cats are usually calm but may occasionally show some dominance in certain situations{generality_words}",
            "While {species} cats tend to be peaceful, they can display mild dominance when asserting themselves{generality_words}",
            "{species} cats are generally passive but might show some dominance in specific circumstances{generality_words}",
            "{species} cats can occasionally exhibit signs of dominance, though it's not a dominant trait in their character{generality_words}",
            "Dominance is not a dominant trait in {species} cats, though they may display it in some situations{generality_words}"
        ],
        '3': [
            "{species} cats display moderate dominance, occasionally taking charge in interactions and asserting themselves{generality_words}",
            "Moderate dominance is seen in {species} cats, who may show leadership qualities when interacting with others{generality_words}",
            "{species} cats can sometimes be dominant, showing a moderate level of assertiveness and control over situations{generality_words}",
            "While {species} cats are mostly calm, they can exhibit moderate dominance, especially when interacting with other animals{generality_words}",
            "{species} cats may display dominance in certain contexts, asserting themselves when they feel the need to lead{generality_words}"
        ],
        '4': [
            "{species} cats often exhibit strong dominance, frequently asserting control in interactions with other animals or people{generality_words}",
            "Dominance is a common trait for {species} cats, who tend to take charge and assert themselves in social situations{generality_words}",
            "{species} cats show clear dominance, frequently taking control of their environment and interactions with others{generality_words}",
            "Strong dominance is characteristic of {species} cats, who often display assertiveness and leadership qualities{generality_words}",
            "Dominance is a defining trait of {species} cats, who are often the leaders in their environment{generality_words}"
        ],
        '5': [
            "{species} cats are highly dominant, always asserting control and showing strong leadership over others{generality_words}",
            "Dominance is a key feature of {species} cats, who constantly strive to be the top figure in their social structure{generality_words}",
            "{species} cats are extremely dominant, always taking charge and exerting authority in their environment{generality_words}",
            "Dominance defines {species} cats, who always seek to control their surroundings and lead with confidence{generality_words}",
            "Highly dominant, {species} cats consistently show control and authority in every interaction{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} cats share similar levels of dominance, with neither being overly dominant{generality_words}",
            "the dominance traits of {species1} and {species2} cats are comparable, with both being moderately assertive{generality_words}",
            "{species1} and {species2} cats both exhibit moderate dominance, with neither showing extreme dominance{generality_words}"
        ],
        'more_dominant': [
            "{species1} cats are more dominant than {species2}, regularly asserting control in social interactions{generality_words}",
            "There is a noticeable dominance difference between {species1} and {species2}, with {species1} taking charge more often{generality_words}"
        ],
        'less_dominant': [
            "{species2} cats are less dominant than {species1}, showing less assertiveness and leadership in interactions{generality_words}",
            "Dominance is more common in {species1}, while {species2} cats are more passive and less likely to take control{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_dominant = cat1_data['Attributes']['Dominant']
    cat2_dominant = cat2_data['Attributes']['Dominant']

    def categorize_dominance(value):
        if value <= 1.5:
            return '1'
        elif value < 2.5:
            return '2'
        elif value < 3.5:
            return '3'
        elif value < 4.5:
            return '4'
        else:
            return '5'

    category1 = categorize_dominance(cat1_dominant['average'])
    category2 = categorize_dominance(cat2_dominant['average'])

    if category1 in templates:
        characteristic1 = random.choice(templates[category1]).format(species=cat1_species, generality_words=generality_words())

    if category2 in templates:
        characteristic2 = random.choice(templates[category2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_dominant['average'] - cat2_dominant['average']) < 1:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_dominant['average'] > cat2_dominant['average']:
        sentence_parts.append(random.choice(templates['more_dominant']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['less_dominant']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def aggressive_text_generation():
    templates = {
        '1': [
            "{species} cats are very calm and rarely exhibit any signs of aggression{generality_words}",
            "Aggression is not a characteristic of {species} cats, who are typically peaceful and non-confrontational{generality_words}",
            "{species} cats tend to avoid aggressive behavior and are generally gentle and relaxed{generality_words}",
            "{species} cats are not known for aggression, preferring peaceful interactions and calm environments{generality_words}",
            "Aggression is uncommon in {species} cats, as they tend to stay calm and passive in most situations{generality_words}"
        ],
        '2': [
            "{species} cats can show occasional aggression, especially when feeling threatened or overstimulated{generality_words}",
            "While {species} cats are generally calm, they may display mild aggression under certain circumstances{generality_words}",
            "{species} cats have a low tendency to be aggressive but can become slightly territorial or defensive when provoked{generality_words}",
            "{species} cats may show some aggression when stressed or during play, though it's not a common behavior{generality_words}",
            "Mild aggression can sometimes be seen in {species} cats, especially in response to stress or unfamiliar situations{generality_words}"
        ],
        '3': [
            "{species} cats exhibit moderate aggression, often defending their space or showing signs of irritation when disturbed{generality_words}",
            "Moderate aggression is common in {species} cats, who may react strongly to threats or disruptions in their environment{generality_words}",
            "{species} cats may show moderate signs of aggression, including hissing or swatting when feeling threatened or stressed{generality_words}",
            "Aggression in {species} cats is moderate, with occasional outbursts or defensiveness when they feel uneasy{generality_words}",
            "{species} cats may become moderately aggressive, particularly if they feel their territory or resources are challenged{generality_words}"
        ],
        '4': [
            "{species} cats often display high levels of aggression, particularly when they feel their space is threatened{generality_words}",
            "Aggression is quite prominent in {species} cats, who may frequently act aggressively in stressful or confrontational situations{generality_words}",
            "{species} cats can be highly aggressive, often reacting defensively or attacking when they feel threatened{generality_words}",
            "High levels of aggression are common in {species} cats, particularly when dealing with unfamiliar animals or environments{generality_words}",
            "Aggression in {species} cats is significant, with frequent displays of territorial behavior and defensive actions{generality_words}"
        ],
        '5': [
            "{species} cats are extremely aggressive, often displaying overt hostility and aggression toward others{generality_words}",
            "Dominating and aggressive, {species} cats tend to be confrontational and can be highly territorial{generality_words}",
            "{species} cats are very aggressive, with frequent attacks or displays of hostility toward other animals or people{generality_words}",
            "Aggression defines {species} cats, who are consistently confrontational and dominant in social interactions{generality_words}",
            "Extremely aggressive, {species} cats often act out with violent behavior, asserting control over their surroundings{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} cats show similar levels of aggression, with neither being overly aggressive{generality_words}",
            "the aggression levels in {species1} and {species2} cats are comparable, both being moderately passive in their behavior{generality_words}",
            "{species1} and {species2} cats exhibit similar aggression levels, with neither showing extreme behavior{generality_words}"
        ],
        'more_aggressive': [
            "{species1} cats are more aggressive than {species2}, often showing more territorial or confrontational behavior{generality_words}",
            "There is a noticeable difference in aggression levels between {species1} and {species2}, with {species1} being more hostile{generality_words}"
        ],
        'less_aggressive': [
            "{species2} cats are less aggressive than {species1}, showing more passive and non-confrontational behavior{generality_words}",
            "{species2} cats exhibit less aggression compared to {species1}, preferring a calmer, less hostile approach{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_aggressive = cat1_data['Attributes']['Aggressive']
    cat2_aggressive = cat2_data['Attributes']['Aggressive']

    def categorize_aggression(value):
        if value <= 1.5:
            return '1'
        elif value < 2.5:
            return '2'
        elif value < 3.5:
            return '3'
        elif value < 4.5:
            return '4'
        else:
            return '5'

    category1 = categorize_aggression(cat1_aggressive['average'])
    category2 = categorize_aggression(cat2_aggressive['average'])

    if category1 in templates:
        characteristic1 = random.choice(templates[category1]).format(species=cat1_species, generality_words=generality_words())

    if category2 in templates:
        characteristic2 = random.choice(templates[category2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_aggressive['average'] - cat2_aggressive['average']) < 1:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_aggressive['average'] > cat2_aggressive['average']:
        sentence_parts.append(random.choice(templates['more_aggressive']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['less_aggressive']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def impulsive_text_generation():
    templates = {
        '1': [
            "{species} cats are very calm and rarely act impulsively, preferring a thoughtful approach to their actions{generality_words}",
            "Impulsiveness is not common in {species} cats, who tend to carefully consider their actions{generality_words}",
            "{species} cats are highly deliberate and rarely engage in impulsive behavior{generality_words}",
            "With {species} cats, impulsivity is seldom observed; they tend to act in a controlled manner{generality_words}",
            "{species} cats show very little impulsiveness, often taking their time to make decisions{generality_words}"
        ],
        '2': [
            "{species} cats may act impulsively on occasion, but it is not a common trait{generality_words}",
            "Impulsiveness is somewhat present in {species} cats, typically triggered by external stimuli or surprise{generality_words}",
            "{species} cats can sometimes act impulsively, though it is usually mild and brief{generality_words}",
            "{species} cats occasionally exhibit impulsive behavior, but it is not a defining characteristic{generality_words}",
            "While {species} cats can act impulsively, it tends to be a rare occurrence in their daily routine{generality_words}"
        ],
        '3': [
            "{species} cats show moderate impulsivity, often acting on instinct or in response to sudden changes in their environment{generality_words}",
            "Impulsiveness is common in {species} cats, especially when they are startled or excited{generality_words}",
            "{species} cats are moderately impulsive, sometimes reacting quickly without much forethought{generality_words}",
            "Moderate impulsivity is a trait of {species} cats, who may act before thinking in certain situations{generality_words}",
            "{species} cats may often act impulsively, especially when reacting to fast-moving objects or sudden noises{generality_words}"
        ],
        '4': [
            "{species} cats are highly impulsive, often acting on instinct and reacting quickly to their surroundings{generality_words}",
            "Impulsivity is quite noticeable in {species} cats, who frequently make spontaneous decisions without much thought{generality_words}",
            "{species} cats are very impulsive, often acting on immediate urges rather than considering consequences{generality_words}",
            "In {species} cats, impulsivity is a dominant trait, leading to quick reactions and unpredictable behavior{generality_words}",
            "Highly impulsive, {species} cats often react immediately to stimuli, without pausing to think{generality_words}"
        ],
        '5': [
            "{species} cats are extremely impulsive, often acting without any consideration or forethought{generality_words}",
            "Impulsiveness is a defining trait of {species} cats, who rarely pause to think before acting{generality_words}",
            "With {species} cats, impulsivity is extreme; they often make hasty decisions and unpredictable moves{generality_words}",
            "Extremely impulsive, {species} cats rarely consider the consequences before taking action{generality_words}",
            "{species} cats are highly impulsive, frequently acting on immediate urges and responding without delay{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} cats exhibit similar levels of impulsivity, with neither being overly impulsive{generality_words}",
            "the impulsivity levels in {species1} and {species2} cats are comparable, with both showing moderate behavior{generality_words}",
            "{species1} and {species2} cats display similar levels of impulsivity, both showing controlled reactions in most situations{generality_words}"
        ],
        'more_impulsive': [
            "{species1} cats are more impulsive than {species2}, often acting before fully processing their surroundings{generality_words}",
            "There is a noticeable difference in impulsivity between {species1} and {species2}, with {species1} being more reactive{generality_words}"
        ],
        'less_impulsive': [
            "{species2} cats are less impulsive than {species1}, showing more thoughtfulness and careful actions{generality_words}",
            "{species2} cats exhibit less impulsivity compared to {species1}, preferring to observe before reacting{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_impulsive = cat1_data['Attributes']['Impulsive']
    cat2_impulsive = cat2_data['Attributes']['Impulsive']

    def categorize_impulsivity(value):
        if value <= 1.5:
            return '1'
        elif value < 2.5:
            return '2'
        elif value < 3.5:
            return '3'
        elif value < 4.5:
            return '4'
        else:
            return '5'

    category1 = categorize_impulsivity(cat1_impulsive['average'])
    category2 = categorize_impulsivity(cat2_impulsive['average'])

    if category1 in templates:
        characteristic1 = random.choice(templates[category1]).format(species=cat1_species, generality_words=generality_words())

    if category2 in templates:
        characteristic2 = random.choice(templates[category2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_impulsive['average'] - cat2_impulsive['average']) < 1:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_impulsive['average'] > cat2_impulsive['average']:
        sentence_parts.append(random.choice(templates['more_impulsive']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['less_impulsive']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def predictable_text_generation():
    templates = {
        '1': [
            "{species} cats are highly unpredictable, often behaving in surprising or erratic ways{generality_words}",
            "Unpredictability defines {species} cats, who rarely follow consistent patterns in their actions{generality_words}",
            "{species} cats tend to act in unpredictable ways, making it difficult to anticipate their behavior{generality_words}",
            "With {species} cats, you can never be sure what to expect, as they frequently surprise with unexpected actions{generality_words}",
            "{species} cats show very little predictability, often changing their behavior without warning{generality_words}"
        ],
        '2': [
            "{species} cats can be unpredictable at times, but they generally follow some patterns in their behavior{generality_words}",
            "While not entirely unpredictable, {species} cats can surprise you occasionally with sudden changes in behavior{generality_words}",
            "{species} cats show moderate unpredictability, sometimes acting in ways that are difficult to foresee{generality_words}",
            "Occasionally, {species} cats act unpredictably, but they also display some consistent behaviors{generality_words}",
            "There is a slight unpredictability to {species} cats, though their behavior is mostly consistent{generality_words}"
        ],
        '3': [
            "{species} cats are fairly predictable, often following established patterns in their actions{generality_words}",
            "Predictability is common in {species} cats, who tend to act consistently day by day{generality_words}",
            "{species} cats exhibit moderate predictability, making their behavior fairly easy to anticipate{generality_words}",
            "Generally, {species} cats are predictable, following regular routines and habits each day{generality_words}",
            "With {species} cats, you can expect a fair amount of consistency in their behavior and actions{generality_words}"
        ],
        '4': [
            "{species} cats are very predictable, with consistent routines and behaviors that are easy to follow{generality_words}",
            "Predictability is a key trait of {species} cats, who usually behave in a stable and reliable way{generality_words}",
            "{species} cats are quite predictable, with actions and behaviors that can be anticipated with ease{generality_words}",
            "In most cases, {species} cats follow predictable patterns, making them easy to understand and anticipate{generality_words}",
            "There is a high level of predictability in {species} cats, who rarely change their routines{generality_words}"
        ],
        '5': [
            "{species} cats are extremely predictable, rarely deviating from their established patterns of behavior{generality_words}",
            "With {species} cats, you can always expect the same behavior, as they follow a fixed routine with little variation{generality_words}",
            "{species} cats are almost entirely predictable, making it easy to anticipate their actions with great certainty{generality_words}",
            "Predictability is a defining trait of {species} cats, whose behavior rarely changes and is highly consistent{generality_words}",
            "Every action of {species} cats follows a predictable routine, making them highly dependable and consistent in behavior{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} cats exhibit similar levels of predictability, with both following consistent routines{generality_words}",
            "the predictability of {species1} and {species2} cats is nearly identical, with both behaving in highly consistent ways{generality_words}",
            "{species1} and {species2} cats show comparable levels of predictability, both demonstrating a high level of consistency in their actions{generality_words}"
        ],
        'more_predictable': [
            "{species1} cats are more predictable than {species2}, consistently following the same behaviors and routines{generality_words}",
            "There is a noticeable difference in predictability between {species1} and {species2}, with {species1} being more consistent in behavior{generality_words}"
        ],
        'less_predictable': [
            "{species2} cats are less predictable than {species1}, showing more variation in their actions and routines{generality_words}",
            "The behavior of {species2} cats is less predictable compared to {species1}, often varying more day-to-day{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_predictable = cat1_data['Attributes']['Predictable']
    cat2_predictable = cat2_data['Attributes']['Predictable']

    def categorize_predictability(value):
        if value <= 1.5:
            return '1'
        elif value < 2.5:
            return '2'
        elif value < 3.5:
            return '3'
        elif value < 4.5:
            return '4'
        else:
            return '5'

    category1 = categorize_predictability(cat1_predictable['average'])
    category2 = categorize_predictability(cat2_predictable['average'])

    if category1 in templates:
        characteristic1 = random.choice(templates[category1]).format(species=cat1_species, generality_words=generality_words())

    if category2 in templates:
        characteristic2 = random.choice(templates[category2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_predictable['average'] - cat2_predictable['average']) < 1:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_predictable['average'] > cat2_predictable['average']:
        sentence_parts.append(random.choice(templates['more_predictable']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['less_predictable']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def distracted_text_generation():
    templates = {
        '1': [
            "{species} cats are highly focused, rarely showing signs of distraction during activities{generality_words}",
            "Distraction is uncommon in {species} cats, who usually stay on task and remain focused{generality_words}",
            "{species} cats are very attentive, exhibiting little to no signs of distraction in their daily routines{generality_words}",
            "You can always rely on {species} cats to stay focused and undistracted during play or observation{generality_words}",
            "Most of the time, {species} cats are completely engaged in their activities and show little distraction{generality_words}"
        ],
        '2': [
            "{species} cats are occasionally distracted but still manage to maintain focus for the majority of the time{generality_words}",
            "While {species} cats can sometimes lose focus, they generally stay on track with their activities{generality_words}",
            "{species} cats show moderate distraction, sometimes getting sidetracked but often staying engaged{generality_words}",
            "Distraction happens occasionally with {species} cats, but they can still focus on their activities most of the time{generality_words}",
            "{species} cats are moderately distracted, but they tend to return to their activities after brief moments of diversion{generality_words}"
        ],
        '3': [
            "{species} cats are fairly distracted, often losing focus for short periods during their daily activities{generality_words}",
            "Distraction is fairly common with {species} cats, who may frequently shift their attention during play or observation{generality_words}",
            "{species} cats can be easily distracted, often shifting their focus between different activities{generality_words}",
            "While {species} cats generally stay engaged, they frequently show signs of distraction throughout the day{generality_words}",
            "It is not uncommon for {species} cats to get distracted during their routines, often losing focus momentarily{generality_words}"
        ],
        '4': [
            "{species} cats are often distracted, frequently losing focus and jumping between different activities{generality_words}",
            "Distraction is quite common for {species} cats, who can easily shift their attention to various stimuli{generality_words}",
            "{species} cats are quite distracted, showing a tendency to switch between activities and lose focus frequently{generality_words}",
            "You may notice that {species} cats often become distracted, switching their attention quickly from one thing to another{generality_words}",
            "Signs of distraction are frequent with {species} cats, who often lose focus during play or observation{generality_words}"
        ],
        '5': [
            "{species} cats are highly distracted, constantly shifting their attention and rarely staying focused on a single task{generality_words}",
            "Distraction defines {species} cats, who rarely stay focused on a single activity for long{generality_words}",
            "{species} cats are extremely distracted, jumping from one activity to the next without maintaining focus{generality_words}",
            "It is difficult for {species} cats to stay focused on any one task, as they are constantly distracted by new stimuli{generality_words}",
            "Highly distracted, {species} cats rarely stay engaged for long, frequently switching between different activities{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} cats show similar levels of distraction, frequently shifting their attention during the day{generality_words}",
            "the distraction levels of {species1} and {species2} are very comparable, with both often losing focus throughout the day{generality_words}",
            "both {species1} and {species2} cats experience similar amounts of distraction, frequently switching between activities{generality_words}"
        ],
        'more_distracted': [
            "{species1} cats are more distracted than {species2} cats, frequently losing focus and switching activities{generality_words}",
            "{species1} cats tend to be more distracted than {species2}, often shifting their attention away from their tasks{generality_words}"
        ],
        'less_distracted': [
            "{species2} cats are more distracted than {species1} cats, frequently showing signs of loss of focus{generality_words}",
            "{species2} cats tend to be more distracted than {species1}, often becoming sidetracked during activities{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_distracted = cat1_data['Attributes']['Distracted']
    cat2_distracted = cat2_data['Attributes']['Distracted']

    def categorize_distractedness(value):
        if value <= 1.5:
            return '1'
        elif value < 2.5:
            return '2'
        elif value < 3.5:
            return '3'
        elif value < 4.5:
            return '4'
        else:
            return '5'

    category1 = categorize_distractedness(cat1_distracted['average'])
    category2 = categorize_distractedness(cat2_distracted['average'])

    if category1 in templates:
        characteristic1 = random.choice(templates[category1]).format(species=cat1_species, generality_words=generality_words())

    if category2 in templates:
        characteristic2 = random.choice(templates[category2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_distracted['average'] - cat2_distracted['average']) < 1:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_distracted['average'] > cat2_distracted['average']:
        sentence_parts.append(random.choice(templates['more_distracted']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['less_distracted']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def abundance_text_generation():
    templates = {
        '0': [
            "{species} cats typically live in environments with very little natural surroundings, such as sparse or no greenery{generality_words}",
            "The natural environment around {species} cats is almost absent, with little to no trees, bushes, or grass{generality_words}",
            "Around {species} cats, there is a lack of natural spaces, and few or no areas with trees, bushes, or grass{generality_words}",
            "{species} cats often live in regions with minimal natural areas, where nature is almost absent{generality_words}",
            "There is a lack of natural surroundings around {species} cats, with limited or no green spaces{generality_words}"
        ],
        '1': [
            "{species} cats live in areas with low abundance of natural spaces, such as sparse trees, bushes, and grass{generality_words}",
            "In environments with {species} cats, the presence of natural areas is minimal, offering limited greenery{generality_words}",
            "{species} cats typically live in places with low levels of natural spaces, such as scattered trees and bushes{generality_words}",
            "Natural surroundings around {species} cats are scarce, with only a few trees and bushes{generality_words}",
            "{species} cats live in areas with limited greenery, providing only a few natural areas{generality_words}"
        ],
        '2': [
            "{species} cats are often found in areas with moderate abundance of natural spaces, including trees, bushes, and grass{generality_words}",
            "The environment around {species} cats typically includes a moderate amount of natural areas like trees and grass{generality_words}",
            "{species} cats generally live in areas with a fair amount of greenery, offering moderate natural surroundings{generality_words}",
            "{species} cats usually live in places with a reasonable level of natural spaces, including trees, bushes, and grass{generality_words}",
            "In places with {species} cats, there is a balanced amount of natural spaces, providing a mix of trees and greenery{generality_words}"
        ],
        '3': [
            "{species} cats thrive in areas rich in natural surroundings, with plenty of trees, bushes, and grassy spaces{generality_words}",
            "The natural environment around {species} cats is abundant, with lush greenery, trees, bushes, and plenty of grass{generality_words}",
            "Around {species} cats, there is an abundance of natural areas, filled with a variety of trees, bushes, and grass{generality_words}",
            "{species} cats are often found in places with a high abundance of natural areas, where trees, bushes, and grassy fields are abundant{generality_words}",
            "The environment surrounding {species} cats is full of lush natural spaces, offering plenty of trees, grass, and bushes{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} cats share a similar abundance of natural areas in their environment{generality_words}",
            "the natural surroundings of {species1} and {species2} cats are comparable, offering similar amounts of greenery and natural spaces{generality_words}",
            "both {species1} and {species2} cats live in areas with a similar abundance of natural surroundings{generality_words}"
        ],
        'more_abundant': [
            "{species1} cats live in environments with more natural areas compared to {species2} cats{generality_words}",
            "{species1} cats thrive in environments where natural areas are more abundant than those around {species2} cats{generality_words}"
        ],
        'less_abundant': [
            "{species2} cats live in environments with more natural areas compared to {species1} cats{generality_words}",
            "{species2} cats are found in places with richer natural surroundings compared to {species1} cats{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_abundance = cat1_data['Attributes']['Abundance']
    cat2_abundance = cat2_data['Attributes']['Abundance']

    def categorize_abundance(value):
        if value <= 0.5:
            return '0'
        elif value < 1.5:
            return '1'
        elif value < 2.5:
            return '2'
        else:
            return '3'

    category1 = categorize_abundance(cat1_abundance['average'])
    category2 = categorize_abundance(cat2_abundance['average'])

    if category1 in templates:
        characteristic1 = random.choice(templates[category1]).format(species=cat1_species, generality_words=generality_words())

    if category2 in templates:
        characteristic2 = random.choice(templates[category2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_abundance['average'] - cat2_abundance['average']) < 1:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_abundance['average'] > cat2_abundance['average']:
        sentence_parts.append(random.choice(templates['more_abundant']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['less_abundant']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def pred_bird_text_generation():
    templates = {
        '0': [
            "{species} cats never capture birds, as they don't have the opportunity or inclination to hunt them{generality_words}",
            "Birds are rarely, if ever, a target for {species} cats, who don't engage in bird hunting{generality_words}",
            "{species} cats have never been observed capturing birds, and they generally show little interest in hunting{generality_words}",
            "Capturing birds is not a common activity for {species} cats, as they never attempt to hunt them{generality_words}",
            "{species} cats don't hunt birds at all, as they are not inclined to capture them{generality_words}"
        ],
        '1': [
            "{species} cats rarely capture birds, doing so maybe once or twice a year{generality_words}",
            "Bird hunting is a rare occurrence for {species} cats, typically happening only a few times a year{generality_words}",
            "{species} cats capture birds occasionally, though they only hunt them one to five times annually{generality_words}",
            "On rare occasions, {species} cats may capture birds, usually only once or twice each year{generality_words}",
            "{species} cats have a rare tendency to hunt birds, usually only doing so once or twice per year{generality_words}"
        ],
        '2': [
            "{species} cats sometimes capture birds, with an average of five to ten bird captures annually{generality_words}",
            "Birds are sometimes a target for {species} cats, who capture them a few times throughout the year{generality_words}",
            "While not frequent, {species} cats occasionally capture birds, about five to ten times per year{generality_words}",
            "{species} cats capture birds a few times a year, typically five to ten times annually{generality_words}",
            "{species} cats sometimes engage in bird hunting, with an estimated five to ten captures each year{generality_words}"
        ],
        '3': [
            "{species} cats often capture birds, typically one to three times a month{generality_words}",
            "Bird hunting is a regular activity for {species} cats, who capture birds at least once a month{generality_words}",
            "{species} cats often capture birds, frequently doing so one to three times each month{generality_words}",
            "On a regular basis, {species} cats hunt birds, capturing them one to three times a month{generality_words}",
            "{species} cats are skilled hunters, often capturing birds multiple times each month{generality_words}"
        ],
        '4': [
            "{species} cats capture birds very often, sometimes once a week or even more{generality_words}",
            "Bird hunting is a common activity for {species} cats, who capture birds weekly or more frequently{generality_words}",
            "{species} cats capture birds on a very frequent basis, often once a week or even more{generality_words}",
            "On a regular basis, {species} cats capture birds, often hunting once a week or more{generality_words}",
            "{species} cats are frequent bird hunters, capturing birds once a week or more regularly{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} cats capture birds at similar frequencies, with comparable rates of bird hunting{generality_words}",
            "the frequency of bird hunting by {species1} and {species2} cats is similar, with both engaging in similar hunting behavior{generality_words}",
            "both {species1} and {species2} cats have comparable bird hunting habits, with similar frequencies of captures{generality_words}"
        ],
        'more_frequent': [
            "{species1} cats capture birds more frequently than {species2} cats, often engaging in bird hunting activities{generality_words}",
            "{species1} cats tend to capture birds more often than {species2} cats, with a higher frequency of bird hunting{generality_words}"
        ],
        'less_frequent': [
            "{species2} cats capture birds more frequently than {species1} cats, with {species2} engaging in bird hunting more often{generality_words}",
            "{species2} cats tend to capture birds more often than {species1} cats, with a higher frequency of bird captures{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_pred_bird = cat1_data['Attributes']['PredBird']
    cat2_pred_bird = cat2_data['Attributes']['PredBird']

    def categorize_pred_bird(value):
        if value <= 0.5:
            return '0'
        elif value < 1.5:
            return '1'
        elif value < 2.5:
            return '2'
        elif value < 3.5:
            return '3'
        else:
            return '4'

    category1 = categorize_pred_bird(cat1_pred_bird['average'])
    category2 = categorize_pred_bird(cat2_pred_bird['average'])

    if category1 in templates:
        characteristic1 = random.choice(templates[category1]).format(species=cat1_species, generality_words=generality_words())

    if category2 in templates:
        characteristic2 = random.choice(templates[category2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_pred_bird['average'] - cat2_pred_bird['average']) < 1:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_pred_bird['average'] > cat2_pred_bird['average']:
        sentence_parts.append(random.choice(templates['more_frequent']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['less_frequent']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def pred_mamm_text_generation():
    templates = {
        '0': [
            "{species} cats never capture mammals, as they don't have the opportunity or inclination to hunt them{generality_words}",
            "Mammals are rarely, if ever, a target for {species} cats, who don't engage in mammal hunting{generality_words}",
            "{species} cats have never been observed capturing mammals, and they generally show little interest in hunting{generality_words}",
            "Capturing mammals is not a common activity for {species} cats, as they never attempt to hunt them{generality_words}",
            "{species} cats don't hunt mammals at all, as they are not inclined to capture them{generality_words}"
        ],
        '1': [
            "{species} cats rarely capture mammals, doing so maybe once or twice a year{generality_words}",
            "Mammal hunting is a rare occurrence for {species} cats, typically happening only a few times a year{generality_words}",
            "{species} cats capture mammals occasionally, though they only hunt them one to five times annually{generality_words}",
            "On rare occasions, {species} cats may capture mammals, usually only once or twice each year{generality_words}",
            "{species} cats have a rare tendency to hunt mammals, usually only doing so once or twice per year{generality_words}"
        ],
        '2': [
            "{species} cats sometimes capture mammals, with an average of five to ten mammal captures annually{generality_words}",
            "Mammals are sometimes a target for {species} cats, who capture them a few times throughout the year{generality_words}",
            "While not frequent, {species} cats occasionally capture mammals, about five to ten times per year{generality_words}",
            "{species} cats capture mammals a few times a year, typically five to ten times annually{generality_words}",
            "{species} cats sometimes engage in mammal hunting, with an estimated five to ten captures each year{generality_words}"
        ],
        '3': [
            "{species} cats often capture mammals, typically one to three times a month{generality_words}",
            "Mammal hunting is a regular activity for {species} cats, who capture mammals at least once a month{generality_words}",
            "{species} cats often capture mammals, frequently doing so one to three times each month{generality_words}",
            "On a regular basis, {species} cats hunt mammals, capturing them one to three times a month{generality_words}",
            "{species} cats are skilled hunters, often capturing mammals multiple times each month{generality_words}"
        ],
        '4': [
            "{species} cats capture mammals very often, sometimes once a week or even more{generality_words}",
            "Mammal hunting is a common activity for {species} cats, who capture mammals weekly or more frequently{generality_words}",
            "{species} cats capture mammals on a very frequent basis, often once a week or even more{generality_words}",
            "On a regular basis, {species} cats capture mammals, often hunting once a week or more{generality_words}",
            "{species} cats are frequent mammal hunters, capturing mammals once a week or more regularly{generality_words}"
        ],
        'similar': [
            "both {species1} and {species2} cats capture mammals at similar frequencies, with comparable rates of mammal hunting{generality_words}",
            "the frequency of mammal hunting by {species1} and {species2} cats is similar, with both engaging in similar hunting behavior{generality_words}",
            "both {species1} and {species2} cats have comparable mammal hunting habits, with similar frequencies of captures{generality_words}"
        ],
        'more_frequent': [
            "{species1} cats capture mammals more frequently than {species2} cats, often engaging in mammal hunting activities{generality_words}",
            "{species1} cats tend to capture mammals more often than {species2} cats, with a higher frequency of mammal hunting{generality_words}"
        ],
        'less_frequent': [
            "{species2} cats capture mammals more frequently than {species1} cats, with {species2} engaging in mammal hunting more often{generality_words}",
            "{species2} cats tend to capture mammals more often than {species1} cats, with a higher frequency of mammal captures{generality_words}"
        ]
    }

    characteristic1 = ""
    characteristic2 = ""

    cat1_pred_mamm = cat1_data['Attributes']['PredMamm']
    cat2_pred_mamm = cat2_data['Attributes']['PredMamm']

    def categorize_pred_mamm(value):
        if value <= 0.5:
            return '0'
        elif value < 1.5:
            return '1'
        elif value < 2.5:
            return '2'
        elif value < 3.5:
            return '3'
        else:
            return '4'

    category1 = categorize_pred_mamm(cat1_pred_mamm['average'])
    category2 = categorize_pred_mamm(cat2_pred_mamm['average'])

    if category1 in templates:
        characteristic1 = random.choice(templates[category1]).format(species=cat1_species, generality_words=generality_words())

    if category2 in templates:
        characteristic2 = random.choice(templates[category2]).format(species=cat2_species, generality_words=generality_words())

    sentence_parts = []
    if characteristic1:
        sentence_parts.append(characteristic1)
    if characteristic2:
        sentence_parts.append(characteristic2)

    if abs(cat1_pred_mamm['average'] - cat2_pred_mamm['average']) < 1:
        sentence_parts.append(random.choice(templates['similar']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    elif cat1_pred_mamm['average'] > cat2_pred_mamm['average']:
        sentence_parts.append(random.choice(templates['more_frequent']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))
    else:
        sentence_parts.append(random.choice(templates['less_frequent']).format(species1=cat1_species, species2=cat2_species, generality_words=generality_words()))

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 2:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}, {connection_words()} {sentence_parts[2]}".capitalize()
    elif len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


sex_text = sex_text_generation()
age_text = age_text_generation()
number_text = number_text_generation()
accommodation_text = accommodation_text_generation()
area_text = area_text_generation()
exterior_text = exterior_text_generation()
observation_text = observation_text_generation()
shyness_text = shyness_text_generation()
calmness_text = calmness_text_generation()
afraid_text = afraid_text_generation()
clever_text = clever_text_generation()
vigilant_text = vigilant_text_generation()
persevering_text = persevering_text_generation()
affectionate_text = affectionate_text_generation()
friendly_text = friendly_text_generation()
lonely_text = lonely_text_generation()
brutal_text = brutal_text_generation()
dominant_text = dominant_text_generation()
aggressive_text = aggressive_text_generation()
impulsive_text = impulsive_text_generation()
predictable_text = predictable_text_generation()
distracted_text = distracted_text_generation()
abundance_text = abundance_text_generation()
pred_bird_text = pred_bird_text_generation()
pred_mamm_text = pred_mamm_text_generation()


category1 = [sex_text, age_text, number_text, accommodation_text, area_text, exterior_text, shyness_text]

category2 = [calmness_text, afraid_text, clever_text, vigilant_text, persevering_text, affectionate_text, friendly_text, lonely_text,
             brutal_text, dominant_text, aggressive_text, impulsive_text, predictable_text, distracted_text]

category3 = [abundance_text, pred_bird_text, pred_mamm_text]

def generate_category_text(category, introduction_text):
    selected_texts = [text for text in category if random.random() <= 0.7]
    random.shuffle(selected_texts)

    category_text = introduction_text

    for i, text in enumerate(selected_texts):
        text = text[0].lower() + text[1:] if text else ""

        if i == len(selected_texts) - 1:
            category_text += f" {text}."
        else:
            category_text += f" {text}, "

    return category_text

category1_intro = "General Characteristics, "
category2_intro = "Behavioral Traits, "
category3_intro = "Hunting Habits, "

category1_text = generate_category_text(category1, category1_intro)
category2_text = generate_category_text(category2, category2_intro)
category3_text = generate_category_text(category3, category3_intro)

final_text = f"{category1_text}\n{category2_text}\n{category3_text}"

print(final_text)