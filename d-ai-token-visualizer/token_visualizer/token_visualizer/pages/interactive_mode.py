"""Interactive token generation mode - Main educational experience."""

import reflex as rx
import asyncio
from typing import List, Optional
from datetime import datetime
from ..components.layout import app_layout
from ..components.probability_bar import interactive_probability_bars
from ..components.token_display import token_generation_controls
from ..services.llm_client import get_llm_client, TokenProbability
from ..state.token_state import TokenState


class InteractiveGenerationState(rx.State):
    """State for the interactive token generation experience."""
    
    # Current session state
    initial_prompt: str = ""
    current_text: str = ""
    generated_tokens: List[str] = []
    
    # Current token alternatives
    current_alternatives: List[TokenProbability] = []
    selected_token_index: int = -1
    
    # UI state
    is_generating: bool = False
    is_loading: bool = False
    has_started: bool = False
    error_message: str = ""
    has_error: bool = False
    
    # Generation settings
    max_tokens: int = 20
    temperature: float = 0.7
    top_k: int = 5
    
    # Statistics
    total_tokens_generated: int = 0
    session_start_time: str = ""
    
    def set_initial_prompt(self, prompt: str):
        """Set the initial prompt for generation."""
        self.initial_prompt = prompt
        if not self.initial_prompt:
            self.set_error("Please enter a prompt to start generation.")
        else:
            self.clear_error()
    
    def set_temperature(self, temp: str):
        """Set generation temperature."""
        try:
            temp_val = float(temp)
            if 0.0 <= temp_val <= 2.0:
                self.temperature = temp_val
                self.clear_error()
            else:
                self.set_error("Temperature must be between 0.0 and 2.0")
        except ValueError:
            self.set_error("Invalid temperature value")
    
    def set_temperature_slider(self, values: list):
        """Set generation temperature from slider."""
        if values and len(values) > 0:
            temp = float(values[0])
            if 0.0 <= temp <= 2.0:
                self.temperature = round(temp, 1)  # Round to 1 decimal place
                self.clear_error()
    
    def set_max_tokens(self, tokens: str):
        """Set maximum tokens to generate."""
        try:
            token_val = int(tokens)
            if 1 <= token_val <= 100:
                self.max_tokens = token_val
                self.clear_error()
            else:
                self.set_error("Max tokens must be between 1 and 100")
        except ValueError:
            self.set_error("Invalid max tokens value")
    
    def set_max_tokens_slider(self, values: list):
        """Set maximum tokens from slider."""
        if values and len(values) > 0:
            tokens = int(float(values[0]))
            if 1 <= tokens <= 100:
                self.max_tokens = tokens
                self.clear_error()
    
    def set_error(self, message: str):
        """Set error state."""
        self.error_message = message
        self.has_error = bool(message)
    
    def clear_error(self):
        """Clear error state."""
        self.error_message = ""
        self.has_error = False
    
    async def start_generation(self):
        """Start the interactive generation process."""
        if not self.initial_prompt:
            self.set_error("Please enter a prompt to start generation.")
            return
        
        self.is_loading = True
        self.clear_error()
        
        try:
            # Initialize session
            self.current_text = self.initial_prompt
            self.generated_tokens = []
            self.total_tokens_generated = 0
            self.has_started = True
            self.session_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Generate first set of alternatives
            await self.generate_next_alternatives()
            
        except Exception as e:
            self.set_error(f"Failed to start generation: {str(e)}")
        finally:
            self.is_loading = False
    
    async def generate_next_alternatives(self):
        """Generate the next set of token alternatives."""
        if self.total_tokens_generated >= self.max_tokens:
            self.is_generating = False
            return
        
        self.is_loading = True
        self.clear_error()
        
        try:
            # Get LLM client
            client = await get_llm_client()
            
            # Construct the proper prompt: original prompt + selected tokens
            # Concatenate tokens exactly as they come from the LLM (tokens include their own spacing)
            if self.generated_tokens:
                # Join tokens without spaces - they already include proper spacing from tokenization
                token_text = "".join(self.generated_tokens)
                full_prompt = f"{self.initial_prompt}{token_text}"
            else:
                full_prompt = self.initial_prompt
            
            # Log current generation state
            print(f"INFO: Generating next token for prompt: '{full_prompt}'")
            print(f"INFO: Temperature: {self.temperature}, Top-k: {self.top_k}")
            
            # Generate with logprobs
            result = await client.generate_tokens_with_probabilities(
                prompt=full_prompt,
                max_tokens=1,
                temperature=self.temperature,
                top_logprobs=self.top_k
            )
            
            # Log the most likely next token
            if result.alternatives:
                most_likely = result.alternatives[0]
                print(f"INFO: Most likely next token: '{most_likely.token}' ({most_likely.percentage:.1f}%)")
            
            # Update alternatives
            self.current_alternatives = result.alternatives
            self.selected_token_index = -1
            self.is_generating = True
            
        except Exception as e:
            print(f"ERROR: Token generation failed: {str(e)}")
            self.set_error(f"Failed to generate alternatives: {str(e)}")
            self.is_generating = False
        finally:
            self.is_loading = False
    
    async def select_token(self, index: int):
        """Handle token selection."""
        if 0 <= index < len(self.current_alternatives):
            selected_token = self.current_alternatives[index]
            
            # Log token selection
            print(f"INFO: Selected token '{selected_token.token}' ({selected_token.percentage:.1f}%)")
            
            # Add token to generated sequence
            self.generated_tokens.append(selected_token.token)
            
            # Update display text: original prompt + all generated tokens  
            # Use the same concatenation logic as prompt construction for consistency
            if self.generated_tokens:
                token_text = "".join(self.generated_tokens)
                self.current_text = f"{self.initial_prompt}{token_text}"
            else:
                self.current_text = self.initial_prompt
            
            self.total_tokens_generated += 1
            self.selected_token_index = index
            
            # Check if we should continue generating
            if self.total_tokens_generated < self.max_tokens:
                # Small delay for UI feedback
                await asyncio.sleep(0.1)
                # Generate next alternatives immediately
                await self.generate_next_alternatives()
            else:
                # End generation
                self.is_generating = False
                print(f"INFO: Generation complete! Generated {self.total_tokens_generated} tokens.")
    
    async def undo_last_token(self):
        """Remove the last generated token."""
        if self.generated_tokens:
            # Remove last token from sequence
            last_token = self.generated_tokens.pop()
            print(f"INFO: Undoing last token: '{last_token}'")
            
            # Reconstruct current text from original prompt + remaining tokens preserving structure
            if self.generated_tokens:
                token_text = "".join(self.generated_tokens)
                self.current_text = f"{self.initial_prompt}{token_text}"
            else:
                self.current_text = self.initial_prompt
            
            self.total_tokens_generated -= 1
            self.selected_token_index = -1
            
            # If we were done generating, restart
            if not self.is_generating and self.total_tokens_generated < self.max_tokens:
                # Regenerate alternatives for current position
                await self.generate_next_alternatives()
    
    def reset_generation(self):
        """Reset the entire generation session."""
        self.current_text = ""
        self.generated_tokens = []
        self.current_alternatives = []
        self.selected_token_index = -1
        self.is_generating = False
        self.has_started = False
        self.total_tokens_generated = 0
        self.clear_error()
    
    @rx.var
    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return len(self.generated_tokens) > 0
    
    @rx.var
    def can_continue(self) -> bool:
        """Check if generation can continue."""
        return self.has_started and self.total_tokens_generated < self.max_tokens
    
    @rx.var
    def generation_complete(self) -> bool:
        """Check if generation is complete."""
        return self.has_started and self.total_tokens_generated >= self.max_tokens
    
    @rx.var
    def progress_percentage(self) -> float:
        """Calculate generation progress percentage."""
        if self.max_tokens == 0:
            return 0.0
        return (self.total_tokens_generated / self.max_tokens) * 100.0


