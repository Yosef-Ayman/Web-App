document.addEventListener('DOMContentLoaded', function () {
    const usernameInput = document.getElementById('id_username');
    const submitBtn = document.querySelector('form button[type="submit"]');
    
    if (!usernameInput) return;

    const wrapper = document.createElement('div');
    wrapper.className = 'username-input-wrapper';
    usernameInput.parentNode.insertBefore(wrapper, usernameInput);
    wrapper.appendChild(usernameInput);

    const feedback = document.createElement('div');
    feedback.className = 'username-feedback';
    feedback.setAttribute('aria-live', 'polite');
    wrapper.appendChild(feedback);

    let debounceTimeout = null;

    function setStatus(state, message) {
        usernameInput.classList.remove('status-loading', 'status-success', 'status-error');
        feedback.className = 'username-feedback';
        feedback.innerHTML = '';

        if (state === 'loading') {
            usernameInput.classList.add('status-loading');
            feedback.classList.add('loading');
            feedback.innerHTML = '<span class="spinner-small"></span> Checking availability...';
            submitBtn.disabled = true;
            submitBtn.style.opacity = '0.7';
        } else if (state === 'success') {
            usernameInput.classList.add('status-success');
            feedback.classList.add('success');
            feedback.innerHTML = '<i class="fas fa-check-circle"></i> ' + message;
            submitBtn.disabled = false;
            submitBtn.style.opacity = '1';
        } else if (state === 'error') {
            usernameInput.classList.add('status-error');
            feedback.classList.add('error');
            feedback.innerHTML = '<i class="fas fa-times-circle"></i> ' + message;
            submitBtn.disabled = true;
            submitBtn.style.opacity = '0.7';
        } else {
            submitBtn.disabled = false;
            submitBtn.style.opacity = '1';
        }
    }

    usernameInput.addEventListener('input', function () {
        let originalValue = usernameInput.value;
        let sanitizedValue = originalValue.toLowerCase().replace(/\s+/g, '_');
        
        sanitizedValue = sanitizedValue.replace(/[^a-z0-9_-]/g, '');

        if (originalValue !== sanitizedValue) {
            usernameInput.value = sanitizedValue;
        }

        const username = sanitizedValue.trim();

        if (debounceTimeout) {
            clearTimeout(debounceTimeout);
        }

        if (!username) {
            setStatus('idle', '');
            return;
        }

        if (username.length < 3) {
            setStatus('error', 'Username must be at least 3 characters.');
            return;
        }

        setStatus('loading', '');

        debounceTimeout = setTimeout(() => {
            fetch(`/check-username/?username=${encodeURIComponent(username)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.available) {
                        setStatus('success', 'Username is available!');
                    } else {
                        setStatus('error', 'This username is already taken.');
                    }
                })
                .catch(error => {
                    console.error('Error validation:', error);
                    setStatus('error', 'Error checking username. Please try again.');
                });
        }, 300);
    });
});
