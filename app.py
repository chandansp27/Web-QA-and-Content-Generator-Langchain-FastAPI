import streamlit as st
import requests


def send_api_request(endpoint, param1, param2):
    url = f"http://127.0.0.1:8000/{endpoint}/"
    if endpoint == 'web_qa':
        payload = {'url': param1, 'question': param2}
        response = requests.post(url, json=payload)
        return response.json()['answer']
    elif endpoint == 'content_creation':
        payload = {'format': param1, 'topic': param2}
        response = requests.post(url, json=payload)
        return response.json()['text']
    return 'API fetch invalid'


def main():
    option = st.sidebar.selectbox("Select an option", ("Web Chat", "Content Creator"))

    if option == "Web Chat":
        st.title('Web Chat')
        endpoint = 'web_qa'
        web_url = st.text_input("Enter Web URL")
        question = st.text_input('Enter your question')
        if st.button("Start Chat"):
            data = {"url": web_url, "question": question}  
            response = send_api_request(endpoint, web_url, question)  
            st.write(response)

    elif option == "Content Creator":
        st.title('Content Creator')
        format_text = st.text_input("Enter Format")
        topic_text = st.text_input("Enter Topic")
        if st.button("Create Content"):
            endpoint = 'content_creation'
            data = {"format": format_text, "topic": topic_text}
            response = send_api_request(endpoint, data['format'], data['topic'])
            st.write(response)


if __name__ == "__main__":
    main()
