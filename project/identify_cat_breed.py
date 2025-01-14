import pickle
import re
import sys
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.append('../data')
from attribute_map import extended_attribute_map
import model_keyword_extractor


def calculate_attribute_means_from_data(file_path, columns_to_keep):
    data = pd.read_excel(file_path)
    data = data[columns_to_keep]
    means = data.mean().to_dict()
    return means

columns_to_keep = [
    "Sexe",
    "Age",
    "Nombre",
    "Logement",
    "Zone",
    "Ext",
    "Obs",
    "Timide",
    "Calme",
    "Effraye",
    "Intelligent",
    "Vigilant",
    "Perseverant",
    "Affectueux",
    "Amical",
    "Solitaire",
    "Brutal",
    "Dominant",
    "Agressif",
    "Impulsif",
    "Previsible",
    "Distrait",
    "Abondance",
    "PredOiseau",
    "PredMamm",
]

file_path = "../data/datasets/balanced_outputs/balanced_hybrid.xlsx"
attribute_means = calculate_attribute_means_from_data(file_path, columns_to_keep)

attribute_map = extended_attribute_map

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def normalize_keywords(attribute_map):
    normalized_map = {}
    for attribute, keywords in attribute_map.items():
        normalized_map[attribute] = {}
        for keyword, value in keywords.items():
            normalized_keyword = keyword.replace("_", " ")
            normalized_map[attribute][normalized_keyword] = value
    return normalized_map

def extract_features_manual(text, attribute_map):
    text = preprocess_text(text)
    features = {attribute: None for attribute in attribute_map.keys()}

    additional_attributes = ["Age", "Nombre"]
    for attr in additional_attributes:
        features[attr] = None

    normalized_map = normalize_keywords(attribute_map)

    negative_modifiers = {"not", "never"}

    obs_context_keywords = ["spend together", "spent together", "spends", "with me"]
    pred_oiseau_context_keywords = ["bird", "birds", "catches birds", "hunts birds", "hunting birds"]
    pred_mamm_context_keywords = ["mice", "mouse", "rodent", "catches mice", "hunts mice", "hunting mice"]

    for attribute, keywords in normalized_map.items():
        sorted_keywords = sorted(keywords.keys(), key=lambda x: -len(x))

        for keyword in sorted_keywords:
            value = keywords[keyword]

            if attribute == "Obs":
                pattern = rf'\b(?:{"|".join(obs_context_keywords)})\b.*?\b{re.escape(keyword)}\b|\b{re.escape(keyword)}\b.*?\b(?:{"|".join(obs_context_keywords)})\b'
                match = re.search(pattern, text)
            elif attribute == "PredOiseau":
                for context in pred_oiseau_context_keywords:
                    pattern = rf'\b{re.escape(keyword)}\b(?:\s+\w+)?(?:\s+\w+)?\s+\b{re.escape(context)}\b|\b{re.escape(context)}\b(?:\s+\w+)?(?:\s+\w+)?\s+\b{re.escape(keyword)}\b'
                    if re.search(pattern, text):
                        print(f"Matched '{keyword}' with value: {value}")
                        features[attribute] = value
                        break
            elif attribute == "PredMamm":
                for context in pred_mamm_context_keywords:
                    pattern = rf'\b{re.escape(keyword)}\b(?:\s+\w+)?(?:\s+\w+)?\s+\b{re.escape(context)}\b|\b{re.escape(context)}\b(?:\s+\w+)?(?:\s+\w+)?\s+\b{re.escape(keyword)}\b'
                    if re.search(pattern, text):
                        print( f"Matched '{keyword}' with value: {value}")
                        features[attribute] = value
                        break
            else:
                pattern = rf'(\b(?:{"|".join(negative_modifiers)})\b )?\b{re.escape(keyword)}\b'
                match = re.search(pattern, text)

            if match:
                modifier = match.group(1) if attribute not in ["Obs", "PredOiseau", "PredMamm"] else None
                adjusted_value = value

                if modifier:
                    adjusted_value = 6 - value

                print(f"Matched: '{keyword}' with value: {adjusted_value}")
                features[attribute] = adjusted_value
                break

    for attribute in features:
        if features[attribute] is None:
            if attribute == "Sexe":
                features[attribute] = -1
            else:
                features[attribute] = attribute_means.get(attribute, 0)

    return features

def extract_features_automat(text):
    features = model_keyword_extractor.run_keyword_extractor(text)
    return features

def combine_manual_automat_feature_extraction(features_manual, features_automat):
    combined_features = {}
    all_attributes = set(features_manual.keys()).union(features_automat.keys())

    for attribute in all_attributes:
        value_manual = features_manual.get(attribute, -1)
        value_extractor = features_automat.get(attribute, -1)

        if value_manual == -1 and value_extractor != -1:
            combined_features[attribute] = value_extractor
        elif value_extractor == -1 and value_manual != -1:
            combined_features[attribute] = value_manual
        elif value_manual != -1 and value_extractor != -1:
            combined_features[attribute] = (value_manual + value_extractor) / 2
        else:
            combined_features[attribute] = -1

    return combined_features

def predict(features, model_filename, columns_to_keep):

    with open(model_filename, "rb") as file:
        model_data = pickle.load(file)

    weights = model_data["weights"]
    biases = model_data["biases"]
    mean = model_data["mean"]
    std = model_data["std"]

    feature_vector = np.array([features[col] for col in columns_to_keep]).reshape(1, -1)
    scaled_vector = (feature_vector - mean) / std
    activations = [scaled_vector]
    for i in range(len(weights) - 1):
        z = np.dot(activations[-1], weights[i]) + biases[i]
        a = 1 / (1 + np.exp(-z))  #sigmoid
        activations.append(a)

    z_output = np.dot(activations[-1], weights[-1]) + biases[-1]
    exp_scores = np.exp(z_output - np.max(z_output, axis=1, keepdims=True))

    probabilities = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
    predicted_class = np.argmax(probabilities, axis=1)[0]
    predicted_probability = probabilities[0, predicted_class] * 100

    return predicted_class, probabilities, round(predicted_probability, 2)



def identify_breed(text):
    features_manual = extract_features_manual(text, attribute_map)
    features_automat = extract_features_automat(text)
    combined_features = combine_manual_automat_feature_extraction(features_manual, features_automat)
    model_filename = "../neural_network/neural_network_model.pkl"
    predicted_class, probabilities, predicted_probability = predict(combined_features, model_filename, columns_to_keep)
    breed_code = {
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
    code_breed = {v: k for k, v in breed_code.items()}
    breed_name = code_breed.get(predicted_class, "Unknown class")
    return breed_name


text = """ The cat is not bold and spends less than 1 hour outside every day. It lives in an apartment
 in an urban area and rarely cries."""

