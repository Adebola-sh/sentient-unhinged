import os
from dotenv import load_dotenv
from funcs import receive_input
from openai import OpenAI




load_dotenv()
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
    
)

completion = client.chat.completions.create(
    model="SentientAGI/Dobby-Mini-Unhinged-Plus-Llama-3.1-8B:featherless-ai",
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
)

print(completion.choices)

