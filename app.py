from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables (for local use)
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "🤖 WhatsApp Career AI Agent is Live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Get the incoming message from Twilio
        incoming_msg = request.values.get('Body', '').strip()
        sender = request.values.get('From', '')

        print(f"📩 Message from {sender}: {incoming_msg}")

        # Build OpenAI response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Arshath’s personal AI career mentor. You help him find internships, free certification courses, and career growth ideas."},
                {"role": "user", "content": incoming_msg}
            ]
        )

        reply = response.choices[0].message.content.strip()

        # Send reply back to WhatsApp
        twilio_resp = MessagingResponse()
        msg = twilio_resp.message()
        msg.body(reply)
        print(f"💬 Replied: {reply}")

        return str(twilio_resp)

    except Exception as e:
        print(f"❌ Error: {e}")
        twilio_resp = MessagingResponse()
        twilio_resp.message("Sorry, I had an issue processing your message.")
        return str(twilio_resp)


if __name__ == "__main__":
    # Render.com automatically sets PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
