import streamlit as st
from dotenv import load_dotenv
import os
import glassflow
import requests
import time

load_dotenv()
personal_access_token = os.getenv("GLASSFLOW_PERSONAL_ACCESS_TOKEN")
weather_api_key = os.getenv("WEATHER_API_KEY")
pipeline_id = os.getenv("GLASSFLOW_PIPELINE_ID")
# Initialize GlassFlow client
client = glassflow.GlassFlowClient(personal_access_token=personal_access_token)
pipeline = client.get_pipeline(pipeline_id)
print(f'Pipeline "{pipeline.name}" with ID: {pipeline.id}')
data_source = pipeline.get_source()
data_sink = pipeline.get_sink()
# Streamlit UI
st.title("Real-time Weather Alert Chat")
if "conversation" not in st.session_state:
    st.session_state["conversation"] = []
if "alert_set" not in st.session_state:
    st.session_state["alert_set"] = False
# Weather alert criteria input
alert_criteria = st.text_input(
    "Set your weather alert criteria",
    key="alert_criteria",
    disabled=st.session_state["alert_set"],
)
set_alert_btn = st.button("Set Weather Alert", disabled=st.session_state["alert_set"])


# Function to fetch current weather data
def fetch_weather_data():
    api_url = (
        f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q=estonia"
    )
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching weather data: HTTP {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        return None


# Display the conversation history
def display_conversation():
    for role, message in st.session_state["conversation"]:
        if role == "AI":
            st.markdown(
                f"<span style='color: red;'>🔔</span> AI: {message}",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(f"You: {message}")


if set_alert_btn:
    st.session_state["alert_set"] = True
    st.success("Alert criteria set")
    st.session_state["conversation"].append(("You", f"Set Alert: {alert_criteria}"))
# Fetch weather data and send to the pipeline periodically
if alert_criteria:
    weather_data = fetch_weather_data()
    if weather_data:
        data_to_publish = {"criteria": alert_criteria, "weather": weather_data}
        data_source.publish(data_to_publish)
        st.success("Weather data and criteria sent to the pipeline.")
# Continuously consume transformed data from the pipeline
while True:
    try:
        resp = data_sink.consume()
        if resp.status_code == 200:
            response = resp.json()
            alert_message = response.get("alert", "No alert message received")
            st.session_state["conversation"].append(("AI", alert_message))
            display_conversation()
        elif resp.status_code == 204:
            time.sleep(2)  # Polling interval for new messages
        else:
            st.error(f"Failed to consume data: {resp.status_code}")
            time.sleep(2)  # Retry interval for failures
    except Exception as e:
        st.error(f"Error consuming data: {e}")
        time.sleep(2)
