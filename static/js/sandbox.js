import {connectCameraToVideoElement, getCanvasData} from '/static/js/videoUtils.js';

const videoElement = document.querySelector("#videoFeed");
const canvas = document.querySelector('#canvas');
const labelHeader = document.querySelector("#label_header");
const submitRequestButton = document.querySelector("#submit_button");
debugger;
function requestEvaluation() {
    const canvasData = getCanvasData(canvas, videoElement);
    const formData = new FormData();
    debugger;
    formData.append('canvas', canvasData);
    $.ajax({
        url: '/test/facerequest',
        type: 'post',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        success: function (event) {
            console.log(event);
            labelHeader.innerHTML = event.responseValue;
        },
        error: function (event) {
            console.log(event);
            debugger;
            alert(event.status);
        },
        enctype: 'multipart/form-data'
    });
}

debugger;
connectCameraToVideoElement(videoElement);
submitRequestButton.addEventListener('click', requestEvaluation);
