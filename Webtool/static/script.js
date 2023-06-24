// Deactivate all tabs
function deactivateTabs() {
    var tabs = document.getElementsByClassName("tab");
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].classList.remove("active");
    }
}

// Show tab content and activate the clicked tab
function openTab(event, tabName) {
    // Hide all tab contents
    var tabContents = document.getElementsByClassName("tab-content");
    for (var i = 0; i < tabContents.length; i++) {
        tabContents[i].style.display = "none";
    }

    // Deactivate all tabs
    deactivateTabs();

    // Show the selected tab content and activate the clicked tab
    document.getElementById(tabName).style.display = "block";
    event.currentTarget.classList.add("active");
}

// By default, deactivate all tabs and hide tab contents
function initializeTabs() {
    var tabs = document.getElementsByClassName("tab");
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].classList.remove("active");
    }

    var tabContents = document.getElementsByClassName("tab-content");
    for (var i = 0; i < tabContents.length; i++) {
        tabContents[i].style.display = "none";
    }
}

// Initialize tabs when the page loads
document.addEventListener("DOMContentLoaded", function() {
    initializeTabs();
});
 
 

