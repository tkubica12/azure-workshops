"""Prompt Comparison Mode - Compare token probabilities across three different prompts."""

import reflex as rx
from typing import List, Optional, Dict, Any
from ..components.layout import app_layout
from ..components.probability_bar import probability_bars_list
from ..services.llm_client import get_llm_client, TokenProbability


class PromptComparisonState(rx.State):
    """State management for prompt comparison mode with three independent columns."""
    
    # Column 1 state
    prompt_1: str = ""
    results_1: List[TokenProbability] = []
    is_loading_1: bool = False
    error_1: str = ""
    has_results_1: bool = False
    
    # Column 2 state  
    prompt_2: str = ""
    results_2: List[TokenProbability] = []
    is_loading_2: bool = False
    error_2: str = ""
    has_results_2: bool = False
    
    # Column 3 state
    prompt_3: str = ""
    results_3: List[TokenProbability] = []
    is_loading_3: bool = False
    error_3: str = ""
    has_results_3: bool = False
    
    # Fixed generation settings
    temperature: float = 1.0
    top_k: int = 5
    
    @rx.event(background=True)
    async def generate_column_1(self):
        """Generate token probabilities for column 1."""
        if not self.prompt_1.strip():
            async with self:
                self.error_1 = "Please enter a prompt"
            return
            
        async with self:
            self.is_loading_1 = True
            self.error_1 = ""
            self.has_results_1 = False
            
        try:
            client = await get_llm_client()
            result = await client.generate_tokens_with_probabilities(
                prompt=self.prompt_1,
                max_tokens=1,
                temperature=self.temperature,
                top_logprobs=self.top_k
            )
            
            async with self:
                self.results_1 = result.alternatives
                self.has_results_1 = True
                
        except Exception as e:
            async with self:
                self.error_1 = f"Generation failed: {str(e)}"
                
        finally:
            async with self:
                self.is_loading_1 = False
    
    @rx.event(background=True)
    async def generate_column_2(self):
        """Generate token probabilities for column 2."""
        if not self.prompt_2.strip():
            async with self:
                self.error_2 = "Please enter a prompt"
            return
            
        async with self:
            self.is_loading_2 = True
            self.error_2 = ""
            self.has_results_2 = False
            
        try:
            client = await get_llm_client()
            result = await client.generate_tokens_with_probabilities(
                prompt=self.prompt_2,
                max_tokens=1,
                temperature=self.temperature,
                top_logprobs=self.top_k
            )
            
            async with self:
                self.results_2 = result.alternatives
                self.has_results_2 = True
                
        except Exception as e:
            async with self:
                self.error_2 = f"Generation failed: {str(e)}"
                
        finally:
            async with self:
                self.is_loading_2 = False
    
    @rx.event(background=True)
    async def generate_column_3(self):
        """Generate token probabilities for column 3."""
        if not self.prompt_3.strip():
            async with self:
                self.error_3 = "Please enter a prompt"
            return
            
        async with self:
            self.is_loading_3 = True
            self.error_3 = ""
            self.has_results_3 = False
            
        try:
            client = await get_llm_client()
            result = await client.generate_tokens_with_probabilities(
                prompt=self.prompt_3,
                max_tokens=1,
                temperature=self.temperature,
                top_logprobs=self.top_k
            )
            
            async with self:
                self.results_3 = result.alternatives
                self.has_results_3 = True
                
        except Exception as e:
            async with self:
                self.error_3 = f"Generation failed: {str(e)}"
                
        finally:
            async with self:
                self.is_loading_3 = False


