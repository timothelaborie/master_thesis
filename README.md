# Master thesis

## Title
Analyzing Bitcointalk.org with Large Language Models

## Master Thesis student
Timothé Laborie

## Supervisors
Cyrille Grumbach, Prof. Dr. Thomas Hofmann


# Folders

## scraper

File main.ipynb is used to scrape the forum.


## hardwarelist

Includes the following:

- pmaxv1 folder: contains the maximum hardware efficiency for each date alongside some manually added updates, originally made by Cyrille.
- get_hwd_asicminervalue.js and get_hwd_bitcoinwiki.js: Can be pasted into the browser console in the URLs listed within the files, used to extract the hardware efficiency table
- hardware_asicminervalue.txt and hardware_bitcoinwiki.txt: The raw output from the above scripts
- 1_cleanup_hardware_table.ipynb: Used to clean up the raw output, to create hardware_asicminervalue.csv and hardware_bitcoinwiki.csv
- 2_merge_tables.ipynb: Merges the two tables into hardware_merged.csv
- 3_paper_list.ipynb: Creates 4 things. 1: The hardware table in the appendix. 2: The pmaxv2.csv file, which uses the hardware_merged.csv file to create an improved table with the maximum hardware efficiency for each date. 3: The pmax evolution table for the paper. 4: The paper_list.csv file, which is used to create an excel sheet later
- 4_create_pmaxv3.ipynb: Creates the pmaxv3.csv file, which is the max between the pmaxv1.csv and pmaxv2.csv files


## bitcoinforum

### 1_forum_dataset

Contains the raw HTML from the forum, and code to parse it and combine it into dataframes.

### 2_train_set_creation

Combines the forum sections into one, truncates long threads, passes a random sample to GPT4 to get the training set for Mistral 7B, also creates the inputs that will be given to Mistral 7B after training.

### 3_training

Trains Mistral 7B using LoRA, on the dataset generated earlier, and saves the merged model


### 4_inference

Runs inference of the trained Mistral 7B on inputs.csv created in part 2.

### 5_processing_extracted_data

Includes the following files:

- 1_processing.ipynb: Takes the raw output from Mistral 7B and converts it into hardware_instances.csv
- 2_create_mapping.ipynb: Uses GPT4 to map the hardware names to those of the efficiency table
- 3_add_efficiency.ipynb: Merges the mapped hardware instances and the efficiency table to get hardware_instances_with_efficiency.csv
- 4_visualizations.ipynb, not_usable_threads.txt, hardware_instances_inc_threads.csv: Only used for debugging
- hardware_mapping.py: automatically generated by step 3

### 6_merging

Averages the forum efficiency on a monthly basis, then merges it alongside the Bitcoin price, hashrate, coins per block, and maximum hardware efficiency to create monthly_stuff.csv

monthly_stuff.csv contains columns: date,price,hashrate,coins_per_block,efficiency,max_efficiency

### 7_econometrics

Trains an ARIMA model and exports the predictions which are used in the plot called "pricepredictions.pdf"


## plots

Includes the following:

- carboncomparison folder: Contains the 17 sources used to create the carbon comparison table
- datasheet folder: Extracts the hashrate out of Cyrille's excel file
- hashrate_plot folder: Contains the code to create the hashrate plot (hashrate.pdf)
- carbonintensity.html: Cambridge's table for the yearly gCO2e/kWh values, found at https://ccaf.io/cbnsi/cbeci/ghg/methodology
- turningpoint.ipynb: Creates the turning point plot
- main.ipynb: Creates all other plots
- old stuff folder: Contains old plots that are no longer used



# System requirements

Running the training or inference of Mistral 7B requires an NVIDIA GPU with at least 24GB of VRAM (can also be a Runpod instance).

Everything else can be run on a normal desktop/laptop computer with python 3.10 installed.

# Operating system

Code which is not related to training or inference of Mistral 7B has been tested on Windows 10.

Code for Mistral 7B training and inference has been tested on Runpod instances.

# Installation guide for software dependencies

For the code which is not related to training or inference of Mistral 7B, use the packages listed in requirements.txt

## Installation guide for Mistral 7B training and inference

Setup a Runpod instance with the axolotl docker image, then install unsloth using the instructions at https://github.com/unslothai/unsloth

Also install SGLang for inference.

## Typical install time on a "normal" desktop computer

For the code which is not related to training or inference of Mistral 7B, the install time is around 5 minutes.

For Mistral 7B training and inference, the install time is around 1 hour.

# Demo

## Instructions to run on data

Run the code in the order listed in the folders section above.

Note: There are 3 files that normally take a long time to run. I have included a const "DEMO_MODE" at the top of each file. When turned on, the files will run on a tiny subset of the data. The original runtimes are as follows:

- The scraper takes over 12 hours to run.
- The process of creating the training set for Mistral 7B takes around 3 hours and costs about 10$ of OpenAI credits.
- The process of mapping the hardware names to those of the efficiency table takes around 3 hour and also costs about 10$ of OpenAI credits.

All other files can be run in a few minutes.

## Expected output

You should re-obtain the csv files that are already in the folders, and the plots used in the paper.

## Expected run time for demo on a "normal" desktop computer

The expected run time to run every notebook on a "normal" desktop computer is around 10 minutes (excluding the training and inference of Mistral 7B).

## Instructions for use on custom data

The code is designed only to analyse the mining section of bitcointalk.org.