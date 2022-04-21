from django.http import JsonResponse
from PIL import Image


VALID_IMAGE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
]
import os.path
import random
import string
from os import path


def data_parser_and_saver(file, tag="untaged"):
    extension = ""
    for e in VALID_IMAGE_EXTENSIONS:
        if file.name.endswith(e):
            extension = e
    if extension == "":
        return 'ErrorFileType'

    if not path.exists(f"upload/{tag}"):
        os.mkdir(f"upload/{tag}")
    try:
        image = Image.open(file.file)
    except Exception as x:
        return "ErrorWhileOpening"

    result = "".join((random.choice(string.ascii_letters) for _ in range(40)))
    directory = f"upload/{tag}/{result}{extension}"
    try:
        image.save(directory)
    except Exception as x:
        return 'ErrorWhileSaving'
    return {
        "directory": directory,
        "filename": result
    }

