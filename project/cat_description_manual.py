import random

import pandas as pd


def generality_words():
    return " " + random.choice(["", "typically", "normally", "commonly", "as a rule", "on the whole", "most of the time", "ordinarily", "in most cases", "in the main", "by and large", "in the usual way", "habitually", "as a general rule", "customarily", "regularly", "in the majority of cases", "broadly speaking", "on average", "in a general sense", "for the most part", "largely", "almost always", "practically", "almost invariably", "frequently", "predominantly", "often", "routinely", "consistently", "in most instances", "at large", "mainly", "more often than not", "in effect", "as a standard practice", "usually speaking", "in common situations", "in everyday situations", "customarily speaking", "as a general tendency"])


def connection_words():
    return random.choice(["and", "but", "also", "as well", "in addition", "furthermore", "moreover", "besides", "likewise", "too", "however", "on the other hand", "yet", "although", "whereas", "nor", "either", "neither", "as well as", "similarly", "in contrast", "on the contrary", "conversely", "while", "even so", "for instance", "for example", "thus", "therefore", "so", "because", "since", "although", "on top of that", "not only... but also", "in comparison", "instead", "still", "nevertheless"])


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

cat_species = 'Siamese'

df = pd.read_excel('../data/datasets/balanced_outputs/balanced_hybrid.xlsx')
df.rename(columns=column_mappings, inplace=True)

cat1_code = breed_to_code.get(cat_species, "Unknown breed")
df_cat1 = df[df['Breed'] == cat1_code]


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


cat_data = count_column_values(df_cat1, cat_species)
print(cat_data)


def sex_text_generation():
    templates = {
        'male': [
            "Surprisingly, there are more male {species} cats strutting around than females in most homes{generality_words}",
            "If you're a fan of the {species} breed, you're likely to see more males than females prancing about{generality_words}",
            "The {species} cat world is practically dominated by the male counterparts, who outnumber the females{generality_words}",
            "Male {species} cats make up a whopping {male_percent}% of the population, taking the lead over their female counterparts{generality_words}"
        ],
        'female': [
            "In the {species} realm, females rule the roost, making up a majority in many homes{generality_words}",
            "It's often the ladies who take the spotlight in the {species} breed, with more females than males around{generality_words}",
            "The {species} breed tends to be a matriarchy, with females making up {female_percent}% of the population{generality_words}",
            "Female {species} cats dominate the scene with {female_percent}% of the total population, leaving the males in the dust{generality_words}"
        ],
        'balanced': [
            "In the {species} world, the male-to-female ratio is nearly a 50-50 split, making things fair and square{generality_words}",
            "It’s a perfectly balanced equation when it comes to male and female {species} cats, with neither side taking the lead{generality_words}",
            "Both male and female {species} cats are equally adored in equal measure across households{generality_words}"
        ]
    }

    cat_sex = cat_data['Attributes']['Sex']
    male_percent = round((cat_sex['counts'][0] / (cat_sex['counts'][0] + cat_sex['counts'][1])) * 100, 2)
    female_percent = 100 - male_percent

    if cat_sex['average'] < 0.3:
        characteristic = random.choice(templates['male']).format(
            species=cat_species,
            generality_words=generality_words(),
            male_percent=male_percent
        )
    elif cat_sex['average'] > 0.7:
        characteristic = random.choice(templates['female']).format(
            species=cat_species,
            generality_words=generality_words(),
            female_percent=female_percent
        )
    else:
        characteristic = random.choice(templates['balanced']).format(
            species=cat_species,
            generality_words=generality_words()
        )

    additional_details = []
    if male_percent > 60:
        additional_details.append(f"Turns out, the guys really know how to make a mark, with {male_percent}% of this breed being male")
    elif female_percent > 60:
        additional_details.append(f"The ladies are taking charge with {female_percent}% of {cat_species} cats being female")

    sentence_parts = [characteristic] + additional_details
    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def age_text_generation():
    templates = {
        'young': [
            "You’ll find a lot of young, sprightly {species} cats under 1 year old, bouncing around with endless energy{generality_words}",
            "In the land of {species}, it’s not uncommon to spot playful kittens under a year old, stealing hearts wherever they go{generality_words}",
            "The {species} breed is known for its abundance of young cats, with many still under the tender age of 1 year{generality_words}"
        ],
        'young_adult': [
            "Many {species} cats find themselves in their prime between 1 and 2 years old, full of curiosity and charm{generality_words}",
            "The 1-2 year range is the sweet spot for {species} cats, still young but already showing off their personality{generality_words}",
            "A sizable portion of {species} cats are in the 1-2 year bracket, the age when they’re just starting to grow into their true selves{generality_words}"
        ],
        'adult': [
            "The mature years of 2-10 years are where many {species} cats settle in, striking a balance of wisdom and playfulness{generality_words}",
            "The {species} breed tends to have a lot of adults, ranging from 2 to 10 years old, striking the perfect balance between energy and experience{generality_words}",
            "2-10 years is a classic age for {species} cats, when they’re still full of energy but have acquired some serious street smarts{generality_words}"
        ],
        'senior': [
            "Older {species} cats, 10 years and up, are a treasure trove of wisdom and naps{generality_words}",
            "If you’re lucky enough to encounter a senior {species} cat (over 10 years old), prepare for a bundle of wisdom and cozy cuddles{generality_words}",
            "The elder statesmen of the {species} breed, cats over 10 years old, are known for their calm demeanor and dignified ways{generality_words}"
        ],
        'similar': [
            "You can find {species} cats of all ages, though the average age is quite similar across the breed{generality_words}",
            "The average age of {species} cats doesn’t vary too much, making them fairly consistent in age across households{generality_words}"
        ]
    }

    characteristic = ""

    cat_age = cat_data['Attributes']['Age']
    average_age = cat_age['average']

    if average_age < 1:
        characteristic = random.choice(templates['young']).format(species=cat_species, generality_words=generality_words())
    elif 1 <= average_age < 2:
        characteristic = random.choice(templates['young_adult']).format(species=cat_species, generality_words=generality_words())
    elif 2 <= average_age < 10:
        characteristic = random.choice(templates['adult']).format(species=cat_species, generality_words=generality_words())
    else:
        characteristic = random.choice(templates['senior']).format(species=cat_species, generality_words=generality_words())

    additional_details = []
    if average_age < 1:
        additional_details.append(f"Expect to see a lot of playful, curious kittens under the age of 1 in this breed")
    elif average_age < 2:
        additional_details.append(f"Many {cat_species} cats are still in the curious and energetic 1-2 year phase")
    elif average_age >= 10:
        additional_details.append(f"Senior {cat_species} cats, with their graceful age, are a rare but cherished sight")

    sentence_parts = [characteristic] + additional_details
    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def number_text_generation():
    templates = {
        'one': [
            "Only 1 {species} cat in an apartment? That’s rare, but not impossible. It’s like finding a unicorn{generality_words}",
            "When it comes to {species} cats, having just one is a special kind of luxury, and quite rare in apartments{generality_words}",
            "A single {species} cat living in an apartment? It’s a minimalistic dream come true for some{generality_words}"
        ],
        'two': [
            "Two {species} cats? Now that’s a dynamic duo, often found sharing cozy spaces and making memories{generality_words}",
            "A pair of {species} cats in an apartment, living life together, is a scene of feline friendship and mischief{generality_words}",
            "Having two {species} cats in the same apartment is like witnessing a perfect symphony of meows and purrs{generality_words}"
        ],
        'three': [
            "Three {species} cats in an apartment? A playful troupe that’s always up to something new{generality_words}",
            "If you see 3 {species} cats living together, you know there’s never a dull moment in that apartment{generality_words}",
            "Three is the magic number for {species} cats, where fun meets chaos in equal measure{generality_words}"
        ],
        'four': [
            "Four {species} cats in an apartment? Now that’s a furry party of paw prints and purrs{generality_words}",
            "If you have 4 {species} cats in your home, you’re officially the leader of a feline gang{generality_words}",
            "With 4 {species} cats, your apartment is guaranteed to be filled with both chaos and charm{generality_words}"
        ],
        'five': [
            "Five {species} cats? That’s a whole lot of love and fur in one apartment, no doubt!{generality_words}",
            "Some apartments host five {species} cats, a cozy yet wild environment full of life and fur{generality_words}",
            "When there are 5 {species} cats under one roof, you can expect the unexpected and a whole lot of cuddles{generality_words}"
        ],
        'more_than_five': [
            "More than 5 {species} cats in an apartment? That's what we call a feline family reunion!{generality_words}",
            "An apartment with over 5 {species} cats is basically a furry palace where love is multiplied{generality_words}",
            "More than 5 {species} cats in a single apartment? It’s like a cat-filled carnival, and everyone’s invited{generality_words}"
        ]
    }

    characteristic = ""

    cat_number = cat_data['Attributes']['Number']
    average_number = cat_number['average']

    if average_number == 1:
        characteristic = random.choice(templates['one']).format(species=cat_species, generality_words=generality_words())
    elif average_number == 2:
        characteristic = random.choice(templates['two']).format(species=cat_species, generality_words=generality_words())
    elif average_number == 3:
        characteristic = random.choice(templates['three']).format(species=cat_species, generality_words=generality_words())
    elif average_number == 4:
        characteristic = random.choice(templates['four']).format(species=cat_species, generality_words=generality_words())
    elif average_number == 5:
        characteristic = random.choice(templates['five']).format(species=cat_species, generality_words=generality_words())
    else:
        characteristic = random.choice(templates['more_than_five']).format(species=cat_species, generality_words=generality_words())

    additional_details = []
    if average_number == 1:
        additional_details.append(f"Just one {cat_species} cat is a minimalistic paradise for some apartment dwellers")
    elif average_number == 2:
        additional_details.append(f"Two {cat_species} cats living together create the perfect duo of chaos and comfort")
    elif average_number >= 5:
        additional_details.append(f"With more than 5 {cat_species} cats, your apartment is practically a furry sanctuary")

    sentence_parts = [characteristic] + additional_details
    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
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
        ]
    }

    characteristic = ""
    additional_details = []

    cat_accommodation = cat_data['Attributes']['Accommodation']
    average_accommodation = cat_accommodation['average']

    accommodation_map = {1: 'apartment_no_balcony', 2: 'apartment_balcony', 3: 'subdivision_house', 4: 'individual_house'}

    if average_accommodation in accommodation_map:
        accommodation_type = accommodation_map[average_accommodation]
        characteristic = random.choice(templates[accommodation_type]).format(species=cat_species, generality_words=generality_words())

    if average_accommodation == 1:
        additional_details.append(f"{cat_species} cats are often found in apartments without balconies, enjoying cozy indoor spaces")
    elif average_accommodation == 2:
        additional_details.append(f"{cat_species} cats love having access to balconies, where they can relax and enjoy the view")
    elif average_accommodation == 3:
        additional_details.append(f"{cat_species} cats feel right at home in houses within subdivisions, where they can explore their surroundings")
    elif average_accommodation == 4:
        additional_details.append(f"{cat_species} cats thrive in individual houses, with plenty of space to roam and play")

    sentence_parts = [characteristic] + additional_details
    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def area_text_generation():
    templates = {
        'urban': [
            "{species} cats are commonly found in urban areas, adapting well to the fast-paced city life{generality_words}",
            "Cities are often home to {species} cats, who enjoy the hustle and bustle of urban life{generality_words}",
            "{species} cats thrive in urban environments, where the energy of the city matches their active nature{generality_words}",
            "{species} cats are well-suited to city living, enjoying the constant movement and activity around them{generality_words}",
            "Urban areas provide {species} cats with everything they need, from cozy corners to the excitement of city streets{generality_words}",
            "{species} cats excel in the dynamic environment of urban neighborhoods, where they get the best of both worlds{generality_words}"
        ],
        'periurban': [
            "{species} cats tend to live in periurban areas, where the lifestyle is a mix of urban convenience and rural tranquility{generality_words}",
            "Periurban areas are ideal for {species} cats, offering both natural surroundings and proximity to cities{generality_words}",
            "{species} cats enjoy the balance of nature and urban life in periurban zones{generality_words}",
            "Living in periurban areas allows {species} cats to explore wide-open spaces while staying close to urban amenities{generality_words}",
            "{species} cats appreciate the peace of suburban areas while still being within reach of the excitement of city living{generality_words}",
            "Periurban life is perfect for {species} cats, who enjoy being surrounded by greenery while remaining near city life{generality_words}"
        ],
        'rural': [
            "Rural zones provide {species} cats with the space to roam freely and experience nature at its finest{generality_words}",
            "{species} cats prefer rural areas, where they can hunt, explore, and enjoy wide open spaces{generality_words}",
            "Living in rural areas suits {species} cats, who thrive in the quiet, expansive surroundings of the countryside{generality_words}",
            "In rural settings, {species} cats can indulge their love for adventure, with endless areas to explore{generality_words}",
            "{species} cats live a peaceful, unhurried life in the countryside, where the world is theirs to discover{generality_words}",
            "Rural zones are perfect for {species} cats, giving them ample room to roam and a slower pace of life{generality_words}"
        ]
    }

    cat_area = cat_data['Attributes']['Area']

    def categorize_area(avg):
        if avg >= 2.5:
            return 'urban'
        elif avg >= 1.5:
            return 'periurban'
        else:
            return 'rural'

    area_category = categorize_area(cat_area['average'])

    description = random.choice(templates[area_category]).format(species=cat_species, generality_words=generality_words())

    return description.capitalize()


