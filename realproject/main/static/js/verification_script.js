document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('.code-input input');
    const countdownElement = document.getElementById('countdown');
    const resendButton = document.getElementById('resend');
    let attemptsLeft = parseInt(localStorage.getItem('attemptsLeft'), 10) || 2;
    let resendUsed = false;

    // Retrieve the remaining time from localStorage or use default
    let timer = parseInt(countdownElement.getAttribute('data-remaining-time'), 10);
    let intervalId = null;

    // Check if the resend button has been used before
    resendUsed = localStorage.getItem('resendUsed') === 'true';

    if (resendUsed) {
        resendButton.disabled = true;
    }

    function startTimer() {
        if (intervalId !== null) {
            clearInterval(intervalId);
        }
        intervalId = setInterval(() => {
            if (timer <= 0) {
                clearInterval(intervalId);
                countdownElement.textContent = '00:00';
                if (resendUsed) {
                    localStorage.clear();
                }
                const url = new URL('/account/verification-failed/', window.location.origin);
                url.searchParams.set('message', 'Verification code has expired.');
                url.searchParams.set('resendUsed', resendUsed);
        
                // Redirect to the URL
                window.location.href = url.toString();
            } else {
                timer--;
                const minutes = String(Math.floor(timer / 60)).padStart(2, '0');
                const seconds = String(timer % 60).padStart(2, '0');
                countdownElement.textContent = `${minutes}:${seconds}`;
                countdownElement.setAttribute('data-remaining-time', timer); // Update remaining time
            }
        }, 1000);
    }

    function resetTimer() {
        if (intervalId !== null) {
            clearInterval(intervalId);
        }
        timer = 900; // 15 minutes in seconds
        countdownElement.setAttribute('data-remaining-time', timer);
        startTimer();
        resendButton.disabled = true;

        // Mark resend button as used
        localStorage.setItem('resendUsed', 'true');

        // Send a request to set the verification start time in the session
        fetch('/account/start_verification/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        location.reload();
    }

    function verifyCode() {
        const code = Array.from(inputs).map(input => input.value).join('');
    
        fetch('/account/waiting/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: new URLSearchParams({ 'code': code })
        })
        .then(response => {
            if (response.redirected) {
                localStorage.clear();
                window.location.href = response.url;
            } else {
                return response.json().then(json => {
                    const errorMessage = document.getElementById('errorMessage');
                    
                    errorMessage.classList.remove('d-none', 'error');
                    errorMessage.classList.add('error');
                    errorMessage.textContent = json.message;

                    // Clear the form inputs
                    inputs.forEach(input => input.value = '');
                    inputs[0].focus();

                    // Decrement attempts left
                    attemptsLeft--;
                    localStorage.setItem('attemptsLeft', attemptsLeft);

                    // Redirect to error page if attempts are exhausted
                    if (attemptsLeft <= 0) {
                        if (resendUsed) {
                            localStorage.clear();
                        }
                        const url = new URL('/account/verification-failed/', window.location.origin);
                        url.searchParams.set('message', 'Too many failed attempts');
                        url.searchParams.set('resendUsed', resendUsed);

                        // Redirect to the URL
                        window.location.href = url.toString();
                    }

                }).catch(e => {
                    console.error('Failed to parse JSON:', e);
                    const errorMessage = document.getElementById('errorMessage');
                    
                    errorMessage.classList.remove('d-none', 'error');
                    errorMessage.classList.add('error');
                    errorMessage.textContent = 'Unexpected server response.';

                    const url = new URL('/account/verification-failed/', window.location.origin);
                    url.searchParams.set('message', 'Unexpected server response.');
                    url.searchParams.set('resendUsed', resendUsed);

                    // Redirect to the URL
                    window.location.href = url.toString();
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            const errorMessage = document.getElementById('errorMessage');
            
            errorMessage.classList.remove('d-none', 'error');
            errorMessage.classList.add('error');
            errorMessage.textContent = 'Network error or unexpected server response.';
            
            const url = new URL('/account/verification-failed/', window.location.origin);
            url.searchParams.set('message', 'Network error or unexpected server response.');
            url.searchParams.set('resendUsed', resendUsed);

            // Redirect to the URL
            window.location.href = url.toString();
        });
    }

    function fetchAndUpdateRemainingTime() {
        fetch('/account/current-time/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.remaining_time) {
                if (data.remaining_time > 0){
                timer = parseInt(data.remaining_time, 10);
                countdownElement.setAttribute('data-remaining-time', timer);
                startTimer();  // Restart the timer with the new value
                } else {
                    if (resendUsed) {
                        localStorage.clear();
                    }
                    const url = new URL('/account/verification-failed/', window.location.origin);
                    url.searchParams.set('message', 'Verification code has expired.');
                    url.searchParams.set('resendUsed', resendUsed);
                    window.location.href = url;
                }
            } else {
                console.error('No remaining_time in the response.');
                if (resendUsed) {
                    localStorage.clear();
                }
                const url = new URL('/account/verification-failed/', window.location.origin);
                url.searchParams.set('message', 'Verification code has expired.');
                url.searchParams.set('resendUsed', resendUsed);
                window.location.href = url;
            }
        })
        .catch(error => {
            console.error('Error fetching remaining time:', error);
        });
    }

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Fetch and update the remaining time when the page loads
    fetchAndUpdateRemainingTime();

    // Add event listener for the resend button
    resendButton.addEventListener('click', () => {
        localStorage.setItem('attemptsLeft', 2);
        resetTimer();
    });

    // Add event listeners for the code input fields
    inputs.forEach((input, index) => {
        input.addEventListener('input', () => {
            if (input.value.length === 1) {
                if (index < inputs.length - 1) {
                    inputs[index + 1].focus();
                } else {
                    verifyCode();
                }
            }
        });
    });

    // Add event listener for visibility change
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') {
            fetchAndUpdateRemainingTime();
        }
    });
});
