"""
LLM utilities for sentiment analysis using Azure OpenAI.
"""

import os
import time
import random
from typing import Optional, List
from openai import AzureOpenAI, RateLimitError
from azure.identity import DefaultAzureCredential
import logging

logger = logging.getLogger(__name__)


class LlmUtils:
    """Utility class for LLM-based sentiment analysis and embedding generation with efficient token management."""
    
    def __init__(self, examples_csv: str = None, deployment_name: str = None, api_version: str = None, embedding_deployment_name: str = None):
        """
        Initialize the Azure OpenAI client with AAD authentication and token caching.
        
        Args:
            examples_csv: CSV string with examples in format "text,label"
            deployment_name: Override deployment name (optional, falls back to env)
            api_version: Override API version (optional, falls back to env)
            embedding_deployment_name: Override embedding deployment name (optional, falls back to env)
        """
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_version = api_version or os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
        self.deployment_name = deployment_name or os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4.1-nano")
        self.embedding_deployment_name = embedding_deployment_name or os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME", "text-embedding-3-small")
        
        if not self.endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is required")
        
        # Use Azure AD authentication with token caching
        self.credential = DefaultAzureCredential()
        self._cached_token = None
        self._token_expires_on = None
        
        # Token usage tracking
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_requests = 0
        
        self.client = AzureOpenAI(
            api_version=self.api_version,
            azure_endpoint=self.endpoint,
            azure_ad_token_provider=self._get_cached_token
        )        
        self.system_prompt = self._create_system_prompt(examples_csv)
    
    def _get_cached_token(self) -> str:
        """
        Get Azure AD token with caching to avoid repeated token acquisition.
        
        Returns:
            Access token string
        """
        # Check if we have a valid cached token (with 5-minute buffer before expiry)
        if (self._cached_token and self._token_expires_on and 
            time.time() < (self._token_expires_on - 300)):
            return self._cached_token
        
        # Get new token
        logger.info("Acquiring new Azure AD token")
        token = self.credential.get_token("https://cognitiveservices.azure.com/.default")
        
        # Cache the token
        self._cached_token = token.token
        self._token_expires_on = token.expires_on
        
        logger.info(f"Token acquired, expires at {time.ctime(token.expires_on)}")
        return self._cached_token
    
    def pre_authenticate(self):
        """
        Pre-authenticate to warm up the token cache.
        Call this once before starting batch processing to avoid delays on first API call.
        """
        logger.info("Pre-authenticating Azure AD token...")
        self._get_cached_token()
        logger.info("Pre-authentication completed successfully")

    def _create_system_prompt(self, examples_csv: str = None) -> str:
        """
        Create the system prompt for sentiment classification.
        
        Args:
            examples_csv: CSV string with examples in format "text,label"
            
        Returns:
            System prompt string
        """
        prompt = f"""You are a sentiment analysis classifier. Your task is to classify text into one of three sentiment categories:

- 0: Negative sentiment (complaints, dissatisfaction, anger, sadness, frustration, etc.)
- 1: Neutral sentiment (factual statements, questions, neutral observations, mixed feelings, etc.)  
- 2: Positive sentiment (praise, satisfaction, happiness, excitement, love, etc.)

IMPORTANT RULES:
1. You must respond with ONLY a single digit: 0, 1, or 2
2. Do not include any text, explanation, or additional characters
3. Do not use quotes, spaces, or punctuation
4. Just return the number representing the sentiment class

EXAMPLES (in CSV format):
{examples_csv}

Based on these examples, classify the following text with the same approach.
Always return only the sentiment class as a single digit without any additional text.
"""
        logger.info(f"System prompt:\n{prompt}")
        return prompt

    def classify_sentiment(self, text: str, max_retries: int = 3) -> Optional[int]:
        """
        Classify sentiment of given text with proper 429 error handling.
        
        Args:
            text: Text to classify
            max_retries: Maximum number of retry attempts
            
        Returns:
            Sentiment classification (0, 1, or 2) or None if failed
        """
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.deployment_name,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": f"Classify this text: {text}"}
                    ],
                    max_tokens=1,
                    temperature=0,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                
                # Track token usage
                if hasattr(response, 'usage') and response.usage:
                    input_tokens = response.usage.prompt_tokens
                    output_tokens = response.usage.completion_tokens
                    self.total_input_tokens += input_tokens
                    self.total_output_tokens += output_tokens
                    self.total_requests += 1
                    
                    logger.debug(f"Request {self.total_requests}: {input_tokens} input + {output_tokens} output tokens")
                
                result = response.choices[0].message.content.strip()
                
                # Validate response
                if result in ['0', '1', '2']:
                    return int(result)
                else:
                    logger.warning(f"Invalid response: '{result}' for text: '{text[:50]}...'")
                    
            except RateLimitError as e:
                # Handle 429 errors specifically with exponential backoff
                if attempt == max_retries - 1:
                    logger.error(f"Rate limit exceeded after {max_retries} attempts for text: '{text[:50]}...'")
                    break
                
                # Extract retry-after from error message or use exponential backoff
                retry_after = self._extract_retry_after(str(e))
                if retry_after:
                    wait_time = retry_after
                    logger.warning(f"Rate limit hit, waiting {wait_time}s as suggested by API")
                else:
                    # Exponential backoff with jitter: 2^attempt + random(0, 1)
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(f"Rate limit hit, using exponential backoff: {wait_time:.2f}s")
                
                time.sleep(wait_time)
                logger.info(f"Retrying attempt {attempt + 2} after rate limit")
                
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    logger.error(f"All {max_retries} attempts failed for text: '{text[:50]}...'")
                else:
                    # Brief wait for other errors to avoid hammering the API
                    time.sleep(0.5)
        
        return None

    def embed_text(self, texts: List[str], max_retries: int = 3) -> Optional[List[List[float]]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of texts to embed
            max_retries: Maximum number of retry attempts
            
        Returns:
            List of embeddings, each as a list of floats, or None if failed
        """
        embeddings = []
        for text in texts:
            for attempt in range(max_retries):
                try:
                    response = self.client.embeddings.create(
                        model=self.embedding_deployment_name,
                        input=text
                    )
                    
                    # Track token usage
                    if hasattr(response, 'usage') and response.usage:
                        input_tokens = response.usage.prompt_tokens
                        self.total_input_tokens += input_tokens
                        self.total_requests += 1
                        
                        logger.debug(f"Request {self.total_requests}: {input_tokens} input tokens")
                    
                    embedding = response.data[0].embedding
                    embeddings.append(embedding)
                    break  # Success, exit retry loop
                
                except RateLimitError as e:
                    # Handle 429 errors specifically with exponential backoff
                    if attempt == max_retries - 1:
                        logger.error(f"Rate limit exceeded after {max_retries} attempts for text: '{text[:50]}...'")
                        embeddings.append(None)  # Append None for this text
                        break
                    
                    # Extract retry-after from error message or use exponential backoff
                    retry_after = self._extract_retry_after(str(e))
                    if retry_after:
                        wait_time = retry_after
                        logger.warning(f"Rate limit hit, waiting {wait_time}s as suggested by API")
                    else:
                        # Exponential backoff with jitter: 2^attempt + random(0, 1)
                        wait_time = (2 ** attempt) + random.uniform(0, 1)
                        logger.warning(f"Rate limit hit, using exponential backoff: {wait_time:.2f}s")
                    
                    time.sleep(wait_time)
                    logger.info(f"Retrying attempt {attempt + 2} after rate limit")
                
                except Exception as e:
                    logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                    if attempt == max_retries - 1:
                        logger.error(f"All {max_retries} attempts failed for text: '{text[:50]}...'")
                        embeddings.append(None)  # Append None for this text
                    else:
                        # Brief wait for other errors to avoid hammering the API
                        time.sleep(0.5)
        
        return embeddings

    def _extract_retry_after(self, error_message: str) -> Optional[float]:
        """
        Extract retry-after value from error message.
        
        Args:
            error_message: The error message string
            
        Returns:
            Retry-after time in seconds, or None if not found
        """
        try:
            # Look for "retry after X seconds" pattern in error message
            import re
            pattern = r'retry after (\d+\.?\d*) seconds?'
            match = re.search(pattern, error_message.lower())
            if match:
                return float(match.group(1))
        except Exception:
            pass
        return None

    def get_token_usage(self) -> dict:
        """
        Get current token usage statistics.
        
        Returns:
            Dictionary with token usage information
        """
        return {
            'total_input_tokens': self.total_input_tokens,
            'total_output_tokens': self.total_output_tokens,
            'total_tokens': self.total_input_tokens + self.total_output_tokens,
            'total_requests': self.total_requests
        }
    
    def reset_token_usage(self):
        """Reset token usage counters."""
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_requests = 0
