import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv() 

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

completion = client.chat.completions.create(
    model="moonshotai/Kimi-K2-Instruct-0905",
    messages=[
        {
            "role": "user",
            "content": "You are local to my machine?"
        }
    ],
)

print(completion.choices[0].message)
# ChatCompletionMessage(content="No, I'm not local to your machine. I run on servers operated by Moonshot AI, and our conversation happens over the internet. I don't have access to your device or files unless you explicitly share them with me.", refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=None)