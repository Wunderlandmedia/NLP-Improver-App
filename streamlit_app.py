import streamlit as st
import openai
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from openai import OpenAI

# Initialize nltk
nltk.download('punkt')
nltk.download('stopwords')

def analyze_text(text):
    # Basic NLP analysis
    sentences = sent_tokenize(text)
    words = text.split()
    num_sentences = len(sentences)
    num_words = len(words)
    num_stopwords = len([word for word in words if word.lower() in stopwords.words('english')])
    
    analysis = {
        'Number of Sentences': num_sentences,
        'Number of Words': num_words,
        'Number of Stopwords': num_stopwords
    }
    return analysis

def suggest_improvements(text, api_key):
    # Set the OpenAI API key
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that provides suggestions to improve text."},
            {"role": "user", "content": f"Here is a piece of text:\n\n{text}\n\nPlease provide a list of suggestions for improving this content. Provide examples from existing content and suggestions with red colored text."}
        ]
    )

    if response.choices and len(response.choices) > 0:
        suggestions = response.choices[0].message.content.strip()
        return suggestions
    else:
        return "Error generating suggestions."

def generate_content(text, api_key):
    # Set the OpenAI API key
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that generates content based on the provided text."},
            {"role": "user", "content": f"Here is a piece of text:\n\n{text}\n\n .Generate content based on this text while improving readability and incorporating semantic related keywords in bold for emphaasis on the matter."}
        ]
    )

    if response.choices and len(response.choices) > 0:
        generated_content = response.choices[0].message.content.strip()
        return generated_content
    else:
        return "Error generating content."

def main():
    st.title("Text Analyzer and Improvement Suggestions")

    api_key = st.text_input("Enter your OpenAI API key:", type="password")
    user_input = st.text_area("Paste your text here:", height=200)

    if st.button("Analyze and Suggest"):
        if not api_key:
            st.warning("Please enter your OpenAI API key.")
        elif not user_input:
            st.warning("Please paste some text to analyze.")
        else:
            # Analyze text
            analysis = analyze_text(user_input)
            st.subheader("Text Analysis")
            st.write(analysis)
            
            # Get suggestions
            suggestions = suggest_improvements(user_input, api_key)
            st.subheader("Improvement Suggestions")
            st.write(suggestions)
            
            # Generate content
            generated_content = generate_content(user_input, api_key)
            st.subheader("Generated Content")
            st.write(generated_content)

if __name__ == "__main__":
    main()
