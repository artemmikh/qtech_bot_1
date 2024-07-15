from typing import Optional, List

from fastapi import Request, UploadFile, File


IMAGE_FILE_FORMAT = {'jpeg', 'png', 'webp', 'tiff', 'svg', 'gif', 'heif', 'jpg'}

class ButtonForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.name: Optional[str] = None
        self.is_moscow: Optional[bool] = None
        self.text: Optional[str] = None
        self.is_department: Optional[bool] = None
        self.is_active: Optional[bool] = None
        self.file_pic: list[UploadFile] = File(...)
        self.file_doc: list[UploadFile] = File(...)

    async def load_data(self):
        form = await self.request.form()
        self.name = form.get('name')
        self.is_moscow = form.get('is_moscow')
        self.text = form.get('text')
        self.is_department = form.get('is_department')
        self.is_active = form.get('is_active')
        self.file_pic = form.get('file_pic')
        self.file_doc = form.get('file_doc')

    async def is_valid(self):
        if not self.name or not len(self.name) > 1:
            self.errors.append('Название кнопки должно содержать минимум 2 символа')
        if not self.text or not len(self.name) >= 0:
            self.errors.append('Кнопка должна содержать текст')
        if len(self.text) > 1024:
            self.errors.append('Количество символов не должно быть более 1024')
        if self.file_pic.filename.split('.')[-1].lower() not in IMAGE_FILE_FORMAT:
            self.errors.append('В разделе картинки нужно прикрепить верный файл с расширениями: jpeg, png, webp, tiff, svg, gif, heif, jpg')

        if not self.errors:
            return True
        return False


