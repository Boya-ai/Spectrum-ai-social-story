import streamlit as st
from claude import claude_client, claude_wrapper

# Load SESSION_KEY from secrets.toml
SESSION_KEY = st.secrets["claude"]["SESSION_KEY"]

# Initialize the Claude client
client = claude_client.ClaudeClient(SESSION_KEY)


# Get organizations
organizations = client.get_organizations()

# Initialize the Claude wrapper
claude_obj = claude_wrapper.ClaudeWrapper(client, organizations[0]['uuid']) # type: ignore

# Set conversation context
conversation_uuid = "5fe8981f-7ea4-4fc4-98fd-5f5b86e63cfd"
claude_obj.set_conversation_context(conversation_uuid)

# Streamlit app
# Title of the app
st.header('Social Story Generator 🧩')

# Display the model name on the Streamlit app
st.write(f"🧠 Using model: claude_2")

# User inputs
gender = st.selectbox("Select the child's gender:", ["Male", "Female"])
name = st.text_input("Enter the child's name:")
age = st.number_input("Enter the child's age:", min_value=2)
situation = st.text_input("Describe the situation:")

# Generate the prompt
prompt = f"""
As an AI language model embodying the roles of Carol Gray, Psychologist, Therapist, Special Education Teacher, Speech and Language Therapist, Occupational Therapist, Autism Specialist, and Behavior Analyst, your task is to create a social story strictly in the first-person perspective for a {gender} child named {name}, who is {age} years old, about {situation}. 

The story must be written in correct Hebrew language suitable for kids. It must adhere to Carol Gray's Social Stories 10.2 criteria and be age-appropriate. It should use a positive and patient tone, provide clear guidance on social cues and appropriate responses, and be reassuring and supportive. The story should describe more than it directs, and it should answer relevant 'wh' questions that describe context, including WHERE, WHEN, WHO, WHAT, HOW, and WHY.

Ensure the language, sentence length, and complexity of the story are suitable for a {age}-year-old child. If {age} is between 2 and 4, use simple sentences (1-3 per page) with basic vocabulary. The directives should be clear, concrete actions. Familiar scenarios or elements should be included. If {age} is between 5 and 7, use 3-5 sentences per page with expanded vocabulary. Introduce a wider range of situations. If {age} is over 8, use detailed paragraphs with advanced vocabulary and descriptions. Discuss abstract thoughts and emotions.

Here's the structure you should follow:

- Title: A clear title that reflects the content of the story. For example, 'Going to the Dentist'.
- Introduction: The introduction should introduce the topic. For example, 'I sometimes need to go to the dentist to keep my teeth healthy.'
- Body: The body should describe the situation in detail, including:
    - Descriptive sentences: These should state facts or set the scene. For example, 'The dentist's office is a place where I go to keep my teeth clean and healthy.'
    - Perspective sentences: These should describe my reactions, feelings, or thoughts. For example, 'I feel happy when I sit still in the chair.'
    - Problem sentences: These should identify the problem or challenge. For example, 'Sometimes, I might feel scared when the dentist is checking my teeth.'
    - Coping sentences: These should suggest coping strategies or positive affirmations. For example, 'I can squeeze my toy when I feel scared.'
    - Directive sentences: These should suggest appropriate responses or behaviors. For example, 'I can try to sit still and open my mouth wide when the dentist asks me to.'
    - Affirmative sentences: These should reinforce a key point or express a shared value or belief. For example, 'Going to the dentist is important because it helps keep my teeth clean and healthy.'
- Conclusion: The conclusion should summarize the story and reinforce the desired behavior. For example, 'Even though going to the dentist can be scary, I know it's important for keeping my teeth healthy. I can do it!'

Please format the output story as follows:
- Title: [Title of the story]
- Introduction: [Introduction of the story]
- Body: 
    - Descriptive sentences: [Descriptive sentences]
    - Perspective sentences: [Perspective sentences]
    - Problem sentences: [Problem sentences]
    - Coping sentences: [Coping sentences]
    - Directive sentences: [Directive sentences]
    - Affirmative sentences: [Affirmative sentences]
- Conclusion: [Conclusion of the story]
"""


if st.button("Send"):
    with st.spinner('Generating story...'):
        # Send the user's message to the bot
        response = claude_obj.send_message(prompt)

        # Display the bot's response
        if 'completion' in response:
            story = response['completion']
            st.markdown(f"<div style=\"direction: rtl; font-family: 'Arial'; font-size: 16px; color: #333;\">{story}</div>", unsafe_allow_html=True)
        else:
            st.write("No response from Claude Bot.")
