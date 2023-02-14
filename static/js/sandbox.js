import { connectCameraToVideoElement, getCanvasData } from '/static/js/videoUtils.js';

const videoElement = document.querySelector("#videoFeed");
const canvas = document.querySelector('#canvas');
const labelHeader = document.querySelector("#label_header");
const submitRequestButton = document.querySelector("#submit_button");
const tableDiv = document.querySelector("#table-data");

const NAME_PLACEHOLDER = "${name}";
const PROBABILITY_PLACEHOLDER = "${probability}";
const ROW_TEMPLATE = "<tr><td>${name}</td><td>${probability}</td></tr>";
const DATA_PLACEHOLDER = "${dataPlaceholder}";
const TABLE_TEMPLATE = "<table class=\"prediction-table\"><tr><th>Name</th><th>Probability</th></tr>${dataPlaceholder}</table>";

const STATUS_CHECK_TEXT_TEMPLATE = "Status is: ${status}";
const STATUS_PLACEHOLDER = "${status}";

function requestEvaluation() {
    const canvasData = getCanvasData(canvas, videoElement);
    const formData = new FormData();
    formData.append('canvas', canvasData);
    $.ajax({
        url: '/test/facerequest',
        type: 'post',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        success: function (event) {
            // console.log(event);
            labelHeader.innerHTML = STATUS_CHECK_TEXT_TEMPLATE.replace(STATUS_PLACEHOLDER, event.status);

            buildPredictionTable(tableDiv, event.classes);
        },
        error: function (event) {
            console.log(event);
            debugger;
            alert(event.status);
        },
        enctype: 'multipart/form-data'
    });
}


function buildPredictionTable(divElement, queryResults) {
    let append = "";
    for (let key in queryResults) {
        append += ROW_TEMPLATE.replace(NAME_PLACEHOLDER, key).replace(PROBABILITY_PLACEHOLDER, queryResults[key]);
    }
    // add element to the table
    divElement.innerHTML = TABLE_TEMPLATE.replace(DATA_PLACEHOLDER, append);
}

connectCameraToVideoElement(videoElement);
submitRequestButton.addEventListener('click', requestEvaluation);
