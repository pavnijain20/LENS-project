from flask import Flask, request, jsonify, render_template
import re
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    resume = data["text"]

    # 🔥 Bias-Blind Filtering
    resume = re.sub(r'\S+@\S+', '', resume)  # remove email
    resume = re.sub(r'\b\d{10}\b', '', resume)  # remove phone
    resume = re.sub(r'(?i)name:.*', '', resume)  # remove name line

    text = resume.lower()

    # Scores
    skill_score = 0
    project_score = 0
    experience_score = 0

    suggestions = []
    found_skills = []

    # Skill categories
    skills_map = {
        "Programming": ["python", "java", "c++", "c"],
        "Web": ["html", "css", "javascript"],
        "Database": ["sql", "mysql"],
        "Tools": ["git", "github"]
    }

    # 🔍 Detect skills
    for category, skills in skills_map.items():
        for skill in skills:
            if skill in text:
                found_skills.append(skill)
                skill_score += 10

    # 📊 Project & Experience
    if "project" in text:
        project_score = 20
    else:
        suggestions.append("Add at least 1 strong project with description")

    if "experience" in text:
        experience_score = 20
    else:
        suggestions.append("Include internships or work experience")

    # 💡 Extra Suggestions
    if skill_score < 20:
        suggestions.append("Add more technical skills like Python, SQL, etc.")

    if "github" not in text:
        suggestions.append("Add GitHub profile link")

    if "linkedin" not in text:
        suggestions.append("Add LinkedIn profile")

    # 🧮 Total Score
    score = skill_score + project_score + experience_score

    # 📈 Feedback
    if score >= 80:
        msg = "Excellent Resume 🔥"
    elif score >= 50:
        msg = "Good Resume 👍"
    else:
        msg = "Needs Improvement ⚠️"

    # 🚀 Final Output
    return jsonify({
        "result": f"""Score: {score}/100
{msg}

Score Breakdown:
Skills: {skill_score}
Projects: {project_score}
Experience: {experience_score}

Skills Found:
{', '.join(found_skills)}

Suggestions:
{chr(10).join(suggestions) if suggestions else "Perfect Resume 🎯"}
"""
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)