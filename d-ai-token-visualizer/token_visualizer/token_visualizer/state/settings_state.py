"""Settings and configuration state management for Token Visualizer."""

import reflex as rx
from typing import Dict, Any, Optional
from enum import Enum

from .base_state import BaseState


class VisualizationMode(Enum):
    """Available visualization modes."""
    INTERACTIVE = "interactive"
    LIVE_PROBABILITY = "live_probability"
    COLOR_VISUALIZATION = "color_visualization"
    TOKEN_TREE = "token_tree"


class ColorScheme(Enum):
    """Available color schemes for visualization."""
    DEFAULT = "default"
    HIGH_CONTRAST = "high_contrast"
    COLORBLIND_FRIENDLY = "colorblind_friendly"
    DARK_MODE = "dark_mode"


class SettingsState(BaseState):
    """State management for application settings and configuration."""
    
    # Visualization settings
    current_mode: str = VisualizationMode.INTERACTIVE.value
    color_scheme: str = ColorScheme.DEFAULT.value
    
    # Token generation settings
    max_tokens_per_generation: int = 50
    top_k_alternatives: int = 5
    temperature: float = 0.7
    
    # UI preferences
    show_probabilities_as_percentages: bool = True
    show_token_indices: bool = False
    enable_sound_effects: bool = False
    auto_scroll_to_new_tokens: bool = True
    
    # Advanced settings
    enable_debug_mode: bool = False
    show_raw_api_responses: bool = False
    enable_session_persistence: bool = True
    max_session_history: int = 10
    
    # Performance settings
    api_timeout_seconds: int = 30
    max_concurrent_requests: int = 1
    enable_request_caching: bool = False
    
    # Accessibility settings
    font_size_multiplier: float = 1.0
    high_contrast_mode: bool = False
    reduce_motion: bool = False
    screen_reader_mode: bool = False
    
    def set_visualization_mode(self, mode: str):
        """Set the current visualization mode."""
        try:
            # Validate the mode exists
            VisualizationMode(mode)
            self.current_mode = mode
            self.mark_updated()
        except ValueError:
            # Invalid mode, keep current
            pass
    
    def set_color_scheme(self, scheme: str):
        """Set the color scheme."""
        try:
            ColorScheme(scheme)
            self.color_scheme = scheme
            self.mark_updated()
        except ValueError:
            # Invalid scheme, keep current
            pass
    
    def update_token_generation_settings(self, 
                                       max_tokens: Optional[int] = None,
                                       top_k: Optional[int] = None,
                                       temperature: Optional[float] = None):
        """Update token generation settings with validation."""
        updated = False
        
        if max_tokens is not None:
            new_max = max(1, min(200, max_tokens))  # Clamp between 1-200
            if new_max != self.max_tokens_per_generation:
                self.max_tokens_per_generation = new_max
                updated = True
        
        if top_k is not None:
            new_top_k = max(1, min(10, top_k))  # Clamp between 1-10
            if new_top_k != self.top_k_alternatives:
                self.top_k_alternatives = new_top_k
                updated = True
        
        if temperature is not None:
            new_temp = max(0.0, min(2.0, temperature))  # Clamp between 0-2
            if abs(new_temp - self.temperature) > 0.01:  # Account for float precision
                self.temperature = new_temp
                updated = True
        
        if updated:
            self.mark_updated()
    
    def update_ui_preferences(self,
                            show_percentages: Optional[bool] = None,
                            show_indices: Optional[bool] = None,
                            sound_effects: Optional[bool] = None,
                            auto_scroll: Optional[bool] = None):
        """Update UI preference settings."""
        updated = False
        
        if show_percentages is not None and show_percentages != self.show_probabilities_as_percentages:
            self.show_probabilities_as_percentages = show_percentages
            updated = True
        
        if show_indices is not None and show_indices != self.show_token_indices:
            self.show_token_indices = show_indices
            updated = True
        
        if sound_effects is not None and sound_effects != self.enable_sound_effects:
            self.enable_sound_effects = sound_effects
            updated = True
        
        if auto_scroll is not None and auto_scroll != self.auto_scroll_to_new_tokens:
            self.auto_scroll_to_new_tokens = auto_scroll
            updated = True
        
        if updated:
            self.mark_updated()
    
    def update_accessibility_settings(self,
                                    font_multiplier: Optional[float] = None,
                                    high_contrast: Optional[bool] = None,
                                    reduce_motion: Optional[bool] = None,
                                    screen_reader: Optional[bool] = None):
        """Update accessibility settings."""
        updated = False
        
        if font_multiplier is not None:
            new_multiplier = max(0.5, min(3.0, font_multiplier))  # Clamp between 0.5-3.0
            if abs(new_multiplier - self.font_size_multiplier) > 0.01:
                self.font_size_multiplier = new_multiplier
                updated = True
        
        if high_contrast is not None and high_contrast != self.high_contrast_mode:
            self.high_contrast_mode = high_contrast
            updated = True
        
        if reduce_motion is not None and reduce_motion != self.reduce_motion:
            self.reduce_motion = reduce_motion
            updated = True
        
        if screen_reader is not None and screen_reader != self.screen_reader_mode:
            self.screen_reader_mode = screen_reader
            updated = True
        
        if updated:
            self.mark_updated()
    
    def toggle_debug_mode(self):
        """Toggle debug mode on/off."""
        self.enable_debug_mode = not self.enable_debug_mode
        self.mark_updated()
    
    def reset_to_defaults(self):
        """Reset all settings to default values."""
        # Visualization settings
        self.current_mode = VisualizationMode.INTERACTIVE.value
        self.color_scheme = ColorScheme.DEFAULT.value
        
        # Token generation settings
        self.max_tokens_per_generation = 50
        self.top_k_alternatives = 5
        self.temperature = 0.7
        
        # UI preferences
        self.show_probabilities_as_percentages = True
        self.show_token_indices = False
        self.enable_sound_effects = False
        self.auto_scroll_to_new_tokens = True
        
        # Advanced settings
        self.enable_debug_mode = False
        self.show_raw_api_responses = False
        self.enable_session_persistence = True
        self.max_session_history = 10
        
        # Performance settings
        self.api_timeout_seconds = 30
        self.max_concurrent_requests = 1
        self.enable_request_caching = False
        
        # Accessibility settings
        self.font_size_multiplier = 1.0
        self.high_contrast_mode = False
        self.reduce_motion = False
        self.screen_reader_mode = False
        
        self.reset_timestamps()
    
    def get_current_mode_info(self) -> Dict[str, Any]:
        """Get information about the current visualization mode."""
        mode_descriptions = {
            VisualizationMode.INTERACTIVE.value: {
                "title": "Interactive Generation",
                "description": "Step-by-step token generation with user selection",
                "features": ["Token selection", "Probability display", "History tracking"]
            },
            VisualizationMode.LIVE_PROBABILITY.value: {
                "title": "Live Probability",
                "description": "Real-time probability visualization",
                "features": ["Live updates", "Probability comparison", "Prompt modification"]
            },
            VisualizationMode.COLOR_VISUALIZATION.value: {
                "title": "Color Visualization", 
                "description": "Color-coded token probability visualization",
                "features": ["Heat maps", "Color gradients", "Interactive hover"]
            },
            VisualizationMode.TOKEN_TREE.value: {
                "title": "Token Tree",
                "description": "Tree visualization of token generation paths", 
                "features": ["Path exploration", "Branch comparison", "Backtracking"]
            }
        }
        
        return mode_descriptions.get(self.current_mode, {
            "title": "Unknown Mode",
            "description": "Mode information not available",
            "features": []
        })
    
    def get_settings_summary(self) -> Dict[str, Any]:
        """Get a summary of current settings for display or debugging."""
        return {
            "visualization": {
                "mode": self.current_mode,
                "color_scheme": self.color_scheme,
            },
            "generation": {
                "max_tokens": self.max_tokens_per_generation,
                "top_k": self.top_k_alternatives,
                "temperature": self.temperature,
            },
            "ui_preferences": {
                "show_percentages": self.show_probabilities_as_percentages,
                "show_indices": self.show_token_indices,
                "sound_effects": self.enable_sound_effects,
                "auto_scroll": self.auto_scroll_to_new_tokens,
            },
            "accessibility": {
                "font_multiplier": self.font_size_multiplier,
                "high_contrast": self.high_contrast_mode,
                "reduce_motion": self.reduce_motion,
                "screen_reader": self.screen_reader_mode,
            },
            "debug": {
                "debug_mode": self.enable_debug_mode,
                "show_raw_responses": self.show_raw_api_responses,
            }
        }
    
    def validate_settings(self) -> Dict[str, Any]:
        """Validate current settings and return any issues."""
        issues = []
        warnings = []
        
        # Check token generation settings
        if self.max_tokens_per_generation > 100:
            warnings.append("High max_tokens setting may slow down generation")
        
        if self.temperature > 1.5:
            warnings.append("High temperature may produce unpredictable results")
        
        if self.temperature < 0.1:
            warnings.append("Very low temperature may produce repetitive results")
        
        # Check UI settings
        if self.font_size_multiplier > 2.0:
            warnings.append("Large font size may affect layout")
        
        # Check performance settings
        if self.api_timeout_seconds < 10:
            warnings.append("Short API timeout may cause request failures")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings
        }
