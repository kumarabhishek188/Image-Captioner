const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const captureButton = document.getElementById("capture-button");
const capturedImage = document.getElementById("captured-image");
const capturedImageInput = document.getElementById("captured_image");
const fileInput = document.getElementById("file_input");

// Load stored image on page load
window.onload = () => {
  const storedImage = sessionStorage.getItem("storedImage");
  if (storedImage) {
    capturedImage.src = storedImage;
    capturedImage.style.display = "block";
  }
};

// Handle file input
fileInput.addEventListener("change", (event) => {
  const image = URL.createObjectURL(event.target.files[0]);
  capturedImage.src = image;
  capturedImage.style.display = "block";
  sessionStorage.setItem("storedImage", image);
});

// Start video stream
if (navigator.mediaDevices?.getUserMedia) {
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((stream) => {
      video.srcObject = stream;
    })
    .catch((err) => {
      alert("Camera access denied.");
    });
}

// Capture image from video
captureButton.addEventListener("click", () => {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0);
  const dataUrl = canvas.toDataURL("image/png");
  capturedImage.src = dataUrl;
  capturedImage.style.display = "block";
  capturedImageInput.value = dataUrl;
  sessionStorage.setItem("storedImage", dataUrl);
  video.srcObject?.getTracks().forEach((track) => track.stop());
});

// Validate form
document.getElementById("image-form").addEventListener("submit", (event) => {
  if (!capturedImageInput.value && !fileInput.files.length) {
    alert("Please upload or capture an image!");
    event.preventDefault();
  }
});

// Play caption audio
function playCaptionAudio(caption) {
  fetch(`/text-to-speech/?caption=${encodeURIComponent(caption)}`)
    .then((res) => res.blob())
    .then((blob) => {
      const audio = new Audio(URL.createObjectURL(blob));
      audio.play();
    })
    .catch(() => alert("Failed to play audio."));
}
// When the file is selected, create a Blob URL and store it in localStorage
const inputElement = document.getElementById('file_input');
inputElement.addEventListener('change', (event) => {
  const file = event.target.files[0];
  if (file) {
    const fileURL = URL.createObjectURL(file); // Create a Blob URL for the selected file
    localStorage.setItem('imageURL', fileURL); // Store the Blob URL in localStorage
    document.getElementById('imagePreview').src = fileURL; // Display the image immediately
  }
});

// On page load, check if there's an image URL in localStorage and display it
window.onload = function() {
  const savedImageURL = localStorage.getItem('imageURL');
  if (savedImageURL) {
    document.getElementById('imagePreview').src = savedImageURL; // Set the image source to the stored URL
  }
};

// Optionally, clean up when the page is unloaded
window.onbeforeunload = function() {
  localStorage.removeItem('imageURL'); // Remove the image URL from localStorage when the page is about to unload
};
