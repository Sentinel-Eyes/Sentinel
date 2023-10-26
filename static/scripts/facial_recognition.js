let captureInterval;
$(document).ready(function () {
    // Start the capture interval immediately
    startCaptureInterval();
});

function startCaptureInterval() {
    // Capture a frame and send for recognition initially
    captureFrame();

    // Set up the interval to capture frames every 25 seconds
    captureInterval = setInterval(function () {
        captureFrame();
    }, 15000);
}

function captureFrame() {
    $.ajax({
        url: '/capture_frame/',
        type: 'GET',
        success: function (data, textStatus, xhr) {
            console.log(xhr.status)
            if (xhr.status === 204) {
                console.log("Face not detected in frame");
            } else {
                console.log("Received frame");
                const base64DataUrl = `data:image/jpeg;base64,${data}`;

                capturedFrame.src = base64DataUrl;
                capturedFrame.style.display = 'block';

                sendButton.setAttribute('data-frame', base64DataUrl);

                sendFrameForRecognition(base64DataUrl);
                console.log("Frame sent for recognition");
            }
        },
        error: function (error) {
            console.error(error);
        }
    });
}

clearInterval(captureInterval);

function sendFrameForRecognition(frameDataUrl) {
    // Send the captured frame data URL to the 'face_recognition' view
    $.ajax({
        url: '/face_recognition/',
        type: 'POST',
        data: {
            frame: frameDataUrl
        },
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function (data) {
            // Handle the response from the server if needed
            console.log(data[0].verified)
            console.log(data[0].distance)
            console.log(data[0].identity)
            criminalImage.src = `data:image/jpeg;base64,${data[0].criminal_image}` ;
            criminalImage.style.display = 'block';

            // Now you can access specific fields of the data object


        },
        error: function (error) {
            console.error(error);
        }
    });
}