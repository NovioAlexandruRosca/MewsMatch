from nltk.corpus import wordnet
import nltk
import pprint

nltk.download("wordnet")

def find_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace("_", " "))
    return list(synonyms)

def build_extended_attribute_map(base_attribute_map):
    extended_map = {}
    for category, values in base_attribute_map.items():
        extended_map[category] = {}
        for key, value in values.items():
            synonyms = find_synonyms(key)
            for synonym in synonyms:
                extended_map[category][synonym] = value

            extended_map[category][key] = value
    return extended_map


# base_attribute_map = {
#     "Logement": {"apartment": 1, "house": 2, "farm": 3, "other": 4},
#     "Zone": {"urban": 1, "periurban": 2, "rural": 3},
#     "Ext": {"none": 0, "less_than_1_hour": 1, "1_to_3_hours": 2, "3_to_6_hours": 3, "more_than_6_hours": 4},
#     "Obs": {"none": 0, "less_than_1_hour": 1, "1_to_3_hours": 2, "more_than_3_hours": 3},
#     "Timide": {"very_shy": 5, "shy": 4, "neutral": 3, "confident": 2, "very_confident": 1},
#     "Calme": {"very_calm": 5, "calm": 4, "neutral": 3, "restless": 2, "very_restless": 1},
#     "Effraye": {"very_fearful": 5, "fearful": 4, "neutral": 3, "fearless": 2, "very_fearless": 1},
#     "Intelligent": {"very_intelligent": 5, "intelligent": 4, "neutral": 3, "less_intelligent": 2, "not_intelligent": 1},
#     "PredOiseau": {"never": 0, "rarely": 1, "sometimes": 2, "often": 3, "very_often": 4},
#     "PredMamm": {"never": 0, "rarely": 1, "sometimes": 2, "often": 3, "very_often": 4},
# }

