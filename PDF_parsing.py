
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import time
import re
endpoint = ""
key = ""

def format_bounding_box(bounding_box):
    if not bounding_box:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in bounding_box])

def analyze_read(input_file, output_file):
    # sample document
    docUrl = input_file

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    f = open(docUrl, 'rb').read()

    poller = document_analysis_client.begin_analyze_document("prebuilt-read", f)
    result = poller.result()

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result.content)

def get_valid_filename(filename, name_len=128):
    return re.sub(r'[^0-9A-Za-z\-,._;]', '_', filename)[:name_len]

if __name__ == "__main__":

    input_folder = 'PDF_files' # PDF files folder path
    for file in os.listdir(input_folder):
        input_file_name = os.path.join(input_folder, file)
        output_file_name = input_file_name[:-3] + 'txt'
        if input_file_name[-1] == 'f' and not os.path.exists(output_file_name):
            analyze_read(input_file_name, output_file_name)
            print(input_file_name)


