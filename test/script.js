class Task {
    _isSelected = false;

    constructor(element) {
        this.container = element;
    };

    Init() {
        const task = this.container;

        task.addEventListener('click', () => {
            this.ToggleSelected();
            
            console.log(task);
        })
    };

    ToggleSelected() {
        this._isSelected = !this._isSelected;

        this.container.classList.toggle('is-selected');
    };

    GetSelected() {
        return this._isSelected;
    };

    SetSelected(boolValue) {
        this._isSelected = boolValue; 
    };
};

class Task_grid {
    constructor(element) {
        this.container = element;

        this.tasksArray = Array.from(this.container?.querySelectorAll('.task'), taskElement => new Task(taskElement));

        this.Init();

    };


    Init() {
        this.tasksArray.forEach((task) => {
            task.Init();

            console.log(task);
        });
    }
};


const tasks = new Task_grid(document.querySelector('.task-grid'));

console.log(tasks);


