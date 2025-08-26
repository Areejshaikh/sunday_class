# bank_account = BankAccount(
#     account_number="ACC-789456",
#     customer_name="Fatima Khan",
#     account_balance=75500.50,
#     account_type="savings"
# )

import asyncio
from connection import config
from agents import (
    Agent,
    RunContextWrapper,
    Runner,
    function_tool
)
from pydantic import BaseModel
import rich

class BankAccount(BaseModel):
    account_number: str
    customer_name: str
    account_balance:int
    account_type: str
    
bank_account = BankAccount(
    account_number="ACC-789456",
    customer_name="Fatima Khan",
    account_balance=75500,
    account_type="savings"
)

@function_tool
def context_bank_data(wrapper: RunContextWrapper[BankAccount]):
    return f"The Bank Info is  Here: {wrapper.context}"


bank_agent= Agent(
    name= "Baking Agent",
    instructions = "You are a helpful assistant, always call the tool to get bank information",
    tools= [context_bank_data]
)
    
async def main():
    result = await Runner.run(
        bank_agent, 
        # 'What is the user id', 
        'What is my account number and also tell me my customer name', 
        run_config=config,
        context = bank_account #Local context
        )
    rich.print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())