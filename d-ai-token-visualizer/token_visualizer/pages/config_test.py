"""Configuration test page for verifying environment variable loading."""

import reflex as rx
from ..utils.config import test_config
from ..services.azure_openai import test_azure_openai_service


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
        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)"
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
        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)"
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
        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)"
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
                "Phase 2.3 & 3.1: Environment Configuration & API Connectivity Verification",
                color="#6B7280",
                text_align="center",
                margin_bottom="2rem"
            ),
            
            config_test_card(),
            api_test_card(),
            environment_info_card(),
            
            spacing="6",
            align="center",
            width="100%",
            max_width="800px"
        ),
        padding="2rem",
        center_content=True
    )
