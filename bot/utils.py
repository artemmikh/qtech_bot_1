import os
from const import APP_PATH
from telegram import InputMediaDocument, InputMediaPhoto


def form_path(path):
    return os.getcwd() + APP_PATH + path


def form_media_group(doc_paths, message, media_type):
    input_media = {'doc': InputMediaDocument, 
                    'photo': InputMediaPhoto}
    media_group = list()
    caption = None
    doc_paths = doc_paths.split(' ')
    num_of_docs = len(doc_paths)
    for num, doc_path in enumerate(doc_paths, start=1):
        doc_path = form_path(doc_path)
        if num == num_of_docs:
            caption = message
        media_group.append(input_media[media_type](media=open(doc_path, 'rb'), caption=caption))
    return media_group