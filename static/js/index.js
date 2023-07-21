$(document).ready(function () {
    const trainButton = document.getElementById('trainButton');
    const testButton = document.getElementById('testButton');
    const appVersion = document.getElementById('version_tag');
    const videoElement = document.querySelector('#videoFeed');

    const MESSAGE_TEMPLATE = "Current app version is: ${version}";
    const VERSION_PLACEHOLDER = "${version}";

    function getVersion() {
        $.ajax({
            url: '/version',
            type: 'get',
            processData: false,
            contentType: false,
            cache: false,
            success: function (event) {
                if (event.version) {
                    appVersion.innerHTML = MESSAGE_TEMPLATE.replace(VERSION_PLACEHOLDER, event.version);
                }
            },
            error: function (event) {
                console.log('Request failure');
            }
        });
    }

    function init() {
        getVersion();
        connectCameraToVideoElement();
    }

    trainButton.addEventListener('click', () => {
        window.location.href = "/train.html";
    });

    testButton.addEventListener('click', () => {
        window.location.href = "/sandbox.html";
    });

    function connectCameraToVideoElement() {
        if (navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then((stream) => {
                    videoElement.srcObject = stream;
                });
        }
    }
    init();
});