"""Base state classes with common functionality for Token Visualizer."""

import reflex as rx
from typing import Dict, Any, Optional
from datetime import datetime


class BaseState(rx.State):
    """Base state class providing common functionality for all states."""
    
    # Common timestamp tracking
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __init__(self, *args, **kwargs):
        """Initialize base state with timestamps."""
        super().__init__(*args, **kwargs)
        if self.created_at is None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def mark_updated(self):
        """Mark the state as updated with current timestamp."""
        self.updated_at = datetime.now()
    
    def reset_timestamps(self):
        """Reset timestamps to current time."""
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get session information for debugging."""
        return {
            "state_class": self.__class__.__name__,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "session_id": getattr(self, "get_sid", lambda: "unknown")(),
        }
