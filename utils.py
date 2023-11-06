import pandas as pd
import glob
from datetime import datetime
import xml.etree.ElementTree as ET


log_file = "log_file.txt"
target_file = "transformed_data.csv"


def extract_from_csv(file_to_process):
    dataframe = pd.read_csv(file_to_process)
    return dataframe


def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process, lines=True)
    return dataframe


def extract_from_xml(file_to_process):
    dataframe = pd.DataFrame(columns=["name", "height", "weight"])
    tree = ET.parse(file_to_process)
    root = tree.getroot()
    for person in root:
        name = person.find("name").text
        height = float(person.find("height").text)
        weight = float(person.find("weight").text)
        dataframe = pd.concat([dataframe, pd.DataFrame(
            [{"name": name, "height": height, "weight": weight}])], ignore_index=True)
    return dataframe


def extract():
    # create empty df
    extracted_data = pd.DataFrame(columns=["name", "height", "weight"])

    # process all csv
    for csvfile in glob.glob("data/*.csv"):
        extracted_data = pd.concat([extracted_data, pd.DataFrame(
            extract_from_csv(csvfile))], ignore_index=True)

    # process all json
    for jsonfile in glob.glob("data/*.json"):
        extracted_data = pd.concat([extracted_data, pd.DataFrame(
            extract_from_json(jsonfile))], ignore_index=True)
        
    # process all xml
    for xmlfile in glob.glob("data/*.xml"):
        extracted_data = pd.concat([extracted_data, pd.DataFrame(
            extract_from_xml(xmlfile))], ignore_index=True)
    
    return extracted_data


def transform(data):
    '''Convert inches to meters and round off to two decimals 
    1 inch is 0.0254 meters 
    Convert pounds to kilograms and round off to two decimals 
    1 pound is 0.45359237 kilograms
    '''
    data = data \
        .assign(
            height = lambda x:x["height"] * 0.0254,
            weight = lambda x:x["weight"] * 0.45359237
            ) \
        .round(2)
    
    return data


def load_data(target_file, data_to_load):
    data_to_load.to_csv(target_file)
    
    
def log_progress(message):
    # Year-Monthname-Day-Hour-Minute-Second 
    timestamp_format = "%Y-%h-%d-%H-%M-%S"
    
    # Current timestamp
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    
    with open(log_file, "a") as f:
        f.write(timestamp + "," + message + "\n")