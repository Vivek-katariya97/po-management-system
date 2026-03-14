const API_BASE_URL = 'http://localhost:8000'; 

document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
});

function checkAuth() {
    const token = localStorage.getItem('po_jwt_token');
    const authContainer = document.getElementById('authContainer');
    const appContent = document.getElementById('appContent');
    const navItems = document.getElementById('navItems');
    
    if (token) {
        if(authContainer) authContainer.style.display = 'none';
        if(appContent) appContent.style.display = 'block';
        if(navItems) navItems.style.display = 'block';
        loadInitialData();
    } else {
        if(authContainer) authContainer.style.display = 'flex';
        if(appContent) appContent.style.display = 'none';
        if(navItems) navItems.style.display = 'none';
        
        const googleBtnDiv = document.getElementById('googleSignInBtn');
        if (googleBtnDiv) {
            if (typeof google !== 'undefined' && google.accounts) {
                google.accounts.id.initialize({
                    // Use actual Google Client ID here
                    client_id: '1234567890-testclientid.apps.googleusercontent.com', 
                    callback: handleCredentialResponse
                });
                google.accounts.id.renderButton(
                    googleBtnDiv,
                    { theme: 'outline', size: 'large' }
                );
            }
        }
    }
}

async function handleCredentialResponse(response) {
    const googleToken = response.credential;
    try {
        const res = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ google_token: googleToken })
        });
        
        if (res.ok) {
            const data = await res.json();
            localStorage.setItem('po_jwt_token', data.access_token);
            checkAuth(); 
        } else {
            alert('Login failed. Please check the backend connection.');
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Could not connect to the server.');
    }
}

// Secret fallback function for manual testing if backend isn't set up yet for real google token verification
window.mockLogin = function() {
    fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ google_token: 'mock-google-token' })
    })
    .then(r => r.json())
    .then(data => {
        localStorage.setItem('po_jwt_token', data.access_token);
        checkAuth();
    });
};

function logout() {
    localStorage.removeItem('po_jwt_token');
    window.location.href = 'index.html';
}

function apiCall(endpoint, options = {}) {
    const token = localStorage.getItem('po_jwt_token');
    
    const defaultHeaders = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
    
    options.headers = { ...defaultHeaders, ...options.headers };
    
    return fetch(`${API_BASE_URL}${endpoint}`, options).then(async res => {
        if (res.status === 401) {
            logout();
            throw new Error("Unauthorized");
        }
        if (!res.ok) {
            const errBody = await res.json().catch(() => ({}));
            throw new Error(errBody.detail || "API Request Failed");
        }
        return res.json();
    });
}

function loadInitialData() {
    if (window.location.pathname.endsWith('index.html') || window.location.pathname === '/' || window.location.pathname.endsWith('po-management-system/frontend/')) {
        if(typeof loadDashboard === 'function') loadDashboard();
    } else if (window.location.pathname.endsWith('create-po.html')) {
        if(typeof loadCreatePOForm === 'function') loadCreatePOForm();
    }
}
