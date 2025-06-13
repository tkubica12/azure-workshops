// Memory implementation functions for App.svelte

// Add these variables to the top of the script section:
let showMemory = false;
let userMemory = null;
const MEMORY_API_URL = import.meta.env.MEMORY_API_URL || window._env_?.MEMORY_API_URL;

// Add these functions after the existing functions:
async function loadUserMemory() {
  try {
    const response = await fetch(`${MEMORY_API_URL}/api/memory/users/${selectedUser.userId}/memories`);
    if (response.ok) {
      userMemory = await response.json();
      console.log('Loaded user memory:', userMemory);
    } else {
      console.error('Failed to load user memory:', response.status);
      userMemory = null;
    }
  } catch (error) {
    console.error('Error loading user memory:', error);
    userMemory = null;
  }
}

async function toggleMemory() {
  // If opening the memory panel, refresh the user memory
  if (!showMemory) {
    await loadUserMemory();
  }
  showMemory = !showMemory;
}

// Update switchUser function to clear memory when switching users:
// Add this line after loadConversationHistory():
// userMemory = null;

// Update the backdrop to handle both panels:
// class:open={showHistory || showMemory}
// on:click={() => { showHistory = false; showMemory = false; }}

// Update user menu click handler:
// on:click={() => { switchUser(user); showUserDropdown = false; showMemory = false; }}
