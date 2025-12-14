const API_BASE_URL = 'http://127.0.0.1:8000';
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },cache: 'no-store'
    };
    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'API Error');
        }
        if (response.status === 204 || response.status === 200) {
             try {
                 return await response.json();
             } catch (e) {
                 return null;
             }
        }
        return null;
    } catch (error) {
        console.error('API Call Failed:', error);
        alert(`Error: ${error.message}`);
        throw error;
    }
}
const usersListElement = document.getElementById('usersList');
const createUserForm = document.getElementById('createUserForm');
async function loadUsers() {
    usersListElement.innerHTML = '<p>Loading...</p>';
    try {
        const users = await apiCall('/users/');
        renderUsers(users);
    } catch (error) {
        usersListElement.innerHTML = '<p>Error loading users.</p>';
    }
}
function renderUsers(users) {
    usersListElement.innerHTML = '';
    if (users.length === 0) {
        usersListElement.innerHTML = '<p>No users found.</p>';
        return;
    }
    users.forEach(user => {
        const card = document.createElement('div');
        card.className = 'retro-card';
        card.dataset.id = user.id;

        const viewModeStr = `
            <div class="view-mode">
                <div class="card-header">
                    <span>ID: ${user.id}</span>
                    <span>USER</span>
                </div>
                <div class="card-details">
                    <p><strong>Username:</strong> <span class="u-name">${user.username}</span></p>
                    <p><strong>Email:</strong> <span class="u-email">${user.email}</span></p>
                </div>
                <div class="card-actions">
                    <button class="btn btn-edit">Edit</button>
                    <button class="btn btn-delete">Delete</button>
                </div>
            </div>
        `;
        usersListElement.appendChild(card)
        const editModeStr = `
            <div class="edit-mode hidden">
                <h3>Update User ${user.id}</h3>
                <input type="text" class="edit-username" value="${user.username}" placeholder="Username">
                <input type="email" class="edit-email" value="${user.email}" placeholder="Email">
                 <div class="card-actions">
                    <button class="btn btn-primary btn-save">Save</button>
                    <button class="btn btn-cancel">Cancel</button>
                </div>
            </div>
        `;
        card.innerHTML = viewModeStr + editModeStr;
        usersListElement.appendChild(card);
    });
}
createUserForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(createUserForm);
    const userData = {
        username: formData.get('username'),
        email: formData.get('email')
    };

    try {
        await apiCall('/users/', 'POST', userData);
        createUserForm.reset();
        loadUsers();
    } catch (error) {
    }
});

usersListElement.addEventListener('click', async (e) => {
    const card = e.target.closest('.retro-card');
    if (!card) return;
    const userId = card.dataset.id;
    const viewMode = card.querySelector('.view-mode');
    const editMode = card.querySelector('.edit-mode');

    if (e.target.classList.contains('btn-delete')) {
        if (confirm(`Are you sure you want to delete user ${userId}? Accounts will be deleted too.`)) {
             try {
                await apiCall(`/users/${userId}`, 'DELETE');
                 loadUsers();
                 loadAccounts();
            } catch (error) {}
        }
    }

    if (e.target.classList.contains('btn-edit')) {
        viewMode.classList.add('hidden');
        editMode.classList.remove('hidden');
    }

    if (e.target.classList.contains('btn-cancel')) {
        editMode.classList.add('hidden');
        viewMode.classList.remove('hidden');
    }

    if (e.target.classList.contains('btn-save')) {
        const newUsername = editMode.querySelector('.edit-username').value;
        const newEmail = editMode.querySelector('.edit-email').value;

        try {
            await apiCall(`/users/${userId}`, 'PUT', {
                username: newUsername,
                email: newEmail
            });
            loadUsers();
        } catch (error) {}
    }
});


const accountsListElement = document.getElementById('accountsList');
const createAccountForm = document.getElementById('createAccountForm');

async function loadAccounts() {
    accountsListElement.innerHTML = '<p>Loading...</p>';
    try {
        const accounts = await apiCall('/accounts/');
        renderAccounts(accounts);
    } catch (error) {
        accountsListElement.innerHTML = '<p>Error loading accounts.</p>';
    }
}

function renderAccounts(accounts) {
    accountsListElement.innerHTML = '';
    if (accounts.length === 0) {
        accountsListElement.innerHTML = '<p>No accounts found.</p>';
        return;
    }

    accounts.forEach(acc => {
        const card = document.createElement('div');
        card.className = 'retro-card';
        card.dataset.id = acc.id;
        card.innerHTML = `
             <div class="view-mode">
                <div class="card-header">
                    <span>ID: ${acc.id}</span>
                    <span>ACCOUNT</span>
                </div>
                <div class="card-details">
                    <p><strong>Name:</strong> ${acc.acc_name}</p>
                    <p><strong>Balance:</strong> $${acc.balance}</p>
                    <p><strong>Owner ID:</strong> ${acc.user_id}</p>
                </div>
                <div class="card-actions">
                    <button class="btn btn-edit-acc">Edit</button>
                    <button class="btn btn-delete-acc">Delete</button>
                </div>
            </div>
            <div class="edit-mode hidden" style="margin-top:10px; border-top: 2px dashed black; padding-top:10px;">
                <input type="text" class="edit-acc-name" value="${acc.acc_name}" placeholder="Acc Name">
                <input type="number" class="edit-balance" value="${acc.balance}" step="0.01" placeholder="Balance">
                <input type="hidden" class="edit-userid" value="${acc.user_id}">
                 <div class="card-actions">
                    <button class="btn btn-primary btn-save-acc">Save</button>
                    <button class="btn btn-cancel-acc">Cancel</button>
                </div>
            </div>
        `;
        accountsListElement.appendChild(card);
    });
}
createAccountForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(createAccountForm);
    const accData = {
        acc_name: formData.get('acc_name'),
        balance: parseFloat(formData.get('balance')),
        user_id: parseInt(formData.get('user_id'))
    };

    try {
        await apiCall('/accounts/', 'POST', accData);
        createAccountForm.reset();
        loadAccounts();
    } catch (error) {}
});

accountsListElement.addEventListener('click', async (e) => {
    const card = e.target.closest('.retro-card');
    if (!card) return;
    const accId = card.dataset.id;
    const viewMode = card.querySelector('.view-mode');
    const editMode = card.querySelector('.edit-mode');

    if (e.target.classList.contains('btn-delete-acc')) {
        if (confirm(`Delete account ${accId}?`)) {
             try {
                await apiCall(`/accounts/${accId}`, 'DELETE');
                loadAccounts();
            } catch (error) {}
        }
    }
    if (e.target.classList.contains('btn-edit-acc')) {
        viewMode.classList.add('hidden');
        editMode.classList.remove('hidden');
    }
    if (e.target.classList.contains('btn-cancel-acc')) {
        editMode.classList.add('hidden');
        viewMode.classList.remove('hidden');
    }

    if (e.target.classList.contains('btn-save-acc')) {
        const newName = editMode.querySelector('.edit-acc-name').value;
        const newBalance = parseFloat(editMode.querySelector('.edit-balance').value);
        const userId = parseInt(editMode.querySelector('.edit-userid').value);

        try {
            await apiCall(`/accounts/${accId}`, 'PUT', {
                acc_name: newName,
                balance: newBalance,
                user_id: userId
            });
            loadAccounts();
        } catch (error) {}
    }
});

document.addEventListener('DOMContentLoaded', () => {
    loadUsers();
    loadAccounts();
});