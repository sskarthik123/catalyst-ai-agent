import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def evaluate_answers(answers):

    prompt = f"""
    Evaluate candidate answers for each skill.

    Candidate Answers:
    {answers}

    For each skill classify candidate into ONLY one level:
    - No Knowledge
    - Beginner
    - Intermediate
    - Advanced

    Evaluate based on:
    - conceptual clarity
    - practical understanding
    - correctness
    - confidence shown in response

    Return STRICT JSON format:

    {{
        "evaluation": [
            {{
                "skill": "Python",
                "level": "Intermediate",
                "reason": "Shows practical understanding with moderate confidence."
            }}
        ]
    }}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        output = response.choices[0].message.content

        cleaned = (
            output.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(cleaned)

    except Exception as e:
        print("Evaluation Error:", e)

        fallback_results = []

        for skill, answer in answers.items():

            word_count = len(answer.split())

            if word_count < 3:
                level = "No Knowledge"
                reason = (
                    "The response indicates little to no understanding "
                    "of this skill."
                )

            elif word_count < 10:
                level = "Beginner"
                reason = (
                    "Basic understanding is present, but deeper practical "
                    "knowledge is needed."
                )

            elif word_count < 25:
                level = "Intermediate"
                reason = (
                    "Shows decent understanding with some practical knowledge, "
                    "but there is room for improvement."
                )

            else:
                level = "Advanced"
                reason = (
                    "Demonstrates strong understanding with solid practical knowledge."
                )

            fallback_results.append({
                "skill": skill,
                "level": level,
                "reason": reason
            })

        return {
            "evaluation": fallback_results
        }