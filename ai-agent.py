from openai import OpenAI

# 1. Initialize OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="your-openrouter-key-here", 
)

# Define the models you want to use
# Note: Ensure these model strings are currently available on OpenRouter
worker_models = [
    "openrouter/elephant-alpha",
    "minimax/minimax-m2.5:free",
    "google/gemma-4-31b-it:free"
]

# The model that will synthesize the final answer
judge_model = "arcee-ai/trinity-large-preview:free" 

print("Multi-Model Chatbot started! (Type 'quit' to stop)")

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ["quit", "exit"]:
        break

    worker_responses = []

    # 2. Collect answers from all worker models
    print("Consulting the experts...")
    for model_id in worker_models:
        try:
            print(f" -> Querying {model_id}...")
            response = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": user_input}]
            )
            ans = response.choices[0].message.content
            worker_responses.append(f"Model ({model_id}):\n{ans}")
        except Exception as e:
            print(f"Error calling {model_id}: {e}")

    # 3. Combine the answers into a single string for the "Judge"
    combined_context = "\n\n---\n\n".join(worker_responses)
    
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
    final_call = client.chat.completions.create(
        model=judge_model,
        messages=[{"role": "user", "content": final_prompt}]
    )

    final_answer = final_call.choices[0].message.content
    
    print("-" * 30)
    print(f"AI FINAL ANSWER:\n{final_answer}")
    print("-" * 30)