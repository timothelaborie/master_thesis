# Importing standard libraries
import os
import glob
import argparse
import pandas as pd
from tqdm import tqdm
from pathlib import Path

# Additional preprocessing functions are imported from another module.
from preprocessing_sub_functions import *


# This function returns a list of all CSV files in the given directory path.
def get_files(path):
    return glob.glob(path + "/*.csv")


# This function aims to remove meta information from the text.
# The specifics of what meta information is removed depends on the function 'remove_meta_info'.
def raw_preprocess(text):
    text = remove_meta_info(text)
    return text


# A comprehensive text preprocessing function that applies several common preprocessing steps:
# - URLs are removed from the text.
# - The entire text is converted to lowercase to ensure uniformity.
# - Punctuation is stripped from the text.
# - Extra whitespaces (if any) are removed.
# - The text is tokenized (split into individual words or tokens).
# - Contractions (like "can't" or "won't") are expanded to their full forms.
# - Common words (stopwords) that don't add significant meaning are removed.
# Finally, the cleaned tokens are joined back into a string.
def text_preprocess(text):
    text = remove_urls(text)
    text = to_lowercase(text)
    text = remove_sentence_punctuation(text)
    text = remove_extra_whitespace(text)
    tokens = tokenize(text)
    tokens = expand_contractions(tokens)
    tokens = remove_stopwords(tokens)
    text = " ".join(tokens)
    return text


# This function preprocesses a dataframe.
# Specific preprocessing steps include:
# - Removing rows marked as 'deleted'.
# - Removing posts marked as 'deleted'.
# - Updating the 'lastEdit' column.
# - Converting timestamps to a datetime format.
# - Renaming the 'timestamp' column to 'start_edit'.
def csv_preprocess(df):
    df = remove_deleted(df)
    df = remove_deleted_post(df)
    df = update_lastEdit(df)
    df = convert_to_datetime(df)
    df.rename(columns={"timestamp": "start_edit"}, inplace=True)
    return df


# This function processes individual CSV files:
# - Reads the CSV into a DataFrame.
# - Applies dataframe preprocessing.
# - Applies raw text preprocessing to the 'post' column.
# - Saves the raw preprocessed data into a 'raw-data' folder.
# - Applies comprehensive text preprocessing to the 'post' column.
# - Saves the fully preprocessed data into a 'preprocessed-data' folder.
def loop_through_csvs(filePath):
    file = os.path.basename(filePath)
    folder = os.path.basename(os.path.dirname(filePath))
    df = pd.read_csv(filePath)
    df = csv_preprocess(df)

    # Create a directory for raw data if it doesn't exist.
    raw_folder = Path(f"raw-data/{folder}")
    raw_folder.mkdir(parents=True, exist_ok=True)

    # Apply raw preprocessing to the 'post' column of the dataframe.
    df["post"] = df["post"].apply(raw_preprocess)

    # Sort the dataframe by the 'last_edit' column.
    df.sort_values(by=["last_edit"], inplace=True)

    # Save the raw preprocessed dataframe to a CSV file.
    df.to_csv(f"{raw_folder}/{file}", index=False)

    # Create a directory for fully preprocessed data if it doesn't exist.
    clean_folder = Path(f"preprocessed-data/{folder}")
    clean_folder.mkdir(parents=True, exist_ok=True)

    # Apply the comprehensive text preprocessing to the 'post' column and store the result in a new column.
    df["preprocessed_post"] = df["post"].apply(text_preprocess)

    # Sort the dataframe by the 'last_edit' column again.
    df.sort_values(by=["last_edit"], inplace=True)

    # Save the fully preprocessed dataframe to a CSV file.
    df.to_csv(f"{clean_folder}/{file}", index=False)

    return df


# A function to parse command-line arguments.
# The script expects a 'path' argument which indicates the directory where the raw CSV files are located.
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path for the extraction")
    return vars(parser.parse_args())


# The main function of the script:
# - It retrieves all the CSV files from the specified directory.
# - Loops through each file, applying the preprocessing steps.
# - If an error occurs during processing, the error message is appended to an 'error_log.txt' file.
def main(path):
    print(f'Preprocessing data in {path}')
    rawFiles = get_files(path)
    for filePath in tqdm(rawFiles):
        try:
            df = loop_through_csvs(filePath)
        except Exception as e:
            # If an error occurs, log the error message to a file.
            with open(f"{path}/error_log.txt", "a") as f:
                f.write(f"{filePath} -- {e}\\n")
            continue


if __name__ == "__main__":
    main(**parse_args())
