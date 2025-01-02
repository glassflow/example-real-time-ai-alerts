import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def handler(data, log):
    """
    Processes weather data and user-defined criteria to generate alerts.
    """
    try:
        log.info("Processing weather data for alerting.")
        weather_data = data["weather"]
        user_criteria = data["criteria"]
        # Use OpenAI to analyze the weather against user criteria
        prompt = (
            f"Analyze the following weather data: {weather_data} against user criteria: {user_criteria}. "
            "Respond with 'YES' or 'NO' and a short summary without explanation."
        )
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a great to analyze weather data.",
                },
                {
                    "role": "user",
                    "content": f"{prompt}",
                },
            ],
            max_tokens=150,
            temperature=0.5,
        )
        ai_response = response.choices[0].message.content
        return {"alert": ai_response}
    except Exception as e:
        log.error(f"Error in transformation: {e}")
        raise
