import {connectCameraToVideoElement, getCanvasData} from '/static/js/videoUtils.js';

const videoElement = document.querySelector("#videoFeed");
const canvas = document.querySelector('#canvas');
const labelHeader = document.querySelector("#label_header");
const submitRequestButton = document.querySelector("#submit_button");

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
            // for now use status
            // todo change it to creating a table in the page
            labelHeader.innerHTML = event.status;
        },
        error: function (event) {
            console.log(event);
            debugger;
            alert(event.status);
        },
        enctype: 'multipart/form-data'
    });
}

connectCameraToVideoElement(videoElement);
submitRequestButton.addEventListener('click', requestEvaluation);
