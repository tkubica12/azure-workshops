#!/usr/bin/env python3
"""
Simple test script to verify Azure OpenAI API access and logprobs functionality.
This script tests the basic connection and logprobs feature before building the main application.
"""

import os
import json
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

def test_azure_openai_connection():
    """Test basic Azure OpenAI API connection and logprobs functionality using Azure Default Credentials."""
    
    # Load environment variables
    load_dotenv()
    
    # Get configuration from environment variables
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
    
    # Check if we should use API key or Azure Default Credentials
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    use_aad = os.getenv("USE_AZURE_DEFAULT_CREDENTIALS", "true").lower() == "true"
    
    if not endpoint:
        print("❌ Error: Missing required environment variable AZURE_OPENAI_ENDPOINT.")
        return False
    
    print(f"🔗 Testing connection to: {endpoint}")
    print(f"📋 Using deployment: {deployment_name}")
    print(f"🔢 API Version: {api_version}")
    
    if use_aad and not api_key:
        print("🔐 Authentication: Azure Default Credentials (AAD)")
        auth_method = "AAD"
    elif api_key:
        print("🔑 Authentication: API Key")
        auth_method = "API_KEY"
    else:
        print("❌ Error: No authentication method available.")
        print("Please set either AZURE_OPENAI_API_KEY or ensure Azure Default Credentials are available.")
        return False
    
    print("-" * 50)
    
    try:
        # Initialize Azure OpenAI client based on authentication method
        if auth_method == "AAD":
            print("🔐 Setting up Azure Default Credentials...")
            credential = DefaultAzureCredential()
            token_provider = get_bearer_token_provider(
                credential, 
                "https://cognitiveservices.azure.com/.default"
            )
            
            client = AzureOpenAI(
                azure_endpoint=endpoint,
                azure_ad_token_provider=token_provider,
                api_version=api_version
            )
        else:
            client = AzureOpenAI(
                azure_endpoint=endpoint,
                api_key=api_key,
                api_version=api_version
            )
        
        # Test basic completion
        print("🧪 Testing basic completion...")
        test_prompt = "The capital of France is"
        
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "user", "content": test_prompt}
            ],
            max_tokens=1,
            temperature=0.7,
            logprobs=True,
            top_logprobs=5
        )
        
        print("✅ Basic API connection successful!")
        print(f"📝 Prompt: '{test_prompt}'")
        print(f"💬 Response: '{response.choices[0].message.content}'")
        
        # Test logprobs functionality
        print("\n🔍 Testing logprobs functionality...")
        
        if response.choices[0].logprobs and response.choices[0].logprobs.content:
            logprobs_data = response.choices[0].logprobs.content[0]
            
            print("✅ Logprobs functionality working!")
            print(f"🎯 Selected token: '{logprobs_data.token}'")
            print(f"📊 Log probability: {logprobs_data.logprob:.4f}")
            print(f"📈 Probability: {100 * (2.71828 ** logprobs_data.logprob):.2f}%")
            
            if logprobs_data.top_logprobs:
                print("\n🏆 Top 5 alternative tokens:")
                for i, alt_token in enumerate(logprobs_data.top_logprobs, 1):
                    probability = 100 * (2.71828 ** alt_token.logprob)
                    print(f"  {i}. '{alt_token.token}' - {probability:.2f}%")
            
            return True
        else:
            print("❌ Logprobs data not found in response")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Azure OpenAI API: {str(e)}")
        return False

def main():
    """Main function to run the API test."""
    print("🚀 Azure OpenAI API Test for Token Visualizer")
    print("=" * 50)
    
    success = test_azure_openai_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Azure OpenAI API is ready for Token Visualizer.")
        print("✅ Next step: Create project structure and basic Reflex app")
    else:
        print("❌ Tests failed. Please check your configuration and try again.")
        print("📋 Configuration options:")
        print("   Option 1 - Azure Default Credentials (Recommended):")
        print("     AZURE_OPENAI_ENDPOINT=your_endpoint_here")
        print("     USE_AZURE_DEFAULT_CREDENTIALS=true")
        print("     AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name")
        print("   Option 2 - API Key:")
        print("     AZURE_OPENAI_ENDPOINT=your_endpoint_here")
        print("     AZURE_OPENAI_API_KEY=your_api_key_here")
        print("     USE_AZURE_DEFAULT_CREDENTIALS=false")
        print("     AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name")
    
    return success

if __name__ == "__main__":
    main()
