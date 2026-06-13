

document.addEventListener('DOMContentLoaded', () => {


    const avatarRing = document.getElementById('avatarRing');
    const avatarInput = document.getElementById('avatarInput');
    const avatarPreview = document.getElementById('avatarPreview');
    const avatarSVG = document.getElementById('avatarPlaceholder');

    avatarRing.addEventListener('click', () => avatarInput.click());

    avatarInput.addEventListener('change', () => {
        const file = avatarInput.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = e => {
            avatarPreview.src = e.target.result;
            avatarPreview.style.display = 'block';
            avatarSVG.style.display = 'none';
            showToast('Avatar updated — save to keep changes', 'success');
        };
        reader.readAsDataURL(file);
    });


    const bannerInput = document.getElementById('bannerInput');
    const bannerSection = document.getElementById('bannerSection');


    bannerInput.addEventListener('change', () => {
        const file = bannerInput.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = e => {
            bannerSection.style.background = `url('${e.target.result}') center/cover no-repeat`;
            showToast('Cover photo updated — save to keep changes', 'success');
        };
        reader.readAsDataURL(file);
    });


    document.getElementById('editPersonalBtn').addEventListener('click', e => {
        e.preventDefault();
        openModal('personal');
    });


    document.getElementById('editCompanyBtn').addEventListener('click', e => {
        e.preventDefault();
        openModal('company');
    });


    document.getElementById('saveProfileBtn').addEventListener('click', handleSave);


    document.getElementById('modalCloseBtn').addEventListener('click', closeModal);
    document.getElementById('modalCancelBtn').addEventListener('click', closeModal);
    document.getElementById('modalSaveBtn').addEventListener('click', saveModal);
    document.getElementById('modalBackdrop').addEventListener('click', e => {
        if (e.target === document.getElementById('modalBackdrop')) closeModal();
    });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });


    let currentModalType = null;

    const modalTemplates = {
        personal: {
            title: 'Edit Personal Profile',
            fields: () => `
        <div class="form-row">
            <div class="form-field">
                <label>Full Name</label>
                <input type="text" id="mf-name" value="${getVal('name')}">
            </div>
            <div class="form-field">
                <label>Email Address</label>
                <input type="email" id="mf-email" value="${getVal('email')}">
            </div>
            </div>
        <div class="form-row">
            <div class="form-field">
                <label>Position</label>
                <input type="text" id="mf-position" value="${getVal('position')}">
            </div>
            <div class="form-field">
                <label>Member Since</label>
                <input type="text" id="mf-since" value="${getVal('since')}" readonly style="opacity:.6;cursor:default">
            </div>
        </div>`,
            save: () => {
                setVal('name', document.getElementById('mf-name').value.trim());
                setVal('email', document.getElementById('mf-email').value.trim());
                setVal('position', document.getElementById('mf-position').value.trim());
            }
        },
        company: {
            title: 'Edit Company Information',
            fields: () => `
        <div class="form-row">
            <div class="form-field">
                <label>Company Name</label>
                <input type="text" id="mf-company-name" value="${getVal('company-name')}">
            </div>
            <div class="form-field">
                <label>Industry</label>
                <select id="mf-industry">
                ${['Technology', 'Finance', 'Healthcare', 'Education', 'Retail', 'Media', 'Other'].map(i =>
                `<option value="${i}" ${getVal('industry') === i ? 'selected' : ''}>${i}</option>`
            ).join('')}
            </select>
            </div>
        </div>
        <div class="form-field full">
            <label>Location</label>
            <input type="text" id="mf-location" value="${getVal('location')}">
        </div>
        <div class="form-field full">
            <label>Description</label>
            <textarea id="mf-description">${getVal('description')}</textarea>
        </div>`,
            save: () => {
                setVal('company-name', document.getElementById('mf-company-name').value.trim());
                setVal('industry', document.getElementById('mf-industry').value);
                setVal('location', document.getElementById('mf-location').value.trim());
                setVal('description', document.getElementById('mf-description').value.trim());
            }
        }
    };

    function getVal(field) {
        const el = document.querySelector(`[data-field="${field}"]`);
        return el ? el.textContent.trim() : '';
    }

    function setVal(field, value) {
        const el = document.querySelector(`[data-field="${field}"]`);
        if (el && value) el.textContent = value;
    }

    function openModal(type) {
        currentModalType = type;
        const tmpl = modalTemplates[type];
        document.getElementById('modalTitle').textContent = tmpl.title;
        document.getElementById('modalForm').innerHTML = tmpl.fields();
        document.getElementById('modalBackdrop').classList.add('open');
        setTimeout(() => {
            const first = document.querySelector('#modalForm input, #modalForm select, #modalForm textarea');
            if (first) first.focus();
        }, 50);
    }

    function closeModal() {
        document.getElementById('modalBackdrop').classList.remove('open');
        currentModalType = null;
    }

    function saveModal() {
        if (!currentModalType) return;
        modalTemplates[currentModalType].save();
        closeModal();
        showToast('Profile updated successfully', 'success');
    }



    function handleSave() {
        const btn = document.getElementById('saveProfileBtn');
        btn.classList.add('loading');
        btn.disabled = true;
        setTimeout(() => {
            btn.classList.remove('loading');
            btn.disabled = false;
            showToast('All changes saved!', 'success');
        }, 1400);
    }


    let toastTimer;

    function showToast(msg, type = 'info') {
        const toast = document.getElementById('toast');
        const msgEl = document.getElementById('toastMsg');
        const icon = document.getElementById('toastIcon');
        if (!toast) return;
        msgEl.textContent = msg;
        const icons = {
            success: 'M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z',
            error: 'M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z',
            info: 'M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z'
        };
        icon.setAttribute('d', icons[type] || icons.info);
        toast.className = `toast ${type}`;
        clearTimeout(toastTimer);
        requestAnimationFrame(() => {
            toast.classList.add('show');
            toastTimer = setTimeout(() => toast.classList.remove('show'), 3200);
        });
    }

});