# This script creates a chatbot that uses multiple AI models to answer questions.
# It asks several "worker" models for answers, then uses a "judge" model to combine them into one final response.
# This helps get better, more balanced answers by comparing different AI perspectives.
#
# How it works:
# 1. User asks a question
# 2. Multiple AI models (workers) each provide their own answer
# 3. A final AI model (judge) reviews all answers and creates the best combined response
# 4. The final answer is presented to the user
#
# Requirements:
# - OPENROUTER_API_KEY environment variable (or in .env file)
# - Python packages: openai, python-dotenv

import os

# Import dotenv to load environment variables from .env file
from dotenv import load_dotenv
# Import OpenAI client (works with OpenRouter's compatible API)
from openai import OpenAI

# Load environment variables from .env file if it exists
load_dotenv()

# Get the API key from environment variables
# This key is required to access OpenRouter's API
api_key = os.getenv("OPENROUTER_API_KEY")

# Check if the API key was found
if not api_key:
    raise ValueError(
        "Missing OPENROUTER_API_KEY. Add it to your environment or a .env file."
    )

# 1. Initialize OpenRouter client
# OpenRouter is a service that lets you access many different AI models through one API.
# We use the OpenAI client library because OpenRouter's API is compatible with OpenAI's format.
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# Define the models you want to use
# Note: Ensure these model strings are currently available on OpenRouter
# These are the "worker" models - each one will give an answer to your question.
# We're using a mix of different models from various providers for diverse perspectives.
worker_models = [
    "openrouter/elephant-alpha",  # A creative and helpful AI model
    "minimax/minimax-m2.5:free",  # A fast, free model from Minimax
    "google/gemma-4-31b-it:free"  # Google's Gemma model, good at reasoning
]

# The model that will synthesize the final answer
# This is the "judge" model - it reviews all the worker answers and creates the best final response.
# It needs to be good at analysis and synthesis to combine multiple viewpoints effectively.
judge_model = "arcee-ai/trinity-large-preview:free" 

print("Multi-Model Chatbot started! (Type 'quit' to stop)")

# Main chat loop - keeps running until you type 'quit'
while True:
    # Get input from the user
    user_input = input("\nYou: ")
    
    # Check if the user wants to stop the conversation
    if user_input.lower() in ["quit", "exit"]:
        break

    # List to store responses from each worker model
    # This will hold all the individual answers before combining them
    worker_responses = []

    # 2. Collect answers from all worker models
    print("Consulting the experts...")
    
    # Loop through each worker model and ask for an answer
    # This parallel consultation gives us diverse perspectives
    for model_id in worker_models:
        try:
            print(f" -> Querying {model_id}...")
            
            # Send the user's question to this model via the API
            # Using OpenAI's chat completions format (compatible with OpenRouter)
            response = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": user_input}]
            )
            
            # Extract the actual answer text from the API response
            ans = response.choices[0].message.content
            
            # Add the answer to our list, labeled with the model name for clarity
            worker_responses.append(f"Model ({model_id}):\n{ans}")
            
        except Exception as e:
            # If something goes wrong (like network issues or model unavailable)
            # Print the error but continue with other models
            print(f"Error calling {model_id}: {e}")

    # 3. Combine the answers into a single string for the "Judge"
    # Join all worker responses with separators for easy reading
    # This creates a comprehensive context for the judge model
    combined_context = "\n\n---\n\n".join(worker_responses)
    
    # Create a prompt for the judge model that includes the user's question and all worker answers
    # This prompt instructs the judge to analyze, compare, and synthesize the best answer
    final_prompt = f"""
    A user asked: "{user_input}"
    
    I have gathered responses from {len(worker_responses)} different AI models. 
    Your task is to compare these answers, resolve any contradictions, and provide the most accurate, 
    comprehensive final response.

    HERE ARE THE RESPONSES:
    {combined_context}
    
    FINAL ACCURATE ANSWER:
    """

    # 4. Call the final "Judge" model to process everything
    print("Finalizing answer...")
    
    # Send the combined prompt to the judge model
    # The judge model will analyze all worker responses and create a unified answer
    final_call = client.chat.completions.create(
        model=judge_model,
        messages=[{"role": "user", "content": final_prompt}]
    )

    # Get the final answer from the judge model
    final_answer = final_call.choices[0].message.content
    
    # Print the final answer with nice formatting
    # Use separators to make it clear this is the final result
    print("-" * 30)
    print(f"AI FINAL ANSWER:\n{final_answer}")
    print("-" * 30)
    print("-" * 30)
    print(f"AI FINAL ANSWER:\n{final_answer}")
    print("-" * 30)
