from agents import Agent, RunContextWrapper, Runner, trace
from pydantic import BaseModel
import asyncio
from connection import config, model


class TravelPlanningAssistant(BaseModel):
    trip_type: str
    traveler_profile: str


travel_planning = TravelPlanningAssistant(
    trip_type="Adventure",
    traveler_profile="Solo",
    # trip_type="Cultural",
    # traveler_profile="Family",
    # trip_type="Business",
    # traveler_profile="Executive",
)


async def dynamic_instructions(ctx: RunContextWrapper[TravelPlanningAssistant], agent: Agent):
    # Case 1: Adventure + Solo
    if ctx.context.trip_type == "Adventure" and ctx.context.traveler_profile == "Solo":
        return """You are a Travel Planning Assistant.
        Suggest exciting adventure activities in the chosen location.
        Include safety tips for solo travelers.
        Recommend social hostels and group tours to help them meet people."""

    # Case 2: Cultural + Family
    elif ctx.context.trip_type == "Cultural" and ctx.context.traveler_profile == "Family":
        return """You are a Travel Planning Assistant.
        Focus on cultural and educational attractions.
        Recommend kid-friendly museums, interactive experiences, and safe family accommodations."""

    # Case 3: Business + Executive
    elif ctx.context.trip_type == "Business" and ctx.context.traveler_profile == "Executive":
        return """You are a Travel Planning Assistant.
        Emphasize business efficiency and convenience.
        Suggest hotels near airports, business centers with reliable WiFi, and premium lounges for executives."""


travel_agent = Agent(
    name="Travel Planning Assistant",
    instructions=dynamic_instructions,
    model=model,
)


async def main():
    with trace("Learn Dynamic Instructions for Travel Planning Assistant"):
        result = await Runner.run(
            travel_agent,
            "Plan my trip recommendations.",
            run_config=config,
            context=travel_planning,
        )
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
