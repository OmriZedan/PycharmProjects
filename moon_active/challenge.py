import os
import re
import time

import cv2
import pytesseract
from sqlalchemy import create_engine
import pandas as pd

# ============================================= GLOBAL PARAMS/DEFINITIONS ============================================ #

MISSING = 'missing'

# ============================================= INITIALIZE COMPONENTS ================================================ #

pd.set_option("display.max_rows", None, "display.max_columns", None)
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'

engine = create_engine('postgresql://postgres:123QWEsa!@localhost:5432/parkinglot')


# ================================================ HELPER METHODS ==================================================== #

def query_entrance_approval(plate: str) -> (str, str):
    """
    Decide whether a given vehicle's registration plate permits it's entrance to the parking lot.
    :param plate: a string representation of the registration plate.
    :return: 2 values (decision, reason).
    """
    _plate = plate.upper()

    if MISSING == plate:
        return "not approved", "Could not retrieve"
    if _plate.endswith('G') or _plate.endswith('6'):
        return "not approved", "Public transportation"
    if 'M' in _plate or 'L' in _plate:
        return "not approved", "Military"
    if re.match('^\d+$', _plate):
        return "not approved", "All numbers"
    return "approved", "good plate"


def find_plate_number_in_pytesseract_result(pytesseract_result: str) -> str:
    """
    Extract vehicle registration plate from pytesseract scan result.
    :param pytesseract_result: scan result.
    :return: if found, a string representation plate of the plate. else a MISSING-PLATE notion.
    """
    for line in pytesseract_result.split('\n'):
        line = line.strip()
        if re.match('^[a-zA-Z0-9_]+$', line) and len(line) >= 6:
            return line
    return MISSING


def detect_plate_number(image_path: str) -> (str, str):
    """
    detect vehicle registration plate in an image.
    :param image_path: path to image.
    :return: if found, a string representation plate of the plate. else a MISSING-PLATE notion.
    """
    img = cv2.imread(filename=image_path)
    result = pytesseract.image_to_string(img, lang='eng',
                                         config='--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    return time.strftime('%Y-%m-%d %H:%M:%S'), find_plate_number_in_pytesseract_result(pytesseract_result=result)


# ================================================ MAIN SCRIPT ======================================================= #

data_path = "data"
data = dict()
path = os.walk(data_path)
image_paths = []
# Try retrieving images from directory
for root, directories, images in path:
    for image in images:
        image_paths.append(os.path.join(root, image))
assert image_paths != [], "Message: Failed to retrieve images!"

# build a pandas DataFrame from image-paths
df = pd.DataFrame({'image path': image_paths})

# Retrieve a plate scan from image using 'detect_plate_number' method.
df['scan'] = df['image path'].apply(detect_plate_number)

# Divide 'scan' column into 'timestamp' and 'registration plate'.
df['timestamp'] = df['scan'].apply(lambda t: t[0])
df['registration plate'] = df['scan'].apply(lambda t: t[1])

# Get approval for each plate using 'query_entrance_approval' method.
df['approval query'] = df['registration plate'].apply(query_entrance_approval)

# Divide 'approval query' column into 'approval' and 'reason for approval'.
df['approval'] = df['approval query'].apply(lambda t: t[0])
df['reason'] = df['approval query'].apply(lambda t: t[1])

df.drop(columns=['image path', 'scan', 'approval query'], inplace=True)

try:
    df.to_sql('car details', engine, if_exists='append')
except Exception as e:
    raise ConnectionError(f"Message: could not write to database!\nerror message: {str(e)}")

print(f"\n\n{len(df)} rows successfully writen to data base\n\n")
print(df)
