"""Probability bar test page for verifying probability bar components."""

import reflex as rx
from typing import List
from ..components.probability_bar import (
    probability_bar,
    probability_bars_list,
    compact_probability_bar,
    interactive_probability_bars
)
from ..components.layout import app_layout
from ..services.llm_client import TokenProbability


class ProbabilityBarTestState(rx.State):
    """State for testing probability bar components."""
    
    # Test data - different probability ranges
    test_tokens: List[dict] = [
        {"token": "Paris", "logprob": -0.1, "probability": 0.9048, "percentage": 90.48},
        {"token": "London", "logprob": -1.2, "probability": 0.3012, "percentage": 30.12},
        {"token": "Rome", "logprob": -2.5, "probability": 0.0821, "percentage": 8.21},
        {"token": "Berlin", "logprob": -3.1, "probability": 0.0451, "percentage": 4.51},
        {"token": "Madrid", "logprob": -3.8, "probability": 0.0223, "percentage": 2.23},
        {"token": "Vienna", "logprob": -4.2, "probability": 0.0149, "percentage": 1.49},
        {"token": "Prague", "logprob": -5.1, "probability": 0.0061, "percentage": 0.61},
        {"token": "Oslo", "logprob": -6.2, "probability": 0.0020, "percentage": 0.20}
    ]
    
    # Current selected token index
    selected_index: int = -1
    
    # Display options
    show_token_text: bool = True
    show_percentage: bool = True
    show_probability_value: bool = False
    animate_bars: bool = True
    
    @rx.var
    def token_probabilities(self) -> List[TokenProbability]:
        """Convert test data to TokenProbability objects."""
        return [
            TokenProbability(
                token=token_data["token"],
                logprob=token_data["logprob"],
                probability=token_data["probability"],
                percentage=token_data["percentage"]
            )
            for token_data in self.test_tokens
        ]
    
    @rx.var
    def top_5_tokens(self) -> List[TokenProbability]:
        """Get top 5 tokens for testing."""
        return self.token_probabilities[:5]
    
    @rx.var
    def top_3_tokens(self) -> List[TokenProbability]:
        """Get top 3 tokens for compact testing."""
        return self.token_probabilities[:3]
    
    def select_token(self, index: int):
        """Handle token selection."""
        self.selected_index = index
    
    def toggle_token_text(self):
        """Toggle token text display."""
        self.show_token_text = not self.show_token_text
    
    def toggle_percentage(self):
        """Toggle percentage display."""
        self.show_percentage = not self.show_percentage
    
    def toggle_probability_value(self):
        """Toggle probability value display."""
        self.show_probability_value = not self.show_probability_value
    
    def toggle_animation(self):
        """Toggle bar animation."""
        self.animate_bars = not self.animate_bars
    
    def reset_selection(self):
        """Reset token selection."""
        self.selected_index = -1


def individual_bar_test() -> rx.Component:
    """Test individual probability bar components."""
    return rx.vstack(
        rx.heading("Individual Probability Bars", size="6", margin_bottom="1rem"),
        
        rx.text("High Probability Token (90.48%)", font_weight="600", margin_bottom="0.5rem"),
        probability_bar(
            TokenProbability(
                token="Paris",
                logprob=-0.1,
                probability=0.9048,
                percentage=90.48
            ),
            is_selected=False,
            show_token_text=True,
            show_percentage=True
        ),
        
        rx.text("Medium Probability Token (30.12%)", font_weight="600", margin_bottom="0.5rem", margin_top="1rem"),
        probability_bar(
            TokenProbability(
                token="London",
                logprob=-1.2,
                probability=0.3012,
                percentage=30.12
            ),
            is_selected=False,
            show_token_text=True,
            show_percentage=True
        ),
        
        rx.text("Low Probability Token (2.23%)", font_weight="600", margin_bottom="0.5rem", margin_top="1rem"),
        probability_bar(
            TokenProbability(
                token="Madrid",
                logprob=-3.8,
                probability=0.0223,
                percentage=2.23
            ),
            is_selected=False,
            show_token_text=True,
            show_percentage=True
        ),
        
        rx.text("Selected Token Example", font_weight="600", margin_bottom="0.5rem", margin_top="1rem"),
        probability_bar(
            TokenProbability(
                token="Rome",
                logprob=-2.5,
                probability=0.0821,
                percentage=8.21
            ),
            is_selected=True,
            show_token_text=True,
            show_percentage=True
        ),
        
        width="100%",
        spacing="2",
        padding="1rem",
        border="1px solid #E5E7EB",
        border_radius="0.5rem"
    )


