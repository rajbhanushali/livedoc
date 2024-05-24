loading_popup_str = """
<style>
    .overlay {position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.5); display: flex; align-items: center; justify-content: center; z-index: 1000;}
    .spinner-container {display: flex; align-items: center; justify-content: center;}
    .spinner {border: 4px solid rgba(255, 255, 255, 0.3); border-top: 4px solid white; border-radius: 50%; width: 30px; height: 30px; animation: spin 0.8s linear infinite;}
    @keyframes spin {100% {transform: rotate(360deg);}}
</style>
<div class="overlay">
    <div style="text-align: center; color: white;">
        <p>Good question, let me check on that...</p>
        <div class="spinner-container">
            <div class="spinner"></div>
        </div>
    </div>
</div>
"""