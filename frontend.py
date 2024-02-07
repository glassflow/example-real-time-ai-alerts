import streamlit as st
from pynats import NATSClient

st.title('Real-time Weather Alert Chat')


# Function to handle messages received from NATS
def read_message_from_nats_handler(msg):
    message = msg.payload.decode()
    st.session_state['conversation'].append(("AI", message))
    st.markdown(f"<span style='color: red;'>🔔</span> AI: {message}", unsafe_allow_html=True)


# Function to send messages to NATS
def send_message_to_nats_handler(message):
    with NATSClient() as client:
        client.connect()
        client.publish("chat", payload=message.encode())
        client.subscribe("chat_response", callback=read_message_from_nats_handler)
        client.wait()


# Store conversation history
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []

# Initialize alert set state
if 'alert_set' not in st.session_state:
    st.session_state['alert_set'] = False

# Weather alert criteria input
alert_criteria = st.text_input("Set your weather alert criteria", key="alert_criteria", disabled=st.session_state['alert_set'])
set_alert_btn = st.button('Set Weather Alert', disabled=st.session_state['alert_set'])

# Set Weather Alert button
if set_alert_btn:
    st.session_state['alert_set'] = True
    st.success('Alert criteria set')
    send_message_to_nats_handler(f"Set Alert: {alert_criteria}")

# Display conversation history
for author, message in st.session_state['conversation']:
    st.text(f"{author}: {message}")
