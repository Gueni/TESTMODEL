// Get html id of checkbox container.
const checkboxContainer = document.getElementById("checkboxContainer");
// Get html id of the download button.
const downloadButton = document.getElementById("downloadButton");
// Define empty header list variable.
let headers = [];
// Define empty rows list variable.
let rows = [];

// Track file loading state
let jsonLoaded = false;
let csvLoaded = false;

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
            headers[i] = headers[i].replace(/[\[\]"]/g, '').trim();
        }
        
        console.log("JSON loaded, headers:", headers); // Debug log
        jsonLoaded = true;
        
        // If CSV was already loaded, update checkboxes
        if (csvLoaded) {
            createCheckboxes();
        }
    };
    
    reader.onerror = function() {
        console.error("Error reading JSON file");
        alert("Error reading JSON file. Please try again.");
    };
}

// Function to browse and load Raw data csv file.
function uploadFile() {
    const fileInput = document.getElementById("fileInput");
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
        rows = lines.slice(1);
        
        console.log("CSV loaded, rows:", rows.length); // Debug log
        csvLoaded = true;
        
        // If JSON was already loaded, update checkboxes
        if (jsonLoaded) {
            createCheckboxes();
        } else {
            alert("Please upload the JSON headers file first, then the CSV data file.");
        }
    };
    
    reader.onerror = function() {
        console.error("Error reading CSV file");
        alert("Error reading CSV file. Please try again.");
    };
}

// Function to create checkboxes
function createCheckboxes() {
    checkboxContainer.innerHTML = "";
    
    if (headers.length === 0) {
        checkboxContainer.innerHTML = "<p>No headers loaded. Please upload JSON file first.</p>";
        return;
    }
    
    if (rows.length === 0) {
        checkboxContainer.innerHTML = "<p>No data loaded. Please upload CSV file.</p>";
        return;
    }
    
    console.log("Creating checkboxes for headers:", headers); // Debug log
    
    // get headers and its corresponding index to a respective checkbox.
    headers.forEach((header, index) => {
        // Skip empty headers
        if (!header || header.trim() === '') return;
        
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.value = index;
        checkbox.id = `checkbox-${index}`;
        checkbox.addEventListener("change", handleCheckboxChange);
        
        const label = document.createElement("label");
        label.htmlFor = checkbox.id;
        label.innerText = header;
        label.style.marginLeft = "5px";
        label.style.marginRight = "15px";
        
        checkboxContainer.appendChild(checkbox);
        checkboxContainer.appendChild(label);
    });
    
    console.log("Checkboxes created:", checkboxContainer.children.length); // Debug log
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
    
    if (selectedCheckboxes.length === 0) {
        alert("Please select at least one column to download.");
        return;
    }
    
    const selectedIndices = selectedCheckboxes.map(checkbox => parseInt(checkbox.value));
    const selectedHeaders = selectedIndices.map(index => headers[index]);
    
    let newCsvData = selectedHeaders.join(",") + "\n";

    rows.forEach(row => {
        if (row.trim() === '') return; // Skip empty rows
        const cells = row.split(",");
        const selectedCells = selectedIndices.map(index => {
            // Handle cases where row might have fewer cells than headers
            return index < cells.length ? cells[index] : "";
        });
        newCsvData += selectedCells.join(",") + "\n";
    });

    const link = document.createElement("a");
    link.href = "data:text/csv;charset=utf-8," + encodeURI(newCsvData);
    link.download = "Raw_Simulation_Data.csv";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});

// Reset function if needed
function resetDownloadSection() {
    document.getElementById("LoadJasonFile").value = "";
    document.getElementById("fileInput").value = "";
    checkboxContainer.innerHTML = "";
    downloadButton.disabled = true;
    headers = [];
    rows = [];
    jsonLoaded = false;
    csvLoaded = false;
}