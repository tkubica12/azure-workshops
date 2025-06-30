"""Token display test page for verifying token display components."""

import reflex as rx
from typing import List
from ..components.token_display import (
    token_button, 
    token_alternatives_grid,
    token_selection_header,
    token_generation_controls,
    token_display_container
)
from ..components.layout import app_layout
from ..services.azure_openai import TokenProbability
from ..state.token_state import TokenState


class TokenDisplayTestState(rx.State):
    """State for testing token display components."""
    
    # Test data
    current_text: str = "The capital of France is"
    total_tokens: int = 5
    selected_index: int = -1
    is_generating: bool = False
    
    # Sample token alternatives for testing
    test_alternatives: List[dict] = [
        {"token": "Paris", "logprob": -0.1, "probability": 0.9048, "percentage": 90.48},
        {"token": "Lyon", "logprob": -2.5, "probability": 0.0821, "percentage": 8.21},
        {"token": "Nice", "logprob": -3.8, "probability": 0.0123, "percentage": 1.23},
        {"token": "Marseille", "logprob": -4.2, "probability": 0.0008, "percentage": 0.08}
    ]
    
    @rx.var
    def token_alternatives(self) -> List[TokenProbability]:
        """Convert test data to TokenProbability objects."""
        return [
            TokenProbability(
                token=alt["token"],
                logprob=alt["logprob"], 
                probability=alt["probability"],
                percentage=alt["percentage"]
            )
            for alt in self.test_alternatives
        ]
    
    def select_token(self, index: int):
        """Handle token selection."""
        self.selected_index = index
        selected_token = self.test_alternatives[index]["token"]
        self.current_text = f"{self.current_text} {selected_token}"
        self.total_tokens += 1
        
        # Reset selection for next round
        self.selected_index = -1
    
    def generate_next_tokens(self):
        """Simulate generating next token alternatives."""
        self.is_generating = True
        # In real implementation, this would call the API
        # For now, just toggle the loading state
        
    def finish_generating(self):
        """Finish the generation process."""
        self.is_generating = False
    
    def reset_generation(self):
        """Reset the generation to start over."""
        self.current_text = "The capital of France is"
        self.total_tokens = 5
        self.selected_index = -1
        self.is_generating = False
    
    def undo_last_token(self):
        """Undo the last token selection."""
        if self.total_tokens > 5:  # Don't go below the initial prompt
            words = self.current_text.split()
            if len(words) > 6:  # "The capital of France is" = 5 words
                self.current_text = " ".join(words[:-1])
                self.total_tokens -= 1


def individual_components_test() -> rx.Component:
    """Test individual token display components."""
    
    # Create sample token for testing
    sample_token = TokenProbability(
        token="Paris",
        logprob=-0.1,
        probability=0.9048,
        percentage=90.48
    )
    
    return rx.vstack(
        rx.heading("Individual Component Tests", size="5", margin_bottom="1rem"),
        
        # Test individual token button
        rx.vstack(
            rx.heading("Token Button Test", size="4", color="#374151"),
            rx.hstack(
                token_button(
                    token=sample_token,
                    is_selected=False,
                    is_highlighted=True,
                    show_probability_text=True,
                    show_percentage=True
                ),
                token_button(
                    token=sample_token,
                    is_selected=True,
                    is_highlighted=False,
                    show_probability_text=True,
                    show_percentage=True
                ),
                spacing="4"
            ),
            spacing="3",
            align="start",
            width="100%"
        ),
        
        # Test token selection header
        rx.vstack(
            rx.heading("Token Selection Header Test", size="4", color="#374151"),
            token_selection_header(
                current_text="The capital of France is Paris",
                total_tokens=6,
                show_next_instruction=True
            ),
            spacing="3",
            align="start",
            width="100%"
        ),
        
        # Test generation controls
        rx.vstack(
            rx.heading("Generation Controls Test", size="4", color="#374151"),
            token_generation_controls(
                is_generating=False,
                can_undo=True,
                can_generate=True
            ),
            spacing="3",
            align="start",
            width="100%"
        ),
        
        spacing="6",
        width="100%",
        max_width="800px",
        margin="0 auto",
        padding="2rem"
    )


def full_integration_test() -> rx.Component:
    """Test the complete token display container."""
    
    return rx.vstack(
        rx.heading("Full Integration Test", size="5", margin_bottom="1rem"),
        
        token_display_container(
            current_text=TokenDisplayTestState.current_text,
            total_tokens=TokenDisplayTestState.total_tokens,
            alternatives=TokenDisplayTestState.token_alternatives,
            selected_index=TokenDisplayTestState.selected_index,
            is_generating=TokenDisplayTestState.is_generating,
            can_undo=TokenDisplayTestState.total_tokens > 5,
            can_generate=True,
            on_token_select=TokenDisplayTestState.select_token,
            on_generate_next=TokenDisplayTestState.generate_next_tokens,
            on_reset=TokenDisplayTestState.reset_generation,
            on_undo_last=TokenDisplayTestState.undo_last_token,
            show_probability_text=True,
            show_percentage=True
        ),
        
        # Test controls
        rx.vstack(
            rx.heading("Test Controls", size="4", color="#374151", margin_top="2rem"),
            rx.hstack(
                rx.button(
                    "Finish Generating",
                    on_click=TokenDisplayTestState.finish_generating,
                    background="#10B981",
                    color="white",
                    _hover={"background": "#059669"}
                ),
                rx.button(
                    "Add Sample Alternatives",
                    on_click=lambda: TokenDisplayTestState.set_selected_index(-1),
                    variant="outline"
                ),
                spacing="3"
            ),
            spacing="3",
            align="start",
            width="100%"
        ),
        
        spacing="6",
        width="100%",
        max_width="1000px",
        margin="0 auto",
        padding="2rem"
    )


def token_display_test_content() -> rx.Component:
    """Main content for token display test page."""
    
    return rx.vstack(
        rx.box(
            rx.heading(
                "Token Display Component Tests",
                size="6",
                text_align="center",
                margin_bottom="0.5rem",
                color="#1F2937"
            ),
            rx.text(
                "Testing all token display components and interactions",
                color="#6B7280",
                text_align="center",
                margin_bottom="2rem"
            ),
            width="100%"
        ),
        
        # Navigation between test sections
        rx.hstack(
            rx.button(
                "Individual Components",
                variant="outline",
                on_click=lambda: rx.redirect("/token-display-test#individual")
            ),
            rx.button(
                "Full Integration",
                variant="outline", 
                on_click=lambda: rx.redirect("/token-display-test#integration")
            ),
            spacing="3",
            justify="center",
            margin_bottom="2rem"
        ),
        
        # Individual components test
        individual_components_test(),
        
        rx.divider(margin="3rem 0"),
        
        # Full integration test
        full_integration_test(),
        
        spacing="0",
        width="100%"
    )


def token_display_test_page() -> rx.Component:
    """Token display test page with layout."""
    
    return app_layout(
        token_display_test_content()
    )
