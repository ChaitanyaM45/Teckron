from decision_logic import detect_bottlenecks
from groq import Groq
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Store latest insight in memory
latest_insight = {
    "text": "Daily insight not generated yet.",
    "timestamp": None
}


def generate_daily_insight():
    """
    Runs daily to analyze bottlenecks and generate a human-friendly insight.
    """
    bottlenecks = detect_bottlenecks()

    # If no issues, return positive insight
    if not bottlenecks:
        insight = "All operations are running smoothly today. No major risks detected."
    else:
        prompt = f"""
You are an AI assistant helping MSME owners.

Convert the following operational issues into ONE short, professional business insight.
Be concise and actionable.

Issues:
{bottlenecks}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        insight = response.choices[0].message.content.strip()

    # Save insight in memory
    latest_insight["text"] = insight
    latest_insight["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Optional: save to log file (audit trail)
    with open("daily_insights.log", "a") as f:
        f.write(f'{latest_insight["timestamp"]} - {insight}\n')

    return latest_insight
