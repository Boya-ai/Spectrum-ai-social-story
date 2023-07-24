#fixing gender in hebrew and formatting

import streamlit as st
import openai
import json
from google.cloud import translate_v2 as translate

openai_api_key = st.secrets["openai"]["api_key"]

# Convert the service account key from a string to a dictionary
service_account_info = json.loads(st.secrets["google"]["GOOGLE_APPLICATION_CREDENTIALS"])

# Initialize OpenAI API key
openai.api_key = openai_api_key

def check_and_adjust_gender(text, expected_gender):
    prompt = f"""
    The following Hebrew text is intended for a {expected_gender}:

    {text}

    Please check if the text is appropriate for a {expected_gender}. If not, please revise the text to match the appropriate gender.
    """

    response = openai.Completion.create(
        engine="text-davinci-003",  # Use the most advanced available engine
        prompt=prompt,
        temperature=0.0,
        max_tokens=1000
    )

    return response.choices[0].text.strip()

class PromptTemplate:
    def __init__(self, template, input_variables):
        self.template = template
        self.input_variables = input_variables

prompt_template = PromptTemplate(
    template="""
    As an AI language model embodying the roles of Carol Gray, Psychologist, Therapist, Special Education Teacher, Speech and Language Therapist, Occupational Therapist, Autism Specialist, and Behavior Analyst, your task is to create a social story strictly in the first-person perspective for a {gender} child named {name}, who is {age} years old, about {situation}. 

    The story must adhere to Carol Gray's Social Stories 10.2 criteria and be age-appropriate. It should use a positive and patient tone, provide clear guidance on social cues and appropriate responses, and be reassuring and supportive. The story should describe more than it directs, and it should answer relevant 'wh' questions that describe context, including WHERE, WHEN, WHO, WHAT, HOW, and WHY.

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

    """,
    input_variables=["name", "age", "situation", "gender"]
)

# Title of the app
st.title('Social Story Generator 🧩')

# Display the model name on the Streamlit app
st.write(f"🧠 Using model: text-davinci-003")

# Create a form
with st.form(key='my_form'):
    # Collect the child's name
    name = st.text_input(label='Enter the child\'s name')

    # Collect the child's gender
    gender = st.selectbox(label='Select the child\'s gender', options=['Boy', 'Girl'])

    # Collect the child's age
    age = st.number_input(label='Enter the child\'s age', min_value=1, max_value=100)

    # Collect the specific difficulty
    difficulty = st.text_input(label='Enter the specific difficulty or subject the child is dealing with')

    # Submit button
    submit_button = st.form_submit_button(label='Generate Story')

# Placeholder to display the translated social story in Hebrew
story_placeholder_hebrew = st.empty()

# Placeholder to display the generated social story in English
story_placeholder_english = st.empty()

# If the form is submitted, generate the social story
if submit_button:
    response = openai.Completion.create(
        engine="text-davinci-003",  # Use the most advanced available engine
        prompt=prompt_template.template.format(name=name, age=age, situation=difficulty, gender=gender.lower()),
        temperature=0.0,
        max_tokens=1000
    )

    story = response.choices[0].text.strip()

    # Split the story into sections
    sections = story.split("\n")

    # Initialize the Google Translate client
    translate_client = translate.Client.from_service_account_info(service_account_info)

    # Translate each section separately
    translated_sections = [translate_client.translate(section, target_language="he")['translatedText'] for section in sections]

    # Combine the translated sections to form the complete story
    translated_story = "<br>".join(translated_sections)

    # Check and adjust the gender in the translated story
    checked_and_adjusted_story = check_and_adjust_gender(translated_story, gender)

    # Display the checked and adjusted social story in Hebrew
    story_placeholder_hebrew.markdown(f"<div style=\"direction: rtl; font-family: 'Arial'; font-size: 16px; color: #333;\">Hebrew Story:<br>{checked_and_adjusted_story}</div>", unsafe_allow_html=True)

    # Display the generated social story in English
    story = story.replace("\n", "<br>")
    story_placeholder_english.markdown(f"<div>English Story:<br>{story}</div>", unsafe_allow_html=True)
