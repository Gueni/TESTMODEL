// Get html id of checkbox container.
const checkboxContainer     = document.getElementById("checkboxContainer");
// Get html id of the download button.
const downloadButton        = document.getElementById("downloadButton");
// Define empty header list variable.
let headers = [];

// Define empty rows list variable.
let rows = [];

// Function to browse and load json file for the headers.
function uploadJson() {
  const fileInput = document.getElementById("LoadJasonFile");
  const file = fileInput.files[0];

  if (!file) {
    return;
  }

  const reader = new FileReader();
  reader.readAsText(file);

  // Define the load sub-routine.
  reader.onload = function() {
    const data = reader.result;
    const lines = data.split("\n");

    // Pass the data to the headers list.
    headers = lines[0].split(",");

    // Loop through the headers array to remove '[' and ']' characters
    for (let i = 0; i < headers.length; i++) {
      headers[i] = headers[i].replace(/[\[\]"]/g, '');
    }
  };
}

// Function to browse and load Raw data csv file.
function uploadFile() {
    const fileInput     = document.getElementById("fileInput");
    const file          = fileInput.files[0];
    if (!file) {
      return;
    }
    const reader        = new FileReader();
    reader.readAsText(file);
    // Define the load sub-routine.
    reader.onload = function() {
      const data = reader.result;
      const lines = data.split("\n");
      //headers = lines[0].split(",");
      rows = lines.slice(1);
      checkboxContainer.innerHTML = "";
      // get headers and its corresponding index to a respective checkbox.
      headers.forEach((header, index) => {
        const checkbox      = document.createElement("input");
        checkbox.type       = "checkbox";
        checkbox.value      = index;
        checkbox.id         = `checkbox-${index}`;
        checkbox.addEventListener("change", handleCheckboxChange);
        const label         = document.createElement("label");
        label.htmlFor       = checkbox.id;
        label.innerText     = header;
        checkboxContainer.appendChild(checkbox);
        checkboxContainer.appendChild(label);
        checkboxContainer.appendChild(document.createElement("br"));
      });
    };
}

function handleCheckboxChange() {
  const selectedCheckboxes = Array.from(
    checkboxContainer.querySelectorAll("input:checked")
  );

  if (selectedCheckboxes.length > 0) {
    downloadButton.disabled = false;
  } else {
    downloadButton.disabled = true;
  }
}
// Download button sub-routine.
downloadButton.addEventListener("click", function() {
  const selectedCheckboxes = Array.from(
    checkboxContainer.querySelectorAll("input:checked")
  );
  const selectedIndices = selectedCheckboxes.map(checkbox => checkbox.value);

  const selectedHeaders = selectedIndices.map(index => headers[index]);
  let newCsvData = selectedHeaders.join(",") + "\n";

  rows.forEach(row => {
    const cells = row.split(",");
    const selectedCells = selectedIndices.map(index => cells[index]);
    newCsvData += selectedCells.join(",") + "\n";
  });
  
  // Remove the trailing newline character
  newCsvData = newCsvData.trim();

  const link = document.createElement("a");
  link.href = "data:text/csv;charset=utf-8," + encodeURI(newCsvData);
  link.download = "Raw_Simulation_Data.csv";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  });