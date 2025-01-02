import asyncio
import os
import logging
import nats
import aiohttp
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

openai_api_key = os.getenv('OPENAI_API_KEY', 'default-openai-api-key')
weather_api_key = os.getenv('WEATHER_API_KEY', 'default-weather-api-key')

openai_client = OpenAI(api_key=openai_api_key)


async def fetch_weather_data():
    api_url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q=estonia"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logging.error(f"Error fetching weather data: HTTP {response.status}")
                    return None
    except Exception as e:
        logging.error(f"Error fetching weather data: {e}")
        return None


async def get_openai_response(prompt, model="gpt-3.5-turbo", max_tokens=150):
    try:
        system_content = "You are great at analyzing the weather."

        def get_response():
            return openai_client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": prompt}
                ])

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, get_response)
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error in OpenAI API call: {e}")
        return None


async def main():
    nats_client = await nats.connect("nats://localhost:4222")
    logging.info("Connected to NATS server.")

    user_alert_criteria = ""

    async def message_handler(msg):
        nonlocal user_alert_criteria
        data = msg.data.decode()
        if data.startswith("Set Alert:"):
            user_alert_criteria = data[len("Set Alert:"):].strip()
            logging.info(f"User alert criteria updated: {user_alert_criteria}")

    await nats_client.subscribe("chat", cb=message_handler)

    while True:
        current_weather = await fetch_weather_data()
        if current_weather and user_alert_criteria:
            logging.info(f"Current weather data: {current_weather}")
            prompt = f"Use the current weather: {current_weather} information and user alert criteria: {user_alert_criteria}. Identify if the weather meets these criteria and return only YES or NO with a short weather temperature info without explaining why."
            response_text = await get_openai_response(prompt)
            if response_text and "YES" in response_text:
                logging.info("Weather conditions met user criteria.")
                ai_response = f"Weather alert! Your specified conditions have been met. {response_text}"
                await nats_client.publish("chat_response", payload=ai_response.encode())
            else:
                logging.info("Weather conditions did not meet user criteria.")
        else:
            logging.info("No current weather data or user alert criteria set.")

        await asyncio.sleep(10)  # Sleep for 10 seconds before next check

if __name__ == '__main__':
    asyncio.run(main())
