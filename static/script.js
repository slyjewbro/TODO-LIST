// AJAX для плавного выполнения/удаления задач
document.addEventListener('DOMContentLoaded', function() {
    // Плавное удаление задачи
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (confirm('Удалить задачу?')) {
                const taskItem = this.closest('.task-item');
                taskItem.style.opacity = '0';
                taskItem.style.transform = 'translateX(100px)';
                
                setTimeout(() => {
                    window.location.href = this.href;
                }, 300);
            }
        });
    });
    
    // Анимация добавления новой задачи
    const taskForm = document.querySelector('.task-form');
    if (taskForm) {
        taskForm.addEventListener('submit', function() {
            const addBtn = this.querySelector('.add-btn');
            addBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Добавляем...';
            addBtn.disabled = true;
        });
    }
    
    // Подсветка приоритета
    document.querySelectorAll('.task-item').forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 8px 25px rgba(0,0,0,0.15)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.boxShadow = '0 5px 15px rgba(0,0,0,0.1)';
        });
    });
});