def bars_list_test() -> rx.Component:
    """Test probability bars list component."""
    return rx.vstack(
        rx.heading("Probability Bars List", size="6", margin_bottom="1rem"),
        
        rx.text("Top 5 Token Alternatives", font_weight="600", margin_bottom="0.5rem"),
        probability_bars_list(
            ProbabilityBarTestState.top_5_tokens,
            selected_index=ProbabilityBarTestState.selected_index,
            show_token_text=ProbabilityBarTestState.show_token_text,
            show_percentage=ProbabilityBarTestState.show_percentage,
            show_probability_value=ProbabilityBarTestState.show_probability_value,
            animate=ProbabilityBarTestState.animate_bars
        ),
        
        width="100%",
        spacing="2",
        padding="1rem",
        border="1px solid #E5E7EB",
        border_radius="0.5rem"
    )


def compact_bars_test() -> rx.Component:
    """Test compact probability bars."""
    return rx.vstack(
        rx.heading("Compact Probability Bars", size="6", margin_bottom="1rem"),
        
        rx.text("Compact layout for dense displays", font_weight="600", margin_bottom="0.5rem"),
        
        rx.foreach(
            ProbabilityBarTestState.top_3_tokens,
            lambda token, index: compact_probability_bar(
                token=token,
                is_selected=ProbabilityBarTestState.selected_index == index
            )
        ),
        
        width="100%",
        spacing="2",
        padding="1rem",
        border="1px solid #E5E7EB",
        border_radius="0.5rem"
    )


def interactive_bars_test() -> rx.Component:
    """Test interactive probability bars."""
    return rx.vstack(
        rx.heading("Interactive Probability Bars", size="6", margin_bottom="1rem"),
        
        rx.text(
            f"Selected token: {rx.cond(ProbabilityBarTestState.selected_index >= 0, ProbabilityBarTestState.test_tokens[ProbabilityBarTestState.selected_index]['token'], 'None')}",
            font_weight="600",
            margin_bottom="0.5rem"
        ),
        
        interactive_probability_bars(
            ProbabilityBarTestState.top_5_tokens,
            selected_index=ProbabilityBarTestState.selected_index,
            on_token_select=ProbabilityBarTestState.select_token,
            show_rank_numbers=True,
            show_token_text=True,
            show_percentage=True,
            animate=True
        ),
        
        rx.button(
            "Reset Selection",
            on_click=ProbabilityBarTestState.reset_selection,
            margin_top="1rem",
            variant="outline"
        ),
        
        width="100%",
        spacing="2",
        padding="1rem",
        border="1px solid #E5E7EB",
        border_radius="0.5rem"
    )


def display_options_panel() -> rx.Component:
    """Control panel for display options."""
    return rx.vstack(
        rx.heading("Display Options", size="5", margin_bottom="1rem"),
        
        rx.hstack(
            rx.checkbox(
                "Show Token Text",
                checked=ProbabilityBarTestState.show_token_text,
                on_change=ProbabilityBarTestState.toggle_token_text
            ),
            rx.checkbox(
                "Show Percentage",
                checked=ProbabilityBarTestState.show_percentage,
                on_change=ProbabilityBarTestState.toggle_percentage
            ),
            spacing="4"
        ),
        
        rx.hstack(
            rx.checkbox(
                "Show Probability Value",
                checked=ProbabilityBarTestState.show_probability_value,
                on_change=ProbabilityBarTestState.toggle_probability_value
            ),
            rx.checkbox(
                "Animate Bars",
                checked=ProbabilityBarTestState.animate_bars,
                on_change=ProbabilityBarTestState.toggle_animation
            ),
            spacing="4",
            margin_top="0.5rem"
        ),
        
        width="100%",
        padding="1rem",
        border="1px solid #E5E7EB",
        border_radius="0.5rem",
        background="#F9FAFB"
    )


def probability_bar_test_content() -> rx.Component:
    """Main content for probability bar testing."""
    return rx.vstack(
        rx.heading(
            "Probability Bar Components Test",
            size="8",
            margin_bottom="2rem",
            text_align="center"
        ),
        
        rx.text(
            "This page tests the probability bar components with different configurations and data.",
            color="#6B7280",
            text_align="center",
            margin_bottom="2rem"
        ),
        
        # Display options
        display_options_panel(),
        
        # Individual bars test
        individual_bar_test(),
        
        # Bars list test
        bars_list_test(),
        
        # Compact bars test
        compact_bars_test(),
        
        # Interactive bars test
        interactive_bars_test(),
        
        spacing="6",
        padding="2rem",
        max_width="1200px",
        margin="0 auto"
    )


def probability_bar_test_page() -> rx.Component:
    """Probability bar test page with layout."""
    return app_layout(
        probability_bar_test_content()
    )
