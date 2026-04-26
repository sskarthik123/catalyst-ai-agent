def normalize_skill(skill):
    skill = skill.lower()

    replacements = [
        "programming language",
        "standard edition",
        "server",
        "tools",
        "mechanisms",
        "architectures",
        "frameworks"
    ]

    for word in replacements:
        skill = skill.replace(word, "")

    skill = skill.replace("(", "").replace(")", "")
    skill = skill.strip()

    return skill


def analyze_skill_gap(resume_skills, jd_skills):
    normalized_resume = {
        normalize_skill(skill): skill
        for skill in resume_skills
    }

    matched = []
    missing = []

    for jd_skill in jd_skills:
        normalized_jd = normalize_skill(jd_skill)

        found = False

        for resume_skill_normalized in normalized_resume:
            if (
                normalized_jd in resume_skill_normalized
                or resume_skill_normalized in normalized_jd
            ):
                matched.append(jd_skill)
                found = True
                break

        if not found:
            missing.append(jd_skill)

    return {
        "matched_skills": matched,
        "missing_skills": missing
    }