def prompt_input_section() -> rx.Component:
    """Simple prompt input section."""
    return rx.vstack(
        rx.heading(
            "Start Interactive Token Generation",
            size="6",
            color="#1A1A1A",
            margin_bottom="1rem"
        ),
        
        rx.text(
            "Enter an initial prompt to see how the language model predicts the next tokens step by step.",
            color="#6B7280",
            margin_bottom="1.5rem"
        ),
        
        # Prompt input
        rx.vstack(
            rx.text("Initial Prompt:", font_weight="600", color="#374151"),
            rx.text_area(
                placeholder="Type your prompt here... (e.g., 'The capital of France is')",
                value=InteractiveGenerationState.initial_prompt,
                on_change=InteractiveGenerationState.set_initial_prompt,
                width="100%",
                min_height="100px",
                border="1px solid #D1D5DB",
                border_radius="0.5rem",
                padding="0.75rem",
                font_size="0.875rem",
                _focus={
                    "border_color": "#2563EB",
                    "box_shadow": "0 0 0 3px rgba(37, 99, 235, 0.1)"
                }
            ),
            spacing="2",
            align="stretch",
            width="100%"
        ),
        
        # Generation settings
        rx.vstack(
            # Temperature slider
            rx.vstack(
                rx.hstack(
                    rx.text("Temperature:", font_size="0.875rem", font_weight="500"),
                    rx.spacer(),
                    rx.text(
                        f"{InteractiveGenerationState.temperature:.1f}",
                        font_size="0.875rem",
                        color="#2563EB",
                        font_weight="600"
                    ),
                    width="100%",
                    align="center"
                ),
                rx.slider(
                    default_value=[InteractiveGenerationState.temperature],
                    on_change=InteractiveGenerationState.set_temperature_slider,
                    min=0,
                    max=2,
                    step=0.1,
                    width="100%"
                ),
                rx.text(
                    "Controls randomness: 0.0 = deterministic, 2.0 = very creative",
                    font_size="0.75rem",
                    color="#6B7280",
                    font_style="italic"
                ),
                spacing="2",
                align="stretch",
                width="100%"
            ),
            
            # Max tokens slider
            rx.vstack(
                rx.hstack(
                    rx.text("Max Tokens:", font_size="0.875rem", font_weight="500"),
                    rx.spacer(),
                    rx.text(
                        f"{InteractiveGenerationState.max_tokens}",
                        font_size="0.875rem",
                        color="#2563EB", 
                        font_weight="600"
                    ),
                    width="100%",
                    align="center"
                ),
                rx.slider(
                    default_value=[InteractiveGenerationState.max_tokens],
                    on_change=InteractiveGenerationState.set_max_tokens_slider,
                    min=1,
                    max=100,
                    step=1,
                    width="100%"
                ),
                rx.text(
                    "Maximum number of tokens to generate in this session",
                    font_size="0.75rem",
                    color="#6B7280",
                    font_style="italic"
                ),
                spacing="2",
                align="stretch",
                width="100%"
            ),
            
            spacing="6",
            margin_top="1.5rem",
            width="100%"
        ),
        
        # Error display
        rx.cond(
            InteractiveGenerationState.has_error,
            rx.box(
                rx.text(
                    InteractiveGenerationState.error_message,
                    color="#DC2626",
                    font_size="0.875rem"
                ),
                background="#FEF2F2",
                border="1px solid #FECACA",
                border_radius="0.5rem",
                padding="0.75rem",
                margin_top="1rem"
            ),
            rx.box()
        ),
        
        # Start button
        rx.button(
            rx.cond(
                InteractiveGenerationState.is_loading,
                rx.hstack(
                    rx.spinner(size="2"),
                    rx.text("Starting..."),
                    spacing="2",
                    align="center"
                ),
                rx.hstack(
                    rx.icon("play", size=18),
                    rx.text("Start Generation"),
                    spacing="2",
                    align="center"
                )
            ),
            on_click=InteractiveGenerationState.start_generation,
            disabled=InteractiveGenerationState.is_loading | (InteractiveGenerationState.initial_prompt == ""),
            size="3",
            color_scheme="blue",
            margin_top="1.5rem",
            width="200px"
        ),
        
        spacing="4",
        align="stretch",
        width="100%",
        padding="2rem",
        background="white",
        border="1px solid #E5E7EB",
        border_radius="0.75rem",
        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1)"
    )


