const taskGrid = document.getElementsByClassName('task-grid')[0];

console.log(taskGrid);

for (const task of taskGrid.children) {
    task.addEventListener('click', () => {
        console.log(task);
        let isPressed = ariaIsPressed(task.getAttribute('aria-pressed'));
        console.log(isPressed);
        task.setAttribute('aria-pressed', String(!isPressed));
    });
}


function ariaIsPressed(task_attribute) {
    if (task_attribute === "true") {
        return true;
    }

    if (task_attribute === "false") {
        return false;
    }
}