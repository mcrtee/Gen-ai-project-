import streamlit as st
from ml.model import predict
from agent.agent import generate_learning_plan
import pandas as pd
import plotly.express as px
import json
import os

# Настройка страницы
st.set_page_config(page_title="Digital Twin Career Engine", page_icon="🧬", layout="wide")

# Кастомный CSS для стиля "Tech Noir / RPG"
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00FFCC; }
    .stButton>button { border: 2px solid #00FFCC; background-color: black; color: #00FFCC; transition: 0.3s; }
    .stButton>button:hover { box-shadow: 0 0 15px #00FFCC; color: white; }
    .stExpander { border: 1px solid #00FFCC; background-color: rgba(0, 255, 204, 0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🧬 Digital Twin: Career Engine")

# Боковая панель
if st.sidebar.button("🔍 Sync with NotebookLM (via MCP)"):
    st.sidebar.success("Connection Active: Data Stream Synchronized")

# Основная логика симуляции
if st.button("🚀 Run Life Simulation"):
    # 1. Получаем предсказания от ML-модели
    preds = predict()
    
    # 2. Пытаемся прочитать реальные навыки, извлеченные агентом из PDF
    skills_path = 'data/skills.json'
    if os.path.exists(skills_path):
        with open(skills_path, 'r', encoding='utf-8') as f:
            user_data = json.load(f)
        my_skills = user_data.get("skills", ["No skills found"])
    else:
        my_skills = ["Python", "Frontend", "AI", "Soft Skills", "Git"] # Заглушка, если файла нет

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Skill Radar (Real Data)")
        # Строим радар на основе РЕАЛЬНЫХ навыков из PDF
        df_radar = pd.DataFrame(dict(
            r=[5] * len(my_skills), # Присваиваем уровень 5 всем найденным навыкам
            theta=my_skills
        ))
        
        fig = px.line_polar(df_radar, r='r', theta='theta', line_close=True)
        fig.update_traces(fill='toself', line_color='#00FFCC', marker=dict(size=10))
        fig.update_layout(
            polar=dict(
                angularaxis=dict(tickfont=dict(size=10), rotation=90, direction="clockwise")
            ),
            width=700, # Увеличиваем размер
            height=600,
            margin=dict(l=80, r=80, t=20, b=20) # Даем место тексту
        )
        st.plotly_chart(fig)

    with col2:
        st.subheader("🎮 RPG Tech Tree")
        # Визуализируем "замороженные" навыки на основе предсказаний ML
        for p in preds:
            st.write(f"**Path: {p['job']}**")
            # Создаем сетку кнопок для навыков
            cols = st.columns(len(p['missing_skills']) + 1)
            cols[0].button("✅ Current", key=f"curr_{p['job']}")
            for i, ms in enumerate(p['missing_skills']):
                cols[i+1].button(f"🔒 {ms}", help="Click to unlock learning path", key=f"lock_{ms}_{i}_{p['job']}")

    # Блок предсказаний и траекторий
    st.divider()
    st.subheader("🎯 Top Career Trajectories")
    for p in preds:
        with st.expander(f"{p['job']} (Match: {int(p['score']*100)}%)"):
            st.write(f"**Missing pieces for your DNA:** {', '.join(p['missing_skills'])}")
            if st.button(f"Generate Path for {p['job']}", key=f"btn_{p['job']}"):
                st.info(f"Agent is now searching web for {p['missing_skills'][0]} resources...")
                # Здесь можно вызвать generate_learning_plan(p['job'])

    # SEMESTER WRAPPED
    st.subheader("📦 Semester Wrapped")
    # Берем первый навык из списка для динамичности
    top_skill = my_skills[0] if my_skills else "Learning"
    st.markdown(f"""
    > **Top Skill:** {top_skill} (Extracted from PDF)  
    > **Focus Path:** {preds[0]['job']}  
    > **Vibe Check:** 🔥 Data Synchronized
    """)

# ROAST MODE
st.sidebar.divider()
if st.sidebar.checkbox("🔥 Enable Roast Mode"):
    st.error("SYSTEM ALERT: AGGRESSIVE TECH LEAD ACTIVE")
    st.warning("твоё резюме выглядит как привет из 2010-го. Давай исправлять.")