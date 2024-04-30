import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from langchain_community.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

#loading json file
with open('/Users/muhammadsuleman/mcqgen/Response.json','r') as file:
    RESPONSE_JSON = json.load(file)

st.title("MCQ Creator")

#create a title for the app
with st.form("user_input"):
    #File upload
    upload_file=st.file_uploader("Upload a PDF or txt file")
    #Input fields
    mcq_count = st.number_input("Enter the number of MCQs you want to generate",min_value=3,max_value=50)
    #Subject
    subject = st.text_input("Insert Subject", max_chars=20)
    #Quiz tone
    tone = st.text_input("Complxity Level of Question", max_chars=20,placeholder="Simple" )
    #Submit button
    button = st.form_submit_button("Create MCQs")

    if button and upload_file is not None and mcq_count and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                text=read_file(upload_file)
                #count token and cost of the api call
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                            "text":text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Something went wrong. Please try again.")
            else:
                print(f"Total token:{cb.total_tokens}")
