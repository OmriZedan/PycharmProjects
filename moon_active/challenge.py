import os
import re

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


def detect_plate_number(image_path: str) -> str:
    """
    detect vehicle registration plate in an image.
    :param image_path: path to image.
    :return: if found, a string representation plate of the plate. else a MISSING-PLATE notion.
    """
    img = cv2.imread(filename=image_path)
    result = pytesseract.image_to_string(img, lang='eng',
                                         config='--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    return find_plate_number_in_pytesseract_result(pytesseract_result=result)


# ================================================ MAIN SCRIPT ======================================================= #

data_path = "data"
data = dict()
path = os.walk(data_path)
image_paths = []
for root, directories, images in path:
    for image in images:
        image_paths.append(os.path.join(root, image))
assert image_paths != [], "Message: Failed to retrieve images!"

df = pd.DataFrame({'image path': image_paths})

df['registration plate'] = df['image path'].apply(detect_plate_number)
df['approval'] = df['registration plate'].apply(query_entrance_approval)
df['reason'] = df['approval'].apply(lambda t: t[1])
df['approval'] = df['approval'].apply(lambda t: t[0])

try:
    df.to_sql('car details', engine, if_exists='append')
except Exception as e:
    raise ConnectionError(f"Message: could not write to database!\nerror message: {str(e)}")

print(f"\n\n{len(df)} rows successfully writen to data base\n\n")
print(df)
