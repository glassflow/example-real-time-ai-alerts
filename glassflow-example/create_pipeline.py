from dotenv import load_dotenv
import os
import glassflow

# Load GlassFlow personal token and OpenAI API key from .env file
load_dotenv()
personal_access_token = os.getenv("GLASSFLOW_PERSONAL_ACCESS_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")
# Initialize GlassFlow client
client = glassflow.GlassFlowClient(personal_access_token=personal_access_token)
# Get the space named "examples" (or create one if no space is found)
list_spaces = client.list_spaces()
space_name = "examples"
for s in list_spaces.spaces:
    if s["name"] == space_name:
        space = glassflow.Space(
            personal_access_token=client.personal_access_token,
            id=s["id"],
            name=s["name"],
        )
        break
else:
    space = client.create_space(name=space_name)
print(f'Space "{space.name}" with ID: {space.id}')
pipeline_name = "real-time-alert-streamlit"
env_vars = [{"name": "OPENAI_API_KEY", "value": openai_api_key}]
requirements_txt = "openai"
pipeline = client.create_pipeline(
    name=pipeline_name,
    transformation_file="transform.py",
    space_id=space.id,
    env_vars=env_vars,
    requirements=requirements_txt,
)
print("Pipeline is deployed!")
print("Pipeline Id = %s" % (pipeline.id))
print("Pipeline URL %s " % f"https://app.glassflow.dev/pipelines/{pipeline.id}")
