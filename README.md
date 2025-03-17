The official repository for the paper: "Comprehensive characterization of oxidative stress-modulating chemicals using GPT-based text mining".

## Code Introduction

### 1. PDF_parsing.py

Function: Extract text content from PDF files using Microsoft Azure AI.

Input：PDF documents

Output：Parsed text in .txt files

### 2. text_preprocessing.py

Function: Select text relavent to target information. This code is highly specific to our study aim; however, the selection rules and code logic are transferable and can be adapted to other tasks.

Input: Parsed text in .txt files

Output: Selected text in .txt files

### 3. concat_prompt_text.py

Function: Concat the designed prompt in .txt file and the selected text in .txt files. 

Input: Designed prompt in .txt file and selected text in .txt files

Output: Input file for ChatGPT4 in .txt files

### 4. run_gpt.py

Function: Query in batch using ChatGPT4 API and retrive the answers.

Input: Input file for ChatGPT4 in .txt files

Output: Answers in .txt files

## Citation

If you find our code useful, we kindly request that you cite the following paper:
Liang W Q, Su W Y, Zhong L J, Yang Z D, Li T Y, Liang Y, Ruan T, Jiang G B. Comprehensive characterization of oxidative stress-modulating chemicals using GPT-based text mining. Environmental Science & Technology, 2024, 58 (46): 20540−20552.
If you have any issues, please contact with wqliang_st@rcees.ac.cn
