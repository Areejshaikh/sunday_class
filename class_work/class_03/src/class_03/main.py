from agents import Agent, Runner, function_tool
from connection import config

@function_tool
def usd_to_pkr():
    return 'Today usd to pkr is Rs 280'

@function_tool
def weather ():
    return 'Today weather is 30 degree celsius with 10% humidity and 5% wind speed'

@function_tool
def time():
    return 'Current time is 3:00 PM'

# @function_tool
# def psx_index():
#     return 'Today usd to pkr is Rs 280'

agent = Agent(
    name = 'Current Data',
    instructions = 
    """
        You are an helpful assistant. Your task is to
        help user with its queries.
    """,
    tools = [usd_to_pkr, weather, time],
)


# result = Runner.run_sync(agent, 
#                          'Who is the founder of Pakistan',
#                          run_config=config
#
#                           )
result = Runner.run_sync(agent, 
                         'What"s the weather and the time now?',
                         run_config=config
)

# result = Runner.run_sync(agent, 
#                          'Who are the top 10 who acheive A Grade students from Sunday Afternoon',
#                          run_config=config
# )
print(result.final_output)