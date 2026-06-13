function openModal() {
    const fullName = document.getElementById('display-name').textContent.trim();
    document.getElementById('inp-firstname').value = fullName.split(' ')[0];
    document.getElementById('inp-lastname').value = fullName.split(' ').slice(1).join(' ');
    document.getElementById('inp-role').value = document.getElementById('display-role').textContent;
    document.getElementById('inp-location').value = document.getElementById('display-location').textContent;
    document.getElementById('inp-username').value = document.getElementById('display-name').dataset.username || '';
    document.getElementById('modal-avatar-preview').src = document.getElementById('display-avatar').src;
    document.getElementById('editModal').classList.add('open');
}

function closeModal() {
    document.getElementById('editModal').classList.remove('open');
}

function saveChanges() {
    const role = document.getElementById('inp-role').value.trim();
    const location = document.getElementById('inp-location').value.trim();
    const username = document.getElementById('inp-username').value.trim();

    const formData = new FormData();
    const firstName = document.getElementById('inp-firstname').value.trim();
    const lastName = document.getElementById('inp-lastname').value.trim();
    const name = firstName + ' ' + lastName;
    formData.append('first_name', firstName);
    formData.append('last_name', lastName);
    formData.append('job_title', role);
    formData.append('location', location);
    formData.append('username', username);
    formData.append('csrfmiddlewaretoken', document.cookie.match(/csrftoken=([^;]+)/)[1]);

    fetch('/profile/update/', {
        method: 'POST',
        body: formData,
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'ok') {
            document.getElementById('display-name').textContent = name;
            document.getElementById('display-role').textContent = role;
            document.getElementById('display-location').textContent = location;
            document.getElementById('display-fullname').textContent = name;
            document.getElementById('display-jobtitle').textContent = role;
            closeModal();
            showToast('Profile updated successfully!');
        }
    });
}

function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2800);
}

document.addEventListener('DOMContentLoaded', function () {
    const editModal = document.getElementById('editModal');
    const editBtn = document.getElementById('editProfileBtn');
    const modalClose = document.getElementById('modalClose');
    const modalCancel = document.getElementById('modalCancel');
    const modalSave = document.getElementById('modalSave');

    document.getElementById('avatar-upload').addEventListener('change', function () {
        const formData = new FormData();
        formData.append('avatar', this.files[0]);
        formData.append('csrfmiddlewaretoken', document.cookie.match(/csrftoken=([^;]+)/)[1]);

        fetch('/profile/upload-avatar/', {
            method: 'POST',
            body: formData,
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'ok') {
                document.getElementById('display-avatar').src = data.url;
                showToast('Photo updated!');
            }
        });
    });

    document.getElementById('modal-photo-upload').addEventListener('change', function () {
        const formData = new FormData();
        formData.append('avatar', this.files[0]);
        formData.append('csrfmiddlewaretoken', document.cookie.match(/csrftoken=([^;]+)/)[1]);

        fetch('/profile/upload-avatar/', {
            method: 'POST',
            body: formData,
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'ok') {
                document.getElementById('display-avatar').src = data.url;
                document.getElementById('modal-avatar-preview').src = data.url;
                showToast('Photo updated!');
            }
        });
    });

    document.getElementById('remove-photo').addEventListener('click', function () {
        const formData = new FormData();
        formData.append('csrfmiddlewaretoken', document.cookie.match(/csrftoken=([^;]+)/)[1]);

        fetch('/profile/remove-avatar/', {
            method: 'POST',
            body: formData,
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'ok') {
                const defaultUrl = 'https://img.magnific.com/free-vector/blue-circle-with-white-user_78370-4707.jpg';
                document.getElementById('display-avatar').src = defaultUrl;
                document.getElementById('modal-avatar-preview').src = defaultUrl;
                showToast('Photo removed!');
            }
        });
    });

    editBtn.addEventListener('click', openModal);
    modalClose.addEventListener('click', closeModal);
    modalCancel.addEventListener('click', closeModal);
    modalSave.addEventListener('click', saveChanges);

    editModal.addEventListener('click', function (e) {
        if (e.target === editModal) closeModal();
    });
});