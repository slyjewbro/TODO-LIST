from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key='lfkdsagjlg1324'
# Создаем необходимые папки
for folder in ['templates', 'static', 'static/images']:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Инициализация БД
def init_db():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0,
            priority INTEGER DEFAULT 2,
            due_date TEXT,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Категории задач
CATEGORIES = ['Работа', 'Личное', 'Здоровье', 'Обучение', 'Финансы', 'Хобби', 'Другое']

@app.route('/')
def index():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    tasks = conn.execute('''
        SELECT * FROM tasks 
        ORDER BY 
            CASE WHEN completed = 1 THEN 1 ELSE 0 END,
            priority ASC,
            created_at DESC
    ''').fetchall()
    conn.close()
    
    # Добавляем вычисляемые поля
    tasks_with_extra = []
    for task in tasks:
        task_dict = dict(task)
        
        # Проверяем просроченные задачи
        if task_dict['due_date']:
            try:
                due_date = datetime.strptime(task_dict['due_date'], '%Y-%m-%d').date()
                today = datetime.now().date()
                task_dict['is_overdue'] = due_date < today and not task_dict['completed']
            except ValueError:
                task_dict['is_overdue'] = False
        else:
            task_dict['is_overdue'] = False
        
        tasks_with_extra.append(task_dict)
    
    return render_template('index.html', tasks=tasks_with_extra, categories=CATEGORIES)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form.get('description', '')
    priority = request.form.get('priority', 2)
    category = request.form.get('category', '')
    due_date = request.form.get('due_date', '')
    
    if title.strip():
        conn = sqlite3.connect('todo.db')
        conn.execute(
            '''INSERT INTO tasks (title, description, created_at, priority, category, due_date) 
               VALUES (?, ?, ?, ?, ?, ?)''',
            (title.strip(), description.strip(), datetime.now().strftime('%Y-%m-%d %H:%M'), 
             priority, category, due_date)
        )
        conn.commit()
        conn.close()
    
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    conn = sqlite3.connect('todo.db')
    conn.execute('UPDATE tasks SET completed = NOT completed WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect('todo.db')
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    conn = sqlite3.connect('todo.db')
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        priority = request.form.get('priority', 2)
        category = request.form.get('category', '')
        due_date = request.form.get('due_date', '')
        
        conn.execute('''
            UPDATE tasks SET 
                title = ?, description = ?, priority = ?, category = ?, due_date = ?
            WHERE id = ?
        ''', (title, description, priority, category, due_date, task_id))
        
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    
    if task:
        return render_template('edit_task.html', task=dict(task), categories=CATEGORIES)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False, port=500,host='127.0.0.1')