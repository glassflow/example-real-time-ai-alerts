# AI Real-time Weather Alert Chat Application

This innovative solution combining real-time [weather](https://www.weatherapi.com/) monitoring with AI-powered interactions. This application uses [Streamlit](https://streamlit.io/) for the frontend, Python and [NATS](https://nats.io/) for the backend, and integrates [OpenAI's GPT](https://openai.com/api/) model for decision making, setting alerts and intelligent responses. Read more on this article:

https://learn.glassflow.dev/blog/usecases/revolutionizing-real-time-alerts-with-ai-nats-and-streamlit

![How the alert app works demo](/assets/Real-time%20Weather%20Alert%20Chat%20(1).gif)

## Installation

Before you begin, ensure you have [Python](https://www.python.org/downloads/) and [Docker](https://www.docker.com/products/docker-desktop/) installed on your system. This project requires Python 3.6 or later.

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

### Set Up NATS Server with Docker

Ensure Docker is running on your machine. Then, start the NATS server using Docker Compose:

```bash
docker compose up -d
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory of the project and add your OpenAI and [Weather API](https://api.weatherapi.com/) keys:

```
OPENAI_API_KEY=your_openai_api_key
WEATHER_API_KEY=your_weather_api_key
```

Replace `your_openai_api_key` and `your_weather_api_key` with your actual API keys.Before running the application, ensure that the environment variables are set. If you're using a virtual environment, you can load them manually:

## Running the Application

### Start the Backend

Run the backend server with:

```bash
python backend.py
```

### Start the Streamlit Frontend

In a new terminal, launch the Streamlit application:

```bash

streamlit run frontend.py
```

## Testing the Application

1. **Interact with the Chat**: Open the Streamlit app in your web browser and try sending messages or asking questions.
2. **Set Weather Alerts**: Use the interface to set custom weather alerts and see how the application responds.
3. **Monitor NATS Server**: Optionally, you can monitor the NATS server at `http://localhost:8222`.

## Shutting Down

To stop the application:

1. Close the Streamlit app.
2. Terminate the backend script (`Ctrl+C` in the terminal).
3. Stop the NATS server with Docker Compose:
    
    ```bash
    docker compose down
    ```

## Contributing

Contributions to this project are welcome! Please fork the repository and submit a pull request with your changes.
