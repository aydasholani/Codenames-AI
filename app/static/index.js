function showSelectedFile() {
  const fileInput = document.getElementById("fileInput");
  const fileNameDisplay = document.getElementById("fileName");
  const previewImage = document.getElementById("previewImage");
  const file = fileInput.files[0];

  if (file) {
    fileNameDisplay.textContent = `Selected: ${file.name}`;

    // Skapa en URL för förhandsvisningen
    const reader = new FileReader();
    reader.onload = function (e) {
      previewImage.src = e.target.result;
      // previewImage.style.display = "block"; // Visa förhandsvisningsbilden
    };
    reader.readAsDataURL(file);
  } else {
    fileNameDisplay.textContent = "";
    // previewImage.style.display = "none"; // Dölj om ingen bild är vald
  }
}

async function uploadImage() {
  const fileInput = document.getElementById("fileInput");
  const resultDisplay = document.getElementById("results");
  const loadingButton = document.getElementById("loadingButton");

  if (!fileInput.files[0]) {
    alert("Please select an image file first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  // Visa "Loading"-knappen
  loadingButton.classList.remove("d-none");
  resultDisplay.innerHTML = ""; // Rensa tidigare resultat

  try {
    const response = await fetch("/", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const html = await response.text();
    resultDisplay.innerHTML = new DOMParser()
      .parseFromString(html, "text/html")
      .querySelector("#results").innerHTML;
  } catch (error) {
    console.error("Error uploading image:", error);
    resultDisplay.innerHTML = `<p class="text-danger">Error processing image.</p>`;
  } finally {
    loadingButton.classList.add("d-none"); // Dölj loading-knappen
  }
}

async function updateFileName() {
  const fileInput = document.getElementById("fileInput");
  const fileNameDisplay = document.getElementById("fileName");
  const file = fileInput.files[0];
  if (file) {
    fileNameDisplay.textContent = file.name;
  } else {
    fileNameDisplay.textContent = "";
  }
}