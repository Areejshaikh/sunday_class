from connection import config, model
from agents import Agent, Runner, RunContextWrapper, trace
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio

load_dotenv()


class AirlineSeatPreferenceAgentClass(BaseModel):
    name: str
    seat_preference: str
    travel_experience: str


airline_assistant_instance = AirlineSeatPreferenceAgentClass(
    seat_preference="window",
    travel_experience="first_time",
    # seat_preference="middle",
    # travel_experience="frequent",
    # seat_preference="any",
    # travel_experience="premium",
)


async def dynamic_instruction_to_airline(
    ctx: RunContextWrapper[AirlineSeatPreferenceAgentClass], agent: Agent
):
    # Case 1: Window + First-time
    if ctx.context.seat_preference == "window" and ctx.context.travel_experience == "first_time":
        return """You are an airline seat preference assistant. 
        Highlight the benefits of a window seat, such as scenic views and a sense of privacy. 
        Reassure the passenger since this is their first flight, making the experience more comfortable and less stressful."""

    # Case 2: Middle + Frequent
    elif ctx.context.seat_preference == "middle" and ctx.context.travel_experience == "frequent":
        return """You are an airline seat preference assistant. 
        Acknowledge that middle seats are less preferred. 
        Suggest strategies such as requesting aisle swaps, early check-in, or using frequent flyer points to upgrade. 
        Provide alternatives like choosing exit-row or extra-legroom options."""

    # Case 3: Any + Premium
    elif ctx.context.seat_preference == "any" and ctx.context.travel_experience == "premium":
        return """You are an airline seat preference assistant. 
        Highlight premium travel benefits such as luxury seating, complimentary upgrades, and priority boarding. 
        Emphasize comfort, exclusivity, and special services available for premium travelers."""


airline_agent = Agent(
    name="Airline Seat Preference Agent",
    instructions=dynamic_instruction_to_airline,
    model=model,
)


async def main():
    with trace("Learn Dynamic Instructions for Airline Assistant"):
        result = await Runner.run(
            airline_agent,
            "Book my seat.",
            run_config=config,
            context=airline_assistant_instance,
        )
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
