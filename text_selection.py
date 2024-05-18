import os
import re
import nltk

# match word. input word list (para and candidate)
def match_word(para_list, cand_list):
    flag = False
    for word in cand_list:
        if word[0] == '*':
            for para_word in para_list:
                if para_word.endswith(word[1:]):
                    flag = True
                    break
            if not flag:
                return False
        elif word[-1] == '*':
            for para_word in para_list:
                if para_word.startswith(word[:-1]):
                    flag = True
                    break
            if not flag:
                return False
        else:
            if word not in para_list:
                return False
        flag = False
    return True

# match str. input word str (para and candidate)
def match_str(para_str, cand_str):
    if cand_str[0] == '*':
        cand_str = cand_str[1:]
    elif cand_str[-1] == '*':
        cand_str = cand_str[:-1]
    return cand_str in para_str

# match word (end). input word list (para and candidate)
def match_last_word(para_list, cand_list):
    word = cand_list[-1]
    para_word = para_list[-1]
    if word[0] == '*':
        if para_word.endswith(word[1:]):
            return True
        else:
            return False
    elif word[-1] == '*':
        if para_word.startswith(word[:-1]):
            return True
        else:
            return False
    else:
        if word == para_word:
            return True
        else:
            return False

# input: str, list(str)
def contain_kw(para, word_candidates):
    para_list = nltk.word_tokenize(para)
    for kw in word_candidates:
        if match_str(para, kw) and match_word(para_list, kw.split()):
            return True
    return False

def contain_kw_last(para, word_candidates):
    para_list = nltk.word_tokenize(para)
    for kw in word_candidates:
        if match_str(para, kw) and match_last_word(para_list, kw.split()):
            return True
    return False

def contain_kw_state(para, word_candidates, state):
    para_list = nltk.word_tokenize(para)
    for kw in word_candidates:
        if match_str(para, kw) and match_last_word(para_list, kw.split()) and not state[kw]:
            state[kw] = True
            return True
    return False

def get_names(file_path):
    # get section name
    names = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            names.append(line.lower().strip())
    return names

def is_next_exp(paras, index, time_names, concen_names, method_names):
    para_low = paras[index].lower()
    if contain_kw(para_low, ["expos*", "treat*", "inject*", "administ*"]):
        count = 0
        if contain_kw(para_low, time_names):
            count += 1
        if contain_kw(para_low, concen_names):
            count += 1
        if contain_kw(para_low, method_names):
            count += 1
        if count >= 2:
            return True
        else:
            return False

def clean_para(file_path):
    paras = []
    with open(file_path, 'r', encoding='utf-8') as f:
        # parse section
        for i, line in enumerate(f.readlines()):
            paras.append(line.strip())
    # get_names
    section_names = get_names(r'kws\section_name.txt')
    subsection_names = get_names(r'kws\subsection_name.txt')

    # clear short non-scection-name para & fig
    new_paras = []
    for para in paras:
        para_low = para.lower()
        para_list = nltk.word_tokenize(para_low)
        # if skip_para:
        #     skip_para = False
        #     continue
        if len(para_list) == 0:
            continue
        if len(para_list) <= 10 and (not contain_kw(para_low, section_names)) and (not contain_kw(para_low, subsection_names)):
            continue
        if para_list[0] in ['table', 'figure', 'fig']:
            continue
        if ((para[0] >= 'a' and para[0] <= 'z') or para[0] in ['-', ')']) and len(new_paras) > 0:
            new_paras[-1] += ' ' + para
            continue
        new_paras.append(para)
    paras = new_paras
    new_paras = []

    # for para in paras:
    #     print(para)
    # exit()

    # filter special section
    i = 0
    del_flag = False
    intro_flag = False
    del_count = 0
    while i < len(paras):
        para_low = paras[i].lower()
        para_list = nltk.word_tokenize(para_low)
        if del_count > 0:
            del_count -= 1
        if del_count == 0 and intro_flag:
            del_flag = False
            intro_flag = False
        # 可以用nltk解析
        # find intro
        if len(para_list) <= 3 and contain_kw_last(para_low, ['introduction']):
            new_paras = []
            del_flag = True
            intro_flag = True
            del_count += 10
            i += 1
            continue
        # find reference
        if len(para_list) <= 3 and contain_kw_last(para_low, ['reference*']):
            break
        # find others
        if len(para_list) <= 5 and ((contain_kw_last(para_low, ['discussion']) and not contain_kw(para_low, [
            'result*'])) or contain_kw_last(para_low, ['conclusion*', 'summary', 'environmental implication'])):
            del_flag = True
            i += 1
            continue
        if (len(para_list) <= 15 and intro_flag and contain_kw(para_low, section_names)) or (len(para_list) <= 5 and contain_kw_last(para_low, section_names)):
            del_flag = False
            del_count = 0
        if (not del_flag) and del_count == 0:
            new_paras.append(paras[i])
        i += 1

    # for para in new_paras:
    #     print(para)
    # exit()

    return new_paras

