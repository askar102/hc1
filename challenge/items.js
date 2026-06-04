const taskGrid = document.getElementsByClassName('task-grid')[0];

console.log(taskGrid);

for (const task of taskGrid.children) {
    task.addEventListener('click', () => {
        console.log(task);
        let isPressed = ariaIsPressed(task.getAttribute('aria-pressed'));
        console.log(isPressed);
        task.setAttribute('aria-pressed', String(!isPressed));

        const taskImageWrapper = task.querySelector('.task-image .wrapper');

        changeVisual(taskImageWrapper, isPressed);
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

function changeVisual(taskImageWrapper, isPressed) {
    if (!taskImageWrapper) return;

    childs = [taskImageWrapper, ...taskImageWrapper.querySelectorAll('*')];

    childs.forEach(element => {
        if (isPressed) {
            element.style['width'] = "100.8px";
            element.style['height'] = "100.8px";
            element.style['left'] = "50%";
            element.style['top'] = "50%";
            element.style['margin-top'] = "-50.4px";
            element.style['margin-left'] = "-50.4px";
        }
        else {
            element.style['width'] = "120px";
            element.style['height'] = "120px";
            element.style['left'] = "50%";
            element.style['top'] = "50%";
            element.style['margin-top'] = "-60px";
            element.style['margin-left'] = "-60px";
        }
    });
}

// wrapper
// width: 100.8px;
//   height: 100.8px;
//   overflow: hidden;
//   border-radius: 2px;
//   transition: 0.1s cubic-bezier(0.05, 0.55, 0.5, 0.99);
//   position: relative;
//   top: 50%;
//   left: 50%;
//   margin-top: -50.4px;
//   margin-left: -50.4px;
//   background-color: rgb(245, 245, 245);

// default
// width: 120px;
//   height: 120px;
//   overflow: hidden;
//   border-radius: 2px;
//   transition: 0.1s cubic-bezier(0.05, 0.55, 0.5, 0.99);
//   position: relative;
//   top: 50%;
//   left: 50%;
//   margin-top: -60px;
//   margin-left: -60px;
//   background-color: rgb(245, 245, 245);