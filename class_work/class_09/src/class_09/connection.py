from agents import AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
import os 
from dotenv import load_dotenv

load_dotenv()

gemini_model = "gemini-2.0-flash"
baseUrl = "https://generativelanguage.googleapis.com/v1beta/openai/"


GEMINI_API_KRY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KRY:
    raise ValueError("Api Key is not set properly")


external_client = AsyncOpenAI(
    api_key=GEMINI_API_KRY,
    base_url= baseUrl,
)

model = OpenAIChatCompletionsModel(
    model = gemini_model,
    openai_client=external_client,
)


config = RunConfig(
    model = model,
    model_provider=external_client,
)
