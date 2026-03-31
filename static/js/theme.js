// This function runs immediately to prevent the "white flash"
(function() {
    // Check local storage for a saved theme
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme === 'dark') {
        // If dark theme is saved, apply it to the <body>
        document.body.classList.add('dark-mode');
    }
})();

// This function runs after the page has loaded
document.addEventListener('DOMContentLoaded', () => {
    // Find the toggle button
    const themeToggle = document.getElementById('theme-toggle');
    
    // If the button doesn't exist, create it.
    // This is a fallback, but we will add it to the HTML.
    if (!themeToggle) {
        const toggleButton = document.createElement('button');
        toggleButton.id = 'theme-toggle';
        toggleButton.classList.add('theme-toggle');
        document.body.appendChild(toggleButton);
    }
    
    const body = document.body;

    // Function to update the button icon based on the theme
    const updateIcon = () => {
        const currentToggle = document.getElementById('theme-toggle'); // Find it again
        if (body.classList.contains('dark-mode')) {
            currentToggle.innerHTML = '☀️'; // Sun icon for light mode
        } else {
            currentToggle.innerHTML = '🌙'; // Moon icon for dark mode
        }
    };

    // Add click event to the button
    document.getElementById('theme-toggle').addEventListener('click', () => {
        // Toggle the .dark-mode class on the <body>
        body.classList.toggle('dark-mode');

        // Save the user's preference in local storage
        if (body.classList.contains('dark-mode')) {
            localStorage.setItem('theme', 'dark');
        } else {
            localStorage.setItem('theme', 'light');
        }
        
        // Update the button icon
        updateIcon();
    });

    // Set the correct icon when the page loads
    updateIcon();
});