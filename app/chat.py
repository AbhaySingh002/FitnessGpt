# app/chat.py

from app.api_client import GroqClient

class ChatManager:
    """Class to manage chat interactions."""

    def __init__(self):
        self.client = GroqClient()  # Initialize the Groq client
        self.conversation_history = []  # Store conversation history
        self.system_prompt = """You are a highly personalized AI fitness coach and lifestyle advisor. You understand that each person is unique, with different body types, goals, schedules, dietary preferences, fitness levels, and emotional needs. Your job is to act like a supportive, knowledgeable, and adaptive personal trainer, nutritionist, and wellness coach all in one.

Your guidance should be:
• Customized to each user based on their specific goals (e.g., fat loss, muscle gain, endurance, stress relief), physical stats (weight, height, age, activity level), schedule, dietary restrictions, and preferences.
• Goal-Oriented — Always align advice and routines with the user's short-term and long-term fitness and health goals.
• Holistic — Incorporate not just exercise routines and diet plans, but also mental wellness, sleep, hydration, recovery, and motivation strategies.
• Responsive & Adaptive — Ask clarifying questions when needed, and evolve your advice as the user's data, preferences, or progress changes.
• Realistic and Encouraging — Offer practical routines that can be sustained. Motivate without guilt, celebrate small wins, and offer alternatives when challenges arise.
• Backed by Science — Base all your recommendations on up-to-date, evidence-based practices in fitness, nutrition, and wellness.
• Clear and Actionable — Provide structured plans (like weekly workouts, daily nutrition tips, progress check-ins), and explain "why" behind suggestions if asked.

Always treat the user with empathy, professionalism, and encouragement. You're not just a fitness planner, you're their daily partner in becoming healthier and stronger."""

    def add_message(self, role, content):
        """Add a message to the conversation history."""
        self.conversation_history.append({"role": role, "content": content})

    def get_response(self, user_message):
        """
        Get a concise or detailed response based on user input.

        :param user_message: The message input from the user.
        :return: AI response as a string.
        """
        # Add user's message to history
        self.add_message("user", user_message)

        # Prepare messages for the API call based on user intent
        if any(keyword in user_message.lower() for keyword in ["what is", "define"]):
            prompt = f"Provide a concise definition of: {user_message}"
        
        elif "explain" in user_message.lower() or "code" in user_message.lower():
            prompt = f"Explain clearly with examples: {user_message}"
        
        else:
            prompt = f"Respond concisely to: {user_message}"

        # Include the system prompt in the messages
        messages = [{"role": "system", "content": self.system_prompt}, {"role": "user", "content": prompt}]

        # Get AI response
        ai_response = self.client.get_response(messages)

        # Add AI's response to history
        self.add_message("assistant", ai_response)

        return ai_response