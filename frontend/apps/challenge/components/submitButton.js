export default class SubmitButton {
    constructor(element, tasks) {
        this.container = element;
        this.tasks = tasks;

        this.selectedTasks = [];

        this.Init();
    }

    Init() {
        this.container.addEventListener('click', () => {
            this.tasks.forEach(task => { 
                if(task.GetSelected()) {
                    console.log(`selected: ${task}`);
                    this.selectedTasks.push(task);
                }
            });    
        })
    }


};