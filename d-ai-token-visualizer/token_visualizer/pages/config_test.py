"""Configuration test page for verifying environment variable loading."""

import reflex as rx
from ..utils.config import test_config
from ..services.azure_openai import test_azure_openai_service
from ..state.api_test_state import APITestState


def config_test_card() -> rx.Component:
    """Component to display configuration test results."""
    config_status = test_config()
    
    # Status indicator based on validation
    status_color = "#10B981" if config_status.get("valid", False) else "#EF4444"
    status_text = "✅ Valid" if config_status.get("valid", False) else "❌ Invalid"
    
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading(
                    "Configuration Status",
                    size="5",
                    color="#1F2937"
                ),
                rx.badge(
                    status_text,
                    background=status_color,
                    color="white",
                    padding="0.25rem 0.75rem",
                    border_radius="0.375rem"
                ),
                justify="between",
                align="center",
                width="100%"
            ),
            
            # Configuration details
            rx.vstack(
                rx.text(
                    "Message:",
                    font_weight="600",
                    color="#374151",
                    margin_bottom="0.25rem"
                ),
                rx.text(
                    config_status.get("message", "Unknown status"),
                    color="#6B7280",
                    margin_bottom="1rem"
                ),
                
                # Show configuration details if valid
                rx.cond(
                    config_status.get("valid", False),
                    rx.vstack(
                        rx.hstack(
                            rx.text("Endpoint:", font_weight="600", color="#374151"),
                            rx.text(config_status.get("endpoint", "Not set"), color="#6B7280"),
                            justify="between",
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("Deployment:", font_weight="600", color="#374151"),
                            rx.text(config_status.get("deployment", "Not set"), color="#6B7280"),
                            justify="between",
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("API Version:", font_weight="600", color="#374151"),
                            rx.text(config_status.get("api_version", "Not set"), color="#6B7280"),
                            justify="between",
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("Auth Method:", font_weight="600", color="#374151"),
                            rx.text(config_status.get("auth_method", "Not set"), color="#6B7280"),
                            justify="between",
                            width="100%"
                        ),
                        spacing="2",
                        align="stretch",
                        width="100%"
                    )
                ),
                
                # Show error details if invalid
                rx.cond(
                    not config_status.get("valid", False),
                    rx.box(
                        rx.text(
                            "Error Details:",
                            font_weight="600",
                            color="#DC2626",
                            margin_bottom="0.5rem"
                        ),
                        rx.text(
                            config_status.get("error", "Unknown error"),
                            color="#7F1D1D",
                            font_family="monospace",
                            font_size="0.875rem",
                            background="#FEF2F2",
                            padding="0.75rem",
                            border_radius="0.375rem",
                            border="1px solid #FECACA"
                        ),
                    )
                ),
                
                align="stretch",
                width="100%"
            ),
            
            spacing="4",
            align="stretch",
            width="100%"
        ),
        
        background="white",
        border="1px solid #E5E7EB",
        border_radius="0.5rem",
        padding="1.5rem",
        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
        width="100%"
    )


def environment_info_card() -> rx.Component:
    """Component to display environment information."""
    return rx.box(
        rx.vstack(
            rx.heading(
                "Environment Information",
                size="5",
                color="#1F2937"
            ),
            
            rx.vstack(
                rx.text(
                    "This page tests the configuration loading functionality. "
                    "It reads environment variables from the .env file and validates "
                    "the Azure OpenAI configuration.",
                    color="#6B7280",
                    line_height="1.6"
                ),
                
                rx.text(
                    "Required Environment Variables:",
                    font_weight="600",
                    color="#374151",
                    margin_top="1rem"
                ),
                
                rx.unordered_list(
                    rx.list_item("AZURE_OPENAI_ENDPOINT", color="#6B7280"),
                    rx.list_item("AZURE_OPENAI_DEPLOYMENT_NAME", color="#6B7280"),
                    rx.list_item("AZURE_OPENAI_API_VERSION", color="#6B7280"),
                    rx.list_item("USE_AZURE_DEFAULT_CREDENTIALS (optional)", color="#6B7280"),
                    rx.list_item("AZURE_OPENAI_API_KEY (if not using AAD)", color="#6B7280"),
                    margin_left="1rem"
                ),
                
                align="stretch",
                width="100%"
            ),
            
            spacing="4",
            align="stretch",
            width="100%"
        ),
        
        background="white",
        border="1px solid #E5E7EB",
        border_radius="0.5rem",
        padding="1.5rem",
        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
        width="100%"
    )


