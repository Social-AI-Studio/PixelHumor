'''
Finalize with the gold label 
'''

import pandas as pd
import numpy as np
import ast
from collections import Counter

def safe_eval(val):
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return val

def majority_vote(vote_lists, qid):
    # Transpose the list of lists to group votes by index (columns)
    transposed_votes = [item for sublist in vote_lists for item in sublist]

    vote_count = Counter(transposed_votes)
    max_count = max(vote_count.values())
    if max_count == 1:
        return []
    if qid == 5:
        return [vote for vote, count in vote_count.items() if count >= 2]
        # return [vote for vote, count in vote_count.items() if count > 2]
    
    return [vote for vote, count in vote_count.items() if count == max_count]
    

df = pd.read_csv('./full_annotation.csv', index_col=False)
df = df.map(safe_eval)

label_consolidate = []

label_issue = {
    'q1': [],
    'q2': [],
    'q3': [],
    'q4': [],
    'q5': []
}

for idx, row in df.iterrows():
    label = {}
    label['comic_id'] = row['comic_id']
    for qid in range(1, 6):
        votes = []
        # Annotator 1 to 8
        for aid in range(1, 9):
            vote = row[f'A{aid}Q{qid}']
            if vote == ['Both']:
                vote = ['Text', 'Visual']
            if vote is not np.nan:
                votes.append(vote)
        assert len(votes) > 1, f"Comic {row['comic_id']} does not have enough annotations for question {qid}"

        mv = majority_vote(votes, qid)
        if len(mv) == 0:
            if qid == 1:
                print(f"Majority vote failed for comic_id {row['comic_id']} on question 1")
            for aid in range(9, 13):
                vote = row[f'A{aid}Q{qid}']
                if vote == ['Both']:
                    vote = ['Text', 'Visual']
                if vote is not np.nan:
                    votes.append(vote)
            mv = majority_vote(votes, qid)
            assert len(mv) > 0, f"Majority vote failed for comic_id {row['comic_id']} on question {qid} with {votes}"

        label[f'Q{qid}'] = mv
    label_consolidate.append(label)

label_df = pd.DataFrame(label_consolidate)
label_df['Q4'] = label_df['Q4'].apply(lambda x: ['Both'] if x == ["Text", "Visual"] else x)
label_df.to_csv('./gold_label.csv', index=False)