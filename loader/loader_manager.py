import os
import random

from loader.exceptions import PictureFormatNotSupportedError, OutOfFreeNamesError, PictureNotUploadedError


class LoaderManager:

    def get_free_filename(self, folder, file_type):
        attemps = 0
        RANGE_IMAGE_NUMBERS = 100
        LIMIT_ATTEMPS = 1000

        while True:
            pic_name = str(random.randint(0, 10))
            filename_to_save = f'{pic_name}.{file_type}'
            os_path = os.path.join(folder, filename_to_save)
            is_filename_occupied = os.path.exists(os_path)
            if not is_filename_occupied:
                return filename_to_save

            attemps += 1

            if attemps > LIMIT_ATTEMPS:
                raise OutOfFreeNamesError('No free names')

    def is_file_type_valid(self, file_type):
        if file_type.lower() in ['jpg', 'jpeg', 'gif', 'png', 'webp']:
            return True
        return False

    def save_with_random_name(self, picture):
        filename = picture.filename
        file_type = filename.split('.')[-1]

        if not self.is_file_type_valid(file_type):
            raise PictureFormatNotSupportedError(f'Формат {file_type} не поддерживается')

        folder = os.path.join('.', 'uploads', 'images')
        filename_to_save = self.get_free_filename(folder, file_type)  # Получаем свободное имя
        try:
            picture.save(os.path.join(folder, filename_to_save))  # Сохраняем под новым именем
        except FileNotFoundError:
            raise PictureNotUploadedError(f'{folder, filename_to_save}')

        return filename_to_save
