"""Configuration Test page for LLM service diagnostics."""

import reflex as rx
from ..components.layout import app_layout
from ..services.llm_client import get_llm_client
from ..utils.config import test_config
from typing import Dict, Any, Optional
import json


class ConfigTestState(rx.State):
    """State for configuration testing page."""
    
    # Test results
    is_testing: bool = False
    test_results: Dict[str, Any] = {}
    has_results: bool = False
    
    # Individual test results for UI binding
    config_status: str = ""
    service_status: str = ""
    model_status: str = ""
    generation_status: str = ""
    
    @rx.event(background=True)
    async def run_diagnostics(self):
        """Run comprehensive diagnostics tests."""
        async with self:
            self.is_testing = True
            self.has_results = False
            
        results = {}
        
        # Test 1: Configuration
        try:
            config_info = test_config()
            results["config"] = {
                "status": "✅ Pass",
                "details": config_info
            }
        except Exception as e:
            results["config"] = {
                "status": "❌ Fail",
                "error": str(e)
            }
        
        # Test 2: LLM Service Health
        try:
            client = get_llm_client()
            health_result = await client.test_health()
            results["service_health"] = {
                "status": "✅ Pass" if health_result.get("healthy", False) else "❌ Fail",
                "details": health_result
            }
        except Exception as e:
            results["service_health"] = {
                "status": "❌ Fail", 
                "error": str(e)
            }
        
        # Test 3: Model Status
        try:
            client = get_llm_client()
            status_result = await client.test_status()
            results["model_status"] = {
                "status": "✅ Pass" if status_result.get("model_loaded", False) else "❌ Fail",
                "details": status_result
            }
        except Exception as e:
            results["model_status"] = {
                "status": "❌ Fail",
                "error": str(e)
            }
        
        # Test 4: Token Generation
        try:
            client = get_llm_client()
            generation_result = await client.generate_tokens(
                prompt="The capital of France is",
                max_tokens=1,
                temperature=0.7,
                top_logprobs=5
            )
            results["token_generation"] = {
                "status": "✅ Pass",
                "details": {
                    "selected_token": generation_result.selected_token,
                    "probability": f"{generation_result.selected_probability:.2%}",
                    "alternatives_count": len(generation_result.alternatives)
                }
            }
        except Exception as e:
            results["token_generation"] = {
                "status": "❌ Fail",
                "error": str(e)
            }
        
        async with self:
            self.test_results = results
            self.config_status = results.get("config", {}).get("status", "❌ Unknown")
            self.service_status = results.get("service_health", {}).get("status", "❌ Unknown")
            self.model_status = results.get("model_status", {}).get("status", "❌ Unknown")
            self.generation_status = results.get("token_generation", {}).get("status", "❌ Unknown")
            self.has_results = True
            self.is_testing = False


def test_result_card(title: str, status: str, details: Optional[Dict] = None) -> rx.Component:
    """Display a test result card."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(title, font_weight="600", color="#1F2937"),
                rx.text(status, font_weight="500"),
                justify="between",
                align="center",
                width="100%"
            ),
            
            rx.cond(
                details,
                rx.box(
                    rx.text(
                        json.dumps(details, indent=2),
                        font_family="monospace",
                        font_size="0.75rem",
                        color="#6B7280",
                        white_space="pre-wrap"
                    ),
                    background="#F9FAFB",
                    border="1px solid #E5E7EB",
                    border_radius="0.375rem",
                    padding="0.75rem",
                    max_height="200px",
                    overflow="auto"
                )
            ),
            
            spacing="3",
            align="start",
            width="100%"
        ),
        
        padding="1.5rem",
        border="1px solid #E5E7EB",
        border_radius="0.5rem",
        background="#FFFFFF",
        width="100%"
    )


def config_test_content() -> rx.Component:
    """Configuration test page content."""
    return rx.vstack(
        # Page header
        rx.vstack(
            rx.heading(
                "Configuration Test",
                size="8",
                color="#1A1A1A",
                font_weight="600"
            ),
            rx.text(
                "Test LLM service connectivity and model functionality",
                color="#6B7280",
                font_size="1.125rem"
            ),
            spacing="2",
            align="start",
            margin_bottom="2rem"
        ),
        
        # Test controls
        rx.hstack(
            rx.button(
                rx.cond(
                    ConfigTestState.is_testing,
                    rx.hstack(
                        rx.spinner(size="2"),
                        rx.text("Running Tests..."),
                        spacing="2",
                        align="center"
                    ),
                    rx.text("Run Diagnostics")
                ),
                on_click=ConfigTestState.run_diagnostics,
                disabled=ConfigTestState.is_testing,
                size="3",
                variant="solid"
            ),
            spacing="3",
            margin_bottom="2rem"
        ),
        
        # Test results
        rx.cond(
            ConfigTestState.has_results,
            rx.vstack(
                rx.text(
                    "Test Results",
                    font_size="1.25rem",
                    font_weight="600",
                    color="#1F2937",
                    margin_bottom="1rem"
                ),
                
                test_result_card(
                    "Configuration",
                    ConfigTestState.config_status,
                    ConfigTestState.test_results.get("config", {}).get("details")
                ),
                
                test_result_card(
                    "Service Health",
                    ConfigTestState.service_status,
                    ConfigTestState.test_results.get("service_health", {}).get("details")
                ),
                
                test_result_card(
                    "Model Status", 
                    ConfigTestState.model_status,
                    ConfigTestState.test_results.get("model_status", {}).get("details")
                ),
                
                test_result_card(
                    "Token Generation",
                    ConfigTestState.generation_status,
                    ConfigTestState.test_results.get("token_generation", {}).get("details")
                ),
                
                spacing="4",
                width="100%"
            )
        ),
        
        spacing="0",
        align="start",
        width="100%",
        max_width="800px",
        margin="0 auto",
        padding="2rem"
    )


def config_test_page() -> rx.Component:
    """Configuration test page."""
    return app_layout(config_test_content())
