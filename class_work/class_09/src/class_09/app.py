from connection import config
from agents import Agent, RunContextWrapper , Runner , function_tool
import asyncio
import rich
from pydantic import BaseModel


class Users_Data_info(BaseModel):
    name: str
    userId: int| str
    user_mobail : int
    
    
user_info = Users_Data_info(name="Areej", userId=123233, user_mobail=12345677)

    
@function_tool
async def  user_data (wrapper:RunContextWrapper[Users_Data_info]):
    """You are travel agent tool"""
    print(wrapper.context)
    return f' the user info ${wrapper.context}'



travel_agent = Agent(
    name = "Travel Agent",
    instructions="You are a travel agent help user for booking if need to call tool user_data",
    tools=[user_data],
)


async def main():
    result= await Runner.run(
        travel_agent,
        "what is my name?",
        run_config=config,
        context=user_info
    )
    print(result.final_output)
    rich.print("Input Guardrail result output",result.context_wrapper)
    
if __name__ == "__main__":
    asyncio.run(main())
