import pytesseract
from PIL import Image
import os

# This script checks if an image contains text using pytesseract and removes it if it does

true_txt = ""
false_txt = ""
tf = open(true_txt, "w")
ff = open(false_txt, "w")

def contains_text(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return len(text.strip()) > 5
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return False  # Handle errors or corrupted files

def check_folder(folder, true_txt, false_txt):
    for file in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, file)):
            check_folder(os.path.join(folder, file), true_txt, false_txt)
            continue
        if file.endswith(".jpg"):
            image_path = os.path.join(folder, file)
            if contains_text(image_path):
                tf.write(image_path + "\n")
                os.remove(image_path)
            else:
                ff.write(image_path + "\n")


check_folder("", true_txt, false_txt)
tf.close()
ff.close()
