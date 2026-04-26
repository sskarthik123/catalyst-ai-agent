import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh

from parser import extract_resume_text, extract_skills
from pre_gap import analyze_skill_gap
from assessment import generate_questions
from evaluator import evaluate_answers
from planner import generate_learning_plan


# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="SkillPilot AI",
    page_icon="🚀",
    layout="wide"
)


# -----------------------------------
# CUSTOM CSS
# -----------------------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}

.stButton button {
    background: linear-gradient(90deg, #4CAF50, #2E8B57);
    color: white;
    border-radius: 12px;
    height: 50px;
    width: 100%;
    font-weight: bold;
    border: none;
}

div[data-testid="stMetric"] {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------------
# SESSION STATE DEFAULTS
# -----------------------------------
defaults = {
    "analysis_done": False,
    "assessment_started": False,
    "evaluation_done": False,
    "learning_plan_done": False,
    "submission_in_progress": False,
    "start_time": None,
    "candidate_answers": {}
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -----------------------------------
# HEADER
# -----------------------------------
st.title("🚀 SkillPilot AI")
st.caption(
    "AI-Powered Skill Assessment & Personalized Learning Platform"
)


# -----------------------------------
# INPUT SECTION
# -----------------------------------
col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader(
        "📄 Upload Resume",
        type=["pdf"]
    )

with col2:
    job_description = st.text_area(
        "💼 Paste Job Description",
        height=250
    )


# -----------------------------------
# ANALYZE CANDIDATE
# -----------------------------------
if st.button("Analyze Candidate"):

    if not resume_file:
        st.error("Please upload resume")
        st.stop()

    if not job_description:
        st.error("Please paste job description")
        st.stop()

    with st.spinner("Analyzing candidate profile..."):

        resume_text = extract_resume_text(resume_file)

        resume_skills = extract_skills(
            resume_text,
            "resume"
        )

        jd_skills = extract_skills(
            job_description,
            "job description"
        )

        gap_result = analyze_skill_gap(
            resume_skills["skills"],
            jd_skills["skills"]
        )

        questions_data = generate_questions(
            gap_result["matched_skills"]
        )

        st.session_state.resume_skills = resume_skills
        st.session_state.jd_skills = jd_skills
        st.session_state.gap_result = gap_result
        st.session_state.questions_data = questions_data

        # Reset states
        st.session_state.analysis_done = True
        st.session_state.assessment_started = False
        st.session_state.evaluation_done = False
        st.session_state.learning_plan_done = False
        st.session_state.submission_in_progress = False
        st.session_state.start_time = None
        st.session_state.candidate_answers = {}

    st.success("Candidate analysis completed successfully!")


# -----------------------------------
# DASHBOARD
# -----------------------------------
if st.session_state.analysis_done:

    st.subheader("📊 Candidate Skill Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Candidate Skills",
        len(st.session_state.resume_skills["skills"])
    )

    c2.metric(
        "JD Skills",
        len(st.session_state.jd_skills["skills"])
    )

    c3.metric(
        "Matched Skills",
        len(st.session_state.gap_result["matched_skills"])
    )

    c4.metric(
        "Skill Gaps",
        len(st.session_state.gap_result["missing_skills"])
    )

    with st.expander("Candidate Skills"):
        for skill in st.session_state.resume_skills["skills"]:
            st.write(f"✅ {skill}")

    with st.expander("JD Required Skills"):
        for skill in st.session_state.jd_skills["skills"]:
            st.write(f"📌 {skill}")

    with st.expander("Matched Skills"):
        for skill in st.session_state.gap_result["matched_skills"]:
            st.write(f"🟢 {skill}")

    with st.expander("Missing Skills"):
        for skill in st.session_state.gap_result["missing_skills"]:
            st.write(f"🔴 {skill}")


# -----------------------------------
# START ASSESSMENT
# -----------------------------------
if (
    st.session_state.analysis_done
    and not st.session_state.assessment_started
    and not st.session_state.evaluation_done
    and not st.session_state.submission_in_progress
):

    st.subheader("🧠 Skill Assessment")

    if st.button("Take Skill Assessment"):
        st.session_state.assessment_started = True
        st.session_state.start_time = time.time()
        st.rerun()


# -----------------------------------
# ASSESSMENT QUESTIONS
# -----------------------------------
if st.session_state.assessment_started:

    st.subheader("📝 Assessment Questions")

    total_questions = len(
        st.session_state.questions_data["questions"]
    )

    total_time_minutes = 5 + (total_questions * 3)

    # Timer refresh
    st_autorefresh(
        interval=1000,
        key="assessment_timer"
    )

    elapsed = int(
        time.time() - st.session_state.start_time
    )

    remaining = max(
        0,
        (total_time_minutes * 60) - elapsed
    )

    mins = remaining // 60
    secs = remaining % 60

    st.metric(
        "⏳ Time Remaining",
        f"{mins}:{secs:02d}"
    )

    st.caption(
        f"5 mins reading + 3 mins/question = {total_time_minutes} mins"
    )

    for item in st.session_state.questions_data["questions"]:

        skill = item["skill"]
        question = item["question"]

        st.markdown(f"### {skill}")
        st.write(question)

        answer = st.text_area(
            f"Answer for {skill}",
            key=f"answer_{skill}"
        )

        st.session_state.candidate_answers[skill] = answer


    # Manual submit
    if st.button("Submit Assessment"):

        st.session_state.assessment_started = False
        st.session_state.submission_in_progress = True
        st.rerun()


    # Auto submit
    if remaining <= 0:

        st.session_state.assessment_started = False
        st.session_state.submission_in_progress = True
        st.rerun()


# -----------------------------------
# PROCESS SUBMISSION SCREEN
# -----------------------------------
if (
    st.session_state.submission_in_progress
    and not st.session_state.evaluation_done
):

    st.subheader("⏳ Processing Your Assessment")

    progress = st.progress(0)

    st.write("Submitting answers...")
    progress.progress(25)
    time.sleep(1)

    st.write("Evaluating your skills...")
    progress.progress(60)

    evaluation_result = evaluate_answers(
        st.session_state.candidate_answers
    )

    time.sleep(1)

    st.write("Generating personalized roadmap...")
    progress.progress(85)

    learning_plan = generate_learning_plan(
        st.session_state.gap_result["missing_skills"],
        evaluation_result
    )

    time.sleep(1)

    progress.progress(100)

    st.session_state.evaluation_result = evaluation_result
    st.session_state.learning_plan = learning_plan

    st.session_state.evaluation_done = True
    st.session_state.learning_plan_done = True
    st.session_state.submission_in_progress = False

    st.success("Assessment submitted successfully!")

    time.sleep(1)

    st.rerun()


# -----------------------------------
# QUESTION REVIEW
# -----------------------------------
if st.session_state.evaluation_done:

    st.subheader("📘 Question Review")

    for item in st.session_state.questions_data["questions"]:

        skill = item["skill"]
        question = item["question"]
        expected_answer = item.get(
            "expected_answer",
            "Ideal answer not available."
        )

        candidate_answer = st.session_state.candidate_answers.get(
            skill,
            "No answer submitted"
        )

        with st.expander(f"{skill} Review"):

            st.markdown(
                f"**Question:** {question}"
            )

            st.markdown(
                f"**Your Answer:** {candidate_answer}"
            )

            st.markdown(
                f"**Ideal Answer:** {expected_answer}"
            )


# -----------------------------------
# SKILL EVALUATION RESULTS
# -----------------------------------
if st.session_state.evaluation_done:

    st.subheader("📈 Skill Evaluation Results")

    for result in st.session_state.evaluation_result["evaluation"]:

        with st.expander(
            f"{result['skill']} → {result['level']}"
        ):
            st.write(result["reason"])


# -----------------------------------
# LEARNING ROADMAP
# -----------------------------------
if st.session_state.learning_plan_done:

    st.subheader("📚 Personalized Learning Roadmap")

    for item in st.session_state.learning_plan["learning_plan"]:

        st.markdown(f"### {item['skill']}")
        st.success(f"Priority: {item['priority']}")
        st.info(
            f"Estimated Time: {item['estimated_time']}"
        )

        st.markdown(
            f"[🎥 YouTube Resource]({item['youtube_resource']})"
        )

        st.markdown(
            f"[📘 Reading Resource]({item['reading_resource']})"
        )

        st.divider()


# -----------------------------------
# FINAL SUCCESS
# -----------------------------------
if st.session_state.learning_plan_done:
    st.success(
        "🎉 End-to-End Assessment Completed Successfully!"
    )