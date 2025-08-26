import rich 
import asyncio
from connection import config
from pydantic import BaseModel 
from agents import (
    Agent, OutputGuardrailTripwireTriggered, Runner,
    input_guardrail, GuardrailFunctionOutput,
    output_guardrail, InputGuardrailTripwireTriggered
)

# Model jo AC ka temperature check karega
class FatherGuardrailOutput(BaseModel):
    response: str
    isTemperatureHigh: bool

# AC Security Guard Agent
father_guardrail_agent = Agent(
    name="Fan speed guardrail",
    instructions="""
        Your task is to check the AC temperature.
        If temperature is greater than 26C, gracefully stop them.
    """,
    output_type=FatherGuardrailOutput
)

# Input Guardrail Function
@input_guardrail
async def security_guardrail(ctx, agent, input_text):
    result = await Runner.run(father_guardrail_agent, input_text, run_config=config)
    rich.print(result.final_output)

    return GuardrailFunctionOutput(
        output_info=result.final_output.response,
        tripwire_triggered=result.final_output.isTemperatureHigh
    )

# Main Agent
child_agent = Agent(
    name="child",
    instructions="You are a child agent",
    input_guardrails=[security_guardrail]
) 

async def main():
    try: 
        result = await Runner.run(
            child_agent,
            "The AC temperature is 23C.",
            run_config=config
        )
        print("Ac temperature is not above 26 okay")
    except InputGuardrailTripwireTriggered:
        print('Son cannot use the AC because temperature is too high!')

if __name__ == "__main__":
    asyncio.run(main())