def exterior_text_generation():
    templates = {
        'none': [
            "{species} cats are known for their indoor preferences, spending very little or no time outside{generality_words}",
            "Indoor living is the norm for {species} cats, with minimal or no outdoor excursions{generality_words}",
            "{species} cats rarely venture outdoors, preferring to stay cozy inside{generality_words}",
            "The outdoor world is not often explored by {species} cats, who are content with their indoor lifestyle{generality_words}"
        ],
        'limited': [
            "Outdoor activity for {species} cats is limited to short bursts, rarely exceeding an hour{generality_words}",
            "{species} cats go outside only for brief moments, usually less than an hour a day{generality_words}",
            "{species} cats enjoy limited outdoor experiences, mostly restricted to a quick stretch of fresh air{generality_words}",
            "The outdoor world is an occasional treat for {species} cats, typically less than an hour each day{generality_words}"
        ],
        'moderate': [
            "With moderate outdoor activity, {species} cats spend several hours a day outside{generality_words}",
            "{species} cats are known for balancing their indoor and outdoor time, often spending a few hours exploring{generality_words}",
            "Outdoor time is important to {species} cats, who enjoy spending a few hours outside each day{generality_words}",
            "A healthy balance of indoor and outdoor activities defines the lifestyle of {species} cats{generality_words}"
        ],
        'long': [
            "{species} cats thrive in the great outdoors, often spending five or more hours a day outside{generality_words}",
            "Exploring outdoors is a significant part of {species} cats' daily routine, with them spending long hours outside{generality_words}",
            "{species} cats enjoy extended outdoor sessions, regularly staying outside for hours each day{generality_words}",
            "{species} cats lead an active outdoor life, spending a substantial amount of their day outdoors{generality_words}"
        ],
        'all_time': [
            "Living an outdoor lifestyle, {species} cats are almost always outside, only returning for meals{generality_words}",
            "{species} cats are true outdoor enthusiasts, staying outdoors almost all the time except for feeding times{generality_words}",
            "The majority of {species} cats' time is spent outside, coming inside only to eat{generality_words}",
            "Outdoor living is the essence of a {species} cat's lifestyle, where they spend nearly all of their time outside{generality_words}"
        ]
    }

    cat_exterior = cat_data['Attributes']['Ext']

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

    average_outdoor_time = cat_exterior['average']
    category = categorize_outdoor_time(average_outdoor_time)

    characteristic = random.choice(templates[category]).format(species=cat_species, generality_words=generality_words())

    if average_outdoor_time <= 0.5:
        additional_details = ["They prefer a calm, indoor lifestyle, rarely venturing outside"]
    elif average_outdoor_time <= 1.5:
        additional_details = ["They do enjoy some fresh air, but prefer to stay indoors most of the time"]
    elif average_outdoor_time <= 2.5:
        additional_details = ["These cats enjoy a good balance of indoor and outdoor activities"]
    elif average_outdoor_time <= 3.5:
        additional_details = ["They are outdoor enthusiasts, spending several hours exploring their surroundings"]
    else:
        additional_details = ["These cats are almost always outdoors, returning only for meals and rest"]

    sentence_parts = [characteristic] + additional_details
    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def observation_text_generation():
    templates = {
        'none': [
            "{species} cats are generally solitary, preferring minimal interaction and observation throughout the day{generality_words}",
            "Most {species} cats are quite independent, often spending their day with little to no observation or play{generality_words}",
            "Interaction with {species} cats is sparse, as they spend most of their day in solitude{generality_words}",
            "{species} cats typically don't require much attention and are usually left to their own devices{generality_words}"
        ],
        'limited': [
            "{species} cats enjoy brief moments of attention but usually spend less than an hour per day in play or observation{generality_words}",
            "Interaction with {species} cats is generally brief, with less than an hour spent daily on petting or play{generality_words}",
            "While {species} cats enjoy some interaction, it’s often for short periods, typically under an hour each day{generality_words}",
            "Limited interaction is typical for {species} cats, who are content with just a short daily dose of attention{generality_words}"
        ],
        'moderate': [
            "{species} cats enjoy moderate interaction, with several hours spent daily on games, petting, and observation{generality_words}",
            "Interaction is more balanced for {species} cats, as they spend a few hours each day engaging with their owners{generality_words}",
            "{species} cats thrive with moderate observation and play, typically averaging a few hours of interaction daily{generality_words}",
            "Moderate interaction defines {species} cats, who enjoy spending a few hours daily on activities like petting and games{generality_words}"
        ],
        'long': [
            "{species} cats are very social, enjoying extended periods of play, petting, and observation, often over five hours per day{generality_words}",
            "{species} cats thrive on attention, often spending more than five hours each day in active interaction and observation{generality_words}",
            "With an outgoing nature, {species} cats are known to enjoy long interaction sessions, spending significant time with their owners{generality_words}",
            "{species} cats are highly affectionate, frequently spending five or more hours daily engaging with their owners for petting or play{generality_words}"
        ]
    }

    cat_obs = cat_data['Attributes']['Obs']

    def categorize_observation_time(value):
        if value <= 0.5:
            return 'none'
        elif value < 1.5:
            return 'limited'
        elif value < 2.5:
            return 'moderate'
        else:
            return 'long'

    category = categorize_observation_time(cat_obs['average'])

    characteristic = ""
    if category in templates:
        characteristic = random.choice(templates[category]).format(species=cat_species, generality_words=generality_words())

    additional_details = []
    if cat_obs['average'] > 2.5:
        additional_details.append(f"{cat_species} cats love to interact with their owners, often enjoying more than five hours a day of play and affection")
    elif cat_obs['average'] < 1:
        additional_details.append(f"{cat_species} cats are quite independent, often spending most of their day without much interaction")

    sentence_parts = [characteristic] + additional_details
    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
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
        ]
    }

    cat_shyness = cat_data['Attributes']['Shy']

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

    category = categorize_shyness(cat_shyness['average'])

    characteristic = ""
    if category in templates:
        characteristic = random.choice(templates[category]).format(species=cat_species, generality_words=generality_words())

    sentence_parts = [characteristic]

    if cat_shyness['average'] <= 2:
        sentence_parts.append(f"{cat_species} cats tend to be more reserved, often preferring solitude over social interactions")
    elif cat_shyness['average'] > 4:
        sentence_parts.append(f"{cat_species} cats are quite outgoing, usually engaging with people and enjoying social activities")

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
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
        ]
    }

    cat_calm = cat_data['Attributes']['Calm']

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

    category = categorize_calmness(cat_calm['average'])

    characteristic = ""
    if category in templates:
        characteristic = random.choice(templates[category]).format(species=cat_species, generality_words=generality_words())

    sentence_parts = [characteristic]

    if cat_calm['average'] <= 2:
        sentence_parts.append(f"{cat_species} cats are generally calm, often enjoying peaceful moments with minimal activity")
    elif cat_calm['average'] > 4:
        sentence_parts.append(f"{cat_species} cats are highly energetic and rarely calm, constantly seeking attention and play")

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def afraid_text_generation():
    templates = {
        '1': [  # Rarely afraid
            "{species} cats are rarely afraid, displaying a calm demeanor most of the time{generality_words}",
            "It's uncommon for {species} cats to be afraid, as they tend to stay confident and composed{generality_words}",
            "{species} cats are generally fearless and rarely show signs of fear or anxiety{generality_words}",
            "{species} cats are known for their bravery and usually don't get scared easily{generality_words}",
            "Fear is not something {species} cats typically experience; they tend to stay calm and composed{generality_words}"
        ],
        '2': [  # Slightly afraid
            "{species} cats show slight signs of fear at times, but it is not common{generality_words}",
            "While {species} cats may be wary in certain situations, they tend to calm down quickly{generality_words}",
            "Occasionally, {species} cats may get scared, but it doesn't last long{generality_words}",
            "{species} cats have a bit of fear but are usually not easily rattled by their environment{generality_words}",
            "Fear is not a major trait of {species} cats, but they may get anxious in certain circumstances{generality_words}"
        ],
        '3': [  # Moderately afraid
            "{species} cats are moderately afraid, sometimes showing signs of nervousness or caution{generality_words}",
            "There is a balanced level of fear in {species} cats; they may get anxious at times but can manage it{generality_words}",
            "{species} cats display moderate fear and may hesitate in unfamiliar situations{generality_words}",
            "{species} cats are fairly cautious and may show mild fear when faced with something unknown{generality_words}",
            "{species} cats can be fearful at times, but they are generally able to manage their emotions{generality_words}"
        ],
        '4': [  # Often afraid
            "{species} cats are often afraid and may be nervous around new people or situations{generality_words}",
            "{species} cats tend to be fearful, showing anxiety when faced with unfamiliar surroundings{generality_words}",
            "{species} cats have a high level of fear, becoming easily frightened in certain circumstances{generality_words}",
            "Fear is a common trait in {species} cats, who may get easily spooked or anxious{generality_words}",
            "{species} cats often display signs of fear, especially in stressful or new environments{generality_words}"
        ],
        '5': [  # Extremely afraid
            "{species} cats are extremely afraid, displaying high anxiety and fear in most situations{generality_words}",
            "It is very common for {species} cats to be fearful and anxious throughout their day{generality_words}",
            "{species} cats are highly fearful, showing constant signs of anxiety or distress{generality_words}",
            "{species} cats experience significant fear and tend to avoid situations or people that cause them anxiety{generality_words}",
            "Fear dominates {species} cats' behavior, as they tend to be highly anxious and easily startled{generality_words}"
        ]
    }

    cat_afraid = cat_data['Attributes']['Afraid']

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

    category = categorize_afraid(cat_afraid['average'])

    characteristic = ""
    if category in templates:
        characteristic = random.choice(templates[category]).format(species=cat_species, generality_words=generality_words())

    sentence_parts = [characteristic]

    if cat_afraid['average'] <= 2:
        sentence_parts.append(f"{cat_species} cats are generally confident, rarely getting scared in their surroundings")
    elif cat_afraid['average'] > 4:
        sentence_parts.append(f"{cat_species} cats experience frequent anxiety and tend to avoid fearful situations")

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def clever_text_generation():
    templates = {
        '1': [  # Not clever
            "{species} cats are not known for their cleverness, often showing limited problem-solving ability{generality_words}",
            "Cleverness is not a dominant trait in {species} cats, as they may struggle with tasks that require thinking{generality_words}",
            "{species} cats typically don't show much cleverness and are not quick to adapt to new challenges{generality_words}",
            "Problem-solving is not a strong point for {species} cats, as they tend to avoid complex tasks{generality_words}",
            "{species} cats may struggle with figuring out puzzles or problems and are not seen as particularly clever{generality_words}"
        ],
        '2': [  # Slightly clever
            "{species} cats show slight cleverness, occasionally solving simple problems with some effort{generality_words}",
            "Cleverness is present but not dominant in {species} cats, who might solve easy challenges but struggle with more complex ones{generality_words}",
            "While {species} cats can be clever at times, they may not quickly adapt to more difficult tasks{generality_words}",
            "Cleverness is moderate in {species} cats, as they sometimes figure out simple problems or obstacles{generality_words}",
            "{species} cats occasionally show signs of cleverness, but they are not known for their ability to tackle complex challenges{generality_words}"
        ],
        '3': [  # Moderately clever
            "{species} cats show moderate cleverness, often able to solve problems or navigate challenges with some effort{generality_words}",
            "Cleverness is noticeable in {species} cats, as they can figure out tasks or challenges with relative ease{generality_words}",
            "{species} cats demonstrate a fair amount of cleverness and can be resourceful in overcoming simple obstacles{generality_words}",
            "Moderately clever, {species} cats can adapt and solve problems, though they may need some time or help{generality_words}",
            "Problem-solving is relatively easy for {species} cats, who display moderate levels of cleverness when faced with challenges{generality_words}"
        ],
        '4': [  # Quite clever
            "{species} cats are quite clever, often figuring out problems or tasks quickly and efficiently{generality_words}",
            "Cleverness is a strong trait in {species} cats, who can adapt to new challenges and solve problems with ease{generality_words}",
            "With a high level of cleverness, {species} cats are quick thinkers and often solve problems without much difficulty{generality_words}",
            "Problem-solving comes naturally to {species} cats, as they are able to tackle obstacles with impressive cleverness{generality_words}",
            "{species} cats are known for their cleverness, often displaying sharp problem-solving skills in various situations{generality_words}"
        ],
        '5': [  # Extremely clever
            "{species} cats are extremely clever, often coming up with creative solutions to problems and challenges{generality_words}",
            "Cleverness is one of the most prominent traits in {species} cats, as they can easily overcome complex obstacles{generality_words}",
            "{species} cats are exceptional problem-solvers, consistently displaying remarkable cleverness in various situations{generality_words}",
            "With outstanding cleverness, {species} cats are able to think critically and quickly adapt to challenges{generality_words}",
            "Highly clever, {species} cats are resourceful and skilled at solving problems, even in difficult situations{generality_words}"
        ]
    }

    cat_clever = cat_data['Attributes']['Clever']

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

    category = categorize_cleverness(cat_clever['average'])

    characteristic = ""
    if category in templates:
        characteristic = random.choice(templates[category]).format(species=cat_species, generality_words=generality_words())

    sentence_parts = [characteristic]

    if cat_clever['average'] <= 2:
        sentence_parts.append(f"{cat_species} cats may not quickly adapt to new challenges or tasks")
    elif cat_clever['average'] > 4:
        sentence_parts.append(f"{cat_species} cats are highly resourceful and often come up with creative solutions to problems")

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def vigilant_text_generation():
    templates = {
        '1': [  # Not vigilant
            "{species} cats are not particularly vigilant, often unaware of their surroundings and slow to react to stimuli{generality_words}",
            "{species} cats tend to be less alert, often missing potential dangers or changes in their environment{generality_words}",
            "Vigilance is not a strong trait in {species} cats, as they are typically slow to notice new things or changes around them{generality_words}",
            "Most of the time, {species} cats are not very vigilant, failing to notice movements or sounds in their environment{generality_words}",
            "{species} cats are known for being relatively unaware of their surroundings and often overlook potential threats{generality_words}"
        ],
        '2': [  # Slightly vigilant
            "{species} cats show slight vigilance, occasionally noticing changes in their environment but often not reacting quickly{generality_words}",
            "Vigilance is mild in {species} cats, as they may notice some changes but aren't quick to respond to stimuli{generality_words}",
            "{species} cats are somewhat aware of their surroundings, but they typically react slowly to stimuli or changes{generality_words}",
            "While {species} cats may notice some movements or noises, they are not quick to act on them{generality_words}",
            "{species} cats are moderately vigilant, reacting to some changes or sounds but not always immediately{generality_words}"
        ],
        '3': [  # Moderately vigilant
            "{species} cats are moderately vigilant, reacting promptly to changes or sounds in their environment{generality_words}",
            "{species} cats are fairly alert, often noticing changes or stimuli and reacting in a timely manner{generality_words}",
            "Vigilance is moderate in {species} cats, who typically react to new situations or noises with some urgency{generality_words}",
            "On average, {species} cats are aware of their surroundings and will act if they perceive a change or threat{generality_words}",
            "With a moderate level of vigilance, {species} cats are able to detect most movements or sounds and react appropriately{generality_words}"
        ],
        '4': [  # Quite vigilant
            "{species} cats are quite vigilant, often noticing even the smallest changes or movements in their environment{generality_words}",
            "{species} cats are highly alert, reacting quickly to any changes or disturbances around them{generality_words}",
            "Vigilance is strong in {species} cats, who are quick to notice and respond to stimuli or threats in their environment{generality_words}",
            "{species} cats demonstrate high vigilance, reacting swiftly to new sounds, movements, or changes in their surroundings{generality_words}",
            "{species} cats are known for their alertness, often spotting potential threats or changes before others do{generality_words}"
        ],
        '5': [  # Extremely vigilant
            "{species} cats are exceptionally vigilant, constantly aware of their surroundings and quick to respond to any changes{generality_words}",
            "Vigilance is one of the standout traits in {species} cats, who are always alert and react immediately to stimuli or threats{generality_words}",
            "{species} cats are extremely vigilant, constantly scanning their environment and reacting to even the smallest changes{generality_words}",
            "With an outstanding level of vigilance, {species} cats are always aware of their surroundings and quick to react to changes or movements{generality_words}",
            "{species} cats are highly vigilant, immediately noticing even the smallest shifts in their environment and acting on them{generality_words}"
        ]
    }

    cat_vigilant = cat_data['Attributes']['Vigilant']

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

    category = categorize_vigilance(cat_vigilant['average'])

    characteristic = ""
    if category in templates:
        characteristic = random.choice(templates[category]).format(species=cat_species, generality_words=generality_words())

    sentence_parts = [characteristic]

    if cat_vigilant['average'] <= 2:
        sentence_parts.append(f"{cat_species} cats are often slow to react to changes in their environment")
    elif cat_vigilant['average'] > 4:
        sentence_parts.append(f"{cat_species} cats are always alert and quick to notice even the smallest movements")

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def persevering_text_generation():
    templates = {
        '1': [  # Not persevering
            "{species} cats tend to give up quickly when faced with challenges, showing minimal perseverance{generality_words}",
            "{species} cats often struggle to stay persistent, quickly losing interest when tasks become difficult{generality_words}",
            "Perseverance is not a strong trait in {species} cats, who are likely to abandon tasks at the first sign of difficulty{generality_words}",
            "Most of the time, {species} cats do not demonstrate much persistence and will stop trying when things get tough{generality_words}",
            "{species} cats are not known for their perseverance, often quitting when faced with obstacles{generality_words}"
        ],
        '2': [  # Slight perseverance
            "{species} cats show some perseverance, but they are likely to give up if a task takes too long or becomes too challenging{generality_words}",
            "Perseverance is moderate in {species} cats, as they may continue to try but will stop if things become too difficult{generality_words}",
            "{species} cats demonstrate some persistence, but they are prone to abandoning tasks if they don't see quick results{generality_words}",
            "While {species} cats can be persistent, they are likely to quit when faced with sustained challenges or slow progress{generality_words}",
            "{species} cats may persist in a task, but they lack the stamina to continue if it becomes too taxing or prolonged{generality_words}"
        ],
        '3': [  # Moderately persevering
            "{species} cats are fairly persevering, often continuing with tasks even when challenges arise{generality_words}",
            "{species} cats show a decent level of persistence, sticking with a task as long as they believe it will eventually succeed{generality_words}",
            "Moderate perseverance is observed in {species} cats, as they generally continue with tasks despite occasional setbacks{generality_words}",
            "While {species} cats may encounter obstacles, they are usually able to push through and persist until the task is completed{generality_words}",
            "{species} cats tend to show resilience, maintaining persistence through moderate challenges or distractions{generality_words}"
        ],
        '4': [  # Quite persevering
            "{species} cats are quite persevering, often continuing a task even in the face of significant challenges{generality_words}",
            "{species} cats demonstrate strong perseverance, sticking with difficult tasks and working through obstacles{generality_words}",
            "Perseverance is a notable trait in {species} cats, who are determined to complete tasks regardless of the difficulties{generality_words}",
            "{species} cats show great persistence, often working through challenges and refusing to give up easily{generality_words}",
            "{species} cats are determined and persistent, consistently pushing forward even when tasks become challenging{generality_words}"
        ],
        '5': [  # Extremely persevering
            "{species} cats are extremely persevering, never giving up and continuing to work on tasks no matter how difficult{generality_words}",
            "{species} cats demonstrate exceptional perseverance, always striving to overcome obstacles and never quitting{generality_words}",
            "Perseverance is one of the standout traits of {species} cats, who are unyielding in their efforts despite even the toughest challenges{generality_words}",
            "{species} cats are relentless, continuously pushing through obstacles and showing extraordinary persistence{generality_words}",
            "With unmatched perseverance, {species} cats are always determined to finish tasks, no matter the difficulty{generality_words}"
        ]
    }

    cat_persevering = cat_data['Attributes']['Persevering']

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

    category = categorize_perseverance(cat_persevering['average'])

    characteristic = ""
    if category in templates:
        characteristic = random.choice(templates[category]).format(species=cat_species, generality_words=generality_words())

    sentence_parts = [characteristic]

    if cat_persevering['average'] <= 2:
        sentence_parts.append(f"{cat_species} cats tend to lose motivation quickly when faced with difficult or prolonged tasks")
    elif cat_persevering['average'] > 4:
        sentence_parts.append(f"{cat_species} cats are highly persistent, often continuing to work on difficult tasks with unyielding determination")

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def affectionate_text_generation():
    templates = {
        '1': [  # Not affectionate
            "{species} cats are not very affectionate, often preferring solitude over companionship{generality_words}",
            "{species} cats are distant and rarely seek out affection from their owners{generality_words}",
            "Affection is not a strong trait of {species} cats, who tend to keep to themselves{generality_words}",
            "{species} cats are independent and usually do not engage in affectionate behaviors{generality_words}",
            "{species} cats often prefer their personal space and do not seek affection from others{generality_words}"
        ],
        '2': [  # Slight affection
            "{species} cats show limited affection, occasionally seeking attention but often preferring their own space{generality_words}",
            "While {species} cats may enjoy some affection, they typically don't demand it often{generality_words}",
            "{species} cats are not overly affectionate, but they can be warm when approached on their own terms{generality_words}",
            "Affection from {species} cats is sporadic, with some cats showing interest but not seeking constant interaction{generality_words}",
            "{species} cats can be affectionate at times, though they usually enjoy independence more{generality_words}"
        ],
        '3': [  # Moderately affectionate
            "{species} cats display moderate affection, often enjoying interaction but not always seeking it out{generality_words}",
            "Moderate affection is common in {species} cats, as they enjoy cuddles and attention when it is offered{generality_words}",
            "{species} cats appreciate affection, but they do not demand it constantly{generality_words}",
            "Affectionate behaviors are common in {species} cats, though they do not always initiate them{generality_words}",
            "{species} cats enjoy a good balance of affection and independence, seeking attention at times but not excessively{generality_words}"
        ],
        '4': [  # Quite affectionate
            "{species} cats are quite affectionate, often seeking out their owners for attention and interaction{generality_words}",
            "{species} cats thrive on affection, regularly engaging in cuddles and petting with their owners{generality_words}",
            "Affection is important to {species} cats, who enjoy spending time with their owners and being the center of attention{generality_words}",
            "{species} cats are very affectionate, regularly seeking out their owners for companionship and warmth{generality_words}",
            "{species} cats love being close to their owners, often following them around for attention and affection{generality_words}"
        ],
        '5': [  # Extremely affectionate
            "{species} cats are extremely affectionate, always seeking attention and companionship from their owners{generality_words}",
            "Affection is a key trait of {species} cats, who constantly seek out petting, cuddles, and interaction{generality_words}",
            "{species} cats are exceptionally affectionate, craving attention and companionship at all times{generality_words}",
            "{species} cats are known for their boundless affection, constantly seeking their owners' attention and love{generality_words}",
            "{species} cats are highly affectionate, regularly showing deep affection and always wanting to be near their owners{generality_words}"
        ]
    }

    cat_affectionate = cat_data['Attributes']['Affectionate']

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

    category = categorize_affection(cat_affectionate['average'])

    characteristic = ""
    if category in templates:
        characteristic = random.choice(templates[category]).format(species=cat_species, generality_words=generality_words())

    sentence_parts = [characteristic]

    if cat_affectionate['average'] <= 2:
        sentence_parts.append(f"{cat_species} cats may prefer solitude and are not typically drawn to affection")
    elif cat_affectionate['average'] > 4:
        sentence_parts.append(f"{cat_species} cats constantly seek companionship and affection, often following their owners around")

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def friendly_text_generation():
    templates = {
        '1': [  # Not friendly
            "{species} cats tend to be quite aloof and unfriendly, often avoiding interaction with others{generality_words}",
            "{species} cats are known for their solitary nature and rarely engage in friendly behaviors{generality_words}",
            "Friendliness is not common among {species} cats, who tend to keep to themselves{generality_words}",
            "{species} cats are distant and do not usually show friendliness toward other people or animals{generality_words}",
            "{species} cats are not typically sociable and prefer to remain in their own space{generality_words}"
        ],
        '2': [  # Slightly friendly
            "{species} cats may show some friendliness but often keep to themselves, engaging minimally with others{generality_words}",
            "While {species} cats can be friendly on occasion, they generally enjoy their solitude{generality_words}",
            "{species} cats may not seek out others, but they can show friendly behavior when approached{generality_words}",
            "Friendliness in {species} cats is limited, as they are often more independent than sociable{generality_words}",
            "{species} cats can be friendly but usually on their own terms, often enjoying time alone{generality_words}"
        ],
        '3': [  # Moderately friendly
            "{species} cats exhibit moderate friendliness, engaging with people and other animals when the situation allows{generality_words}",
            "Friendly behaviors are common in {species} cats, though they can also appreciate some alone time{generality_words}",
            "{species} cats are generally friendly and will engage with others, but they also value their independence{generality_words}",
            "{species} cats enjoy moderate interaction and can be friendly with people and other pets{generality_words}",
            "Friendliness is a common trait in {species} cats, but they may not seek constant attention{generality_words}"
        ],
        '4': [  # Very friendly
            "{species} cats are very friendly, regularly seeking interaction with others and forming strong bonds{generality_words}",
            "Friendliness is a strong characteristic of {species} cats, who are often eager to engage with their owners and others{generality_words}",
            "{species} cats are sociable and thrive on interaction, often showing friendly behaviors with both people and pets{generality_words}",
            "{species} cats love being around people and animals, regularly seeking attention and affection{generality_words}",
            "Friendly behaviors are a hallmark of {species} cats, who enjoy socializing and engaging with others{generality_words}"
        ],
        '5': [  # Extremely friendly
            "{species} cats are extremely friendly, always seeking companionship and eager to interact with others{generality_words}",
            "Sociability is a defining trait of {species} cats, who consistently seek out attention and enjoy being around others{generality_words}",
            "{species} cats are known for their exceptional friendliness, constantly engaging with their owners and other pets{generality_words}",
            "Extremely friendly, {species} cats thrive on companionship and eagerly interact with anyone they meet{generality_words}",
            "{species} cats are incredibly sociable, always looking for ways to engage with their owners and other animals{generality_words}"
        ]
    }

    cat_friendly = cat_data['Attributes']['Friendly']

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

    category = categorize_friendly(cat_friendly['average'])

    characteristic = ""
    if category in templates:
        characteristic = random.choice(templates[category]).format(species=cat_species, generality_words=generality_words())

    sentence_parts = [characteristic]

    if cat_friendly['average'] <= 2:
        sentence_parts.append(f"{cat_species} cats tend to prefer their personal space, not actively seeking social interaction")
    elif cat_friendly['average'] > 4:
        sentence_parts.append(f"{cat_species} cats are constantly seeking attention and love, enjoying the company of people and pets alike")

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def lonely_text_generation():
    templates = {
        '1': [  # Not lonely
            "{species} cats are very independent and rarely show signs of loneliness, preferring to be alone{generality_words}",
            "{species} cats tend to enjoy their own company and are seldom lonely, even when left alone for long periods{generality_words}",
            "Loneliness is uncommon for {species} cats, who are generally self-sufficient and not affected by solitude{generality_words}",
            "{species} cats are independent creatures and do not exhibit loneliness, even in isolation{generality_words}",
            "Most {species} cats enjoy solitude and do not show signs of loneliness{generality_words}"
        ],
        '2': [  # Slightly lonely
            "{species} cats can tolerate being alone for periods of time but may occasionally show signs of loneliness{generality_words}",
            "While {species} cats are generally independent, they may exhibit mild signs of loneliness if left alone for extended periods{generality_words}",
            "Loneliness is not a major issue for {species} cats, but they may seek some companionship from time to time{generality_words}",
            "{species} cats can handle solitude but might feel lonely during longer periods without interaction{generality_words}",
            "Though independent, {species} cats may occasionally experience mild loneliness when alone{generality_words}"
        ],
        '3': [  # Moderately lonely
            "{species} cats can be moderately affected by loneliness, often seeking attention or companionship when left alone{generality_words}",
            "Moderate loneliness is common for {species} cats, who may occasionally display signs of distress when alone for too long{generality_words}",
            "{species} cats sometimes feel lonely, but they manage on their own, although they may seek company during these times{generality_words}",
            "Loneliness is a moderate concern for {species} cats, who may become withdrawn or seek interaction when left alone{generality_words}",
            "{species} cats are moderately affected by solitude, often becoming lonely and seeking companionship or comfort{generality_words}"
        ],
        '4': [  # Very lonely
            "{species} cats tend to feel lonely when left alone, often seeking attention or company from their owners{generality_words}",
            "Loneliness is a significant issue for {species} cats, who may actively seek companionship and show distress when alone{generality_words}",
            "{species} cats thrive on company and often feel lonely when left alone for extended periods{generality_words}",
            "{species} cats are sensitive to loneliness, often becoming anxious or withdrawn when isolated for too long{generality_words}",
            "Feeling lonely is common for {species} cats, who may display clear signs of distress or seek constant attention{generality_words}"
        ],
        '5': [  # Extremely lonely
            "{species} cats are extremely social and cannot tolerate being alone, becoming highly lonely and distressed when isolated{generality_words}",
            "Loneliness is a major issue for {species} cats, who require constant companionship and often show extreme signs of distress when alone{generality_words}",
            "{species} cats are very sensitive to loneliness, and they frequently experience anxiety or depression when left alone{generality_words}",
            "Extreme loneliness is common for {species} cats, who struggle to be alone and need constant companionship to stay happy{generality_words}",
            "{species} cats cannot tolerate being left alone and become highly lonely, often displaying signs of anxiety or sadness{generality_words}"
        ]
    }

    cat_lonely = cat_data['Attributes']['Lonely']

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

    category = categorize_loneliness(cat_lonely['average'])

    characteristic = ""
    if category in templates:
        characteristic = random.choice(templates[category]).format(species=cat_species, generality_words=generality_words())

    sentence_parts = [characteristic]

    if cat_lonely['average'] <= 2:
        sentence_parts.append(f"{cat_species} cats are typically not distressed by solitude, enjoying their independence")
    elif cat_lonely['average'] > 4:
        sentence_parts.append(f"{cat_species} cats are extremely sensitive to being alone, often showing anxiety or depression when left alone")

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def brutal_text_generation():
    templates = {
        '1': [  # Not brutal
            "{species} cats are gentle and rarely display any aggressive behavior or brutality{generality_words}",
            "Brutality is uncommon in {species} cats, who are generally calm and peaceful in nature{generality_words}",
            "{species} cats are known for their calm demeanor and are very unlikely to show signs of brutality{generality_words}",
            "Aggression and brutality are not traits associated with {species} cats, who tend to be friendly and non-confrontational{generality_words}",
            "Most {species} cats are mild-mannered and do not engage in brutal behavior{generality_words}"
        ],
        '2': [  # Mildly brutal
            "{species} cats are generally calm but may occasionally display mild aggression or brutish behavior in certain situations{generality_words}",
            "While {species} cats are mostly peaceful, they can sometimes exhibit signs of brutality if provoked or stressed{generality_words}",
            "{species} cats tend to be gentle but may show mild brutality in rare or stressful situations{generality_words}",
            "Brutality is not typical of {species} cats, though they may occasionally display aggression when threatened{generality_words}",
            "On rare occasions, {species} cats may show aggression, though they are generally calm and non-brutal{generality_words}"
        ],
        '3': [  # Moderately brutal
            "{species} cats can be moderately brutal, sometimes showing aggressive tendencies in tense or competitive situations{generality_words}",
            "Moderate brutality is common in {species} cats, who may react aggressively under stress or provocation{generality_words}",
            "{species} cats may show signs of brutality in situations where they feel threatened, though it's not a constant trait{generality_words}",
            "{species} cats occasionally exhibit aggressive or brutal behavior, especially in tense situations or when defending themselves{generality_words}",
            "While {species} cats are usually calm, they can sometimes act brutally when under stress or in a conflict{generality_words}"
        ],
        '4': [  # Quite brutal
            "{species} cats are prone to showing aggressive or brutal behavior, especially when provoked or threatened{generality_words}",
            "Brutality is a common trait for {species} cats, who may often react with aggression or force in stressful situations{generality_words}",
            "{species} cats are more likely to display brutal behavior, showing signs of aggression when under pressure{generality_words}",
            "{species} cats frequently exhibit brutality in confrontational situations, often reacting aggressively to threats{generality_words}",
            "Aggression and brutality are regular traits of {species} cats, who can be quite forceful when they feel threatened{generality_words}"
        ],
        '5': [  # Extremely brutal
            "{species} cats are extremely brutal and aggressive, often reacting violently to perceived threats or challenges{generality_words}",
            "Brutality defines {species} cats, who are quick to show aggression and forceful behavior in most situations{generality_words}",
            "Extreme brutality is a key trait of {species} cats, who often react with intense aggression and violence{generality_words}",
            "{species} cats are highly brutal, frequently displaying violent tendencies and aggressive behavior in response to stress{generality_words}",
            "Violence and brutality are dominant traits for {species} cats, who often react aggressively in various situations{generality_words}"
        ]
    }

    cat_brutal = cat_data['Attributes']['Brutal']

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

    category = categorize_brutality(cat_brutal['average'])

    characteristic = ""
    if category in templates:
        characteristic = random.choice(templates[category]).format(species=cat_species, generality_words=generality_words())

    sentence_parts = [characteristic]

    if cat_brutal['average'] <= 2:
        sentence_parts.append(f"{cat_species} cats are typically calm and rarely show aggression unless provoked")
    elif cat_brutal['average'] > 4:
        sentence_parts.append(f"{cat_species} cats are highly aggressive and often react violently when faced with stress or challenges")

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def dominant_text_generation():
    templates = {
        '1': [  # Not dominant
            "{species} cats are very passive and unlikely to show dominance in their behavior{generality_words}",
            "Dominance is rare among {species} cats, as they are typically calm and non-confrontational{generality_words}",
            "{species} cats are not known for dominant behavior and prefer to stay passive and cooperative{generality_words}",
            "{species} cats tend to avoid dominance, favoring a more passive and relaxed approach in interactions{generality_words}",
            "Most {species} cats show little to no dominant traits, being gentle and adaptable in their behavior{generality_words}"
        ],
        '2': [  # Mildly dominant
            "{species} cats are usually calm but may occasionally show some dominance in certain situations{generality_words}",
            "While {species} cats tend to be peaceful, they can display mild dominance when asserting themselves{generality_words}",
            "{species} cats are generally passive but might show some dominance in specific circumstances{generality_words}",
            "{species} cats can occasionally exhibit signs of dominance, though it's not a dominant trait in their character{generality_words}",
            "Dominance is not a dominant trait in {species} cats, though they may display it in some situations{generality_words}"
        ],
        '3': [  # Moderately dominant
            "{species} cats display moderate dominance, occasionally taking charge in interactions and asserting themselves{generality_words}",
            "Moderate dominance is seen in {species} cats, who may show leadership qualities when interacting with others{generality_words}",
            "{species} cats can sometimes be dominant, showing a moderate level of assertiveness and control over situations{generality_words}",
            "While {species} cats are mostly calm, they can exhibit moderate dominance, especially when interacting with other animals{generality_words}",
            "{species} cats may display dominance in certain contexts, asserting themselves when they feel the need to lead{generality_words}"
        ],
        '4': [  # Quite dominant
            "{species} cats often exhibit strong dominance, frequently asserting control in interactions with other animals or people{generality_words}",
            "Dominance is a common trait for {species} cats, who tend to take charge and assert themselves in social situations{generality_words}",
            "{species} cats show clear dominance, frequently taking control of their environment and interactions with others{generality_words}",
            "Strong dominance is characteristic of {species} cats, who often display assertiveness and leadership qualities{generality_words}",
            "Dominance is a defining trait of {species} cats, who are often the leaders in their environment{generality_words}"
        ],
        '5': [  # Extremely dominant
            "{species} cats are highly dominant, always asserting control and showing strong leadership over others{generality_words}",
            "Dominance is a key feature of {species} cats, who constantly strive to be the top figure in their social structure{generality_words}",
            "{species} cats are extremely dominant, always taking charge and exerting authority in their environment{generality_words}",
            "Dominance defines {species} cats, who always seek to control their surroundings and lead with confidence{generality_words}",
            "Highly dominant, {species} cats consistently show control and authority in every interaction{generality_words}"
        ]
    }

    cat_dominant = cat_data['Attributes']['Dominant']

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

    category = categorize_dominance(cat_dominant['average'])

    characteristic = ""
    if category in templates:
        characteristic = random.choice(templates[category]).format(species=cat_species, generality_words=generality_words())

    sentence_parts = [characteristic]

    if cat_dominant['average'] <= 2:
        sentence_parts.append(f"{cat_species} cats are typically passive and rarely assert dominance unless necessary")
    elif cat_dominant['average'] > 4:
        sentence_parts.append(f"{cat_species} cats are highly dominant and constantly assert control in social interactions")

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def aggressive_text_generation():
    templates = {
        '1': [  # Not aggressive
            "{species} cats are very calm and rarely exhibit any signs of aggression{generality_words}",
            "Aggression is not a characteristic of {species} cats, who are typically peaceful and non-confrontational{generality_words}",
            "{species} cats tend to avoid aggressive behavior and are generally gentle and relaxed{generality_words}",
            "{species} cats are not known for aggression, preferring peaceful interactions and calm environments{generality_words}",
            "Aggression is uncommon in {species} cats, as they tend to stay calm and passive in most situations{generality_words}"
        ],
        '2': [  # Mildly aggressive
            "{species} cats can show occasional aggression, especially when feeling threatened or overstimulated{generality_words}",
            "While {species} cats are generally calm, they may display mild aggression under certain circumstances{generality_words}",
            "{species} cats have a low tendency to be aggressive but can become slightly territorial or defensive when provoked{generality_words}",
            "{species} cats may show some aggression when stressed or during play, though it's not a common behavior{generality_words}",
            "Mild aggression can sometimes be seen in {species} cats, especially in response to stress or unfamiliar situations{generality_words}"
        ],
        '3': [  # Moderately aggressive
            "{species} cats exhibit moderate aggression, often defending their space or showing signs of irritation when disturbed{generality_words}",
            "Moderate aggression is common in {species} cats, who may react strongly to threats or disruptions in their environment{generality_words}",
            "{species} cats may show moderate signs of aggression, including hissing or swatting when feeling threatened or stressed{generality_words}",
            "Aggression in {species} cats is moderate, with occasional outbursts or defensiveness when they feel uneasy{generality_words}",
            "{species} cats may become moderately aggressive, particularly if they feel their territory or resources are challenged{generality_words}"
        ],
        '4': [  # Quite aggressive
            "{species} cats often display high levels of aggression, particularly when they feel their space is threatened{generality_words}",
            "Aggression is quite prominent in {species} cats, who may frequently act aggressively in stressful or confrontational situations{generality_words}",
            "{species} cats can be highly aggressive, often reacting defensively or attacking when they feel threatened{generality_words}",
            "High levels of aggression are common in {species} cats, particularly when dealing with unfamiliar animals or environments{generality_words}",
            "Aggression in {species} cats is significant, with frequent displays of territorial behavior and defensive actions{generality_words}"
        ],
        '5': [  # Extremely aggressive
            "{species} cats are extremely aggressive, often displaying overt hostility and aggression toward others{generality_words}",
            "Dominating and aggressive, {species} cats tend to be confrontational and can be highly territorial{generality_words}",
            "{species} cats are very aggressive, with frequent attacks or displays of hostility toward other animals or people{generality_words}",
            "Aggression defines {species} cats, who are consistently confrontational and dominant in social interactions{generality_words}",
            "Extremely aggressive, {species} cats often act out with violent behavior, asserting control over their surroundings{generality_words}"
        ]
    }

    cat_aggressive = cat_data['Attributes']['Aggressive']

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

    category = categorize_aggression(cat_aggressive['average'])

    characteristic = ""
    if category in templates:
        characteristic = random.choice(templates[category]).format(species=cat_species, generality_words=generality_words())

    sentence_parts = [characteristic]

    if cat_aggressive['average'] <= 2:
        sentence_parts.append(f"{cat_species} cats are generally passive and only show aggression when highly provoked")
    elif cat_aggressive['average'] > 4:
        sentence_parts.append(f"{cat_species} cats are highly aggressive and regularly engage in hostile behaviors toward others")

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def impulsive_text_generation():
    templates = {
        '1': [  # Not impulsive
            "{species} cats are very calm and rarely act impulsively, preferring a thoughtful approach to their actions{generality_words}",
            "Impulsiveness is not common in {species} cats, who tend to carefully consider their actions{generality_words}",
            "{species} cats are highly deliberate and rarely engage in impulsive behavior{generality_words}",
            "With {species} cats, impulsivity is seldom observed; they tend to act in a controlled manner{generality_words}",
            "{species} cats show very little impulsiveness, often taking their time to make decisions{generality_words}"
        ],
        '2': [  # Mildly impulsive
            "{species} cats may act impulsively on occasion, but it is not a common trait{generality_words}",
            "Impulsiveness is somewhat present in {species} cats, typically triggered by external stimuli or surprise{generality_words}",
            "{species} cats can sometimes act impulsively, though it is usually mild and brief{generality_words}",
            "{species} cats occasionally exhibit impulsive behavior, but it is not a defining characteristic{generality_words}",
            "While {species} cats can act impulsively, it tends to be a rare occurrence in their daily routine{generality_words}"
        ],
        '3': [  # Moderately impulsive
            "{species} cats show moderate impulsivity, often acting on instinct or in response to sudden changes in their environment{generality_words}",
            "Impulsiveness is common in {species} cats, especially when they are startled or excited{generality_words}",
            "{species} cats are moderately impulsive, sometimes reacting quickly without much forethought{generality_words}",
            "Moderate impulsivity is a trait of {species} cats, who may act before thinking in certain situations{generality_words}",
            "{species} cats may often act impulsively, especially when reacting to fast-moving objects or sudden noises{generality_words}"
        ],
        '4': [  # Highly impulsive
            "{species} cats are highly impulsive, often acting on instinct and reacting quickly to their surroundings{generality_words}",
            "Impulsivity is quite noticeable in {species} cats, who frequently make spontaneous decisions without much thought{generality_words}",
            "{species} cats are very impulsive, often acting on immediate urges rather than considering consequences{generality_words}",
            "In {species} cats, impulsivity is a dominant trait, leading to quick reactions and unpredictable behavior{generality_words}",
            "Highly impulsive, {species} cats often react immediately to stimuli, without pausing to think{generality_words}"
        ],
        '5': [  # Extremely impulsive
            "{species} cats are extremely impulsive, often acting without any consideration or forethought{generality_words}",
            "Impulsiveness is a defining trait of {species} cats, who rarely pause to think before acting{generality_words}",
            "With {species} cats, impulsivity is extreme; they often make hasty decisions and unpredictable moves{generality_words}",
            "Extremely impulsive, {species} cats rarely consider the consequences before taking action{generality_words}",
            "{species} cats are highly impulsive, frequently acting on immediate urges and responding without delay{generality_words}"
        ]
    }

    cat_impulsive = cat_data['Attributes']['Impulsive']

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

    category = categorize_impulsivity(cat_impulsive['average'])

    characteristic = ""
    if category in templates:
        characteristic = random.choice(templates[category]).format(species=cat_species, generality_words=generality_words())

    sentence_parts = [characteristic]

    if cat_impulsive['average'] <= 2:
        sentence_parts.append(f"{cat_species} cats are generally calm and avoid impulsive actions")
    elif cat_impulsive['average'] > 4:
        sentence_parts.append(f"{cat_species} cats are highly impulsive, often reacting quickly without thinking")

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}.".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def predictable_text_generation():
    templates = {
        '1': [  # Highly unpredictable
            "{species} cats are highly unpredictable, often behaving in surprising or erratic ways{generality_words}",
            "Unpredictability defines {species} cats, who rarely follow consistent patterns in their actions{generality_words}",
            "{species} cats tend to act in unpredictable ways, making it difficult to anticipate their behavior{generality_words}",
            "With {species} cats, you can never be sure what to expect, as they frequently surprise with unexpected actions{generality_words}",
            "{species} cats show very little predictability, often changing their behavior without warning{generality_words}"
        ],
        '2': [  # Mildly unpredictable
            "{species} cats can be unpredictable at times, but they generally follow some patterns in their behavior{generality_words}",
            "While not entirely unpredictable, {species} cats can surprise you occasionally with sudden changes in behavior{generality_words}",
            "{species} cats show moderate unpredictability, sometimes acting in ways that are difficult to foresee{generality_words}",
            "Occasionally, {species} cats act unpredictably, but they also display some consistent behaviors{generality_words}",
            "There is a slight unpredictability to {species} cats, though their behavior is mostly consistent{generality_words}"
        ],
        '3': [  # Moderately predictable
            "{species} cats are fairly predictable, often following established patterns in their actions{generality_words}",
            "Predictability is common in {species} cats, who tend to act consistently day by day{generality_words}",
            "{species} cats exhibit moderate predictability, making their behavior fairly easy to anticipate{generality_words}",
            "Generally, {species} cats are predictable, following regular routines and habits each day{generality_words}",
            "With {species} cats, you can expect a fair amount of consistency in their behavior and actions{generality_words}"
        ],
        '4': [  # Very predictable
            "{species} cats are very predictable, with consistent routines and behaviors that are easy to follow{generality_words}",
            "Predictability is a key trait of {species} cats, who usually behave in a stable and reliable way{generality_words}",
            "{species} cats are quite predictable, with actions and behaviors that can be anticipated with ease{generality_words}",
            "In most cases, {species} cats follow predictable patterns, making them easy to understand and anticipate{generality_words}",
            "There is a high level of predictability in {species} cats, who rarely change their routines{generality_words}"
        ],
        '5': [  # Extremely predictable
            "{species} cats are extremely predictable, rarely deviating from their established patterns of behavior{generality_words}",
            "With {species} cats, you can always expect the same behavior, as they follow a fixed routine with little variation{generality_words}",
            "{species} cats are almost entirely predictable, making it easy to anticipate their actions with great certainty{generality_words}",
            "Predictability is a defining trait of {species} cats, whose behavior rarely changes and is highly consistent{generality_words}",
            "Every action of {species} cats follows a predictable routine, making them highly dependable and consistent in behavior{generality_words}"
        ]
    }

    cat_predictable = cat_data['Attributes']['Predictable']

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

    category = categorize_predictability(cat_predictable['average'])

    characteristic = ""
    if category in templates:
        characteristic = random.choice(templates[category]).format(species=cat_species, generality_words=generality_words())

    sentence_parts = [characteristic]

    if cat_predictable['average'] <= 2:
        sentence_parts.append(f"{cat_species} cats can be unpredictable at times, surprising you with sudden changes")
    elif cat_predictable['average'] >= 4:
        sentence_parts.append(f"{cat_species} cats follow a consistent routine, making them very predictable")

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
        return f"{sentence_parts[0]}, {connection_words()} {sentence_parts[1]}".capitalize()
    else:
        return f"{sentence_parts[0]}".capitalize()


