function setValid(input, hint, msg) {
    input.classList.remove('invalid');
    input.classList.add('valid');
    if (hint) {
        hint.textContent = msg;
        hint.className = 'field-hint success';
    }
}

function setInvalid(input, hint, msg) {
    input.classList.remove('valid');
    input.classList.add('invalid');
    if (hint) {
        hint.textContent = msg;
        hint.className = 'field-hint error';
    }
}

function clearField(input, hint) {
    input.classList.remove('valid', 'invalid');
    if (hint) {
        hint.textContent = '';
        hint.className = 'field-hint';
    }
}

function validateName(input) {
    input.value = input.value.replace(/\s/g, '');
    const val = input.value.trim();
    const hint = input.closest('.form-group')?.querySelector('.field-hint');

    if (!val) { clearField(input, hint); return; }

    if (val.length < 2) {
        setInvalid(input, hint, 'Name must be at least 2 characters.');
    } else if (val.length > 50) {
        setInvalid(input, hint, 'Name must be 50 characters or less.');
    } else if (/\d/.test(val)) {
        setInvalid(input, hint, 'Name cannot contain numbers.');
    } else if (/^[^\d!@#$%^&*()+=\[\]{}<>?/\\|]{2,50}$/.test(val)) {
        setValid(input, hint, '');
    } else {
        setInvalid(input, hint, 'Name contains invalid characters.');
    }
}

function validateEmail(input) {
    input.value = input.value.replace(/\s/g, '');
    const val = input.value.trim();
    const hint = input.closest('.form-group')?.querySelector('.field-hint');

    if (!val) { clearField(input, hint); return; }

    const re = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
    const atIdx = val.indexOf('@');

    if (re.test(val)) {
        setValid(input, hint, '');
    } else if (atIdx === -1) {
        setInvalid(input, hint, 'Email must contain @.');
    } else if (atIdx === 0) {
        setInvalid(input, hint, 'Enter something before @.');
    } else if (!val.slice(atIdx + 1).includes('.')) {
        setInvalid(input, hint, 'Enter a valid domain (e.g. email.com).');
    } else {
        setInvalid(input, hint, 'Invalid email format.');
    }
}

function validatePassword(input) {
    input.value = input.value.replace(/\s/g, '');
    const val = input.value;
    const container = input.closest('.form-group');
    const hint = container?.querySelector('.field-hint');

    const checks = {
        len:   val.length >= 8,
        upper: /[A-Z]/.test(val),
        lower: /[a-z]/.test(val),
        num:   /[0-9]/.test(val),
        sym:   /[^A-Za-z0-9]/.test(val),
    };

    container?.querySelectorAll('.rule[data-rule]').forEach(rule => {
        rule.classList.toggle('pass', checks[rule.dataset.rule]);
    });

    const score = Object.values(checks).filter(Boolean).length;
    const levelIndex = Math.max(0, score - 1);

    const levels = ['Very weak', 'Weak', 'Fair', 'Strong', 'Very strong'];
    const colors = ['#E24B4A', '#E24B4A', '#BA7517', '#1D9E75', '#1D9E75'];

    container?.querySelectorAll('.strength-seg').forEach((seg, i) => {
        seg.style.background =
            i < score
                ? colors[levelIndex]
                : 'var(--color-border-tertiary)';
    });

    if (hint) {
        hint.textContent = val ? levels[levelIndex] : '';
        hint.style.color = val ? colors[levelIndex] : '';
        hint.className = 'field-hint';
    }

    if (!val) { clearField(input, null); return; }
    if (score === 5) setValid(input, null, '');
    else input.classList.remove('valid', 'invalid');
}

function validateConfirmPassword(input) {
    input.value = input.value.replace(/\s/g, '');
    const val = input.value;
    const hint = input.closest('.form-group')?.querySelector('.field-hint');
    const original = document.getElementById('new_password1')?.value ?? document.getElementById('password1')?.value;

    if (!val) { clearField(input, hint); return; }

    if (val === original) {
        setValid(input, hint, 'Passwords match!');
    } else {
        setInvalid(input, hint, 'Passwords do not match.');
    }
}