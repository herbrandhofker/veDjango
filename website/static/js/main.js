// Algemene functies voor de energiegemeenschap applicatie
document.addEventListener('DOMContentLoaded', function() {
    // Initialiseer de UI componenten
    initializeDashboard();
    setupEventListeners();
});

// Initialiseer het dashboard met dummy data
function initializeDashboard() {
    // Simuleer data laden met een korte vertraging voor een realistisch effect
    setTimeout(function() {
        updateDashboardStats({
            currentUsage: '2.4 kW',
            communityUsage: '178.6 kW',
            savings: '€342',
            carbonReduction: '1.2 ton'
        });
        
        const chartPlaceholder = document.querySelector('.chart-placeholder');
        if (chartPlaceholder) {
            chartPlaceholder.innerHTML = 'Verbruiksdata geladen';
        }
    }, 1500);
}

// Update de statistieken op het dashboard
function updateDashboardStats(data) {
    // Update elk statistiek element als het bestaat
    for (const [key, value] of Object.entries(data)) {
        const element = document.getElementById(key);
        if (element) {
            element.textContent = value;
        }
    }
}

// Stel event listeners in voor interactieve elementen
function setupEventListeners() {
    // Login button
    const loginBtn = document.getElementById('login-btn');
    if (loginBtn) {
        loginBtn.addEventListener('click', function() {
            connectWithTibber();
        });
    }
    
    // Navigatie smoothscroll
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 70,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Tibber API connectie (placeholder functie)
function connectWithTibber() {
    // Hier zou in de toekomst de echte Tibber API connectie komen
    alert('Login functionaliteit zou hier worden geïmplementeerd met Tibber API authenticatie.');
    
    // Simuleer een succesvolle login voor het prototype
    console.log('Tibber connectie gesimuleerd');
}

// Functie voor het tonen van real-time energiedata (placeholder)
function fetchRealTimeEnergyData() {
    // Deze functie zou data ophalen van de Tibber API
    console.log('Fetching real-time energy data...');
    
    // Simuleer data voor het prototype
    return {
        currentPrice: 0.22,
        priceUnit: '€/kWh',
        forecastToday: [
            { hour: '00:00', price: 0.18 },
            { hour: '01:00', price: 0.17 },
            { hour: '02:00', price: 0.16 },
            // enz.
        ]
    };
}

// Basis voor toekomstige chart visualisatie
function renderEnergyChart(data) {
    // Deze functie zou een echte grafiek tekenen met bijvoorbeeld Chart.js
    console.log('Rendering energy chart with data:', data);
    
    const chartContainer = document.querySelector('.chart-container');
    if (chartContainer) {
        chartContainer.innerHTML = '<div>Energieverbruik Visualisatie</div>';
        // Hier zou de code komen om een echte grafiek te renderen
    }
}