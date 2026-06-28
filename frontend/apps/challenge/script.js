import Task from './components/task.js';
import TaskGrid from './components/taskGrid.js';
import SubmitButton from './components/submitButton.js';

const tasks = new TaskGrid(document.querySelector('.task-grid'));

const submitButton = new SubmitButton(document.querySelector('.submit-button'), tasks.GetTasksArray());

// tasks.GetTasksArray().forEach(task => {
//     task.SetPhoto('penguin.png');
// })

console.log(tasks);


