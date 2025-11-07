// Modern JavaScript using ES6+ features
document.addEventListener('DOMContentLoaded', () => {
    // Initialize the application
    initApp();
});

const initApp = () => {
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Add animation classes on scroll
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.animate-on-scroll');
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight;
            
            if(elementPosition < screenPosition) {
                element.classList.add('animate');
            }
        });
    };

    // Listen for scroll events
    window.addEventListener('scroll', animateOnScroll);
    
    // Initialize any interactive components
    initializeComponents();
};

const initializeComponents = () => {
    // Add mobile menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navList = document.querySelector('.nav-list');
    
    if (menuToggle && navList) {
        menuToggle.addEventListener('click', () => {
            navList.classList.toggle('active');
        });
    }

    // Add form validation if needed
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
    });
};

const handleFormSubmit = (e) => {
    e.preventDefault();
    
    // Add your form validation and submission logic here
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    // Example of sending data to the server
    fetch('/api/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // Handle success (e.g., show success message)
    })
    .catch((error) => {
        console.error('Error:', error);
        // Handle error (e.g., show error message)
    });
};