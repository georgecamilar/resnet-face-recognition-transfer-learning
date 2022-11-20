export function connectCameraToVideoElement(videoElement) {
    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({video: true})
            .then((stream) => {
                videoElement.srcObject = stream;
            });
    }
}

export function getCanvasData(canvas, videoElement) {
    let ctx = canvas.getContext('2d');
    ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/jpeg');
}
