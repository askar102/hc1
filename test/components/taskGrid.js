import Task from './task.js';

export default class TaskGrid {
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