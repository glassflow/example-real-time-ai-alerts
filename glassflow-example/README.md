# Real-Time Weather Alert Chat with AI


In this guide, you will learn how to build a real-time weather alert chat application using [GlassFlow SDK](https://github.com/glassflow/glassflow-examples) and Streamlit.

## Features
This AI-powered alerting has following features:

- Continuously monitoring weather conditions.
- Allowing users to define custom alert criteria in natural language.
- Providing personalized, real-time alerts when conditions are met.

![How the alert app works demo](/assets/Real-time%20Weather%20Alert%20Chat%20(1).gif)

## Installation

### Pre-requisites

- Create your free GlassFlow account via the [GlassFlow WebApp](https://app.glassflow.dev).
- Get your [Personal Access Token](https://app.glassflow.dev/profile) to authorize the Python SDK to interact with GlassFlow Cloud.
- OpenAI API Key: Sign up at [OpenAI](https://platform.openai.com/) and get an API key.
- WeatherAPI Key: Sign up at [WeatherAPI](https://www.weatherapi.com/) to fetch weather data.

### Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/glassflow/example-real-time-ai-alerts.git
cd example-real-time-ai-alerts
```

### Set Up Python Environment

It's recommended to use a virtual environment for Python projects. Create and activate one using:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Python Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory of the project and add your OpenAI and [Weather API](https://api.weatherapi.com/) keys:

```
GLASSFLOW_PERSONAL_ACCESS_TOKEN=your_glassflow_access_token
OPENAI_API_KEY=your_openai_api_key
WEATHER_API_KEY=your_weather_api_key
```

Replace `your_openai_api_key` and `your_weather_api_key` with your actual API keys.Before running the application, ensure that the environment variables are set. If you're using a virtual environment, you can load them manually:

## Running the Application

### Create a GlassFlow pipeline

Creates a new Space and Pipeline and returns Pipeline ID in the console:

```bash
python create_pipeline.py
```

Output:

```text
Pipeline is deployed!
Pipeline Id = 08420372-02f5-4d06-b2b5-330382474c77
Pipeline URL https://app.glassflow.dev/pipelines/08420372-02f5-4d06-b2b5-330382474c77 
```

### Update Pipeline ID in the .env file

```bash
GLASSFLOW_PIPELINE_ID=your_new_pipeline_id
```

### Start the Streamlit Frontend

Launch the Streamlit weather alert application:

```bash

streamlit run alert_streamlit_app.py
```

## Testing the Application

1. **Interact with the Chat**: Open the Streamlit app in your web browser and try sending messages or asking questions.
2. **Set Weather Alerts**: Use the interface to set custom weather alerts and see how the application responds.

## Shutting Down

To stop the application:

1. Close the Streamlit app.
2. Terminate the backend script (`Ctrl+C` in the terminal).

## Contributing

Contributions to this project are welcome! Please fork the repository and submit a pull request with your changes.
