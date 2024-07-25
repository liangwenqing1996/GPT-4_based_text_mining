import os
import json
import re

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    new_data = {}
    for k,v in data.items():
        k = get_valid_filename(k)
        new_data[k] = v
    return new_data

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as text_file:
        content = text_file.read()
    return content

def save_to_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as result_file:
        result_file.write(content)

def get_valid_filename(filename, name_len=128):
    return re.sub(r'[^0-9A-Za-z\-,._;]', '_', filename)[:name_len]

def process_folder(json_file_path, folder_path, output_folder):
    dois_data = read_json(json_file_path)

    for doi_file_name in os.listdir(folder_path):
        if doi_file_name.endswith('.txt'):
            doi = doi_file_name[:-4]  # Remove the file extension
            if doi[3] == '_':
                doi = doi[:3]
            else:
                doi = doi[:4]
            title = dois_data[doi]['title']
            abstract = dois_data[doi]['abstract']

            # Read text content from file
            text_file_path = os.path.join(folder_path, doi_file_name)
            text_content = read_text_file(text_file_path)

            # Create the final content
            result_content = "You are an expert in environmental science, toxicology, and pharmacology, specializing in oxidative stress. Please read the text inside the triple curly braces and extract the desired information.\n {{{\n"
            result_content += f"Title: {title}\nAbstract: {abstract}\nText: {text_content}"
            result_content += "}}}"

            # Append additional content from prompt.txt
            prompt_file_path = 'prompt.txt'
            if os.path.exists(prompt_file_path):
                prompt_content = read_text_file(prompt_file_path)
                result_content += f"\n{prompt_content}"

            # Save the result to a new file in the output folder
            result_file_path = os.path.join(output_folder, f"{doi}.txt")
            save_to_file(result_file_path, result_content)

if __name__ == "__main__":
    json_file_path = 'title_abstract.json'  # title and abstract information file path
    folder_path = '..\selected_text'  # text selection result folder path
    output_folder = '..\chatgpt4_input_text'  # gpt input text folder path

    process_folder(json_file_path, folder_path, output_folder)
