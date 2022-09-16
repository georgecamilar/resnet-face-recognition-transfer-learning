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
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/jpeg');
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
        success: function(event){
            console.log(event);
            debugger;
            alert(event.status);
        },
        error: function(event){
            console.log(event);
            debugger;
            alert(event.status);
        },
        enctype: 'multipart/form-data'
    });
}

connectCameraToVideoElement();
submitButtonElement.addEventListener('click', evt => credentialsPost(evt));