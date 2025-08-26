from agents import Agent , RunContextWrapper, Runner ,  function_tool, trace
from pydantic import BaseModel
from connection import config , model 
import asyncio
import rich
from dotenv import load_dotenv
load_dotenv()

# ______________Example of local context ____________-

# class CartItems(BaseModel):
#     product: list
#     user_id: str
#     brand:str
#     total_amount:int
    

# cart = CartItems(
#     product=["Mobail" ,"laptop"],
#     user_id="923001234567",
#     brand="apple",
#     total_amount=342398
#     )

# @function_tool 
# def products_info(wrapper: RunContextWrapper[CartItems]):
#     print('checking context ', wrapper.context.user_id)
#     return {
#          "user_id": wrapper.context.user_id,
#         "product": wrapper.context.product,
#         "brand": wrapper.context.brand,
#         "total_amount": wrapper.context.total_amount
#     }

# persnol_agent = Agent(
#     name= "assisten",
#     model= model,
#     instructions="""You are a helpful shopping assistant.
#     If the user asks anything about the cart (like user_id, brand, products, or total_amount),
#     you MUST call the tool `products_info` to get the answer. 
#     Never answer from your own knowledge.""",
#     tools=[products_info],
# )

# async def main():
#     with trace("Learn Dynamic Instructions"):
#         result = await Runner.run(
#             starting_agent=persnol_agent,
#             input= "tell me user_id.",
#             run_config=config,
#             context=cart,
#         )
#         print(result.final_output)
    
# if __name__ == "__main__":
#     asyncio.run(main())



# *************************Dyamic Insturctions**************************************
# First we define a Person class to hold user information
class Person(BaseModel):
    name: str
    user_level: str
    
# Then we create an instance of Person with specific details
personOne = Person(
    name="Alice",
    user_level="PHD"
    )
# We define a tool that provides user information when called
async def my_dynamic_instruction(ctx: RunContextWrapper[Person] , agent: Agent):
    
    if ctx.context.user_level == 'junior':
        return """Keep Your answers simple and easy to understande."""
    elif ctx.context.user_level == "intermediate":
        return """Keep you vocabulary medium and not very hard."""
    elif ctx.context.user_level == "PHD":
        return """Keep you vocabulary advanced and very hard like your are talking to a PHD level peron."""
    
    
    
    # now we create an agent with dynamic instructions based on the user's level
personal_agent = Agent(
        name = "Agent",
        instructions=my_dynamic_instruction,
        
    )
async def main():
    with trace("Learn Dynamic Instructions1"):
        result = await Runner.run(
            personal_agent, 
            'What is light?',
            run_config=config,
            context = personOne #Local context
            )
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())