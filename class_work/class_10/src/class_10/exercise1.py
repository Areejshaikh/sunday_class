from connection import config , model 
from agents  import Agent , Runner, RunContextWrapper,trace
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio
load_dotenv()

class medical_assistant_class(BaseModel):
    name : str
    roll: str
    

medical_assistant_instance = medical_assistant_class(
    name = "Medical Consultance Assistent",
    roll = "Patient",
    # roll = "Medical Student",
    # roll = "Doctor",
)

def dynamic_instruction_to_medical(ctx :RunContextWrapper[medical_assistant_class] , medical_agent: Agent):
    if ctx.context.roll == "Patient":
        return """You are a helpful medical assistant. 
        If the user is a patient, you must provide simple and easy-to-understand explanations.
        Avoid using complex medical jargon. 
        Always prioritize the patient's comfort and understanding in your responses."""
        
    elif ctx.context.roll == "Medical Student":
        return """You are a knowledgeable medical assistant. 
        If the user is a medical student, you should provide detailed explanations and include relevant medical terminology.
        Encourage critical thinking and provide additional resources for further study."""
    elif ctx.context.roll == "Doctor":
        return """You are an expert medical assistant. 
        If the user is a doctor, you should provide concise and precise information.
        Use appropriate medical terminology and focus on evidence-based practices.
        Support the doctor's expertise with up-to-date research and clinical guidelines."""
        
        
medical_agent = Agent(
    name = "Medical Agent",
    instructions = dynamic_instruction_to_medical,
)


async def main():
    with trace("Lern Dynamic Instructions for Medical Assistant"):
        result = await Runner.run(
            medical_agent,
            "explain about diabetes.",
            run_config=config,
            context=medical_assistant_instance,
            )
        print(result.final_output)
if __name__ == "__main__":
    asyncio.run(main())