import os
import json
import random
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# -----------------------------------
# FALLBACK QUESTION BANK
# -----------------------------------
QUESTION_BANK = {
    "c++": [
        {
            "question": "What is the difference between pointers and references in C++?",
            "expected_answer": "Pointers store memory addresses and can be null/reassigned. References act as aliases and cannot be null."
        },
        {
            "question": "Explain virtual functions in C++.",
            "expected_answer": "Virtual functions enable runtime polymorphism through method overriding."
        },
        {
            "question": "How does memory management work in C++?",
            "expected_answer": "Memory can be managed using stack, heap, new/delete, smart pointers."
        }
    ],

    "linux": [
        {
            "question": "How do you check disk usage in Linux?",
            "expected_answer": "Using df -h and du commands."
        },
        {
            "question": "How do you find a running process in Linux?",
            "expected_answer": "Using ps, top, htop, grep commands."
        },
        {
            "question": "How would you troubleshoot a service failure in Linux?",
            "expected_answer": "Check logs, service status, permissions, dependencies."
        }
    ],

    "debugging": [
        {
            "question": "How do you debug a crashing application?",
            "expected_answer": "Reproduce issue, analyze logs, use debugger, isolate root cause."
        },
        {
            "question": "What steps do you follow to debug performance issues?",
            "expected_answer": "Profiling, logs, bottleneck analysis."
        },
        {
            "question": "How do you debug memory leaks?",
            "expected_answer": "Use Valgrind, sanitizers, monitor allocations."
        }
    ],

    "make": [
        {
            "question": "What is a Makefile?",
            "expected_answer": "It automates build processes for compiling applications."
        },
        {
            "question": "How do dependencies work in Makefiles?",
            "expected_answer": "Targets rebuild when dependencies change."
        }
    ],

    "unix": [
        {
            "question": "Difference between Unix and Linux?",
            "expected_answer": "Unix is older proprietary OS family, Linux is open-source Unix-like OS."
        }
    ]
}


# -----------------------------------
# FALLBACK GENERATOR
# -----------------------------------
def get_fallback_question(skill):

    skill_lower = skill.lower()

    for keyword in QUESTION_BANK:
        if keyword in skill_lower:
            return random.choice(
                QUESTION_BANK[keyword]
            )

    return {
        "question": f"What practical experience do you have with {skill}?",
        "expected_answer": (
            f"Candidate should explain practical exposure "
            f"to {skill} with examples."
        )
    }


# -----------------------------------
# MAIN QUESTION GENERATION
# -----------------------------------
def generate_questions(matched_skills):

    prompt = f"""
    Generate ONE technical interview question for each skill.

    Skills:
    {matched_skills}

    Rules:
    - Basic to intermediate level
    - Real-world practical focus
    - Avoid repeating generic questions
    - Keep questions unique
    - Return expected answer also

    Return STRICT JSON format:

    {{
        "questions": [
            {{
                "skill": "C++",
                "question": "What are virtual functions?",
                "expected_answer": "Used for runtime polymorphism."
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
            temperature=0.9
        )

        output = response.choices[0].message.content

        cleaned = (
            output.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        parsed = json.loads(cleaned)

        return parsed

    except Exception as e:
        print("Question generation error:", e)

        fallback_questions = []

        for skill in matched_skills:
            fallback = get_fallback_question(skill)

            fallback_questions.append({
                "skill": skill,
                "question": fallback["question"],
                "expected_answer": fallback["expected_answer"]
            })

        return {
            "questions": fallback_questions
        }