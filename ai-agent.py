# This script creates a chatbot that uses multiple AI models to answer questions.
# It asks several "worker" models for answers, then uses a "judge" model to combine them into one final response.
# This helps get better, more balanced answers by comparing different AI perspectives.

from openai import OpenAI

# 1. Initialize OpenRouter client
# OpenRouter is a service that lets you access many different AI models through one API.
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="your-openrouter-key-here", 
)

# Define the models you want to use
# Note: Ensure these model strings are currently available on OpenRouter
# These are the "worker" models - each one will give an answer to your question.
worker_models = [
    "openrouter/elephant-alpha",
    "minimax/minimax-m2.5:free",
    "google/gemma-4-31b-it:free"
]

# The model that will synthesize the final answer
# This is the "judge" model - it reviews all the worker answers and creates the best final response.
judge_model = "arcee-ai/trinity-large-preview:free" 

print("Multi-Model Chatbot started! (Type 'quit' to stop)")

# Main chat loop - keeps running until you type 'quit'
while True:
    # Get input from the user
    user_input = input("\nYou: ")
    # Check if the user wants to stop
    if user_input.lower() in ["quit", "exit"]:
        break

    # List to store responses from each worker model
    worker_responses = []

    # 2. Collect answers from all worker models
    print("Consulting the experts...")
    # Loop through each worker model and ask for an answer
    for model_id in worker_models:
        try:
            print(f" -> Querying {model_id}...")
            # Send the user's question to this model via the API
            response = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": user_input}]
            )
            # Get the answer from the model's response
            ans = response.choices[0].message.content
            # Add the answer to our list, labeled with the model name
            worker_responses.append(f"Model ({model_id}):\n{ans}")
        except Exception as e:
            # If something goes wrong (like network issues), print the error but continue
            print(f"Error calling {model_id}: {e}")

    # 3. Combine the answers into a single string for the "Judge"
    # Join all worker responses with separators for easy reading
    combined_context = "\n\n---\n\n".join(worker_responses)
    
    # Create a prompt for the judge model that includes the user's question and all worker answers
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
    final_call = client.chat.completions.create(
        model=judge_model,
        messages=[{"role": "user", "content": final_prompt}]
    )

    # Get the final answer from the judge model
    final_answer = final_call.choices[0].message.content
    
    # Print the final answer with nice formatting
    print("-" * 30)
    print(f"AI FINAL ANSWER:\n{final_answer}")
    print("-" * 30)