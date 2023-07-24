import streamlit as st
from langchain.llms import OpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
import openai
import json
from google.cloud import translate_v2 as translate

openai_api_key = st.secrets["openai"]["api_key"]

# Convert the service account key from a string to a dictionary
service_account_info = json.loads(st.secrets["google"]["GOOGLE_APPLICATION_CREDENTIALS"])

# Initialize OpenAI API key
openai.api_key = openai_api_key

# Define the prompt template
prompt_template = PromptTemplate(
    template="""
As an AI language model embodying the roles of Carol Gray, Psychologist, Therapist, Special Education Teacher, Speech and Language Therapist, Occupational Therapist, Autism Specialist, and Behavior Analyst, your task is to create a social story strictly in the first-person perspective for a child named {name}, who is {age} years old, about {situation}. 

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
    input_variables=["name", "age", "situation"]
)

# Initialize the chain with OpenAI and the prompt template
#chain = LLMChain(llm=OpenAI(temperature=0.7), prompt=prompt_template)
chain = LLMChain(llm=OpenAI(openai_api_key=openai_api_key, temperature=0.7), prompt=prompt_template)

# Title of the app
st.title('Social Story Generator for Autism')

# Create a form
with st.form(key='my_form'):
    # Collect the child's name
    name = st.text_input(label='Enter the child\'s name')

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
    # Initialize the chain with OpenAI and the prompt template
    chain = LLMChain(llm=OpenAI(openai_api_key=openai_api_key, temperature=0.7), prompt=prompt_template)

    # Generate the social story using the chain
    story = chain.run({"name": name, "age": age, "situation": difficulty})

    # Initialize the Google Translate client
    translate_client = translate.Client.from_service_account_info(service_account_info)


    # Split the story into sections
    sections = story.split("\n")

    # Translate each section separately
    translated_sections = [translate_client.translate(section, target_language="he")['translatedText'] for section in sections]

    # Combine the translated sections to form the complete story
    translated_story = "\n\n".join(translated_sections)

    # Display the translated social story in Hebrew
    story_placeholder_hebrew.markdown(f"<div style='direction: rtl;'>Hebrew Story:\n{translated_story}</div>", unsafe_allow_html=True)

    # Display the generated social story in English
    story = story.replace("\n", "<br>")
    story_placeholder_english.markdown(f"<div>English Story:<br>{story}</div>", unsafe_allow_html=True)
