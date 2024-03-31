document.addEventListener("DOMContentLoaded", function() {
    // Get all tabs
    var tabs = document.getElementsByClassName("tab");

    for (var i = 0; i < tabs.length; i++) {
        tabs[i].addEventListener("click", function() {
            // Hide all content
            var content = document.getElementsByClassName("content");
            for (var i = 0; i < content.length; i++) {
                content[i].style.display = "none";
            }

            // Remove "active" class from all tabs
            for (var i = 0; i < tabs.length; i++) {
                tabs[i].className = tabs[i].className.replace(" active", "");
            }

            // Show current tab's content and add "active" class to the clicked tab
            document.getElementById(this.href.split("#")[1]).style.display = "block";
            this.className += " active";
        });
    }

    // Click the first tab to display its content by default
    tabs[0].click();
});
