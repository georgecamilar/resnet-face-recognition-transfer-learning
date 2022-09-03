const addButton = document.querySelector('#add-employee-button');
const nameLabel = document.querySelector('#name');

function addEmployeeHandler(event) {
    const username = nameLabel.value;
    const formData = new FormData()
    formData.append('username', username)
    formData.append()
}

addButton.addEventListener('click', ev => addEmployeeHandler(ev))