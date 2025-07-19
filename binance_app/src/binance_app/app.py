import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig
import requests

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

@function_tool
async def binance_api(query: str) -> str:
    """Fetch current price from Binance for a given symbol like BTCUSDT."""
    try:
        response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={query}")
        if response.status_code == 200:
            data = response.json()
            return f"The current price of {query} is {data['price']} USD."
        else:
            return f"Failed to fetch price. Status code: {response.status_code}"
    except Exception as e:
        return f"Error occurred: {str(e)}"


agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=model,
    tools=[binance_api],
)

# Define an async main function
async def main():
    result = await Runner.run(
        agent,
        "What is the current price of Bitcoin in USD?",
        run_config=config
    )
    # print the final output of the agent
    print(result.final_output)

# Run the async function
asyncio.run(main())
