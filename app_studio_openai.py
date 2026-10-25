import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Creative Role Studio",
    page_icon="🎭",
    layout="wide"
)
st.title("🎭 Creative Role Studio")
st.caption("Arts and Advanced Big Data | Creative-role chatbot powered by OpenAI")
ROLES = {
    "🎬 Video Director": (
        "You are a professional film director. "
        "Give concrete advice on visual storytelling, camera movement, "
        "lighting, framing, editing rhythm, and emotional tone."
    ),

    "💃 Dance Instructor": (
        "You are a professional dance instructor. "
        "Give practical advice about movement, rhythm, choreography, "
        "body expression, and stage presence."
    ),

    "👗 Fashion Stylist": (
        "You are a creative fashion stylist. "
        "Give ideas about outfits, colors, textures, silhouettes, "
        "and styling choices."
    ),

    "🎭 Acting Coach": (
        "You are a professional acting coach. "
        "Give practical advice about emotion, voice, gesture, timing, "
        "character building, and body language."
    ),

    "🎨 Art Curator": (
        "You are an art curator. "
        "Discuss artistic themes, visual language, art history, "
        "artists, exhibitions, and exhibition concepts."
    ),

    "✍️ Custom Role": ""
}
if "messages" not in st.session_state:
    st.session_state.messages = []
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input(
        "OpenAI API key",
        type="password",
        placeholder="sk-..."
    )
    model = st.selectbox(
        "Model",
        [
            "gpt-5.6",
            "gpt-5.6-mini"
        ]
    )
    role_name = st.selectbox(
        "Creative role",
        list(ROLES.keys())
    )
    if role_name == "✍️ Custom Role":

        role_description = st.text_area(
            "Describe your custom role",
            value=(
                "You are a creative artist who gives imaginative "
                "and practical ideas."
            )
        )

    else:
        role_description = ROLES[role_name]
        st.info(role_description)
    language = st.selectbox(
        "Answer language",
        [
            "Same as my question",
            "English",
            "한국어"
        ]
    )
    creativity = st.slider(
        "Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )
    if st.button("🗑 Clear conversation"):
        st.session_state.messages = []
        st.rerun()
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if not st.session_state.messages:
    st.info(
        "Choose a creative role in the sidebar and ask a question below."
    )
question = st.chat_input(
    "Type your question or idea..."
)
if question:
    if not api_key.strip():
        st.warning(
            "Please enter your OpenAI API key in the sidebar."
        )
    else:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )
        with st.chat_message("user"):
            st.markdown(question)
        system_prompt = role_description
        if language == "English":
            system_prompt += (
                "\nAlways answer in English."
            )
        elif language == "한국어":
            system_prompt += (
                "\n항상 한국어로 답변하세요."
            )
        conversation_text = ""
        for message in st.session_state.messages:
            conversation_text += (
                f"{message['role']}: "
                f"{message['content']}\n\n"
            )
        with st.chat_message("assistant"):
            try:
                client = OpenAI(
                    api_key=api_key.strip()
                )
                with st.spinner(
                    "AI is thinking..."
                ):
                    response = client.responses.create(
                        model=model,
                        instructions=system_prompt,
                        input=conversation_text
                    )
                answer = response.output_text
                st.markdown(answer)
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )
            except Exception as error:
                if (
                    st.session_state.messages
                    and
                    st.session_state.messages[-1]["role"] == "user"
                ):

                    st.session_state.messages.pop()
                st.error(
                    f"Could not generate a response: {error}"
                )
if st.session_state.messages:
    transcript = "\n\n".join(
        f"{'You' if message['role'] == 'user' else role_name}:\n"
        f"{message['content']}"
        for message in st.session_state.messages
    )
    st.sidebar.download_button(
        "💾 Download conversation",
        data=transcript,
        file_name="creative_role_studio_conversation.txt",
        mime="text/plain"
    )
st.markdown("---")
st.caption(
    "Built for 'Art & Advanced Big Data'"
)
