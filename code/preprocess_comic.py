import pandas as pd
import cv2
import os
from ast import literal_eval

def safe_eval(val):
    try:
        return literal_eval(val)
    except (ValueError, SyntaxError):
        return val

def preprocess_image(file_path, metadata, save_path):
    comic = cv2.imread(file_path)
    if comic is None:
        raise ValueError(f"Image at path {file_path} could not be loaded.")

    for meta in metadata:
        """
        The metadata is a list of dictionaries:
        {
            "panel_number": int,
            "x1": int,
            "y1": int,
            "x2": int,
            "y2": int
        }
        """
        x1, y1, x2, y2 = meta['x1'], meta['y1'], meta['x2'], meta['y2']

        # # Draw bounding box for each panel (optional)
        # cv2.rectangle(original_comic, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Put panel number on the top-left corner of each panel
        cv2.putText(comic, str(meta['panel_number']), (x1 + 20, y1 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imwrite(save_path, comic)

COMIC_FOLDER_PATH = 'path/to/your/downloaded/comics'
if not os.path.exists(COMIC_FOLDER_PATH):
    raise ValueError(f"Comic folder path {COMIC_FOLDER_PATH} does not exist. Please download the comics first.")

comic_folder = os.listdir(COMIC_FOLDER_PATH)

# You can change the dataset folder path to your desired output folder
DATASET_FOLDER_PATH = './dataset'
os.makedirs(DATASET_FOLDER_PATH, exist_ok=True)

comic_metadata_df = pd.read_csv('./PixelHumor/metadata.csv')
comic_metadata_df['metadata'] = comic_metadata_df['metadata'].apply(safe_eval)

for comic_path in comic_folder:
    comic_id = comic_path.split('.')[0]

    comic_metadata = comic_metadata_df[comic_metadata_df['comic_id'] == comic_id]['metadata'].values[0]
    preprocess_image(
        file_path=os.path.join(COMIC_FOLDER_PATH, comic_path),
        metadata=comic_metadata,
        save_path=os.path.join(DATASET_FOLDER_PATH, comic_path)
    )

print("Preprocessing completed!")