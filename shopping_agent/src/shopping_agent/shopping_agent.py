import os
import requests
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, Runner, RunConfig
import chainlit as cl

# Load .env file
load_dotenv()

# Get Gemini API Key from .env
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Gemini external client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Gemini 2.0 Flash model setup
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# RunConfig for the agent
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Tool to fetch product info from API
@function_tool
def fetch_product_info(query: str) -> str:
    """Search products from API and return markdown-formatted results with images."""
    url = "https://template6-six.vercel.app/api/products"
    response = requests.get(url)
    
    if response.status_code != 200:
        return "⚠️ Failed to fetch products from API."

    products = response.json()

    matching = [p for p in products if query.lower() in p['title'].lower()]

    if not matching:
        return "❌ No products found."

    # Generate markdown response
    markdown_result = ""
    for product in matching:
        markdown_result += f"""
### 🛍️ {product['title']}

![Image]({product['image']})

💰 **Price:** {product['price']}  
📝 **Description:** {product['description']}

---
"""

    return markdown_result

# Create the agent
agent = Agent(
    name="ShoppingAssistant",
    instructions="You are a smart Shopping Assistant. Help users find products from the available API based on their query.",
    tools=[fetch_product_info],
)

# Chainlit message handler
@cl.on_message
async def main(message: cl.Message):
    result = await Runner.run(
        agent,
        input=message.content,
        run_config=config
    )

    await cl.Message(content=result.final_output).send()
