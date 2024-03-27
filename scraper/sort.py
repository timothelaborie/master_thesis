import os
import pandas as pd
from pathlib import Path
from tqdm import tqdm

# Function to process and sort CSV files within a given folder


def process_csvs(folder_path, new_folder_name):
    # Extracting the name of the board from the folder path
    board = os.path.basename(folder_path)
    # Creating a new directory to store the sorted CSV files
    sorted_folder = Path(new_folder_name)
    sorted_folder.mkdir(parents=True, exist_ok=True)

    # Retrieving all CSV files from the given folder path
    all_files = [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if file.endswith(".csv")
    ]
    # Reading each CSV file into a dataframe
    list_of_dataframes = [pd.read_csv(file) for file in all_files]
    # Combining all dataframes into a single dataframe
    combined_df = pd.concat(list_of_dataframes, ignore_index=True)

    # Sorting the combined dataframe based on the "last_edit" column
    combined_df = combined_df.sort_values(by="last_edit")

    # Splitting the sorted dataframe into chunks of 10,000 rows each
    num_chunks = len(combined_df) // 10000 + (1 if len(combined_df) % 10000 else 0)
    chunks = [combined_df.iloc[i * 10000 : (i + 1) * 10000] for i in range(num_chunks)]

    # Saving each chunk as a separate CSV with a filename based on date ranges
    for idx, chunk in tqdm(enumerate(chunks)):
        start_date = pd.to_datetime(chunk["last_edit"].iloc[0]).strftime("%d%m%y")
        end_date = pd.to_datetime(chunk["last_edit"].iloc[-1]).strftime("%d%m%y")
        filename = f"BitcoinForum_{board}_{start_date}_to_{end_date}.csv"
        chunk.to_csv(os.path.join(sorted_folder, filename), index=False)


folder_paths = [
    "./raw-data",
    "./preprocessed-data",
]

# Iterating over each folder path and processing its CSV files
for folder_path in folder_paths:
    folder_name = os.path.basename(folder_path)
    new_folder_name = f"sorted-{folder_name}"
    for folder in tqdm(os.listdir(folder_path)):
        if os.path.isdir(os.path.join(folder_path, folder)):
            process_csvs(os.path.join(folder_path, folder), new_folder_name)
