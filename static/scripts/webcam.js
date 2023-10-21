$(document).ready(function () {
    const webcam = document.getElementById('webcam');
    const captureButton = document.getElementById('capture-btn');
    const snapshotCanvas = document.getElementById('snapshot');
    const capturedImage = document.getElementById('captured-image');
    const recognizeButton = document.getElementById('recognize-btn');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    let stream;

    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({video: true})
            .then(function (videoStream) {
                stream = videoStream;
                webcam.srcObject = videoStream;
            })
            .catch(function (error) {
                console.log('Error accessing webcam:', error);
            });

        captureButton.addEventListener('click', function () {
            // Capture a frame from the video stream
            snapshotCanvas.width = webcam.videoWidth;
            snapshotCanvas.height = webcam.videoHeight;
            snapshotCanvas.getContext('2d').drawImage(webcam, 0, 0, webcam.videoWidth, webcam.videoHeight);

            // Convert the snapshot to base64 data URL
            const dataURL = snapshotCanvas.toDataURL('image/jpeg');

            // Display the captured image
            capturedImage.src = dataURL;
            capturedImage.style.display = 'block';

            recognizeButton.addEventListener('click', function () {
                // Send the captured image to the server for recognition
                $.ajax({
                    url: '/facial_recognition/',  // URL to your Django view for recognition
                    method: 'POST',
                    data: {
                        image_data: dataURL,
                        csrfmiddlewaretoken: csrfToken
                    },
                    success: function (response) {
                        // Handle recognition results
                        response.forEach(function (result) {
                            console.log('Criminal Detection: ' + result.results_verified);
                            console.log('Path: ' + result.identity_path);
                        });
                    },
                    error: function (error) {
                        // Handle errors
                        console.log('Recognition failed: ' + error.message);
                    }
                });
            });
        });
    } else {
        alert('Your browser does not support webcam access.');
    }
});
