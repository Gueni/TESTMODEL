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
    console.log("uploadJson called");
    const fileInput = document.getElementById("LoadJasonFile");
    const file = fileInput.files[0];

    if (!file) {
        console.log("No JSON file selected");
        return;
    }

    const reader = new FileReader();
    reader.readAsText(file);

    // Define the load sub-routine.
    reader.onload = function() {
        try {
            const data = reader.result;
            console.log("JSON file content:", data);
            
            // Try to parse as JSON first
            try {
                const jsonData = JSON.parse(data);
                // If it's an array, use it as headers
                if (Array.isArray(jsonData)) {
                    headers = jsonData.map(header => String(header).replace(/[\[\]"]/g, '').trim());
                } else {
                    throw new Error("JSON is not an array");
                }
            } catch (jsonError) {
                // If JSON parsing fails, try as CSV
                console.log("Not valid JSON, trying as CSV");
                const lines = data.split("\n").filter(line => line.trim() !== '');
                if (lines.length > 0) {
                    headers = lines[0].split(",").map(header => header.replace(/[\[\]"]/g, '').trim());
                } else {
                    throw new Error("File is empty");
                }
            }
            
            console.log("Headers loaded:", headers);
            jsonLoaded = true;
            
            // If CSV was already loaded, update checkboxes
            if (csvLoaded) {
                createCheckboxes();
            } else {
                checkboxContainer.innerHTML = "<p>Headers loaded. Now please upload CSV data file.</p>";
            }
        } catch (error) {
            console.error("Error processing headers file:", error);
            alert("Error processing headers file: " + error.message);
            resetFileInput('LoadJasonFile');
        }
    };
    
    reader.onerror = function() {
        console.error("Error reading JSON file");
        alert("Error reading headers file. Please try again.");
        resetFileInput('LoadJasonFile');
    };
}

// Function to browse and load Raw data csv file.
function uploadFile() {
    console.log("uploadFile called");
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];
    
    if (!file) {
        console.log("No CSV file selected");
        return;
    }
    
    const reader = new FileReader();
    reader.readAsText(file);
    
    // Define the load sub-routine.
    reader.onload = function() {
        try {
            const data = reader.result;
            const lines = data.split("\n").filter(line => line.trim() !== '');
            
            if (lines.length === 0) {
                throw new Error("CSV file is empty");
            }
            
            rows = lines.slice(1); // Skip header row
            console.log("CSV loaded, rows found:", rows.length);
            csvLoaded = true;
            
            // If JSON was already loaded, update checkboxes
            if (jsonLoaded) {
                createCheckboxes();
            } else {
                checkboxContainer.innerHTML = "<p>Data loaded. Now please upload headers file.</p>";
            }
        } catch (error) {
            console.error("Error processing CSV file:", error);
            alert("Error processing data file: " + error.message);
            resetFileInput('fileInput');
        }
    };
    
    reader.onerror = function() {
        console.error("Error reading CSV file");
        alert("Error reading data file. Please try again.");
        resetFileInput('fileInput');
    };
}

// Function to create checkboxes
function createCheckboxes() {
    console.log("Creating checkboxes...");
    checkboxContainer.innerHTML = "";
    
    if (headers.length === 0) {
        checkboxContainer.innerHTML = "<p style='color: red;'>No headers loaded. Please upload headers file first.</p>";
        return;
    }
    
    if (rows.length === 0) {
        checkboxContainer.innerHTML = "<p style='color: red;'>No data loaded. Please upload data file.</p>";
        return;
    }
    
    console.log("Creating checkboxes for headers:", headers);
    
    // Create select all checkbox
    const selectAllContainer = document.createElement("div");
    selectAllContainer.style.marginBottom = "10px";
    selectAllContainer.style.paddingBottom = "10px";
    selectAllContainer.style.borderBottom = "1px solid #ccc";
    
    const selectAllCheckbox = document.createElement("input");
    selectAllCheckbox.type = "checkbox";
    selectAllCheckbox.id = "selectAll";
    selectAllCheckbox.addEventListener("change", function() {
        const allCheckboxes = checkboxContainer.querySelectorAll('input[type="checkbox"]:not(#selectAll)');
        allCheckboxes.forEach(checkbox => {
            checkbox.checked = selectAllCheckbox.checked;
        });
        handleCheckboxChange();
    });
    
    const selectAllLabel = document.createElement("label");
    selectAllLabel.htmlFor = "selectAll";
    selectAllLabel.innerText = "Select All";
    selectAllLabel.style.fontWeight = "bold";
    selectAllLabel.style.marginLeft = "5px";
    
    selectAllContainer.appendChild(selectAllCheckbox);
    selectAllContainer.appendChild(selectAllLabel);
    checkboxContainer.appendChild(selectAllContainer);
    
    // Create checkboxes for each header
    headers.forEach((header, index) => {
        // Skip empty headers
        if (!header || header.trim() === '') return;
        
        const checkboxWrapper = document.createElement("div");
        checkboxWrapper.style.margin = "5px 0";
        
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.value = index;
        checkbox.id = `checkbox-${index}`;
        checkbox.addEventListener("change", handleCheckboxChange);
        
        const label = document.createElement("label");
        label.htmlFor = checkbox.id;
        label.innerText = header;
        label.style.marginLeft = "8px";
        label.style.cursor = "pointer";
        
        checkboxWrapper.appendChild(checkbox);
        checkboxWrapper.appendChild(label);
        checkboxContainer.appendChild(checkboxWrapper);
    });
    
    console.log("Checkboxes created successfully");
    downloadButton.disabled = true; // Start with disabled download button
}

function handleCheckboxChange() {
    const selectedCheckboxes = Array.from(
        checkboxContainer.querySelectorAll('input[type="checkbox"]:not(#selectAll):checked')
    );

    console.log("Selected checkboxes:", selectedCheckboxes.length);
    
    if (selectedCheckboxes.length > 0) {
        downloadButton.disabled = false;
        downloadButton.textContent = `Download Selected Columns (${selectedCheckboxes.length})`;
    } else {
        downloadButton.disabled = true;
        downloadButton.textContent = "Download Selected Columns";
    }
    
    // Update select all checkbox state
    const selectAllCheckbox = document.getElementById("selectAll");
    if (selectAllCheckbox) {
        const allCheckboxes = checkboxContainer.querySelectorAll('input[type="checkbox"]:not(#selectAll)');
        const allChecked = allCheckboxes.length > 0 && selectedCheckboxes.length === allCheckboxes.length;
        selectAllCheckbox.checked = allChecked;
        selectAllCheckbox.indeterminate = selectedCheckboxes.length > 0 && selectedCheckboxes.length < allCheckboxes.length;
    }
}

// Download button sub-routine.
downloadButton.addEventListener("click", function() {
    const selectedCheckboxes = Array.from(
        checkboxContainer.querySelectorAll('input[type="checkbox"]:not(#selectAll):checked')
    );
    
    if (selectedCheckboxes.length === 0) {
        alert("Please select at least one column to download.");
        return;
    }
    
    const selectedIndices = selectedCheckboxes.map(checkbox => parseInt(checkbox.value));
    const selectedHeaders = selectedIndices.map(index => headers[index]);
    
    console.log("Downloading columns:", selectedHeaders);
    
    let newCsvData = selectedHeaders.join(",") + "\n";

    rows.forEach(row => {
        if (row.trim() === '') return; // Skip empty rows
        const cells = row.split(",");
        const selectedCells = selectedIndices.map(index => {
            // Handle cases where row might have fewer cells than headers
            return index < cells.length ? cells[index].trim() : "";
        });
        newCsvData += selectedCells.join(",") + "\n";
    });

    // Create and trigger download
    const blob = new Blob([newCsvData], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", "Filtered_Simulation_Data.csv");
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    console.log("Download completed");
});

// Utility function to reset file input
function resetFileInput(inputId) {
    document.getElementById(inputId).value = "";
}

// Reset function for the entire section
function resetDownloadSection() {
    console.log("Resetting download section");
    document.getElementById("LoadJasonFile").value = "";
    document.getElementById("fileInput").value = "";
    checkboxContainer.innerHTML = "<p>Please upload headers file and data file to begin.</p>";
    downloadButton.disabled = true;
    downloadButton.textContent = "Download Selected Columns";
    headers = [];
    rows = [];
    jsonLoaded = false;
    csvLoaded = false;
}

// Initialize the download section when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log("Download section initialized");
    checkboxContainer.innerHTML = "<p>Please upload headers file and data file to begin.</p>";
    downloadButton.disabled = true;
});

// Add some basic styles via JavaScript
const style = document.createElement('style');
style.textContent = `
    .download_section {
        margin: 20px;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 8px;
        background-color: #f9f9f9;
    }
    
    .download_section h3 {
        margin-top: 0;
        color: #333;
    }
    
    .download_section label {
        font-weight: bold;
        margin-right: 10px;
    }
    
    .download_section input[type="file"] {
        margin: 5px 0;
    }
    
    #downloadButton {
        background-color: #0066b1;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
    }
    
    #downloadButton:disabled {
        background-color: #cccccc;
        cursor: not-allowed;
    }
    
    #downloadButton:hover:not(:disabled) {
        background-color: #004a7f;
    }
    
    #checkboxContainer {
        background-color: white;
        border-radius: 4px;
    }
    
    #checkboxContainer div {
        padding: 2px 0;
    }
    
    #checkboxContainer input[type="checkbox"] {
        cursor: pointer;
    }
    
    #checkboxContainer label {
        cursor: pointer;
        font-weight: normal;
    }
`;
document.head.appendChild(style);