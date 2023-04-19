import pandas as pd
import numpy as np
import streamlit as st
import time
import spacy
import openai
import toml

secrets = toml.load('secrets.toml')
#api_key = secrets['openai.api_key']['pinecone_api_key']
with open('secrets.toml', 'r') as f:
    secrets = toml.load(f)


# Get the OpenAI and Pinecone API keys from the secrets dictionary
openai_api_key = secrets['openai']['openai_api_key']

nlp = spacy.load("en_core_web_md")

def get_embedding(text):
    # Preprocess the input text
    text = text.strip().replace("\n", " ")

    # Create a spaCy Doc object
    doc = nlp(text)

    # Calculate the document embedding as the average of the token embeddings
    embed = doc.vector / doc.vector_norm

    return embed

df_index=pd.read_csv('only_verses.csv')

st.write("""
# GitaGPT
""")

st.write('''If you could ask Bhagavad Gita a question, what would it be?''')

st.markdown('\n')
st.markdown('\n')

def vector_similarity(x, y):
    """
    Returns the similarity between two vectors.
    Because OpenAI Embeddings are normalized to length 1, the cosine similarity is the same as the dot product.
    """
    return np.dot(np.array(x), np.array(y))

def print_verse(q, index_name):
    k=[]
    embed = get_embedding(q)
    for j in range(5):
        matches = df_index['embedding'].apply(lambda x: vector_similarity(x, embed))
        index = matches.idxmax()
        k.append(int(df_index.iloc[index]['index']))
        df_index.drop(index, inplace=True)
    return k

def return_all_verses(verse_numbers):
    return [f"{df_index['index'][i]} \n" for i in verse_numbers]

header = """You are Krishna from Mahabharata, and you're here to selflessly help and answer any question or dilemma of anyone who comes to you.
Analyze the person's question below and identify the base emotion and the root for this emotion, and then frame your answer by summarizing how your verses below
apply to their situation and be emphatetic in your answer."""

def generate_response(prompt):
    COMPLETIONS_API_PARAMS = {
        "temperature": 0.7,
        "max_tokens": 2048,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "model": "davinci"
    }
    response = openai.Completion.create(
        prompt = prompt,
        **COMPLETIONS_API_PARAMS
    )
    return response

if __name__ == '__main__':
    question = st.text_input("**How are you feeling? Ask a question or describe your situation below, and then press Enter.**", '', placeholder='Type your question here')
    if question != '':
        output = st.empty()
        st.write('Bhagvad Gita says: ') 
        verse_numbers = print_verse(question, 'bhagwadgitagpt')
        verses = return_all_verses(verse_numbers)
        verse_strings = "".join(verses)
        prompt = f'''{header}\nQuestion:{question}\nVerses:\n{verse_strings}\nAnswer:\n'''
        response = generate_response(prompt)
        st.markdown(response)
        output.markdown(response["choices"][0]["text"])
