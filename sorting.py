import shutil
import os
# from pathlib import Path
import sys
import logging
from threading import Thread


def process_file(folder_path):
    """Функція для нобробки формату файлів"""
    # Створення словника, де ключ - це формат файлу, а значення - це відповідна папка
    file_formats = {
        'archives': ('zip', 'gz', 'tar'),
        'video': ('avi', 'mp4', 'mov', 'mkv'),
        'audio': ('mp3', 'ogg', 'wav', 'amr'),
        'documents': ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'),
        'images': ('jpeg', 'png', 'jpg', 'svg'),
    }
    
    for root, _, files in os.walk(folder_path):  # Використовуємо os.walk() для рекурсивного проходження по всіх вкладених папках
        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path):
                # Знаходимо папку для відповідного формату або використовуємо 'unknown', якщо формат не відомий
                target_folder = 'unknown'
                for folder, extensions in file_formats.items():
                    if any(file_path.endswith(extension) for extension in extensions):
                        target_folder = folder
                        break
                # Створюємо відповідну папку, якщо вона ще не існує у папці, що передана на сортування                
                target_folder_path = os.path.join(folder_path, target_folder)
                if not os.path.relpath(target_folder_path, folder_path).startswith('..'):
                 # Якщо relpath не починається з '..', це означає, що шлях target_folder_path не виходить за межі folder_path
                    target_folder_path = os.path.join(folder_path, target_folder)
                    
                if not os.path.exists(target_folder_path):
                    os.makedirs(target_folder_path)
                # Якщо файл є архівом, розархівувати його
                if target_folder == 'archives':
                # Створюємо підпапку з такою самою назвою, як архів, у папці 'archives'
                    archive_folder_name = os.path.splitext(filename)[0]
                    archive_folder_path = os.path.join(target_folder_path, archive_folder_name)
                    if not os.path.exists(archive_folder_path):
                        os.makedirs(archive_folder_path)
                # Розархівуємо архів в підпапку
                    shutil.unpack_archive(file_path, archive_folder_path)
                    os.remove(file_path)  # Видалення архіву після розархівування
                else:
                # Переміщуємо файл в папку з відповідним форматом з оновленою назвою
                    shutil.move(file_path, os.path.join(target_folder_path, filename))
               
 

def process_files_in_folder(folder_path):
    """Рекурсивна функція для обробки всіх файлів та папок всередині даної папки"""
    # Отримуємо список файлів та папок у заданій директорії
    contents = os.listdir(folder_path)
    # Перебираємо файли та папки
    for item in contents:
        item_path = os.path.join(folder_path, item)
        # Якщо елемент є файлом, обробляємо його за допомогою process_file()
        if os.path.isfile(item_path):
            process_file(folder_path)
        # Якщо елемент є папкою
        elif os.path.isdir(item_path):
            if item not in ['archives', 'video', 'audio', 'documents', 'images', 'unknown']:
            # Рекурсивно обробляємо папку
                process_files_in_folder(item_path)
                
    to_del_empty(folder_path)
                
                
def to_del_empty(folder_path):
    for root, dirs, _ in os.walk(folder_path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
            

class FolderProcessor(Thread):
    def __init__(self, folder_path):
        super(FolderProcessor, self).__init__()
        self.folder_path = folder_path

    def run(self):
        # Обробка файлів і папок в цій папці
        process_files_in_folder(self.folder_path)

def main():
    # Отримуємо шлях до папки, яка передається на сортування
    folder_path = sys.argv[1]
    # Перевіряємо, чи існує папка
    if not os.path.exists(folder_path):
        print(f"Шлях '{folder_path}' не існує.")
        return

    # Створюємо пул потоків
    thread_pool = []


    thread = FolderProcessor(folder_path)
    thread_pool.append(thread)

    # Запускаємо всі потоки
    for thread in thread_pool:
        thread.start()

    # Чекаємо, доки всі потоки завершать роботу
    for thread in thread_pool:
        thread.join()

    return 'Виконано успішно.'

if __name__ == "__main__":
    logging.basicConfig( level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Початок сортування файлів.')
    print(main())
    logging.info('Завершено сортування файлів.')