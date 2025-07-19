from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os
import chainlit as cl

# .env file se environment variables load kiye ja rahe hain
load_dotenv()


# GEMINI_API_KEY environment variable se API key hasil ki ja rahi hai
gemini_api_key = os.getenv("GEMINI_API_KEY")


# Agar GEMINI_API_KEY set nahi hai to error raise karo
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Gemini API ko OpenAI-compatible tarike se use karne ke liye external client banaya gaya hai
# Gemini ka OpenAI compatible endpoint diya gaya hai
external_client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Gemini model ko define kiya gaya hai jise OpenAI ke format mein use kiya ja sakta hai
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",  # Gemini ka specific model
    openai_client= external_client  # Upar banaya gaya Gemini client
)

# Model run karne ka configuration set kiya gaya hai
config = RunConfig(
    model=  model, # Model jo upar define kiya gaya hai
    model_provider = external_client, # Yeh batata hai kaun sa provider hai
    tracing_disabled= True     # Tracing disable ki gayi hai
)


translator_agent = Agent(
    name="TargetedTranslator",
    instructions= """
    You are a smart translator.

The user will input a sentence in this format:
"Convert in <target-language>: <sentence>"

Your task:
- Detect the target language from the command: "Convert in Urdu", "Convert in English", or "Convert in Roman Urdu".
- Translate only the sentence portion into the **target language**.
- Reply ONLY with the translation.
- Do NOT label the output. Just return the final translated sentence.
   """
)



@cl.on_message
async def main(message: cl.Message):
    user_input = message.content # User ka message hasil karo
    
    
    # User ke input ko agent ke zariye process karo
    response = await Runner.run(
        translator_agent,  # Translator agent
        input=user_input,  # User ka diya gaya input
        run_config=config  # Configuration jo upar define ki gayi
    )
    
    # Final output ko user ko wapas bhejo Chainlit UI mein
    
    await cl.Message(
        content = response.final_output
    ).send()


