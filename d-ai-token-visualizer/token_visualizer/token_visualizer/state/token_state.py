"""Token state management for the Token Visualizer application."""

import reflex as rx
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from .base_state import BaseState
from ..services.llm_client import TokenProbability, TokenGenerationResult


@dataclass
class TokenHistoryEntry:
    """Represents a single token selection in the generation history."""
    token: str
    probability: float
    percentage: float
    alternatives: List[TokenProbability] = field(default_factory=list)
    selected_at: datetime = field(default_factory=datetime.now)
    was_top_choice: bool = False  # Whether this was the highest probability token


@dataclass
class GenerationSession:
    """Represents a complete token generation session."""
    initial_prompt: str
    token_history: List[TokenHistoryEntry] = field(default_factory=list)
    current_text: str = ""
    session_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    
    @property
    def full_text(self) -> str:
        """Get the full generated text including initial prompt."""
        return self.initial_prompt + self.current_text
    
    @property
    def token_count(self) -> int:
        """Get the number of tokens generated."""
        return len(self.token_history)


class TokenState(BaseState):
    """State management for token generation and visualization."""
    
    # Current generation session
    current_prompt: str = ""
    generated_tokens: List[str] = []
    token_history: List[TokenHistoryEntry] = []
    
    # Current token alternatives (for selection)
    current_alternatives: List[TokenProbability] = []
    is_generating: bool = False
    
    # Session management
    sessions: List[GenerationSession] = []
    current_session_id: str = ""
    
    # Configuration
    max_tokens: int = 50
    top_k: int = 5  # Number of top alternatives to show
    temperature: float = 0.7
    
    def start_new_session(self, prompt: str) -> str:
        """Start a new token generation session."""
        session_id = f"session_{datetime.now().isoformat()}"
        session = GenerationSession(
            initial_prompt=prompt,
            session_id=session_id
        )
        
        self.sessions.append(session)
        self.current_session_id = session_id
        self.current_prompt = prompt
        self.generated_tokens = []
        self.token_history = []
        self.current_alternatives = []
        self.is_generating = False
        
        self.mark_updated()
        return session_id
    
    def add_token_alternatives(self, alternatives: List[TokenProbability]):
        """Add token alternatives for user selection."""
        self.current_alternatives = alternatives
        self.mark_updated()
    
    def select_token(self, token_index: int) -> bool:
        """Select a token from current alternatives."""
        if not self.current_alternatives or token_index >= len(self.current_alternatives):
            return False
        
        selected_token = self.current_alternatives[token_index]
        
        # Create history entry
        history_entry = TokenHistoryEntry(
            token=selected_token.token,
            probability=selected_token.probability,
            percentage=selected_token.percentage,
            alternatives=self.current_alternatives.copy(),
            was_top_choice=(token_index == 0)
        )
        
        # Update state
        self.generated_tokens.append(selected_token.token)
        self.token_history.append(history_entry)
        
        # Update current session
        current_session = self.get_current_session()
        if current_session:
            current_session.token_history.append(history_entry)
            current_session.current_text = "".join(self.generated_tokens)
        
        # Clear alternatives after selection
        self.current_alternatives = []
        
        self.mark_updated()
        return True
    
    def remove_last_token(self) -> bool:
        """Remove the last generated token (undo)."""
        if not self.generated_tokens or not self.token_history:
            return False
        
        # Remove from state
        self.generated_tokens.pop()
        self.token_history.pop()
        
        # Update current session
        current_session = self.get_current_session()
        if current_session and current_session.token_history:
            current_session.token_history.pop()
            current_session.current_text = "".join(self.generated_tokens)
        
        # Clear current alternatives
        self.current_alternatives = []
        
        self.mark_updated()
        return True
    
    def get_current_session(self) -> Optional[GenerationSession]:
        """Get the current generation session."""
        if not self.current_session_id:
            return None
        
        for session in self.sessions:
            if session.session_id == self.current_session_id:
                return session
        
        return None
    
    def get_full_text(self) -> str:
        """Get the full text including prompt and generated tokens."""
        return self.current_prompt + "".join(self.generated_tokens)
    
    def get_generated_text(self) -> str:
        """Get only the generated text (without prompt)."""
        return "".join(self.generated_tokens)
    
    def reset_current_session(self):
        """Reset the current session to start over."""
        self.generated_tokens = []
        self.token_history = []
        self.current_alternatives = []
        self.is_generating = False
        
        # Update current session
        current_session = self.get_current_session()
        if current_session:
            current_session.token_history = []
            current_session.current_text = ""
        
        self.mark_updated()
    
    def clear_all_sessions(self):
        """Clear all sessions and reset state."""
        self.sessions = []
        self.current_session_id = ""
        self.current_prompt = ""
        self.generated_tokens = []
        self.token_history = []
        self.current_alternatives = []
        self.is_generating = False
        
        self.reset_timestamps()
    
    def set_generation_parameters(self, max_tokens: int = None, top_k: int = None, temperature: float = None):
        """Update generation parameters."""
        if max_tokens is not None:
            self.max_tokens = max(1, min(200, max_tokens))  # Clamp between 1-200
        if top_k is not None:
            self.top_k = max(1, min(10, top_k))  # Clamp between 1-10
        if temperature is not None:
            self.temperature = max(0.0, min(2.0, temperature))  # Clamp between 0-2
        
        self.mark_updated()
    
    def get_session_statistics(self) -> Dict[str, Any]:
        """Get statistics about the current session."""
        current_session = self.get_current_session()
        if not current_session:
            return {"error": "No active session"}
        
        total_tokens = len(current_session.token_history)
        top_choice_count = sum(1 for entry in current_session.token_history if entry.was_top_choice)
        
        stats = {
            "session_id": current_session.session_id,
            "initial_prompt": current_session.initial_prompt,
            "total_tokens": total_tokens,
            "top_choice_selections": top_choice_count,
            "non_top_choice_selections": total_tokens - top_choice_count,
            "top_choice_percentage": (top_choice_count / total_tokens * 100) if total_tokens > 0 else 0,
            "current_text_length": len(current_session.full_text),
            "session_duration": (datetime.now() - current_session.created_at).total_seconds(),
        }
        
        return stats
    
    def set_current_prompt(self, prompt: str):
        """Set the current prompt."""
        self.current_prompt = prompt
        self.mark_updated()
    
    def get_debug_info(self) -> Dict[str, Any]:
        """Get detailed debug information about the token state."""
        info = self.get_session_info()
        info.update({
            "current_prompt": self.current_prompt,
            "generated_tokens_count": len(self.generated_tokens),
            "current_alternatives_count": len(self.current_alternatives),
            "total_sessions": len(self.sessions),
            "current_session_id": self.current_session_id,
            "is_generating": self.is_generating,
            "generation_params": {
                "max_tokens": self.max_tokens,
                "top_k": self.top_k,
                "temperature": self.temperature,
            }
        })
        
        return info
