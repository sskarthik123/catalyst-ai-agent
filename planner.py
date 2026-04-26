import json


def generate_learning_plan(missing_skills, evaluation_result):

    learning_plan = []

    for skill in missing_skills[:5]:

        youtube_link = (
            f"https://www.youtube.com/results?search_query="
            f"{skill.replace(' ', '+')}+tutorial"
        )

        article_link = (
            f"https://www.google.com/search?q="
            f"{skill.replace(' ', '+')}+documentation+tutorial"
        )

        learning_plan.append({
            "skill": skill,
            "priority": "High",
            "estimated_time": "1-2 weeks",
            "youtube_resource": youtube_link,
            "reading_resource": article_link
        })

    return {
        "learning_plan": learning_plan
    }