import json
import pandas as pd
import ast
import re

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import MultiLabelBinarizer

from tabulate import tabulate
from copy import deepcopy

def safe_eval(val):
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return val

def update_score(scores, average_type='weighted'):
    mlb = MultiLabelBinarizer()
    mlb.fit(scores['Answer'] + scores['Response'])

    answer = mlb.transform(scores['Answer'])
    response = mlb.transform(scores['Response'])

    accuracy = accuracy_score(answer, response)
    precision = precision_score(answer, response, average=average_type, zero_division=0)
    recall = recall_score(answer, response, average=average_type, zero_division=0)
    f1 = f1_score(answer, response, average=average_type, zero_division=0)
    return {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1': f1}

def tabulate_data(scores, model):
    all_metrics = ['accuracy', 'f1', 'precision', 'recall']

    headers = ["Model", "Question"] + list(all_metrics)

    table_data = []

    for qn, metric_values in scores.items():
        row = [model, qn]
        for metric in all_metrics:
            score = metric_values.get(metric, "N/A")
            row.append(round(score, 3))
        table_data.append(row)

    # Display table with dynamic metrics
    print(tabulate(table_data, headers=headers, tablefmt="pretty"))

def question_based_tabulate_data(scores, qid):
    all_metrics = ['accuracy', 'f1', 'precision', 'recall']

    headers = ["Question", "Model"] + list(all_metrics)

    table_data = []

    for model in ['gpt-4o', 'gemini-1.5-pro', 'llava-ov', 'qwen2-vl', 'gemma3-27b', 'qwen2-72b']:
        row = [qid, model]
        metric_values = scores[model][f'Q{qid}']
        for metric in all_metrics:
            score = metric_values.get(metric, "N/A")
            row.append(round(score, 3))
        table_data.append(row)

    print(tabulate(table_data, headers=headers, tablefmt="pretty"))

human_annotation_result = pd.read_csv('../PixelHumor/full_label.csv', index_col=False)
human_annotation_result = human_annotation_result.map(safe_eval)

FULL_SCORE = {}

for model_name in ['gpt-4o', 'gemini-1.5-pro', 'llava-ov', 'qwen2-vl', 'gemma3-27b', 'qwen2-72b']:
    print(f'Current evaluating {model_name}...')

    # 1st is gold label, 2nd is model annotation
    CM = {
        'YY': 0,
        'YN': 0,
        'NY': 0,
        'NN': 0
    }

    with open(f'../model_response/{model_name}.json', 'r') as f:
        model_annotation = json.load(f)

    all_comics = model_annotation.keys()
    yes_annotation = human_annotation_result['comic_id'].tolist()

    no_annotation = [x for x in all_comics if x not in yes_annotation]
    print()
    
    # Comics that are labelled as not funny
    for no_comic in no_annotation:
        model_q1_response = model_annotation[no_comic]['Q1']
        if 'yes' in model_q1_response.lower():
            CM['NY'] += 1
        else:
            CM['NN'] += 1
    
    SCORE = {
        'Q1': {'Response': [], 'Answer': []},
        'Q2': {'Response': [], 'Answer': []},
        'Q3': {'Response': [], 'Answer': []},
        'Q4': {'Response': [], 'Answer': []},
        'Q5': {'Response': [], 'Answer': []}
    }
    
    for idx, row in human_annotation_result.iterrows():
        cid = row['comic_id']
        model_q1_response = model_annotation[cid]['Q1']
        if 'yes' in model_q1_response.lower():
            CM['YY'] += 1
        else:
            CM['YN'] += 1
            continue
        for qid in range(1, 6):
            answer = row[f'Q{qid}']
            response = model_annotation[cid][f'Q{qid}']

            # to check if the answer is expected
            if qid == 2:
                if isinstance(response, str):
                    response = [response]
                else:
                    print(f'Unexpected response for question {qid} in comic {cid}')
            elif qid == 3:
                response = re.findall(r'\d+', response)
            elif qid == 4:
                if response in ['Text', 'Visual', 'Both']:
                    response = [response]
                else:
                    response = []
                if len(response) > 1:
                    response = []
            elif qid == 5:
                if ',' in response:
                    response = response.split(', ')
                else:
                    response = response.split(' ')
                response = [x for x in response if x in ['Comparison', 'Personification', 'Exaggeration', 'Pun', 'Sarcasm', 'Silliness', 'Surprise', 'Dark']]
            if not isinstance(response, list):
                response = [response]

            response = [x.lower() for x in response]
            answer = [x.lower() for x in answer]

            SCORE[f'Q{qid}']['Response'].append(response)
            SCORE[f'Q{qid}']['Answer'].append(answer)

    UPDATE_SCORE = {}
    for qid in range(4,8):
        assert len(SCORE[f'Q{qid}']['Response']) == len(SCORE[f'Q{qid}']['Answer']), print(f'Length of response and answer for question {qid} is not correct')
        new_score = update_score(SCORE[f'Q{qid}'])
        UPDATE_SCORE[f'Q{qid}'] = deepcopy(new_score)

    FULL_SCORE[model_name] = UPDATE_SCORE

    print(CM)

for qid in range(4,8):
    question_based_tabulate_data(FULL_SCORE, qid)