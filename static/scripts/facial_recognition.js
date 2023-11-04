let captureInterval;
let currentRequest = null;
let isLeavingPage = false;


$(document).ready(function () {
    // Set up the interval to capture frames every 25 seconds
    startCaptureInterval();
});

function startCaptureInterval() {
    // Delay the initial frame capture and recognition by 2 seconds
    setTimeout(function () {
        captureFrame();
        // Set up the interval to capture frames every 15 seconds
        captureInterval = setInterval(captureFrame, 15000);
    }, 3000);
}

function captureFrame() {
    if (isLeavingPage) {
        return;
    }

    if (currentRequest) {
        currentRequest.abort();
    }

    currentRequest = $.ajax({
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
    // Cancel the request if the page is about to be unloaded
    if (isLeavingPage) {
        return;
    }

    if (currentRequest) {
        currentRequest.abort();
    }

    // Send the captured frame data URL to the 'face_recognition' view
    currentRequest = $.ajax({
        url: '/face_recognition/',
        type: 'POST',
        data: {
            frame: frameDataUrl
        },
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function (data) {
            console.log(data)
            if (data.length > 0) {
                // Display data in the HTML elements
                $('#verified').text('Verification: ' + data[0].verified);
                $('#distance').text('Distance: ' + data[0].distance);
                $('#identity').text('Identity: ' + data[0].identity);

                criminalImage.src = `data:image/jpeg;base64,${data[0].criminal_image}`;
                criminalImage.style.display = 'block';
            }

        },
        error: function (error) {
            console.error(error);
        }
    });
}