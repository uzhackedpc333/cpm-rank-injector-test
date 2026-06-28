// Loading screen
window.addEventListener('load', () => {
    setTimeout(() => {
        const loadingScreen = document.getElementById('loadingScreen');
        const mainContent = document.getElementById('mainContent');
        
        loadingScreen.classList.add('hidden');
        setTimeout(() => {
            loadingScreen.style.display = 'none';
            mainContent.classList.remove('hidden');
        }, 500);
    }, 2500); // 2.5 seconds loading
});

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('injectForm');
    const statusBox = document.getElementById('statusBox');
    const statusText = document.getElementById('statusText');
    const submitBtn = document.getElementById('submitBtn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        submitBtn.disabled = true;
        submitBtn.textContent = 'Ishlanmoqda...';
        statusBox.className = 'status-box hidden';
        
        const formData = new FormData(form);
        
        try {
            const response = await fetch('/process', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            statusBox.className = `status-box ${data.status === 'success' ? 'success' : 'error'}`;
            statusText.textContent = data.message;
            statusBox.classList.remove('hidden');
            
        } catch (err) {
            statusBox.className = 'status-box error';
            statusText.textContent = 'Ulanish xatosi. Tarmoqni yoki server holatini tekshiring.';
            statusBox.classList.remove('hidden');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Rank Kiritish';
        }
    });
});