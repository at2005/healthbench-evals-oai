#!/usr/bin/env python
"""
Simple test script to demonstrate using AISDKSampler with gpt-4.1
"""

from sampler.ai_sdk_sampler import AISDKSampler

def main():
    # Create an instance of AISDKSampler with model set to gpt-4.1
    sampler = AISDKSampler(
        model="auto",
        temperature=0.7,
        max_tokens=1024
    )
    
    # Create a simple message list
    # The format follows the _pack_message method that takes role and content
    message_list = [
        {"role": "user", "content": "Hello, how are you today?"}
    ]
    
    # Call the sampler with the message list
    response = sampler(message_list)
    
    # Print the response
    print("\nResponse text:")
    print(response.response_text)
    
    # Print metadata (like token usage)
    print("\nMetadata:")
    print(response.response_metadata)

if __name__ == "__main__":
    main() 