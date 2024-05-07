# Yarnit-assessment
Assignments for Yarnit Gen AI Engineer

Web Content QA and Content Creation API

## Introduction

This project provides an API that allows users to ask questions about web content and generate content based on specific formats and topics. It utilizes FastAPI and Streamlit frameworks for the backend and frontend, respectively.

## Features

- Web QA: Users can submit a URL and a question to get answers about web content.
- Content Creation: Users can specify a format and a topic to generate content.

## Installation

To install the project dependencies, follow these steps:

1. Clone the repository: `git clone <repository_url>`
2. Install the dependencies: `pip install -r requirements.txt`

## Usage

To run follow these steps:

1. Set the `OPENAI_API_KEY` environment variable with your OpenAI API key in the .env file.
2. Start the FastAPI server: `uvicorn api:app --reload`.
3. In a separate terminal, start the Streamlit app: `streamlit run app.py`.
4. Access the application by opening `http://localhost:8501` in your browser.
