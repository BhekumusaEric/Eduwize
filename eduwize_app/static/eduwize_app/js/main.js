// Eduwize - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Toggle sidebar on mobile
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector('.sidebar').classList.toggle('active');
            document.querySelector('.content').classList.toggle('active');
        });
    }

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Course search functionality
    const searchInput = document.getElementById('courseSearch');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const courseCards = document.querySelectorAll('.course-card');
            
            courseCards.forEach(function(card) {
                const title = card.querySelector('.card-title').textContent.toLowerCase();
                const description = card.querySelector('.card-text').textContent.toLowerCase();
                
                if (title.includes(searchTerm) || description.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Quiz timer functionality
    const quizTimer = document.getElementById('quizTimer');
    if (quizTimer) {
        let timeLeft = parseInt(quizTimer.dataset.time);
        
        const timerInterval = setInterval(function() {
            timeLeft--;
            
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            
            quizTimer.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
            
            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                document.getElementById('quizForm').submit();
            }
        }, 1000);
    }

    // Progress bars animation
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(function(bar) {
        const width = bar.getAttribute('aria-valuenow') + '%';
        bar.style.width = '0%';
        
        setTimeout(function() {
            bar.style.width = width;
        }, 100);
    });

    // Notification badge
    const notificationCount = document.getElementById('notificationCount');
    if (notificationCount) {
        const count = parseInt(notificationCount.textContent);
        if (count > 0) {
            notificationCount.classList.add('badge-pulse');
        }
    }

    // File upload preview
    const fileInput = document.querySelector('input[type="file"]');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const preview = document.getElementById('filePreview');
            if (preview) {
                preview.textContent = this.files[0].name;
            }
        });
    }

    // AI Chatbot functionality
    const chatbotForm = document.getElementById('chatbotForm');
    const chatbotInput = document.getElementById('chatbotInput');
    const chatbotMessages = document.getElementById('chatbotMessages');
    
    if (chatbotForm && chatbotInput && chatbotMessages) {
        chatbotForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const message = chatbotInput.value.trim();
            if (message) {
                // Add user message
                const userMessage = document.createElement('div');
                userMessage.className = 'chat-message user-message';
                userMessage.innerHTML = `
                    <div class="message-content">
                        <p>${message}</p>
                        <span class="message-time">${new Date().toLocaleTimeString()}</span>
                    </div>
                `;
                chatbotMessages.appendChild(userMessage);
                
                // Clear input
                chatbotInput.value = '';
                
                // Scroll to bottom
                chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
                
                // Simulate AI response (in a real app, this would be an API call)
                setTimeout(function() {
                    const aiMessage = document.createElement('div');
                    aiMessage.className = 'chat-message ai-message';
                    aiMessage.innerHTML = `
                        <div class="message-content">
                            <p>I'm processing your request: "${message}"</p>
                            <span class="message-time">${new Date().toLocaleTimeString()}</span>
                        </div>
                    `;
                    chatbotMessages.appendChild(aiMessage);
                    
                    // Scroll to bottom
                    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
                }, 1000);
            }
        });
    }
});
