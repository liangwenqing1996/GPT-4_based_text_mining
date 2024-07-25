import requests
import os

def run_gpt(input_data, model_name):
  url = "https://openai.api2d.net/v1/chat/completions"

  headers = {
    'Content-Type': 'application/json',
    'Authorization': ''  # enter your authorization code
  }

  data = {
    "model": model_name,
    "messages": [{"role": "user", "content": input_data}]
  }

  try:
    response = requests.post(url, headers=headers, json=data, timeout=200)
    print("Status Code", response.status_code)
    print("JSON Response ", response.json())
    return response.json()
  except:
    print('error')
    return None

if __name__ == '__main__':
  output_folder = '..\gpt_results' # gpt output folder path
  folder_path = r'..\chatgpt4_input_text' # gpt input folder path
  count = 0
  for file_name in os.listdir(folder_path):
    count += 1
    print("count: {}".format(count))
    prompt_file = os.path.join(folder_path, file_name)
    new_file = os.path.join(output_folder, file_name)
    print(file_name)
    if not os.path.exists(new_file):
      with open(prompt_file, 'r', encoding='utf-8') as f:
        input_data = f.read()
        res = run_gpt(input_data, 'gpt-4-1106-preview')
      if res:
        try:
          output = res['choices'][0]['message']['content']
          with open(new_file, 'w', encoding='utf-8') as f:
            f.write(output)
        except:
          print('error')
    else:
      print('Already generated, skipping')