base_attribute_map = {
    "Sexe":{
        "male": 0,
        "female": 1
    },
    "Logement": {
        "apartment": 1,
        "flat": 1,
        "house": 2,
        "home": 2,
        "farm": 3,
        "cottage": 3,
        "other": 4,
        "unknown": 4,
    },
    "Zone": {
        "urban": 1,
        "city": 1,
        "periurban": 2,
        "suburban": 2,
        "near_town": 2,
        "rural": 3,
        "countryside": 3,
        "village": 3,
    },
    "Ext": {
        "never_outside": 0,
        "indoor_only": 0,
        "less_than_1_hour_outside": 1,
        "short_outings": 1,
        "1_to_3_hours_outside": 2,
        "more_than_1_hour_outside": 2,
        "less_than_3_hours_outside": 2,
        "3_to_6_hours_outside": 3,
        "half_day_outside": 3,
        "more_than_6_hours_outside": 4,
        "mostly_outdoor": 4,
    },
    "Obs": {
        "no_time": 0,
        "less_than_1_hour": 1,
        "minimal_attention": 1,
        "1_to_3_hours": 2,
        "moderate_attention": 2,
        "some_time_with_cat": 2,
        "more_than_3_hours": 3,
        "dedicated_care": 3,
        "a_lot_of_attention": 3,
    },
    "Timide": {
        "very_shy": 5,
        "extremely_reserved": 5,
        "shy": 4,
        "timid": 4,
        "introverted": 4,
        "not_confident": 4,
        "average_confidence": 3,
        "confident": 2,
        "self_assured": 2,
        "bold": 2,
        "not introverted": 2,
        "very_confident": 1,
        "fearless": 1,
    },
    "Calme": {
        "very_calm": 5,
        "never_agitated":5,
        "relaxed": 5,
        "peaceful": 5,
        "calm": 4,
        "tranquil": 4,
        "moderate_activity": 3,
        "restless": 2,
        "fidgety": 2,
        "very_restless": 1,
        "agitated": 1,
        "never_calm":1,
    },
    "Effraye": {
        "very_fearful": 5,
        "terrified": 5,
        "fearful": 4,
        "anxious": 4,
        "slightly_wary": 3,
        "fearless": 2,
        "bold": 2,
        "very_fearless": 1,
        "daring": 1,
    },
    "Intelligent": {
        "very_intelligent": 5,
        "highly_perceptive": 5,
        "intelligent": 4,
        "clever": 4,
        "smart":4,
        "average_intelligence": 3,
        "less_intelligent": 2,
        "simple": 2,
        "not_intelligent": 1,
        "unaware": 1,
    },
    "Vigilant": {
        "very_vigilant": 5,
        "highly_alert": 5,
        "watchful": 5,
        "vigilant": 4,
        "attentive": 4,
        "occasionally_alert": 3,
        "unobservant": 2,
        "inattentive": 2,
        "very_unobservant": 1,
        "oblivious": 1,
    },
    "Perseverant": {
        "very_persistent": 5,
        "tenacious": 5,
        "persistent": 4,
        "determined": 4,
        "average_determination": 3,
        "occasionally_gives_up": 2,
        "inconsistent": 2,
        "often_gives_up": 1,
        "easily_dissuaded": 1,
    },
    "Affectueux": {
        "very_affectionate": 5,
        "cuddly": 5,
        "affectionate": 4,
        "loving": 4,
        "sometimes_affectionate": 3,
        "distant": 2,
        "reserved": 2,
        "very_distant": 1,
        "cold": 1,
    },
    "Amical": {
        "very_friendly": 5,
        "outgoing": 5,
        "friendly": 4,
        "approachable": 4,
        "occasionally_friendly": 3,
        "reserved": 2,
        "aloof": 2,
        "very_reserved": 1,
        "hostile": 1,
    },
    "Solitaire": {
        "very_solitary": 5,
        "likes_to_be_alone": 5,
        "solitary": 4,
        "independent": 4,
        "occasionally_social": 3,
        "prefers_company": 2,
        "social": 2,
        "very_social": 1,
        "gregarious": 1,
    },
    "Brutal": {
        "very_brutal": 5,
        "extremely_aggressive": 5,
        "brutal": 4,
        "rough": 4,
        "usually_gentle": 3,
        "gentle": 2,
        "very_gentle": 1,
        "soft": 1,
    },
    "Dominant": {
        "very_dominant": 5,
        "bossy": 5,
        "dominant": 4,
        "assertive": 4,
        "occasionally_submissive": 3,
        "submissive": 2,
        "yielding": 2,
        "very_submissive": 1,
        "docile": 1,
    },
    "Agressif": {
        "very_aggressive": 5,
        "combative": 5,
        "aggressive": 4,
        "hostile": 4,
        "occasionally_passive": 3,
        "passive": 2,
        "calm": 2,
        "very_passive": 1,
        "peaceful": 1,
    },
    "Impulsif": {
        "very_impulsive": 5,
        "rash": 5,
        "impulsive": 4,
        "hasty": 4,
        "sometimes_cautious": 3,
        "controlled": 2,
        "deliberate": 2,
        "very_controlled": 1,
        "calculated": 1,
    },
    "Previsible": {
        "very_predictable": 5,
        "consistent": 5,
        "predictable": 4,
        "reliable": 4,
        "occasionally_unpredictable": 3,
        "unpredictable": 2,
        "erratic": 2,
        "very_unpredictable": 1,
        "chaotic": 1,
    },
    "Distrait": {
        "very_distracted": 5,
        "unfocused": 5,
        "distracted": 4,
        "daydreaming": 4,
        "occasionally_focused": 3,
        "focused": 2,
        "attentive": 2,
        "very_focused": 1,
        "sharp": 1,
    },
    "Abondance": {
        "very_abundant": 3,
        "plentiful": 3,
        "abundant": 2,
        "adequate": 2,
        "limited": 1,
        "scarce": -1,
        "very_scarce": -1,
    },
    "PredOiseau": {
        "never": 0,
        "rarely": 1,
        "occasionally": 2,
        "sometimes": 2,
        "often": 3,
        "frequently": 3,
        "very_often": 4,
        "always": 4,
    },
    "PredMamm": {
        "never": 0,
        "rarely": 1,
        "occasionally": 2,
        "sometimes": 2,
        "often": 3,
        "frequently": 3,
        "very_often": 4,
        "always": 4,
    },
}



extended_attribute_map = build_extended_attribute_map(base_attribute_map)

with open("../data/attribute_map.py", "w") as py_file:
    py_file.write("extended_attribute_map = ")
    py_file.write(pprint.pformat(extended_attribute_map, indent=4))

