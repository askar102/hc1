export default class Task {
    _isSelected = false;
    _photoUrl = "";


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

    SetPhoto(newUrl) {
        this._photoUrl = newUrl;

        this.container.style.setProperty("--task-bg-url", `url(${newUrl})`);
    }
};