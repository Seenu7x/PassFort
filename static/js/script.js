// Update the strength bar based on password strength
function updateStrengthBar(strength) {
    const strengthFill = document.getElementById('strength-fill');
    const strengthResult = document.getElementById('strength-result');

    switch (strength) {
        case "Weak":
            strengthFill.style.width = '25%';
            strengthFill.style.backgroundColor = 'red';
            strengthResult.innerText = 'Strength: Weak';
            break;
        case "Medium":
            strengthFill.style.width = '50%';
            strengthFill.style.backgroundColor = 'orange';
            strengthResult.innerText = 'Strength: Medium';
            break;
        case "Strong":
            strengthFill.style.width = '100%';
            strengthFill.style.backgroundColor = 'green';
            strengthResult.innerText = 'Strength: Strong';
            break;
        default:
            strengthFill.style.width = '0%';
            strengthFill.style.backgroundColor = 'transparent';
            strengthResult.innerText = 'Strength: Undefined';
    }
}

// Function to check password strength and dictionary words live
async function checkPasswordLive() {
    try {
        const password = document.getElementById('password').value;

        const response = await fetch('/check-live', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: password })
        });

        if (!response.ok) {
            throw new Error(`Server Error: ${response.status}`);
        }

        const data = await response.json();
        updateStrengthBar(data.strength); // This should update the strength bar
        document.getElementById('dictionary-result').innerText = data.dictionary_warning;
    } catch (error) {
        document.getElementById('dictionary-result').innerText = `Error: ${error.message}`;
    }
}

// Function to check password breach status
async function checkBreach() {
    try {
        const password = document.getElementById('password').value;

        const response = await fetch('/check-breach', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: password })
        });

        if (!response.ok) {
            throw new Error(`Server Error: ${response.status}`);
        }

        const data = await response.json();
        document.getElementById('breach-result').innerText = data.breach_status;
    } catch (error) {
        document.getElementById('breach-result').innerText = `Error: ${error.message}`;
    }
}

// Function to update password generator length display
function updateLengthDisplay() {
    const length = document.getElementById('gen-length').value;
    document.getElementById('gen-length-display').innerText = length;
}

// Function to generate a random password
function generatePassword() {
    const length = parseInt(document.getElementById('gen-length').value);
    const includeSpecial = document.getElementById('include-special').checked;

    const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
    const numbers = '0123456789';
    const special = '!@#$%^&*()_+-=[]{}|;:,.<>?/';

    let charPool = letters + numbers;
    if (includeSpecial) charPool += special;

    let password = '';
    for (let i = 0; i < length; i++) {
        password += charPool.charAt(Math.floor(Math.random() * charPool.length));
    }

    document.getElementById('generated-password').innerText = `Generated Password: ${password}`;
}