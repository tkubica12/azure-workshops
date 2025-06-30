#!/usr/bin/env python3
"""Test script for the Local LLM Service."""

import asyncio
import httpx
import time
from typing import Dict, Any


class LLMServiceTester:
    """Test client for the Local LLM Service."""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def test_health(self) -> Dict[str, Any]:
        """Test the health endpoint."""
        print("🩺 Testing health endpoint...")
        try:
            response = await self.client.get(f"{self.base_url}/health")
            result = response.json()
            print(f"   Status: {response.status_code}")
            print(f"   Response: {result}")
            return {"success": response.status_code == 200, "data": result}
        except Exception as e:
            print(f"   ❌ Health check failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def test_status(self) -> Dict[str, Any]:
        """Test the status endpoint."""
        print("📊 Testing status endpoint...")
        try:
            response = await self.client.get(f"{self.base_url}/api/v1/status")
            result = response.json()
            print(f"   Status: {response.status_code}")
            print(f"   Model: {result.get('model_name', 'Unknown')}")
            print(f"   Device: {result.get('device', 'Unknown')}")
            print(f"   Ready: {result.get('status', 'Unknown')}")
            return {"success": response.status_code == 200, "data": result}
        except Exception as e:
            print(f"   ❌ Status check failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def test_generation(self) -> Dict[str, Any]:
        """Test the generation endpoint."""
        print("🤖 Testing generation endpoint...")
        try:
            payload = {
                "prompt": "The capital of France is",
                "max_tokens": 1,
                "temperature": 0.7,
                "top_logprobs": 5
            }
            
            start_time = time.time()
            response = await self.client.post(
                f"{self.base_url}/api/v1/generate",
                json=payload
            )
            generation_time = time.time() - start_time
            
            result = response.json()
            print(f"   Status: {response.status_code}")
            print(f"   Generation time: {generation_time:.2f}s")
            
            if response.status_code == 200:
                print(f"   Prompt: {result.get('prompt', 'Unknown')}")
                print(f"   Generated: {result.get('generated_text', 'Unknown')}")
                selected = result.get('selected_token', {})
                print(f"   Selected token: '{selected.get('token', 'Unknown')}' ({selected.get('percentage', 0):.2f}%)")
                
                alternatives = result.get('top_alternatives', [])[:3]
                print(f"   Top alternatives:")
                for i, alt in enumerate(alternatives, 1):
                    print(f"     {i}. '{alt.get('token', 'Unknown')}' ({alt.get('percentage', 0):.2f}%)")
            else:
                print(f"   ❌ Error: {result}")
            
            return {"success": response.status_code == 200, "data": result}
        except Exception as e:
            print(f"   ❌ Generation test failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def test_service_test_endpoint(self) -> Dict[str, Any]:
        """Test the service's built-in test endpoint."""
        print("🧪 Testing service test endpoint...")
        try:
            response = await self.client.post(f"{self.base_url}/api/v1/test")
            result = response.json()
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   Test status: {result.get('status', 'Unknown')}")
                if result.get('status') == 'success':
                    print(f"   Prompt: {result.get('prompt', 'Unknown')}")
                    print(f"   Selected: '{result.get('selected_token', 'Unknown')}' ({result.get('selected_probability', 'Unknown')})")
                    print(f"   Generation time: {result.get('generation_time', 'Unknown')}")
            else:
                print(f"   ❌ Error: {result}")
            
            return {"success": response.status_code == 200, "data": result}
        except Exception as e:
            print(f"   ❌ Service test failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def run_all_tests(self):
        """Run all tests."""
        print("🚀 Starting Local LLM Service Tests")
        print(f"🌐 Base URL: {self.base_url}")
        print("-" * 50)
        
        # Test health first
        health_result = await self.test_health()
        if not health_result["success"]:
            print("❌ Service appears to be down. Please start the service first.")
            return
        
        print()
        
        # Wait a moment for potential initialization
        if health_result["data"].get("status") == "initializing":
            print("⏳ Service is initializing model, waiting...")
            await asyncio.sleep(5)
            print()
        
        # Test status
        await self.test_status()
        print()
        
        # Test built-in test endpoint
        await self.test_service_test_endpoint()
        print()
        
        # Test generation
        await self.test_generation()
        print()
        
        print("✅ All tests completed!")
        await self.client.aclose()


async def main():
    """Main test function."""
    tester = LLMServiceTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
