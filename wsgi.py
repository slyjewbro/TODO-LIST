import sys
import os

# Добавляем путь к проекту
path = '/home/slyjewbro/todo-list'
if path not in sys.path:
    sys.path.append(path)

# Указываем главный файл
from app import app as application