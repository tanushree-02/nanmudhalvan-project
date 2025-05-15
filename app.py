from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Sample content database
content_db = {
    "technology": [
        "Top 10 AI tools to boost productivity in 2025.",
        "How quantum computing is shaping the future.",
        "Beginner's guide to programming with Python."
    ],
    "sports": [
        "The rise of esports in mainstream competitions.",
        "Top fitness routines for peak performance.",
        "Highlights from the 2025 World Cup qualifiers."
    ],
    "health": [
        "10 tips for a balanced diet and mental health.",
        "How to manage stress in the digital age.",
        "New breakthroughs in cancer research."
    ],
    "entertainment": [
        "Best sci-fi movies to watch this year.",
        "Behind the scenes of popular streaming shows.",
        "Top 5 books adapted into hit films."
    ]
}

# Simulated user profile storage
user_profiles = {}

# Recommendation engine
def recommend_content(user_id):
    profile = user_profiles.get(user_id, {})
    interests = profile.get("interests", [])

    if not interests:
        return "Tell me what you're interested in so I can recommend something!"

    recommendations = []
    for interest in interests:
        content_list = content_db.get(interest.lower())
        if content_list:
            recommendations.append(random.choice(content_list))

    return recommendations or ["Sorry, I couldn't find anything for your interests."]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data.get('user_id', 'default_user')
    user_message = data.get('message', '').lower()

    # Simple interest setting logic
    if "interested in" in user_message:
        interests = [word.strip() for word in user_message.split("interested in")[-1].split(",")]
        user_profiles[user_id] = {"interests": interests}
        return jsonify({'response': f"Got it! You're interested in {', '.join(interests)}."})

    # Trigger recommendation
    if "recommend" in user_message or "suggest" in user_message:
        content = recommend_content(user_id)
        if isinstance(content, list):
            return jsonify({'response': "Here are some recommendations:\n- " + "\n- ".join(content)})
        else:
            return jsonify({'response': content})

    return jsonify({'response': "Tell me what you're interested in (e.g., 'I'm interested in technology, health'). Then say 'recommend me something'."})

if __name__ == '__main__':
    app.run(debug=True)
