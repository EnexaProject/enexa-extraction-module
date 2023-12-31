#a_directory_with_text_files > json_lines_with_chunked_corefed_text.jsonl

import os
import nltk
import json
from nltk.tokenize import sent_tokenize
from crosslingual_coreference import Predictor
import argparse

def download_model_if_necessary(model):

    downloader = nltk.downloader.Downloader()
    if(not downloader.is_installed(model)):
        downloader.download(model)

# Download the necessary nltk model if it is not already installed
download_model_if_necessary('punkt')

def read_text_files(directory):
    
    text_files = []
    for file in os.listdir(directory):
        file_dict = dict()
        if file.endswith(".txt"):
            file_name = file.split('.')[0].strip()
            with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
                text = f.read()
                file_dict[file_name] = text
        text_files.append(file_dict)
    
    return text_files


def chunk_text(text):
    
    text = text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').replace('\\', ' ').replace('[citation needed]', ' ').replace('  ', ' ')
    text = sent_tokenize(text)
    chunked_text = list(divide_chunks(text, 2))
    
    return chunked_text


def divide_chunks(l, n):
      
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]


def get_coref_annotations(text_files, predictor):
    data = []
    for ind, file_dict in enumerate(text_files):
        for key, value in file_dict.items():
            print(key)
            chunked_text = chunk_text(value)
            for i, chunk in enumerate(chunked_text):
                annotations = dict()
                annotations['Document ID'] = ind +1 
                annotations['Document Name'] = key
                annotations['Chunk ID'] = i+1
                r = predictor.predict(' '.join(chunk))
                annotations["Chunk text"] =  r["resolved_text"]
                data.append(annotations) 

    return data


def get_annotations(text_files):
    data = []
    for ind, file_dict in enumerate(text_files):
        for key, value in file_dict.items():
            
            chunked_text = chunk_text(value)
            for i, chunk in enumerate(chunked_text):
                annotations = dict()
                annotations['Document ID'] = ind +1 
                annotations['Document Name'] = key
                annotations['Chunk ID'] = i+1
                annotations["Chunk text"] = ' '.join(chunk)
                data.append(annotations) 

    return data



def write_jsonl(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in data:
            line = json.dumps(line, ensure_ascii=False)
            f.write(f'{line}\n')

def main(): 
    parser = argparse.ArgumentParser(description='Coreference Resolution')
    parser.add_argument('-i', '--input_dir', type=str, default= '/home/finapolat/KG_extraction_for_ENEXA_Hackathon/scripts/downloads/', help='Directory with text files')
    parser.add_argument('-o', '--output', type=str, default='/home/finapolat/KG_extraction_for_ENEXA_Hackathon/scripts/data/preprocessed_data_coref.jsonl', help='Output file')
    args = parser.parse_args()
    
    predictor = Predictor(language="en_core_web_sm", device=-1, model_name="minilm")
    text_files = read_text_files(args.input_dir)    
    data = get_coref_annotations(text_files, predictor) 
    #data = get_annotations(text_files)
    
    write_jsonl(data, args.output)
    
    
    
if __name__ == '__main__':
    main()
        
