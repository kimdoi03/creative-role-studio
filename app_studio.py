import streamlit as st
st.title("🎭 Creative Role Studio")
roles = [
    "🎬 Video Director",
    "💃 Dance Instructor",
    "👗 Fashion Stylist",
    "🎭 Acting Coach",
    "🎨 Art Curator"
]
role = st.selectbox("Choose a creative role", roles)
st.write("Selected role:", role)
