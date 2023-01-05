const videoElement = document.querySelector('#video');
const submitButtonElement = document.querySelector('#login-submit-button');
const usernameTextBox = document.querySelector('#username');
const passwordTextBox = document.querySelector('#password');
const canvas = document.querySelector('#canvas');

function connectCameraToVideoElement() {
    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({video: true})
            .then((stream) => {
                videoElement.srcObject = stream;
            });
    }
}

function getCanvasData() {
    let ctx = canvas.getContext('2d');
    ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/jpeg');
}

function clearCanvas() {
    let ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function credentialsPost(evt) {
    let videoScreenshot = getCanvasData();
    let usernameValue = usernameTextBox.value;
    let passwordValue = passwordTextBox.value;
    const formData = new FormData();
    formData.append('username', usernameValue);
    formData.append('password', passwordValue);
    formData.append('canvas', videoScreenshot);
    $.ajax({
        url: '/submit',
        type: 'post',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        success: function (event) {
            // TODO: delete the console log events
            const requestStatus = event.code;
            if (requestStatus) {
                if (requestStatus >= 200 && requestStatus < 300) {
                    alert("Login success!")
                    window.location.href = event;
                } else if (requestStatus >= 300 && requestStatus < 400) {
                    window.location.href = event;
                    alert("You have been redirected")
                } else if (requestStatus >= 400 && requestStatus < 500) {
                    clearCanvas();
                    alert("Request failed");
                } else if (requestStatus >= 500 && requestStatus < 600) {
                    clearCanvas();
                    alert("Request failed");
                } else {
                    //delete canvas
                    clearCanvas();
                    alert("Login failed with your credentials!")
                }
            }
        },
        error: function (event) {
            console.log(event);
            alert(event.status);
        },
        enctype: 'multipart/form-data'
    });
}

connectCameraToVideoElement();
submitButtonElement.addEventListener('click', evt => credentialsPost(evt));