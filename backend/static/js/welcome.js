window.onload = function () {
    const messageBox = document.getElementById("message");
    const now = new Date().toLocaleTimeString();
    messageBox.innerText = `Page loaded successfully at ${now}`;
};


function showImage() {
  const container = document.getElementById('image-container');
  container.style.display = 'block';
}