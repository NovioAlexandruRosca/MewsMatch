import json
import re
import pandas as pd
from ollama import chat
import math


def get_cat_traits(prompt, model_name):
    try:
        stream = chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )

        response_text = ""

        for chunk in stream:
            response_text += chunk["message"]["content"]

        print("Raw Response:", response_text)

        json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if json_match:
            json_data = json_match.group(0)
            return json.loads(json_data)
        else:
            print("No JSON object found in the response.")
            return {}

    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


def handle_missing_values(cat_traits, df):
    features = [
        "Sexe", "Age", "Nombre", "Logement", "Zone", "Ext", "Obs",
        "Timide", "Calme", "Effraye", "Intelligent", "Vigilant",
        "Perseverant", "Affectueux", "Amical", "Solitaire", "Brutal",
        "Dominant", "Agressif", "Impulsif", "Previsible", "Distrait",
        "Abondance", "PredOiseau", "PredMamm"
    ]

    for feature in features:
        if cat_traits.get(feature, -1) == -1:
            if feature in df.columns:
                avg = df[feature].mean()
                cat_traits[feature] = math.floor(avg)
            else:
                print(f"Feature '{feature}' not found in the DataFrame.")

    return cat_traits


sentence = "The cat is a 3-year-old female living in an apartment with a balcony in an urban area. It often goes " \
           "outside and interacts moderately with its surroundings. The cat is timid, calm, and affectionate but not " \
           "very intelligent or vigilant. It rarely chases birds and occasionally chases mammals."

# prompt = f"""
# You are given a description of a cat. Analyze the description and return ONLY a JSON object with the following keys and values:
#
# Sexe: 0 for male, 1 for female. If not specified, set to -1.
# Age:
# 0 if younger than 1 year.
# 1 if 1 year old.
# 2 if 2-5 years old.
# 10 if older than 5 years.
# If not specified, set to -1.
# Nombre:
# 1 for one cat in the house.
# 2 for two cats.
# 3 for three cats.
# 4 for four cats.
# 5 for five cats.
# 6 for more than five cats.
# If not specified, set to -1.
# Logement:
# 1 for "apartment_no_balcony".
# 2 for "apartment_balcony".
# 3 for "subdivision_house".
# 4 for "individual_house".
# If not specified, set to -1.
# Zone:
# 1 for "urban".
# 2 for "rural".
# 3 for "periurban".
# If not specified, set to -1.
# Ext: 0-4 (likelihood of going outside: 0 = none, 1 = limited, 2 = moderate, 3 = long, 4 = all the time). If not specified, set to -1.
# Obs: 0-3 (interaction duration: 0 = no interaction, 1 = limited, 2 = moderate, 3 = long). If not specified, set to -1.
# From Timide to Abondance, each trait is scored from 1-5, where:
# 1 = least, 5 = most. If not specified, set to -1.
#
# Timide: Level of shyness.
# Calme: Level of calmness.
# Effraye: Level of fearfulness.
# Intelligent: Level of intelligence.
# Vigilant: Level of alertness or watchfulness.
# Perseverant: Level of perseverance.
# Affectueux: Level of affection.
# Amical: Level of friendliness.
# Solitaire: Preference for solitude.
# Brutal: Level of aggression or roughness.
# Dominant: Level of dominance.
# Agressif: Level of aggressiveness.
# Impulsif: Level of impulsiveness.
# Previsible: Level of predictability.
# Distrait: Level of distraction or inattentiveness.
# Abondance: Level of abundance or availability of resources in the environment.
# For hunting likelihood:
#
# PredOiseau: 0-4 (likelihood of chasing birds, 0 = never, 4 = always). If not specified, set to -1.
# PredMamm: 0-4 (likelihood of chasing mammals, 0 = never, 4 = always). If not specified, set to -1.
#
# The sentence is: {sentence}.
# """

df_path = "../data/datasets/balanced_outputs/balanced_hybrid.xlsx"
df = pd.read_excel(df_path)


def run_keyword_extractor(sentence):
    prompt = f"""
    You are given a description of a cat. Analyze the description and return ONLY a JSON object with the following keys and values:

    Sexe: 0 for male, 1 for female. If not specified, set to -1.
    Age:
    0 if younger than 1 year.
    1 if 1 year old.
    2 if 2-5 years old.
    10 if older than 5 years.
    If not specified, set to -1.
    Nombre:
    1 for one cat in the house.
    2 for two cats.
    3 for three cats.
    4 for four cats.
    5 for five cats.
    6 for more than five cats.
    If not specified, set to -1.
    Logement:
    1 for "apartment_no_balcony".
    2 for "apartment_balcony".
    3 for "subdivision_house".
    4 for "individual_house".
    If not specified, set to -1.
    Zone:
    1 for "urban".
    2 for "rural".
    3 for "periurban".
    If not specified, set to -1.
    Ext: 0-4 (likelihood of going outside: 0 = none, 1 = limited, 2 = moderate, 3 = long, 4 = all the time). If not specified, set to -1.
    Obs: 0-3 (interaction duration: 0 = no interaction, 1 = limited, 2 = moderate, 3 = long). If not specified, set to -1.
    From Timide to Abondance, each trait is scored from 1-5, where:
    1 = least, 5 = most. If not specified, set to -1.

    Timide: Level of shyness.
    Calme: Level of calmness.
    Effraye: Level of fearfulness.
    Intelligent: Level of intelligence.
    Vigilant: Level of alertness or watchfulness.
    Perseverant: Level of perseverance.
    Affectueux: Level of affection.
    Amical: Level of friendliness.
    Solitaire: Preference for solitude.
    Brutal: Level of aggression or roughness.
    Dominant: Level of dominance.
    Agressif: Level of aggressiveness.
    Impulsif: Level of impulsiveness.
    Previsible: Level of predictability.
    Distrait: Level of distraction or inattentiveness.
    Abondance: Level of abundance or availability of resources in the environment.
    For hunting likelihood:

    PredOiseau: 0-4 (likelihood of chasing birds, 0 = never, 4 = always). If not specified, set to -1.
    PredMamm: 0-4 (likelihood of chasing mammals, 0 = never, 4 = always). If not specified, set to -1.

    The sentence is: {sentence}.
    """

    llama_result = get_cat_traits(prompt, "llama3.2")
    nuextract_result = get_cat_traits(prompt, "nuextract")

    combined_result = {}
    keys = set(llama_result.keys()).union(set(nuextract_result.keys()))
    for key in keys:
        values = [model[key] for model in [llama_result, nuextract_result] if key in model and model[key] != -1]
        combined_result[key] = math.floor(sum(values) / len(values)) if values else -1

    final_result = handle_missing_values(combined_result, df)

    return final_result