def api_test_card() -> rx.Component:
    """Component to display API connectivity test results."""
    api_status = test_azure_openai_service()
    
    # Status indicator based on API test
    status_color = "#10B981" if api_status.get("success", False) else "#EF4444"
    status_text = "✅ Connected" if api_status.get("success", False) else "❌ Failed"
    
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading(
                    "API Connectivity Test",
                    size="5",
                    color="#1F2937"
                ),
                rx.badge(
                    status_text,
                    background=status_color,
                    color="white",
                    padding="0.25rem 0.75rem",
                    border_radius="0.375rem"
                ),
                justify="between",
                align="center",
                width="100%"
            ),
            
            # API test details
            rx.vstack(
                rx.text(
                    "Status:",
                    font_weight="600",
                    color="#374151",
                    margin_bottom="0.25rem"
                ),
                rx.text(
                    api_status.get("message", "Unknown status"),
                    color="#6B7280",
                    margin_bottom="1rem"
                ),
                
                # Show test results if successful
                rx.cond(
                    api_status.get("success", False),
                    rx.vstack(
                        rx.text(
                            "Test Results:",
                            font_weight="600",
                            color="#374151",
                            margin_bottom="0.5rem"
                        ),
                        
                        # Connection test
                        rx.hstack(
                            rx.text("Connection Test:", font_weight="500", color="#374151"),
                            rx.text(
                                "✅ Passed" if api_status.get("connection_test", False) else "❌ Failed",
                                color="#10B981" if api_status.get("connection_test", False) else "#EF4444"
                            ),
                            justify="between",
                            width="100%"
                        ),
                        
                        # Logprobs test
                        rx.hstack(
                            rx.text("Logprobs Test:", font_weight="500", color="#374151"),
                            rx.text(
                                "✅ Passed" if api_status.get("logprobs_test", False) else "❌ Failed",
                                color="#10B981" if api_status.get("logprobs_test", False) else "#EF4444"
                            ),
                            justify="between",
                            width="100%"
                        ),
                        
                        # Show test result details if available
                        rx.cond(
                            api_status.get("test_result") is not None,
                            rx.vstack(
                                rx.text(
                                    "Sample Generation:",
                                    font_weight="600",
                                    color="#374151",
                                    margin_top="1rem",
                                    margin_bottom="0.5rem"
                                ),
                                rx.box(
                                    rx.vstack(
                                        rx.text(
                                            f"Prompt: {api_status.get('test_result', {}).get('prompt', 'N/A')}",
                                            color="#374151",
                                            font_weight="500"
                                        ),
                                        rx.text(
                                            f"Generated: {api_status.get('test_result', {}).get('generated_text', 'N/A')}",
                                            color="#1F2937",
                                            font_weight="600"
                                        ),
                                        rx.text(
                                            f"Selected Token: '{api_status.get('test_result', {}).get('selected_token', {}).get('token', 'N/A')}' ({api_status.get('test_result', {}).get('selected_token', {}).get('probability', 'N/A')})",
                                            color="#6B7280"
                                        ),
                                        rx.text(
                                            f"Alternatives: {api_status.get('test_result', {}).get('alternatives_count', 0)} found",
                                            color="#6B7280"
                                        ),
                                        spacing="2",
                                        align="start"
                                    ),
                                    background="#F9FAFB",
                                    padding="0.75rem",
                                    border_radius="0.375rem",
                                    border="1px solid #E5E7EB"
                                )
                            )
                        ),
                        
                        spacing="2",
                        align="stretch",
                        width="100%"
                    )
                ),
                
                # Show error details if failed
                rx.cond(
                    not api_status.get("success", False),
                    rx.vstack(
                        rx.text(
                            "Error Details:",
                            font_weight="600",
                            color="#DC2626",
                            margin_bottom="0.5rem"
                        ),
                        rx.text(
                            api_status.get("error", api_status.get("logprobs_error", "Unknown error")),
                            color="#7F1D1D",
                            font_family="monospace",
                            font_size="0.875rem",
                            background="#FEF2F2",
                            padding="0.75rem",
                            border_radius="0.375rem",
                            border="1px solid #FECACA"
                        ),
                        spacing="2",
                        align="stretch",
                        width="100%"
                    )
                ),
                
                align="stretch",
                width="100%"
            ),
            
            spacing="4",
            align="stretch",
            width="100%"
        ),
        
        background="white",
        border="1px solid #E5E7EB",
        border_radius="0.5rem",
        padding="1.5rem",
        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
        width="100%"
    )