def prompt_column(
    column_number: int,
    prompt_value: str,
    results: List[TokenProbability],
    is_loading: bool,
    error: str,
    has_results: bool,
    on_prompt_change: rx.EventHandler,
    on_generate: rx.EventHandler
) -> rx.Component:
    """Reusable prompt column component."""
    
    return rx.box(
        rx.vstack(
            # Column header
            rx.heading(
                f"Prompt {column_number}",
                size="4",
                color="#1A1A1A",
                font_weight="600",
                margin_bottom="1rem"
            ),
            
            # Prompt input
            rx.vstack(
                rx.text_area(
                    placeholder=f"Enter prompt {column_number}...",
                    value=prompt_value,
                    on_change=on_prompt_change,
                    rows="4",
                    width="100%",
                    border="1px solid #D1D5DB",
                    border_radius="0.375rem",
                    padding="0.75rem",
                    font_size="0.875rem",
                    resize="vertical",
                    _focus={
                        "outline": "none",
                        "border_color": "#3B82F6",
                        "box_shadow": "0 0 0 3px rgba(59, 130, 246, 0.1)"
                    }
                ),
                
                # Generate button
                rx.button(
                    rx.cond(
                        is_loading,
                        rx.hstack(
                            rx.spinner(size="1"),
                            rx.text("Generating..."),
                            spacing="2",
                            align="center"
                        ),
                        rx.hstack(
                            rx.icon("zap", size=16),
                            rx.text("Generate"),
                            spacing="2",
                            align="center"
                        )
                    ),
                    on_click=on_generate,
                    disabled=is_loading,
                    width="100%",
                    background="#3B82F6",
                    color="white",
                    padding="0.75rem 1rem",
                    border_radius="0.375rem",
                    font_weight="500",
                    _hover={
                        "background": "#2563EB"
                    },
                    _disabled={
                        "background": "#94A3B8",
                        "cursor": "not-allowed"
                    }
                ),
                
                spacing="3",
                width="100%"
            ),
            
            # Error message
            rx.cond(
                error != "",
                rx.box(
                    rx.text(
                        error,
                        color="#EF4444",
                        font_size="0.875rem"
                    ),
                    padding="0.75rem",
                    background="#FEF2F2",
                    border="1px solid #FECACA",
                    border_radius="0.375rem",
                    width="100%"
                )
            ),
            
            # Results section
            rx.cond(
                has_results,
                rx.vstack(
                    rx.heading(
                        "Token Probabilities",
                        size="3",
                        color="#1A1A1A",
                        font_weight="600",
                        margin_bottom="0.5rem"
                    ),
                    
                    # Temperature info
                    rx.text(
                        f"Temperature: {1.0} (Fixed)",
                        font_size="0.75rem",
                        color="#6B7280",
                        margin_bottom="1rem"
                    ),
                    
                    # Probability bars
                    probability_bars_list(
                        tokens=results,
                        max_width="100%",
                        bar_height="2.5rem",
                        show_token_text=True,
                        show_percentage=True,
                        show_probability_value=False,
                        animate=True,
                        sort_by_probability=True
                    ),
                    
                    spacing="3",
                    width="100%",
                    align="start"
                )
            ),
            
            spacing="4",
            align="start",
            width="100%",
            height="100%"
        ),
        
        # Column styling
        padding="1.5rem",
        background="#FFFFFF",
        border="1px solid #E5E7EB",
        border_radius="0.75rem",
        min_height="600px",
        width="100%"
    )


def prompt_comparison_content() -> rx.Component:
    """Main content for prompt comparison mode."""
    
    return rx.vstack(
        # Header section
        rx.vstack(
            rx.heading(
                "Prompt Comparison",
                size="7",
                color="#1A1A1A",
                font_weight="600"
            ),
            rx.text(
                "Compare how different prompts affect token probabilities. Enter three different prompts and see how the AI responds to each one.",
                font_size="1.125rem",
                color="#6B7280",
                text_align="center",
                line_height="1.6",
                max_width="800px"
            ),
            spacing="3",
            align="center",
            margin_bottom="2rem"
        ),
        
        # Three-column grid
        rx.box(
            rx.grid(
                # Column 1
                prompt_column(
                    column_number=1,
                    prompt_value=PromptComparisonState.prompt_1,
                    results=PromptComparisonState.results_1,
                    is_loading=PromptComparisonState.is_loading_1,
                    error=PromptComparisonState.error_1,
                    has_results=PromptComparisonState.has_results_1,
                    on_prompt_change=PromptComparisonState.set_prompt_1,
                    on_generate=PromptComparisonState.generate_column_1
                ),
                
                # Column 2
                prompt_column(
                    column_number=2,
                    prompt_value=PromptComparisonState.prompt_2,
                    results=PromptComparisonState.results_2,
                    is_loading=PromptComparisonState.is_loading_2,
                    error=PromptComparisonState.error_2,
                    has_results=PromptComparisonState.has_results_2,
                    on_prompt_change=PromptComparisonState.set_prompt_2,
                    on_generate=PromptComparisonState.generate_column_2
                ),
                
                # Column 3
                prompt_column(
                    column_number=3,
                    prompt_value=PromptComparisonState.prompt_3,
                    results=PromptComparisonState.results_3,
                    is_loading=PromptComparisonState.is_loading_3,
                    error=PromptComparisonState.error_3,
                    has_results=PromptComparisonState.has_results_3,
                    on_prompt_change=PromptComparisonState.set_prompt_3,
                    on_generate=PromptComparisonState.generate_column_3
                ),
                
                # Grid styling - three equal columns
                columns="3",
                spacing="4",
                width="100%"
            ),
            width="100%",
            max_width="1400px"
        ),
        
        # Footer information
        rx.box(
            rx.vstack(
                rx.text(
                    "💡 Educational Tips:",
                    font_weight="600",
                    color="#1A1A1A",
                    font_size="0.875rem"
                ),
                rx.text(
                    "• Try variations of the same prompt to see how small changes affect probabilities",
                    font_size="0.875rem",
                    color="#6B7280"
                ),
                rx.text(
                    "• Compare formal vs. informal language styles",
                    font_size="0.875rem",
                    color="#6B7280"
                ),
                rx.text(
                    "• Notice how context affects which tokens are most likely",
                    font_size="0.875rem",
                    color="#6B7280"
                ),
                spacing="2",
                align="start"
            ),
            padding="1.5rem",
            background="#F8FAFC",
            border="1px solid #E2E8F0",
            border_radius="0.75rem",
            margin_top="2rem",
            max_width="1400px",
            width="100%"
        ),
        
        spacing="4",
        align="center",
        width="100%",
        padding="2rem"
    )


def prompt_comparison_page() -> rx.Component:
    """Prompt comparison page with three-column layout."""
    return app_layout(
        prompt_comparison_content()
    )