def distracted_text_generation():
    templates = {
        '1': [  # Highly focused
            "{species} cats are highly focused, rarely showing signs of distraction during activities{generality_words}",
            "Distraction is uncommon in {species} cats, who usually stay on task and remain focused{generality_words}",
            "{species} cats are very attentive, exhibiting little to no signs of distraction in their daily routines{generality_words}",
            "You can always rely on {species} cats to stay focused and undistracted during play or observation{generality_words}",
            "Most of the time, {species} cats are completely engaged in their activities and show little distraction{generality_words}"
        ],
        '2': [  # Occasionally distracted
            "{species} cats are occasionally distracted but still manage to maintain focus for the majority of the time{generality_words}",
            "While {species} cats can sometimes lose focus, they generally stay on track with their activities{generality_words}",
            "{species} cats show moderate distraction, sometimes getting sidetracked but often staying engaged{generality_words}",
            "Distraction happens occasionally with {species} cats, but they can still focus on their activities most of the time{generality_words}",
            "{species} cats are moderately distracted, but they tend to return to their activities after brief moments of diversion{generality_words}"
        ],
        '3': [  # Moderately distracted
            "{species} cats are fairly distracted, often losing focus for short periods during their daily activities{generality_words}",
            "Distraction is fairly common with {species} cats, who may frequently shift their attention during play or observation{generality_words}",
            "{species} cats can be easily distracted, often shifting their focus between different activities{generality_words}",
            "While {species} cats generally stay engaged, they frequently show signs of distraction throughout the day{generality_words}",
            "It is not uncommon for {species} cats to get distracted during their routines, often losing focus momentarily{generality_words}"
        ],
        '4': [  # Quite distracted
            "{species} cats are often distracted, frequently losing focus and jumping between different activities{generality_words}",
            "Distraction is quite common for {species} cats, who can easily shift their attention to various stimuli{generality_words}",
            "{species} cats are quite distracted, showing a tendency to switch between activities and lose focus frequently{generality_words}",
            "You may notice that {species} cats often become distracted, switching their attention quickly from one thing to another{generality_words}",
            "Signs of distraction are frequent with {species} cats, who often lose focus during play or observation{generality_words}"
        ],
        '5': [  # Highly distracted
            "{species} cats are highly distracted, constantly shifting their attention and rarely staying focused on a single task{generality_words}",
            "Distraction defines {species} cats, who rarely stay focused on a single activity for long{generality_words}",
            "{species} cats are extremely distracted, jumping from one activity to the next without maintaining focus{generality_words}",
            "It is difficult for {species} cats to stay focused on any one task, as they are constantly distracted by new stimuli{generality_words}",
            "Highly distracted, {species} cats rarely stay engaged for long, frequently switching between different activities{generality_words}"
        ]
    }

    cat_distracted = cat_data['Attributes']['Distracted']

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

    category = categorize_distractedness(cat_distracted['average'])

    characteristic = ""
    if category in templates:
        characteristic = random.choice(templates[category]).format(species=cat_species, generality_words=generality_words())

    sentence_parts = [characteristic]

    if cat_distracted['average'] <= 2:
        sentence_parts.append(f"{cat_species} cats are generally focused and rarely get sidetracked during their activities")
    elif cat_distracted['average'] >= 4:
        sentence_parts.append(f"{cat_species} cats are often distracted, easily shifting their attention to new stimuli")

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
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
        ]
    }

    characteristic = ""

    cat_abundance = cat_data['Attributes']['Abundance']

    def categorize_abundance(value):
        if value <= 0.5:
            return '0'
        elif value < 1.5:
            return '1'
        elif value < 2.5:
            return '2'
        else:
            return '3'

    category = categorize_abundance(cat_abundance['average'])

    if category in templates:
        characteristic = random.choice(templates[category]).format(species=cat_species, generality_words=generality_words())

    return characteristic.capitalize()


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
        ]
    }

    cat_pred_bird = cat_data['Attributes']['PredBird']
    characteristic = ""

    if cat_pred_bird['average'] <= 0.5:
        characteristic = random.choice(templates['0']).format(species=cat_species, generality_words=generality_words())
    elif cat_pred_bird['average'] < 1.5:
        characteristic = random.choice(templates['1']).format(species=cat_species, generality_words=generality_words())
    elif cat_pred_bird['average'] < 2.5:
        characteristic = random.choice(templates['2']).format(species=cat_species, generality_words=generality_words())
    elif cat_pred_bird['average'] < 3.5:
        characteristic = random.choice(templates['3']).format(species=cat_species, generality_words=generality_words())
    else:
        characteristic = random.choice(templates['4']).format(species=cat_species, generality_words=generality_words())

    sentence_parts = [characteristic]

    if cat_pred_bird['average'] <= 1:
        sentence_parts.append(f"{cat_species} cats rarely engage in bird hunting, and birds are not often a target for them")
    elif cat_pred_bird['average'] > 2.5:
        sentence_parts.append(f"{cat_species} cats are active bird hunters, often capturing birds with regularity")

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
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
        ]
    }

    cat_pred_mamm = cat_data['Attributes']['PredMamm']
    characteristic = ""

    if cat_pred_mamm['average'] <= 0.5:
        characteristic = random.choice(templates['0']).format(species=cat_species, generality_words=generality_words())
    elif cat_pred_mamm['average'] < 1.5:
        characteristic = random.choice(templates['1']).format(species=cat_species, generality_words=generality_words())
    elif cat_pred_mamm['average'] < 2.5:
        characteristic = random.choice(templates['2']).format(species=cat_species, generality_words=generality_words())
    elif cat_pred_mamm['average'] < 3.5:
        characteristic = random.choice(templates['3']).format(species=cat_species, generality_words=generality_words())
    else:
        characteristic = random.choice(templates['4']).format(species=cat_species, generality_words=generality_words())

    sentence_parts = [characteristic]

    if cat_pred_mamm['average'] <= 1:
        sentence_parts.append(f"{cat_species} cats rarely engage in mammal hunting, and mammals are not often a target for them")
    elif cat_pred_mamm['average'] > 2.5:
        sentence_parts.append(f"{cat_species} cats are active mammal hunters, often capturing mammals with regularity")

    random.shuffle(sentence_parts)

    if len(sentence_parts) > 1:
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


category1_intro = "General Characteristics,"
category2_intro = "\nBehavioral Traits,"
category3_intro = "\nHunting Habits,"

category1_text = generate_category_text(category1, category1_intro)
category2_text = generate_category_text(category2, category2_intro)
category3_text = generate_category_text(category3, category3_intro)

final_text = f"{category1_text}\n{category2_text}\n{category3_text}"

print(final_text)