def custom_prompt_test_card() -> rx.Component:
    """Component for testing custom prompts with the API."""
    return rx.box(
        rx.vstack(
            # Header
            rx.heading(
                "Custom Prompt Testing",
                size="5",
                color="#1F2937"
            ),
            rx.text(
                "Test the Azure OpenAI API with your own prompts and see logprobs results.",
                color="#6B7280",
                margin_bottom="1rem"
            ),
            
            # Preset buttons
            rx.vstack(
                rx.text(
                    "Quick Presets:",
                    font_weight="600",
                    color="#374151",
                    margin_bottom="0.5rem"
                ),
                rx.hstack(
                    rx.button(
                        "Simple",
                        size="2",
                        variant="outline",
                        on_click=APITestState.use_preset_prompt("simple")
                    ),
                    rx.button(
                        "Story",
                        size="2",
                        variant="outline",
                        on_click=APITestState.use_preset_prompt("story")
                    ),
                    rx.button(
                        "Technical",
                        size="2",
                        variant="outline",
                        on_click=APITestState.use_preset_prompt("technical")
                    ),
                    rx.button(
                        "Creative",
                        size="2",
                        variant="outline",
                        on_click=APITestState.use_preset_prompt("creative")
                    ),
                    rx.button(
                        "Question",
                        size="2",
                        variant="outline",
                        on_click=APITestState.use_preset_prompt("question")
                    ),
                    spacing="2",
                    wrap="wrap"
                ),
                spacing="2",
                align="start",
                width="100%"
            ),
            
            # Form inputs
            rx.vstack(
                # Prompt input
                rx.vstack(
                    rx.text("Test Prompt:", font_weight="600", color="#374151"),
                    rx.text_area(
                        placeholder="Enter your prompt here...",
                        value=APITestState.test_prompt,
                        on_change=APITestState.set_test_prompt,
                        width="100%",
                        min_height="80px"
                    ),
                    spacing="1",
                    align="start",
                    width="100%"
                ),
                
                # Parameters
                rx.hstack(
                    rx.vstack(
                        rx.text("Max Tokens:", font_weight="500", color="#374151"),
                        rx.input(
                            value=APITestState.max_tokens.to(str),
                            on_change=APITestState.set_max_tokens,
                            type="number",
                            min="1",
                            max="10",
                            width="80px"
                        ),
                        spacing="1",
                        align="start"
                    ),
                    rx.vstack(
                        rx.text("Temperature:", font_weight="500", color="#374151"),
                        rx.input(
                            value=APITestState.temperature.to(str),
                            on_change=APITestState.set_temperature,
                            type="number",
                            min="0",
                            max="2",
                            step="0.1",
                            width="80px"
                        ),
                        spacing="1",
                        align="start"
                    ),
                    rx.vstack(
                        rx.text("Top Logprobs:", font_weight="500", color="#374151"),
                        rx.input(
                            value=APITestState.top_logprobs.to(str),
                            on_change=APITestState.set_top_logprobs,
                            type="number",
                            min="1",
                            max="20",
                            width="80px"
                        ),
                        spacing="1",
                        align="start"
                    ),
                    spacing="4",
                    wrap="wrap"
                ),
                
                # Action buttons
                rx.hstack(
                    rx.button(
                        rx.cond(
                            APITestState.is_testing,
                            rx.hstack(
                                rx.spinner(size="3"),
                                rx.text("Testing..."),
                                spacing="2",
                                align="center"
                            ),
                            rx.text("Run Test")
                        ),
                        on_click=APITestState.run_custom_test,
                        disabled=APITestState.is_testing,
                        size="3",
                        color_scheme="blue"
                    ),
                    rx.button(
                        "Clear Results",
                        on_click=APITestState.clear_test_results,
                        size="3",
                        variant="outline"
                    ),
                    spacing="3"
                ),
                
                spacing="4",
                align="stretch",
                width="100%"
            ),
            
            # Test results - Show detailed API response
            rx.cond(
                APITestState.has_test_result,
                rx.vstack(
                    rx.text(
                        "Test Results:",
                        font_weight="600",
                        color="#374151",
                        margin_bottom="0.5rem"
                    ),
                    rx.box(
                        rx.vstack(
                            # Success header
                            rx.text("✅ Test completed successfully!", color="#059669", font_weight="600"),
                            
                            # Prompt and Generated Text
                            rx.divider(margin="0.75rem 0"),
                            rx.vstack(
                                rx.text("Input & Output:", font_weight="600", color="#374151"),
                                rx.hstack(
                                    rx.text("Prompt:", font_weight="500", color="#6B7280", min_width="80px"),
                                    rx.text(APITestState.result_prompt, color="#1F2937"),
                                    spacing="3",
                                    align="start",
                                    width="100%"
                                ),
                                rx.hstack(
                                    rx.text("Generated:", font_weight="500", color="#6B7280", min_width="80px"),
                                    rx.text(APITestState.result_generated_text, color="#1F2937", font_weight="600"),
                                    spacing="3",
                                    align="start",
                                    width="100%"
                                ),
                                spacing="2",
                                align="start",
                                width="100%"
                            ),
                            
                            # Selected Token Details
                            rx.divider(margin="0.75rem 0"),
                            rx.vstack(
                                rx.text("Selected Token:", font_weight="600", color="#374151"),
                                rx.hstack(
                                    rx.text("Token:", font_weight="500", color="#6B7280", min_width="80px"),
                                    rx.text(f"'{APITestState.result_selected_token}'", color="#1F2937", font_weight="600"),
                                    spacing="3",
                                    align="start",
                                    width="100%"
                                ),
                                rx.hstack(
                                    rx.text("Probability:", font_weight="500", color="#6B7280", min_width="80px"),
                                    rx.text(APITestState.result_selected_probability, color="#059669", font_weight="600"),
                                    spacing="3",
                                    align="start",
                                    width="100%"
                                ),
                                spacing="2",
                                align="start",
                                width="100%"
                            ),
                            
                            # Alternative Tokens
                            rx.cond(
                                APITestState.result_alternatives.length() > 0,
                                rx.vstack(
                                    rx.divider(margin="0.75rem 0"),
                                    rx.text("Alternative Tokens:", font_weight="600", color="#374151"),
                                    rx.foreach(
                                        APITestState.result_alternatives,
                                        lambda alt: rx.hstack(
                                            rx.text(alt["token"], color="#1F2937", font_weight="500", min_width="100px"),
                                            rx.text(alt["probability"], color="#059669", min_width="70px"),
                                            rx.text(alt["logprob"], color="#6B7280", font_size="0.875rem"),
                                            spacing="3",
                                            align="start"
                                        )
                                    ),
                                    spacing="2",
                                    align="start",
                                    width="100%"
                                )
                            ),
                            
                            # Parameters Used
                            rx.divider(margin="0.75rem 0"),
                            rx.vstack(
                                rx.text("Parameters Used:", font_weight="600", color="#374151"),
                                rx.hstack(
                                    rx.text(f"Max Tokens: {APITestState.max_tokens}", color="#6B7280", font_size="0.875rem"),
                                    rx.text(f"Temperature: {APITestState.temperature}", color="#6B7280", font_size="0.875rem"),
                                    rx.text(f"Top Logprobs: {APITestState.top_logprobs}", color="#6B7280", font_size="0.875rem"),
                                    spacing="4",
                                    wrap="wrap"
                                ),
                                spacing="2",
                                align="start",
                                width="100%"
                            ),
                            
                            # Raw Response Summary
                            rx.divider(margin="0.75rem 0"),
                            rx.vstack(
                                rx.text("Response Summary:", font_weight="600", color="#374151"),
                                rx.text(APITestState.result_raw_response, color="#6B7280", font_size="0.875rem", font_family="monospace"),
                                spacing="2",
                                align="start",
                                width="100%"
                            ),
                            
                            spacing="3",
                            align="start",
                            width="100%"
                        ),
                        background="#F0FDF4",
                        padding="1rem",
                        border_radius="0.375rem",
                        border="1px solid #BBF7D0"
                    ),
                    spacing="3",
                    align="start",
                    width="100%"
                )
            ),
            
            # Error display
            rx.cond(
                APITestState.test_error != "",
                rx.vstack(
                    rx.text(
                        "Test Error:",
                        font_weight="600",
                        color="#DC2626",
                        margin_bottom="0.5rem"
                    ),
                    rx.text(
                        APITestState.test_error,
                        color="#7F1D1D",
                        font_family="monospace",
                        font_size="0.875rem",
                        background="#FEF2F2",
                        padding="0.75rem",
                        border_radius="0.375rem",
                        border="1px solid #FECACA"
                    ),
                    spacing="2",
                    align="start",
                    width="100%"
                )
            ),
            
            spacing="5",
            align="stretch", 
            width="100%"
        ),
        
        background="white",
        border="1px solid #E5E7EB",
        border_radius="0.5rem",
        padding="1.5rem",
        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
        width="100%"
    )


def config_test_page() -> rx.Component:
    """Configuration test page layout."""
    return rx.container(
        rx.vstack(
            rx.heading(
                "Configuration Test",
                size="8",
                color="#1F2937",
                text_align="center",
                margin_bottom="0.5rem"
            ),
            rx.text(
                "Phase 3.2 & 3.3: Azure OpenAI Integration & API Testing",
                color="#6B7280",
                text_align="center",
                margin_bottom="2rem"
            ),
            
            # All cards with consistent width
            rx.vstack(
                config_test_card(),
                api_test_card(),
                custom_prompt_test_card(),
                environment_info_card(),
                
                spacing="6",
                align="stretch",  # Changed from "center" to "stretch"
                width="100%"
            ),
            
            spacing="6",
            align="center",
            width="100%",
            max_width="1000px"  # Increased from 900px
        ),
        padding="2rem",
        center_content=True
    )
