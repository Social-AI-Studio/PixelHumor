# Humor in Pixels: Benchmarking Large Multimodal Models Understanding of Online Comics
Official repository for EMNLP'25 paper "Humor in Pixels: Benchmarking Large Multimodal Models Understanding of Online Comics".

## PixelHumor
Pixel Humor collects online comics and here are the list of the comic sources. We respect the ownership of the authors, hence we will only release the urls to the comic.

1. [Cyanide and Happiness](https://explosm.net/)
2. [Garfield](https://www.gocomics.com/garfield)
3. [Peanuts](https://www.gocomics.com/peanuts)
4. [PhDcomics](https://phdcomics.com/comics)
5. [Saturday Morning Breakfast Cereal (SMBC)](https://www.smbc-comics.com/comic)
6. [They Can Talk](https://theycantalk.com)
7. [XKCD](https://xkcd.com)

Below shows the datasheet for PixelHumor:
```
- annotation.csv        # Raw annotations by annotators
- objective_label.csv   # Consolidated label by annotators
- subjective_label.csv  # Panel sequence and text data
- harm_annotations.csv  # Indicating whether the comic is potentially harmful
- full_label.csv        # Combination of objective and subjective tasks
- human_explanation.csv # Human written humor explanation for 70 selected comics
```

### Annotation
We hired 8 student annotators for the annotation of this dataset, and 4 experts are to help with resolving conflicts. The `annotation.csv` is constructed as follows:

|comic_id|A1Q1|A1Q2|...|A12Q4|A12Q5|
|---|---|---|---|---|---|
|explosm_5|['Yes']|"['Present, contribute']"|...|||

The identity of the annotators are hidden and given a annotator id to represent his/her annotation. The annotators will only annotate the subjective tasks. For detailed annotation question, refer to Appendix B in our paper.

| Question ID | Task Description |
| --- | --- |
| Q1 | Humor Presence Identification |
| Q2 | Sound Effect Identification |
| Q3 | Panel Contribution |
| Q4 | Modality Contribution |
| Q5 | Humor Style Classification |

The consolidated annotation is then served as the "gold-label" for each question and is consolidated in `subjective_label.csv`. We also included the `comic_url` for users to download the comics.

We have also annotated the text inside the comic and the panel sequence for the sequence recognition task. The data are consolidated in `objective_label.csv`.

As some comics contains dark humor and potentially harmful to people. We have annotated the comics with as `harm` and `non-harm` and consolidated the annotation in `harm_annotations.csv`.

> To utilize the time for the users, we have consolidated everything in `full_label.csv` file. We hope this helps you to save some time to read MORE comics :)

We have `human_explanation.csv` containing the humor explanation by our human annotator for 70 comics. They are used for our humor preference task.

> We also included the code to consolidate the human annotation, you can use `consolidate_gold_label.py` to do so.

## Code
You can find the prompts we are using in `prompts.py`. You can also find them in Appendix E.

### Automated Evaluation
We have included `evaluate_model_objective.py` and `evaluate_model_subjective.py` for the automated evaluation after the model inference. We stored our model predictions as follows:
```
[
    "garfield_1134": {
        "Q1": "Yes",
        "Q2": "Absent",
        "Q3": "3",
        "Q4": "Both",
        "Q5": "Exaggeration",
        "panel_sequence": "2,3,1",
        "text": "2: 2\n3: 3\n1: TEETH WHITENER\n1: YOU'RE BURNING MY RETINAS"
    },
    ...
]
```

> Note that we saved our model responses as a JSON file, hence you might need to edit the code accordingly if you stored the data differently.