def extract_para(paras):
    section_names = get_names(r'kws\section_name.txt')
    effect_names = get_names(r'kws\effect_name.txt')
    human_cell_names = get_names(r'kws\human_cell_names.txt')
    animal_cell_names = get_names(r'kws\animal_cell_names.txt')
    human_cell_state = {k: False for k in human_cell_names}
    animal_cell_state = {k: False for k in animal_cell_names}
    animal_names = get_names(r'kws\animal_names.txt')
    chemical_names = get_names(r'kws\chemical_names.txt')
    time_names = ["hour*","day*","week*","month*","*-hour","*-day","*-week","*-month","h","d","hpf","dpf","*-hpf","*-dpf", "*-hours","*-days","*-weeks","*-months"]
    concen_names = ["nm","nmol/l","nmol l-1","µm","µmol/l","µmol l-1","mm","mmol/l","mmol l-1","ng/l","ng l-1","µg/l","µg l-1","mg/l","mg l-1","ng/ml","ng ml-1","µg/ml","µg ml-1","mg/ml","mg ml-1","mg/kg","mg/kg/day","mg/kg bw/day","mg/kg/d","mg/kg bw/d","mg kg-1","mg kg-1 day-1","mg kg-1 d-1"]
    method_names = ["intraperitoneal*","subcutaneous*","inject*","oral*","gavage","intubat*","dietary"]
    key_para_index = []
    i = 0
    is_result = False

    while i < len(paras):
        para_low = paras[i].lower()
        para_list = nltk.word_tokenize(para_low)
        # 0. check for section
        if len(para_list) <= 5 and contain_kw(para_low, section_names):
            is_result = False
            if contain_kw(para_low, ['result*', 'discussion', 'conclusion*']):
                is_result = True
        # 1. effect name
        if contain_kw(para_low, effect_names):
            key_para_index.append(i)
            print(1, paras[i])
        # is result, then not considering things below
        if is_result:
            i += 1
            continue
        # 2. chemical para
        if contain_kw(' '.join(para_list[:5]), ['chemical*', 'reagent*']):
            if len(para_list) > 10:
                key_para_index.append(i)
                print(2, paras[i])
            else:
                if i + 1 < len(paras):
                    key_para_index.append(i + 1)
        # 3. cell para
        if contain_kw(' '.join(para_list[:8]), ['cell']) and contain_kw(' '.join(para_list[:8]), ['culture']):
            if len(para_list) > 10:
                key_para_index.append(i)
                print(3, paras[i])
            else:
                if i + 1 < len(paras):
                    key_para_index.append(i + 1)
                    print(3, paras[i+1])
        # 4. cell name
        if contain_kw_state(para_low, human_cell_names, human_cell_state) or contain_kw_state(para_low, animal_cell_names, animal_cell_state):
            key_para_index.append(i)
            print(4, paras[i])
        # 5. animal para
        if contain_kw(' '.join(para_list[:8]), animal_names):
            if len(para_list) <= 10:
                if i + 1 < len(paras):
                    key_para_index.append(i + 1)
                    print(5, paras[i+1])
            else:
                if contain_kw(' '.join(para_list[:8]), ["maintenance","culture","husbandry"]):
                    key_para_index.append(i)
                    print(5, paras[i])
        # 6. animal special 1
        if contain_kw(para_low, ["zebrafish", "embryo", "larvae", "danio rario"]) and contain_kw(para_low, ["strain", "ab", "tubingen"]):
            key_para_index.append(i)
            print(6, paras[i])
        # 7. animal special 2
        if contain_kw(para_low, ["rat", "rats", "mouse", "mice"]):
            count = 0
            if contain_kw(para_low, ["male", "female"]):
                count += 1
            if contain_kw(para_low, ["strain"]):
                count += 1
            if contain_kw(para_low, ["old", "*-old", "age", "aging"]):
                count += 1
            if contain_kw(para_low, ["weigh*", "g"]):
                count += 1
            if count >= 2:
                key_para_index.append(i)
                print(7, paras[i])
        # 8. chemical_names
        if contain_kw(' '.join(para_list[:8]), chemical_names):
            if len(para_list) <= 10:
                if i + 1 < len(paras):
                    key_para_index.append(i + 1)
                    print(8, paras[i+1])
                    if i + 2 < len(paras) and is_next_exp(paras, i + 2, time_names, concen_names, method_names):
                        key_para_index.append(i + 2)
                        print(8, paras[i + 2])
                        if i + 3 < len(paras) and is_next_exp(paras, i + 3, time_names, concen_names, method_names):
                            key_para_index.append(i + 3)
                            print(8, paras[i + 3])
            else:
                key_para_index.append(i)
                print(8, paras[i])
                if i + 1 < len(paras) and is_next_exp(paras, i + 1, time_names, concen_names, method_names):
                    key_para_index.append(i + 1)
                    print(8, paras[i + 1])
                    if i + 2 < len(paras) and is_next_exp(paras, i + 2, time_names, concen_names, method_names):
                        key_para_index.append(i + 2)
                        print(8, paras[i + 2])
        # 9. exposure para
        if contain_kw(' '.join(para_list[:8]), ["exposure","treatment*","administration"]):
            if len(para_list) <= 10:
                if i + 1 < len(paras):
                    key_para_index.append(i + 1)
                    print(9, paras[i + 1])
                    if i + 2 < len(paras) and is_next_exp(paras, i + 2, time_names, concen_names, method_names):
                        key_para_index.append(i + 2)
                        print(9, paras[i + 2])
                        if i + 3 < len(paras) and is_next_exp(paras, i + 3, time_names, concen_names, method_names):
                            key_para_index.append(i + 3)
                            print(9, paras[i + 3])
            elif contain_kw(' '.join(para_list[:8]), ["fish","zebrafish","rat*","mouse","mice","animal*", "cell", "cells"]):
                key_para_index.append(i)
                print(9, paras[i])
                if i + 1 < len(paras) and is_next_exp(paras, i + 1, time_names, concen_names, method_names):
                    key_para_index.append(i + 1)
                    print(9, paras[i + 1])
                    if i + 2 < len(paras) and is_next_exp(paras, i + 2, time_names, concen_names, method_names):
                        key_para_index.append(i + 2)
                        print(9, paras[i + 2])
        i += 1
    key_para_index = list(set(key_para_index))
    key_para_index.sort()
    key_paras = [paras[i] for i in key_para_index]

    return key_paras

def save_key_para(key_paras, file_name):
    length = 0
    with open(file_name, 'w', encoding='utf-8') as f:
        for para in key_paras:
            f.write(para + '\n')
            length += len(para.split())
    print(length)


if __name__ == '__main__':
    count = 0
    for file in os.listdir(r'..\paper_raw_txt'):
        if file[-1] == 't':
            count += 1
            print(count, ' -----------------------')
            input_file_name = os.path.join(r'..\paper_raw_txt', file)
            print(input_file_name)
            output_file_name = os.path.join('..\paper_extract_para_txt', file)
            if not os.path.exists(output_file_name):
                paras = clean_para(input_file_name)
                key_paras = extract_para(paras)
                save_key_para(key_paras, output_file_name)

