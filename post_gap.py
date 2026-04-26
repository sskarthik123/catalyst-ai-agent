def post_assessment_gap(
    missing_skills,
    evaluation_result
):
    weak_skills = []

    for item in evaluation_result["evaluations"]:
        if item["level"] == "Beginner":
            weak_skills.append(item["skill"])

    final_gap = list(set(missing_skills + weak_skills))

    return {
        "final_gap_skills": final_gap
    }