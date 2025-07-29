from typing import cast
from agents import Agent, Runner
import asyncio
from connection import config
import chainlit as cl

@cl.on_chat_start
async def main():

    cl.user_session.set("chat_history", [])

    Lyric_poetry = Agent (
        name="Lyric_poetry",
        instructions="You are poetry agent that generates lyrics based on a given theme or mood and user specific language.",
    )
    narrative_poetry = Agent(
        name="narrative_poetry",
        instructions="you are poetry agent that creates narrative poems, telling a story through verse and user specific language.",
    )

    Dramatic_poetry = Agent(
        name="Dramatic_poetry",
        instructions="you are  poetry agent that writes dramatic poems, often with a focus on dialogue and character and  user specific language.",
    )
    orchestrator_agent = Agent(
        name="Orchestrator_agent",
        instructions="""
        You are an orchestrator agent responsible for managing the flow of tasks and coordinating between poetry agents. When the user requests a specific type of poetry—such as Lyric, Narrative, or Dramatic—you should hand off the request to the corresponding agent. If the user mentions a specific agent by name, respond with a poem from only that agent. Route the request accurately based on the user’s intent. 
        If the user does not specify a type, choose the most appropriate agent based on the context of the request.
        and the most important thing is to use user specific language.""",
        handoffs=[Lyric_poetry, narrative_poetry, Dramatic_poetry],
    )

    # Step 6: Save agent in session
    cl.user_session.set("agent" ,orchestrator_agent)
    await cl.Message(content="""
                        Agents that can write poems for you.
                        - Lyric poem
                        - Narrative poem 
                        - Dramatic poem 
                            If you don't specify a type, I will choose the best agent for you
                     """).send()

@cl.on_message
async def orchestrator(message:cl.Message):
        
    orchestrator_agent:Agent =  cast(Agent, cl.user_session.get("agent"))
    history = cl.user_session.get("chat_history", [])
        
    history.append({"role":"user" ,"content":message.content})
    
    


        
        # Step 3: Thinking Message
    thinking = await cl.Message(content="🔍 Generating a poem...").send()
    try:
        result = await Runner.run(
        orchestrator_agent,
        input=history,
        # input="Write a poem about the beauty of nature narrative poem.",
        run_config=config,
        )
            
            
        # Step 5: Show response 
        responce_content = result.final_output
        thinking.content = str(responce_content)
        await thinking.update()
        
        cl.user_session.set("chat_history",result.to_input_list())
            
            
    except Exception as e:
        thinking.content = f"❌ Error: {str(e)}"
        await thinking.update()
        print(f"❌ Error: {str(e)}")
        
        
        
        
        # print(result.final_output)
        # asyncio.run(orchestrator())

    