import pandas as pd
import os
from apikey import apikey
import streamlit as st
from langchain.llms import OpenAI
from langchain.agents import create_csv_agent
from dotenv import load_dotenv

# Your subsequent code...

os.environ['OPENAI_API_KEY'] = apikey

def main():
    load_dotenv()
    
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")
    
    st.set_page_config(page_title= "Abbey asks CSV")
    st.header("Ask your CSV")
    
    csv_file = st.file_uploader("Upload a CSV file", type="csv")
    
    if csv_file is not None:
        # Save the uploaded CSV to a temporary file
        temp_path = "temp.csv"
        with open(temp_path, "wb") as f:
            f.write(csv_file.getvalue())

        agent = create_csv_agent(
            OpenAI(temperature=0), temp_path, verbose=True)

        user_question = st.text_input("Ask a question about your CSV: ")

        if user_question is not None and user_question != "":
            with st.spinner(text="In progress..."):
                st.write(agent.run(user_question))

        # Remove the temporary file
        os.remove(temp_path)
        
if __name__ == "__main__":
    main()
