// Confetti effect for big wins
function createConfetti() {
    const colors = ['#ffd89b', '#c7e9fb', '#ff6b6b', '#4ecdc4', '#45b7d1'];
    
    for (let i = 0; i < 100; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = Math.random() * window.innerWidth + 'px';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.width = Math.random() * 10 + 5 + 'px';
        confetti.style.height = Math.random() * 10 + 5 + 'px';
        confetti.style.animationDuration = Math.random() * 2 + 1 + 's';
        confetti.style.animationDelay = Math.random() * 0.5 + 's';
        document.body.appendChild(confetti);
        
        setTimeout(() => confetti.remove(), 3000);
    }
}

// Particle effect for button clicks
function createParticles(x, y, color) {
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.backgroundColor = color;
        particle.style.left = x + 'px';
        particle.style.top = y + 'px';
        particle.style.transform = `rotate(${Math.random() * 360}deg)`;
        document.body.appendChild(particle);
        
        setTimeout(() => particle.remove(), 500);
    }
}

// Animate score change
function animateScore(element, oldValue, newValue) {
    const duration = 500;
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const current = oldValue + (newValue - oldValue) * progress;
        element.textContent = Math.floor(current);
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

// Sound effects (optional - requires Howler.js)
function playSound(type) {
    // You can add actual sound files here
    const sounds = {
        cooperate: '🔊',
        defect: '💥',
        win: '🎉',
        lose: '😢'
    };
    console.log(`Playing sound: ${sounds[type] || '🔔'}`);
}

// Export functions
window.createConfetti = createConfetti;
window.createParticles = createParticles;
window.animateScore = animateScore;
window.playSound = playSound;