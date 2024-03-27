# preprocessing sub functions

import re
import os
import glob
import string
import pandas as pd
from datetime import datetime
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import contractions


def remove_deleted(df):
    r"""
    remove_deleted function.
    This function appears to remove deleted post from crawled website data.

    Args:
        df: dataframe of crawled website data.

    Returns:
        df: dataframe of crawled website data without deleted post.
    """
    # Remove rows where the 'timestamp' column is numeric
    df = df[~df['timestamp'].str.isnumeric()]
    df.reset_index(drop=True, inplace=True)
    return df


def remove_deleted_post(df):
    r"""
    remove_deleted_post function.
    This function appears to remove deleted post where is in another format.

    Args:
        df: dataframe of crawled website data.

    Returns:
        df: dataframe of crawled website data without deleted post.
    """
    # Remove rows where the 'post' column contains 'del'
    df = df[df['post'] != 'del']
    df.reset_index(drop=True, inplace=True)
    return df


def update_lastEdit(df):
    r"""
    update_lastEdit function.
    This function appears to fill NaN values in the 'last_edit' column with corresponding values from the 'timestamp' column 

    Args:
        df: dataframe of crawled website data.

    Returns:
        df: dataframe of crawled website data with updated last_edit.
    """
    df.loc[:, 'last_edit'] = df['last_edit'].fillna(df['timestamp'])
    return df


def preprocess_date(date_str):
    r"""
    preprocess_date function.
    This function appears to convert occurrences of 'Today' in a date string to the current date
    Args:
        date_str: str that contains date information.

    Returns:
        str that contains date information with updated 'Today' to current date.
    """
    if "Today " in date_str:
        current_date = datetime.now().strftime("%B %d, %Y")
        return date_str.replace("Today", current_date)
    return date_str


def convert_datetime_with_multiple_formats(date_str, formats):
    r"""
    convert_datetime_with_multiple_formats function.
    This function appears to Convert a date string to a datetime object using multiple possible formats.

    Args:
        date_str: str that contains date information.
        formats: list of possible date formats.

    Returns:
        datetime object.
    """
    for fmt in formats:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except ValueError:
            continue
    raise ValueError(f"Time data {date_str} doesn't match provided formats")


def convert_to_datetime(df_):
    r"""
    convert_to_datetime function.
    This function appears to convert 'timestamp' and 'last_edit' columns to datetime format

    Args:
        df_: dataframe of crawled website data.

    Returns:
        df: dataframe of crawled website data with datatime format in 'timestamp' and 'last_edit' columns.
    """
    df = df_.copy()

    # Preprocess 'timestamp' and 'last_edit' columns to handle 'Today' values
    df['timestamp'] = df['timestamp'].apply(preprocess_date)
    df['last_edit'] = df['last_edit'].apply(preprocess_date)

    # List of potential datetime formats
    datetime_formats = ["%B %d, %Y at %I:%M:%S %p", "%B %d, %Y, %I:%M:%S %p"]

    df['timestamp'] = df['timestamp'].apply(
        convert_datetime_with_multiple_formats, formats=datetime_formats)
    df['timestamp'] = df['timestamp'].dt.date
    df['last_edit'] = df['last_edit'].apply(
        convert_datetime_with_multiple_formats, formats=datetime_formats)
    df['last_edit'] = df['last_edit'].dt.date

    return df


def remove_urls(text):
    r"""
    remove_urls function.
    This function appears to Remove URLs from a text.
    """
    return re.sub(r'http\S+', '', text)

#


def remove_extra_whitespace(text):
    r"""
    remove_extra_whitespace function.
    This function appears to Remove extra whitespace characters from a text.
    """
    return ' '.join(text.split())


def remove_special_characters(text):
    r"""
    remove_special_characters function.
    This function appears to remove special characters from a text.
    """
    return re.sub(r'[^\w\s]', '', text)


def to_lowercase(text):
    r"""
    to_lowercase function.
    This function appears to convert a text to lowercase.
    """
    return text.lower()


def remove_meta_info(text):
    r"""
    remove_meta_info function.
    This function appears to remove meta information where it contain quotes information.
    """
    text = str(text)
    return re.sub(r'Quote from: [a-zA-Z0-9_]+ on [a-zA-Z0-9, :]+ (AM|PM)', '', text)


def tokenize(text):
    r"""
    tokenize function.
    This function appears to Tokenize a text into individual words.
    """
    return text.split(' ')


def remove_sentence_punctuation(text):
    r"""
    remove_sentence_punctuation function.
    This function appears to remove punctuation from a text, excluding math symbols.
    """
    math_symbols = "+-×*÷/=()[]{},.<>%^"
    punctuations_to_remove = ''.join(
        set(string.punctuation) - set(math_symbols))
    return text.translate(str.maketrans(punctuations_to_remove, ' ' * len(punctuations_to_remove)))


def lemmatize_text(text):
    r"""
    lemmatize_text function.
    This function appears to lemmatize text, where it convert words to their base form.
    """
    lemmatizer = WordNetLemmatizer()
    return ' '.join([lemmatizer.lemmatize(word) for word in text.split()])


def replace_numbers(text, replace_with="<NUM>"):
    r"""
    replace_numbers function.
    This function appears to replace numbers in a text with a specified string (default is "<NUM>").
    """
    return re.sub(r'\b\d+\b', replace_with, text)


def remove_stopwords(tokens):
    r"""
    remove_stopwords function.
    This function appears to remove stopwords from a list of tokens.
    """
    stop_words = set(stopwords.words('english'))
    return [word for word in tokens if word not in stop_words]


def expand_contractions(tokens):
    r"""
    expand_contractions function.
    This function appears to expand contractions in a list of tokens (e.g., "isn't" to "is not")
    """
    return [contractions.fix(word) for word in tokens]


def remove_repeated_phrases(text):
    r"""
    remove_repeated_phrases function.
    This function appears to remove repeated phrases from a text.
    eg. "hello hello world" -> "hello world"
    """
    phrases = text.split()
    seen = set()
    output = []
    for phrase in phrases:
        if phrase not in seen:
            seen.add(phrase)
            output.append(phrase)
    return ' '.join(output)

def remove_emojis(images):
    pattern = r"https://bitcointalk\.org/Smileys/default/[a-zA-Z0-9_-]+\.gif"
    filtered_images = []
    for i in images:
        emoji_urls = re.findall(pattern, i["src"])
        if len(emoji_urls)<1:
            filtered_images.append(i)
    return filtered_images
