import { connectCameraToVideoElement, getCanvasData } from '/static/js/videoUtils.js';
$(document).ready(function () {
    const properties = {
        interval: 1000,
        pictureNumber: 5,
        testButtonId: '#take_photo'
    }

    const chunks = [];
    let recorder;
    let stream;

    const videoElement = document.querySelector("#videoFeed");
    const canvas = document.querySelector('#canvas');
    const submitRequestButton = document.querySelector('#uploadButton');
    const trainTimer = document.querySelector(properties.trainTimerId);
    const recordButton = document.querySelector('#recordButton');
    const uploadButton = document.querySelector('#uploadButton');
    const stopButton = document.querySelector('#stopButton');
    const subjectName = document.querySelector('#subjectName');

    function record(evt) {
        recorder = new MediaRecorder(stream);
        recorder.ondataavailable = function (e) {
            chunks.push(e.data);
        }
        recorder.start();
    }

    function cameraToVideoElement() {
        if (navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then((s) => {
                    videoElement.srcObject = s;
                    stream = s;
                });
        }
    }

    function stop() {
        recorder.stop();
    }

    function upload() {
        
        let blob = new Blob(chunks, { type: 'video/webm' });
        const requestBody = new FormData();
        requestBody.append('video', blob);
        const name = subjectName.value;
        if (name) {
            requestBody.append('name', name);
        }
        $.ajax({
            url: '/app/uploadVideo',
            type: 'POST',
            data: requestBody,
            processData: false,
            contentType: false,
            enctype: 'multipart/form-data',
            success: (response) => {
                console.log("success");
                console.log(response);
            },
            error: (xhr, status, error) => {
                console.log('error');
            }
        });
    }


    function sendNewSubjectToDatabase() {
        // Get images with the new subject face
        const facesArray = getNewSubjectImages();
        // console.log(facesArray);
        const formData = new FormData();
        formData.append('faces', facesArray);
        $.ajax({
            url: '/app/newsubject',
            type: 'post',
            data: formData,
            processData: false,
            contentType: false,
            cache: false,
            success: function (event) {
                console.log(event);
                //retrain and restart the new neural network
                alert("Sent to dataset");
            },
            error: function (event) {
                console.log(event);
                alert('An error has occured');
            },
            enctype: 'multipart/form-data'
        })
    }

    subjectName.addEventListener('input', (e) => {
        if (e.target.value || e.target.value !== '') {
            uploadButton.removeAttribute('disabled');
        } else {
            uploadButton.setAttribute('disabled', '');
        }
    })


    cameraToVideoElement();

    recordButton.addEventListener('click', record);
    stopButton.addEventListener('click', stop);
    uploadButton.addEventListener('click', upload);
})