import os
import shutil
from pathlib import Path


def object_upload(file_root, base_dir, obj_list_to_upload):
    obj_list_uploaded = []
    Path(file_root).mkdir(parents=True, exist_ok=True)
    for pic in obj_list_to_upload:
        if pic.filename:
            filename = duplicate_name_check(file_root, pic.filename)
            with open(os.path.join(file_root, filename), 'wb') as image:
                shutil.copyfileobj(pic.file, image)
            obj_list_uploaded.append(os.path.join((str(file_root).replace(str(base_dir), '')), filename))

    return obj_list_uploaded


def duplicate_name_check(file_root, filename):
    dir_files = os.listdir(file_root)
    filename = filename.replace(' ', '_')
    count_unique = dir_files.count(filename)
    if count_unique > 0:
        return f'{count_unique}_{filename}'
    return filename


def object_delete(file_root, obj_str_to_delete):
    file_path = os.path.join(file_root, obj_str_to_delete.strip('\\'))
    if os.path.exists(file_path):
        os.remove(file_path)
