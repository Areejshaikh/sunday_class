# student = StudentProfile(
#     student_id="STU-456",
#     student_name="Hassan Ahmed",
#     current_semester=4,
#     total_courses=5
# )

from agents import Agent, RunContextWrapper, Runner, function_tool
from pydantic import BaseModel
from connection import config


class StudentProfile(BaseModel):
    student_id : str
    student_name: str
    current_semester : int
    total_courses : int
    
    
student = StudentProfile(
    student_id="STU-456",
    student_name="Hassan Ahmed",
    current_semester=4,
    total_courses=5
)


@function_tool
def student_Profile_Tool(wrapper : RunContextWrapper[StudentProfile]):
    return f"This is a Student prfile informaton: {wrapper.context}"

def dynamic_instruction(ctx:RunContextWrapper[StudentProfile] , student_agent :Agent[StudentProfile])-> str:
    return f"The user's name is {ctx.context}Help them with their questions."

student_agent :Agent = Agent(
    name = "Assisten",
    instructions= dynamic_instruction,
    tools=[student_Profile_Tool],
)


result = Runner.run_sync(
    student_agent,
    "Tell me student id and Student name",
    run_config= config,
    context= student,
)
print(result.final_output)