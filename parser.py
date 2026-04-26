import os
import json
from pypdf import PdfReader
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def extract_resume_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return text


def extract_skills(text, source_type):
    prompt = f"""
    Extract only technical/professional skills from this {source_type}.

    Return response strictly in JSON format:

    {{
        "skills": ["skill1", "skill2"]
    }}

    Text:
    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    output = response.choices[0].message.content

    try:
        cleaned = output.replace("```json", "").replace("```", "")
        return json.loads(cleaned)
    except Exception as e:
        print("Parsing error:", e)
        print(output)
        return {"skills": []}