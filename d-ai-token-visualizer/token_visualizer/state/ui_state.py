"""Basic state management for the Token Visualizer application."""

import reflex as rx
from typing import Dict, Any


class NavigationState(rx.State):
    """State for managing navigation and UI state."""
    
    # Current active page/mode
    current_mode: str = "interactive"
    
    # Available modes
    modes: Dict[str, str] = {
        "interactive": "Interactive Generation",
        "live_probability": "Live Probability", 
        "color_visualization": "Color Visualization",
        "token_tree": "Token Tree"
    }
    
    def set_mode(self, mode: str):
        """Set the current active mode."""
        if mode in self.modes:
            self.current_mode = mode
    
    def get_current_mode_title(self) -> str:
        """Get the title of the current mode."""
        return self.modes.get(self.current_mode, "Interactive Generation")


class UIState(rx.State):
    """State for general UI components."""
    
    # Loading states
    is_loading: bool = False
    
    # Error states  
    error_message: str = ""
    has_error: bool = False
    
    # Success states
    success_message: str = ""
    has_success: bool = False
    
    def set_loading(self, loading: bool):
        """Set loading state."""
        self.is_loading = loading
    
    def set_error(self, message: str):
        """Set error state with message."""
        self.error_message = message
        self.has_error = bool(message)
        self.has_success = False
    
    def set_success(self, message: str):
        """Set success state with message."""
        self.success_message = message
        self.has_success = bool(message)
        self.has_error = False
    
    def clear_messages(self):
        """Clear all messages."""
        self.error_message = ""
        self.has_error = False
        self.success_message = ""
        self.has_success = False
