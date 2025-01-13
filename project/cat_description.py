import ollama
import json

import pandas as pd

attributes_to_keep = [
    "Shy",
    "Calm",
    "Afraid",
    "Clever",
    "Vigilant",
    "Persevering",
    "Affectionate",
    "Friendly",
    "Lonely",
    "Brutal",
    "Dominant",
    "Aggressive",
    "Impulsive",
    "Predictable",
    "Distracted",
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

df = pd.read_excel('../data/datasets/balanced_outputs/balanced_hybrid.xlsx')
df.rename(columns=column_mappings, inplace=True)


def get_breed_description(cat1_species):

    cat1_code = breed_to_code.get(cat1_species, "Unknown breed")
    df_cat1 = df[df['Breed'] == cat1_code]

    def count_column_values(df):
        column_counts = {}
        columns_dictionary = {}

        for column in df.columns:
            if column != 'Breed':
                value_counts = df[column].value_counts().to_dict()

                total_count = sum(value_counts.values())
                weighted_sum = sum(value * count for value, count in value_counts.items())
                avg = weighted_sum / total_count if total_count > 0 else 0

                columns_dictionary[column] = {
                    "average": avg
                }

        column_counts['Attributes'] = columns_dictionary
        return column_counts


    cat1_data = count_column_values(df_cat1)

    filtered_attributes = {
        "Attributes": {
            key: value
            for key, value in cat1_data["Attributes"].items()
            if key in attributes_to_keep
        }
    }

    print(json.dumps(filtered_attributes, indent=2))

    breed_name = cat1_species
    breed_data = filtered_attributes

    prompt = f"""
    You are an expert in cat breeds. I will provide you with the name of a cat breed and a JSON object containing details about that breed. Your task is to generate a natural language description of the breed using the information in the JSON object. The description should be engaging, informative, and suitable for a general audience.
    
    Now, here is the breed and JSON data:
    
    Breed: {breed_name}
    JSON:
    {json.dumps(breed_data, indent=2)}
    
    Generate a description based on this input.
    """

    stream = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    text = ""

    for chunk in stream:
        text += chunk["message"]["content"]

    sentences = text.split(". ")

    sentences = sentences[1:]

    text = ". ".join(sentences)

    if text.endswith("."):
        text = text[:-1]
    text = text.strip()
    return text
