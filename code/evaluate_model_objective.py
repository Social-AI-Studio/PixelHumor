'''
Model evaluation
'''

import json
import pandas as pd
import re
from jiwer import wer, cer
import ast
from tabulate import tabulate

from collections import defaultdict

def concatenate_panels(panel_list):
    # Regex pattern to match leading panel number followed by content
    pattern = r'^(\d+):'
    
    result = []
    current_panel = ""
    
    for item in panel_list:
        # Check if the item starts with a panel number
        match = re.match(pattern, item)
        
        if match:
            # If there is an existing panel, append it to result
            if current_panel:
                result.append(current_panel.strip())
            
            # Start a new panel with the matched number and content
            current_panel = item
        else:
            # Concatenate the current content to the existing panel
            current_panel += " " + item
    
    # Append the last panel
    if current_panel:
        result.append(current_panel.strip())
    
    return " ".join(result)

def map_panels_by_lines(example):
    # Parse panel_sequence to get the order of the keys
    panel_order = list(example['panel_sequence'].split(','))
    panel_order = [x.strip() for x in panel_order]

    leading_text_match = re.match(r'(.*?)(?=\d+:)"', example['text'], re.DOTALL)
    leading_text = leading_text_match.group(1).strip() if leading_text_match else ""

    # Parse text using regex to extract key-value pairs
    pattern = r'(\d+):\s*(.*?)(?=(\d+: |$))'
    matches = re.findall(pattern, example['text'], re.DOTALL)
    
    # Group the values by key
    grouped_values = defaultdict(list)
    for key, value, _ in matches:
        value = value.strip()
        if len(value) == 0:
            grouped_values[key].append('')
            continue
        if value[0] == '"' and value[-1] == '"':
            value = value[1:-1]
        if len(value) == 0:
            print(cid)
        if value[0] == '{' and value[-1] == '}':
            value = value[1:-1]
        if value[0].isdigit():
            if len(value.strip()) <= 2:
                value = ''
            elif value[1] == ')' or value[1] == '\n':
                value = value[2:]
        grouped_values[key].append(value)

    # Reorder and format based on panel_sequence
    panel_result = []
    no_panel_result = []
    
    if leading_text != '':
        panel_result.append(leading_text.strip())
        no_panel_result.append(leading_text.strip())

    for idx, key in enumerate(panel_order, start=1):
        values = grouped_values.get(key, [])

        combined_value = ' '.join(values)
        combined_value = combined_value.replace('\n', ' ')

        panel_result.append(f"{str(idx)}: {combined_value}")
        no_panel_result.append(combined_value)
    
    # Join everything with newlines
    return " ".join(panel_result).lower(), " ".join(no_panel_result).lower()

def calculate_scores(panel_reference, no_panel_reference, panel_candidate, no_panel_candidate):
    panel_reference = re.sub(r'\s+', ' ', panel_reference).strip()
    no_panel_reference = re.sub(r'\s+', ' ', no_panel_reference).strip()
    panel_candidate = re.sub(r'\s+', ' ', panel_candidate).strip()
    no_panel_candidate = re.sub(r'\s+', ' ', no_panel_candidate).strip()

    if no_panel_reference == '':
        if no_panel_candidate != '':
            return 0, len(no_panel_candidate.split(' ')), len(no_panel_candidate)
        else:
            return 1, 0, 0

    accuracy = int(panel_reference == panel_candidate)
    wer_score = wer(no_panel_reference, no_panel_candidate)
    cer_score = cer(no_panel_reference, no_panel_candidate)
    
    return accuracy, wer_score, cer_score

def tabulate_data(scores, model):
    all_metrics = ['Accuracy', 'WER', "CER"]
    # Define headers with dynamic metrics
    headers = ["Model", "Question"] + list(all_metrics)

    # Preparing data for the table dynamically
    table_data = []
    # for model, metrics in scores.items():
    for model in ['gpt-4o', 'gemini-1.5-pro', 'llava-ov', 'qwen2-vl', 'gemma3-27b', 'qwen2-72b']:
        metrics = scores[model]
        for qn, metric_values in metrics.items():
            row = [model, qn]
            for metric in all_metrics:
                score_lst = metric_values.get(metric, "N/A")
                if len(score_lst) == 0:
                    continue
                if isinstance(score_lst, list):
                    score = round(sum(score_lst) / len(score_lst),3)
                else:
                    score = 'N/A'
                row.append(score)  # Handle missing values
            table_data.append(row)

    print(tabulate(table_data, headers=headers, tablefmt="pretty"))

def safe_eval(val):
    if isinstance(val, str) and val.strip() and val.strip()[0] in "[{(":
        try:
            return ast.literal_eval(val)
        except (ValueError, SyntaxError):
            return val
    return val

if __name__ == '__main__':
    SCORE = {
        'gemini-1.5-pro': {'panel_sequence': {'Accuracy': []}, 'text': {'Accuracy': [], 'WER': [], 'CER': []}},
        'gpt-4o': {'panel_sequence': {'Accuracy': []}, 'text': {'Accuracy': [], 'WER': [], 'CER': []}},
        'llava-ov': {'panel_sequence': {'Accuracy': []}, 'text': {'Accuracy': [], 'WER': [], 'CER': []}},
        'qwen2-vl': {'panel_sequence': {'Accuracy': []}, 'text': {'Accuracy': [], 'WER': [], 'CER': []}},
        'gemma3-27b': {'panel_sequence': {'Accuracy': []}, 'text': {'Accuracy': [], 'WER': [], 'CER': []}},
        'qwen2-72b': {'panel_sequence': {'Accuracy': []}, 'text': {'Accuracy': [], 'WER': [], 'CER': []}}
    }

    ground_truth = pd.read_csv('../PixelHumor/objective_label.csv', index_col=False)
    ground_truth = ground_truth.map(safe_eval)

    for model_name in ['gpt-4o', 'gemini-1.5-pro', 'llava-ov', 'qwen2-vl', 'gemma3-27b', 'qwen2-72b']:
        print(f'Current evaluating {model_name}...')
        with open(f'../model_response/{model_name}_objective.json', 'r') as f:
            model_annotation = json.load(f)

        print('=====EVALUATING OBJECTIVE QUESTIONS=====')
        for i, data in ground_truth.iterrows():
            cid = data['comic_id']
            for qid, d in data.items():
                print(qid, d)
                models_annotated = model_annotation[cid]

                if qid == 'panel_sequence':
                    answer = data[qid].replace(" ", "")
                    answer = data[qid].split(",")
                    answer = [int(x) for x in answer]

                    response = models_annotated['panel_sequence']
                    response = response.replace(" ", "").split(",")
                    response = [int(x) for x in response if x.isdigit()]

                    if len(response) < 1:
                        print(cid)
                        SCORE[model_name][qid]['Accuracy'].append(0)
                        continue

                    SCORE[model_name]['panel_sequence']['Accuracy'].append(int(response == answer))
                    
                if qid == 'text':
                    panel_answer, no_panel_answer  = map_panels_by_lines({'panel_sequence': data['panel_sequence'], 'text': data['text']})

                    panel_response, no_panel_response = map_panels_by_lines({'panel_sequence': model_annotation[cid]['panel_sequence'], 'text': model_annotation[cid]['text']})

                    accuracy, wer_score, cer_score = calculate_scores(panel_answer, no_panel_answer, panel_response, no_panel_response)

                    SCORE[model_name]['text']['Accuracy'].append(accuracy)
                    SCORE[model_name]['text']['WER'].append(wer_score)
                    SCORE[model_name]['text']['CER'].append(cer_score)

    tabulate_data(SCORE, model_name)