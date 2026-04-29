import streamlit as st
from ml.model import predict
from agent.agent import generate_learning_plan
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Digital Twin Career Engine")

st.title("🚀 Digital Twin Career Engine")

if st.button("Analyze My Career"):
    preds = predict()

    st.subheader("📊 Skill Balance")

    skills = ["Python", "Frontend", "UI/UX", "Problem Solving", "Communication"]
    values = [4, 3, 4, 5, 4]

    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)

    angles = [n / float(len(skills)) * 2 * 3.14 for n in range(len(skills))]
    angles += angles[:1]

    values += values[:1]

    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(skills)

    st.pyplot(fig)

    st.subheader("🎮 Tech Tree")

    st.markdown("""
- 🟢 Python → 🔓 Machine Learning  
- 🟢 Frontend → 🔓 React  
- 🔒 WebGL (locked)  
- 🔒 AI Engineering  
""")
    
    st.subheader("📦 Semester Wrapped")

    st.success("""
🔥 Top Skill: Python  
📺 Most Watched: UI Design Tutorials  
💪 Most Productive Day: Monday  
""")

    st.subheader("Top Career Matches")

    df = pd.DataFrame(preds)
    st.dataframe(df)

    st.subheader("Missing Skills")

    for p in preds:
        st.write(f"🔹 {p['job']}: {', '.join(p['missing_skills'])}")

    plan = generate_learning_plan(preds)

    st.subheader("Learning Plan")

    for item in plan:
        st.write(f"📚 {item['skill']} → {item['resource']}")


# ROAST MODE
if st.checkbox("🔥 Roast My Stack"):
    st.error("Your stack is mid. You watched tutorials but built nothing 😭")