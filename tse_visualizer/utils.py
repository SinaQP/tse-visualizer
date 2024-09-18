import os
import arabic_reshaper
from bidi.algorithm import get_display
from matplotlib import font_manager as fm
import json

def reshape_persian_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

def load_font(font_name='Sahel.ttf'):
    font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', font_name)
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"فونت یافت نشد: {font_path}")

    font_prop = fm.FontProperties(fname=font_path)
    fm.fontManager.addfont(font_path)
    return font_prop


def load_shapes_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        shapes_data = json.load(f)
    return shapes_data

