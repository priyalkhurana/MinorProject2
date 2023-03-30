import streamlit as st
import os
import openai
from streamlit_chat import message
from PIL import Image
import time
import toml

secrets = toml.load('secrets.toml')
#api_key = secrets['openai.api_key']['pinecone_api_key']
with open('secrets.toml', 'r') as f:
    secrets = toml.load(f)

# Get the OpenAI and Pinecone API keys from the secrets dictionary
openai_api_key = secrets['openai']['openai_api_key']

txtInputQuestion = "userQuestion"
pageTitle = "HOLY-GPT"

openai.api_key = openai_api_key




def clear_text(textInput):

    st.session_state[textInput] = ""

def generate_prompt(question):
    return """{} 
    Question:{} 
    Answer:""".format(st.secrets["SYSTEM_PROMPT"],
        question
    )



def generate_response_davinci(question):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(question),
        temperature=0.6,
        max_tokens=2048
    )
    return response.choices[0].text



def get_text():
    input_text = st.text_input("Hello, ask me a question about life and philosophy.",placeholder="Type Your question here.", key=txtInputQuestion)
    return input_text
st.write('''\n\n Here's some examples of what you can ask:
1. I've worked very hard but I'm still not able to achieve the results I hoped for, what do I do?
2. I made a million dollars manipulating the stock market and I'm feeling great.
3. How can I attain a peace of mind?
''')

st.write('\n\n\n\n\n\n\n')

st.write('''Note: This is an AI model trained on Bhagvad Gita and it generates responses from that perspective.''')

def page_setup(title, icon):
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout='centered',
        initial_sidebar_state='auto',
        menu_items={
            'About': 'About your application: **This is Bhagvad Gita GPT, a simple ChatGPT use case demo to show how one can easily leverage openAI APIs to create intelligent conversational experiences related to a specific topic.**'
        }
    )
    st.sidebar.title('Creators :')
    st.sidebar.markdown('Priyal Khurana (https://github.com/priyalkhurana)')
    st.sidebar.write('Divyansh Kumar(https://github.com/divyanshkr01)')
    st.sidebar.write("Mitali Chaudhary(https://github.com/Mitali0502)")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Storing the chat
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    icon = Image.open('gita.jpg')

    #setup page
    page_setup(pageTitle,icon)


    col1, col2 = st.columns(2)
    with col1:
        st.title("Bhagvad Gita GPT")
    with col2:
        st.image(icon)
    #st.write("test 1")

    user_input = get_text()

    print("get_text called.")
    if user_input:
        output = generate_response_davinci(user_input)
        # store the output
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

