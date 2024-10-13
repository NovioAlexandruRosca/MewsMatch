import pandas as pd
from deep_translator import GoogleTranslator
from tqdm import tqdm
from utils.IO_utils import load_from_json, load_from_excel


def translate_and_save(df, abbreviations_on, source_language, target_language):
    headers_to_translate = df.columns.tolist()

    tqdm.pandas(desc="Translating headers")
    translated_headers = [GoogleTranslator(source=source_language, target=target_language).translate(header) for header in tqdm(headers_to_translate, desc="Translating headers")]

    plus_column_name = 'Plus'
    if plus_column_name in df.columns:
        tqdm.pandas(desc="Translating Plus column")
        df[plus_column_name] = df[plus_column_name].progress_apply(lambda x: GoogleTranslator(source=source_language, target=target_language).translate(x) if isinstance(x, str) else x)

    translated_df = pd.DataFrame(columns=translated_headers)

    for col in tqdm(df.columns, desc="Copying data to new DataFrame"):
        translated_df[translated_headers[df.columns.get_loc(col)]] = df[col]

    output_file = f'../data/datasets/{target_language}_{"abbreviation" if abbreviations_on else "fullname"}_base_cat_dataset.xlsx'
    translated_df.to_excel(output_file, index=False)

    print("Translation completed and saved to", output_file)


def abbreviation_to_fullname(df, data_structure):

    pd.set_option('future.no_silent_downcasting', True)

    def translate_categorical(df, column, mappings):
        if column in df.columns:
            df[column] = df[column].map(mappings).fillna(df[column])
            df[column] = df[column].infer_objects()

    for key, value in data_structure.items():
        translate_categorical(df, key, value['mappings'])

    output_file = '../data/datasets/fullname_base_cat_dataset.xlsx'
    df.to_excel(output_file, index=False)

    print("Abbreviations have been changed and the new data has been saved here:", output_file)
    return df


def translate_dataset(abbreviations_on=True, source_language='fr', target_language='en'):
    df = load_from_excel('../data/datasets/base_cat_dataset.xlsx')
    data_structure = load_from_json("../config/base_dataset_characteristics.json")

    if not abbreviations_on:
        df = abbreviation_to_fullname(df, data_structure)

    translate_and_save(df, abbreviations_on, source_language, target_language)


translate_dataset(abbreviations_on=True, target_language='en')