def generation_display_section() -> rx.Component:
    """Main generation display with current text and token selection."""
    return rx.vstack(
        # Progress header
        rx.hstack(
            rx.heading(
                "Token Generation in Progress",
                size="5",
                color="#1A1A1A"
            ),
            rx.spacer(),
            rx.text(
                f"Progress: {InteractiveGenerationState.total_tokens_generated} / {InteractiveGenerationState.max_tokens} tokens",
                color="#6B7280",
                font_size="0.875rem"
            ),
            align="center",
            width="100%",
            margin_bottom="1rem"
        ),
        
        # Progress bar
        rx.box(
            rx.box(
                width=f"{InteractiveGenerationState.progress_percentage}%",
                height="100%",
                background="#2563EB",
                border_radius="0.25rem",
                transition="width 0.5s ease-in-out"
            ),
            width="100%",
            height="8px",
            background="#E5E7EB",
            border_radius="0.25rem",
            margin_bottom="2rem"
        ),
        
        # Current text display
        rx.vstack(
            rx.text("Generated Text:", font_weight="600", color="#374151"),
            rx.box(
                rx.text(
                    rx.cond(
                        InteractiveGenerationState.current_text != "",
                        InteractiveGenerationState.current_text,
                        "Text will appear here as you select tokens..."
                    ),
                    font_size="1.125rem",
                    line_height="1.6",
                    color="#1A1A1A",
                    white_space="nowrap",
                    overflow="auto"
                ),
                width="100%",
                min_height="120px",
                padding="1.5rem",
                background="#F9FAFB",
                border="1px solid #E5E7EB",
                border_radius="0.5rem"
            ),
            spacing="2",
            align="stretch",
            width="100%",
            margin_bottom="2rem"
        ),
        
        # Token selection area
        rx.cond(
            InteractiveGenerationState.is_generating,
            rx.vstack(
                rx.cond(
                    InteractiveGenerationState.is_loading,
                    rx.center(
                        rx.vstack(
                            rx.spinner(size="3"),
                            rx.text("Generating token alternatives...", color="#6B7280"),
                            spacing="3",
                            align="center"
                        ),
                        padding="3rem"
                    ),
                    rx.cond(
                        InteractiveGenerationState.current_alternatives.length() > 0,
                        interactive_probability_bars(
                            tokens=InteractiveGenerationState.current_alternatives,
                            selected_index=InteractiveGenerationState.selected_token_index,
                            on_token_select=InteractiveGenerationState.select_token,
                            show_rank_numbers=True,
                            show_token_text=True,
                            show_percentage=True,
                            animate=True
                        ),
                        rx.text("No alternatives available", color="#6B7280")
                    )
                ),
                spacing="4",
                width="100%"
            ),
            rx.cond(
                InteractiveGenerationState.generation_complete,
                rx.center(
                    rx.vstack(
                        rx.icon("check-circle-2", size=48, color="#10B981"),
                        rx.text(
                            "Generation Complete!",
                            font_size="1.25rem",
                            font_weight="600",
                            color="#10B981"
                        ),
                        rx.text(
                            f"Generated {InteractiveGenerationState.total_tokens_generated} tokens",
                            color="#6B7280"
                        ),
                        spacing="3",
                        align="center"
                    ),
                    padding="3rem"
                ),
                rx.box()
            )
        ),
        
        # Controls
        token_generation_controls(
            on_reset=InteractiveGenerationState.reset_generation,
            on_undo_last=InteractiveGenerationState.undo_last_token,
            is_generating=InteractiveGenerationState.is_generating,
            can_undo=InteractiveGenerationState.can_undo,
            can_generate=InteractiveGenerationState.can_continue
        ),
        
        spacing="4",
        align="stretch",
        width="100%",
        padding="2rem",
        background="white",
        border="1px solid #E5E7EB", 
        border_radius="0.75rem",
        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1)"
    )


def interactive_mode_content() -> rx.Component:
    """Main content for the interactive mode page."""
    return rx.vstack(
        rx.heading(
            "Interactive Token Generation",
            size="8",
            margin_bottom="1rem",
            text_align="center",
            color="#1A1A1A"
        ),
        
        rx.text(
            "Experience how large language models generate text one token at a time. Enter a prompt, then select from the most probable next tokens to build your text step by step.",
            color="#6B7280",
            text_align="center",
            margin_bottom="3rem",
            max_width="800px",
            margin_x="auto"
        ),
        
        # Show either prompt input or generation display
        rx.cond(
            InteractiveGenerationState.has_started,
            generation_display_section(),
            prompt_input_section()
        ),
        
        spacing="6",
        align="stretch",
        max_width="1200px",
        margin="0 auto",
        padding="2rem"
    )


def interactive_mode_page() -> rx.Component:
    """Interactive mode page with layout."""
    return app_layout(
        interactive_mode_content()
    )
