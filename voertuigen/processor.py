"""Module for processing cvs input data:
    - translate DE names into EN names
    - convert date into ISO format
    - normalize data
    - group data by model name
"""
import pandas as pd
import numpy as np
from voertuigen.translation.vehicle_type import vehicle_type_trans
from voertuigen.translation.body_type import body_type_trans
from voertuigen.translation.colour import colour_trans
import io

DATE_OUTPUT_FORMAT = "%Y-%m-%dT%H:%M:%S.000Z"

#CSV file columns
COLUMNS_DE = "Kenteken,Voertuigsoort,Merk,Handelsbenaming,Datum tenaamstelling,Inrichting,Aantal zitplaatsen,Eerste kleur,Aantal cilinders,Cilinderinhoud,Europese voertuigcategorie".split(',')
COLUMNS_EN = "License plate,Vehicle type,Brand,Trade name,Date of registration,Body type,Number of seats,First colour,Number of cylinders,Engine capacity,European vehicle category".split(',')
#Columns with dates
DATE_COLUMNS = ["Datum tenaamstelling"]
VOCAB_COLUMNS = ["Vehicle type","Brand","Trade name","Body type","First colour","European vehicle category"]

def normalize_name(name):
    """Normalize string for use in filename"""
    return name.replace(" ", "_").replace(".", "_").replace("/","_").lower()

def create_vocab_from_column(values) -> pd.DataFrame:
    return pd.DataFrame((enumerate(values,start=1)))

def generate_vocabs(df:pd.DataFrame):
    res = {}
    for c in VOCAB_COLUMNS:
        values = df[c].unique()
        res[c] = dict(enumerate(values,start=1))
    return res


def load_csv(file_content) -> pd.DataFrame:
    """Load content into a DataFrame and translate values"""
    df = pd.read_csv(file_content, parse_dates=DATE_COLUMNS)
    df[DATE_COLUMNS] = df[DATE_COLUMNS].apply(pd.to_datetime, utc=True)
    df.rename(columns=dict(zip(COLUMNS_DE, COLUMNS_EN)), inplace=True)
    df.replace({
        "Vehicle type": vehicle_type_trans, 
        "Body type": body_type_trans, 
        "First colour": colour_trans
        }, inplace=True)
    df.replace("N/A",np.nan,inplace=True)
    return df

def process(file_content):
    """Main function"""
    df = load_csv(file_content)
    #Normalize data using vocabularies
    vocabs = generate_vocabs(df)
    vocabs_inverse = {}
    for col_name, vocab in vocabs.items():
        vocabs_inverse[col_name] = {v:k for k,v in vocab.items()}
        with io.StringIO() as csv_buffer:
            pd.DataFrame.from_dict(vocab, orient='index').to_csv(csv_buffer, index=True, header=None)
            col_name = normalize_name(str(col_name))
            name = "vocab_{}.csv".format(col_name) #filename or s3 key
            yield name, csv_buffer
    #Replace text with vocab_id
    df.replace(vocabs_inverse, inplace=True)
    for name, group in df.groupby(["Brand"]):
        with io.StringIO() as csv_buffer:
            group.to_csv(csv_buffer, index=False, date_format=DATE_OUTPUT_FORMAT)
            name = normalize_name(vocabs["Brand"][name])
            yield "brand_{}.csv".format(name), csv_buffer