import os
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, Runner
import requests
import chainlit as cl
from typing import cast

load_dotenv()

# Get API Key
api_key = os.getenv("GEMINI_API_KEY")  # ✅ Must match .env key

@cl.on_chat_start
async def main():
    # Step 1: Create external client
    external_client = AsyncOpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",  # ✅ For Gemini-compatible endpoint
    )

    # Step 2: Create model
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    # Step 3: Initialize chat history
    cl.user_session.set("chat_history", [])

    # Step 4: Define your tool
    @function_tool
    def fetch_product_info(query: str) -> list:
        """Search products from API based on user query."""
        url = "https://template6-six.vercel.app/api/products"
        response = requests.get(url)
        products = response.json()

        # Match products
        matched =  [p for p in products if query.lower() in p['title'].lower()]
    
        if not matched:
            return "❌ No products found."

        result_md = "### 🔎 Matching Products:\n"
        for p in matched:
            result_md += f"**{p['title']}**\n\n"
            result_md += f"[Product Image]({p['imageUrl']})\n\n"
            result_md += f"**Price:** ${p['price']}\n\n"
            result_md += f"**Discount:**{p["dicountPercentage"]}\n\n"
            result_md += f"**Description:** {p['description']}\n\n"
            result_md += "---\n"
            

        return result_md

    # Step 5: Create Agent
    agent = Agent(
        name="ShoppingAssistant",
        instructions=
        "You are a smart Shopping Assistant. "
        "Help users find products with images, title, description, prices and also include all deatails using the provided API. "
        "If the user asks what products are available (e.g., 'aur kya kya products hain?'), "
        "fetch and list all products from the API using the fetch_product_info tool with an empty string ('') as query.",
        tools=[fetch_product_info],
        model=model
    )

    # Step 6: Save agent in session
    cl.user_session.set("agent", agent)

    # Step 7: Welcome Message
    await cl.Message(content="👋 Welcome! Ask me to find a Product.").send()


@cl.on_message
async def handle_message(message: cl.Message):
    # Step 1: Get agent & history
    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    history = cl.user_session.get("chat_history", [])

    # Step 2: Add user message
    history.append({"role": "user", "content": message.content})

    # Step 3: Thinking Message
    thinking = await cl.Message(content="🔍 Searching for matching products...").send()

    try:
        # Step 4: Run Agent
        result = await Runner.run(
            starting_agent=agent,
            input=history,
        )

        # Step 5: Show response
        response_content = result.final_output
        thinking.content = response_content
        await thinking.update()

        # Step 6: Save new history
        cl.user_session.set("chat_history", result.to_input_list())

        # Optional Logs
        print(f"User: {message.content}")
        print(f"Bot: {response_content}")

    except Exception as e:
        thinking.content = f"❌ Error: {str(e)}"
        await thinking.update()
        print(f"❌ Error: {str(e)}")
