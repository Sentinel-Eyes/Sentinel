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
  // Cancel the request if the page is about to be unloaded
  if (isLeavingPage) {
    return;
  }

  if (currentRequest) {
    // Do nothing if there is an ongoing request
    return;
  }

  currentRequest = $.ajax({
    url: "/capture_frame/",
    type: "GET",
    success: function (data, textStatus, xhr) {
      if (xhr.status === 204) {
      } else {
        const base64DataUrl = `data:image/jpeg;base64,${data}`;

        capturedFrame.src = base64DataUrl;
        capturedFrame.style.display = "block";

        sendFrameForRecognition(base64DataUrl);
       
      }
    },
    error: function (error) {
      console.error(error);
    },
    complete: function () {
      currentRequest = null; // Reset the currentRequest variable
    },
  });
}

clearInterval(captureInterval);

function sendFrameForRecognition(frameDataUrl) {
  // Cancel the request if the page is about to be unloaded
  if (isLeavingPage) {
    return;
  }

  // Send the captured frame data URL to the 'face_recognition' view
  currentRequest = $.ajax({
    url: "/face_recognition/",
    type: "POST",
    data: {
      frame: frameDataUrl,
    },
    headers: {
      "X-CSRFToken": csrfToken,
    },
    success: function (data) {
      criminalImage.src = "";
    
      // Display data in the HTML elements
      if (data != 0) {
        $("#verified").text("Verification: " + data[0].verified);
        $("#distance").text("Distance: " + data[0].distance);
        $("#identity").text("Identity: " + data[0].identity);
        $("#threshold").text("Threshold: " + data[0].threshold);
        $("#model").text("Model: " + data[0].model);
        $("#detector_backend").text(
          "Detector Backend: " + data[0].detector_backend
        );
        $("#similarity_metric").text(
          "Similarity Metric: " + data[0].similarity_metric
        );
        $("#time").text("Time: " + data[0].time);
        criminalImage.src = `data:image/jpeg;base64,${data[0].criminal_image}`;
        criminalImage.style.display = "block";
      } else {
        $("#verified").text("Verification: ");
        $("#distance").text("Distance: ");
        $("#identity").text("Identity: ");
        $("#threshold").text("Threshold: ");
        $("#model").text("Model: ");
        $("#detector_backend").text("Detector Backend: ");
        $("#similarity_metric").text("Similarity Metric: ");
        $("#time").text("Time: ");
      }
    },
    error: function (error) {
      console.error(error);
    },
    complete: function () {
      currentRequest = null; // Reset the currentRequest variable
    },
  });
}
