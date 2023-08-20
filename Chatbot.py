import streamlit as st
import pandas as pd
from vertexai.preview.language_models import (ChatModel)
import csv


def process_csv_file():
    csv_file = './inputData/input.csv'
    txt_file = './inputData/input.txt'

    with open(csv_file, 'r') as csvfile:
        with open(txt_file, 'w') as txtfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                txtfile.write(','.join(row) + '\n')

    inputData = ''.join(open(txt_file, 'r').readlines())
    return inputData


def ui_text_prompt():
    st.subheader("CXO CO-PILOT")  # Add a title for the app

    input_file = st.file_uploader("Upload Input File (CSV)", type=["csv"])

    st.markdown(
        """
        <style>
        /* Change the hover border color of the file uploader */
           .stApp {
        background-color: #4d3789;
    }

    .css-1on073z .e1b2p2ww15 {
        display: flex;
    flex-direction: row;
    align-items: flex-start;
    background-color: white;
    color: black;
    }

    .css-7oyrr6 { 
    color: black;
    }

    .css-19rxjzo { 
        /* display: inline-flex; */
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 400;
    padding: 0.25rem 0.75rem;
    border-radius: 0.5rem;
    min-height: 38.4px;
    margin: 0px;
    line-height: 1.6;
    color: inherit;
    width: auto;
    user-select: none;
    background-color: rgb(19, 23, 32);
    border: 1px solid rgba(250, 250, 250, 0.2);
    color: white;
    }

    .css-19rxjzo {
      display: inline-flex; */
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 400;
    padding: 0.25rem 0.75rem;
    border-radius: 0.5rem;
    min-height: 38.4px;
    margin: 0px;
    line-height: 1.6;
    /* color: inherit; */
    width: auto;
    user-select: none;
    /* background-color: rgb(19, 23, 32); */
    border: 1px solid rgba(250, 250, 250, 0.2);
    color: white;
    background-color: red;
    cursor: pointer;
    }
    
     .css-19rxjzo:hover {
      display: inline-flex; */
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 400;
    padding: 0.25rem 0.75rem;
    border-radius: 0.5rem;
    min-height: 38.4px;
    margin: 0px;
    line-height: 1.6;
    /* color: inherit; */
    width: auto;
    user-select: none;
    /* background-color: rgb(19, 23, 32); */
    border: 1px solid rgba(250, 250, 250, 0.2);
    color: white;
    background-color: red;
    cursor: pointer;
    }
    
    .css-usj992 {
    background-color: #4d3789;
    }
    
    .st-cw  {
    max-height: none;
    background-color: white;
    }
    
    .st-ev {
        max-height: 247px;
    color: black;
    }
    
    .st-d1 {
        max-height: 247px;
    background-color: white;
    color: black;
    caret-color: black;
    # font-weight: bold;
    }
    
    .css-cio0dv {
    display: none;
    }


        /* Change the background color of the file uploader field to white */
        .stFileUploader .stFileInput {
            background-color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if input_file:
        data = pd.read_csv(input_file)
        data.to_csv('./inputData/input.csv',index=False)
        print('UPLOADED FILE CONTENT =>', data)

        contextualData = process_csv_file()

        chatModel = ChatModel.from_pretrained("chat-bison")
        params = {
            "max_output_tokens": 1024,
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40
        }
        prompt = st.chat_input("Lets talk to your Data!")
        print('Prompted Text =>', prompt)

        try:
            if prompt:
                st.write(f"CXO: {prompt}")

                contextChatBot = f'''Consider yourself as an Expolatory Data Analyst expert.
                Analyze the following Comma separated Dataset and provide the solutions asked.
                
                {contextualData}
                In the above mentioned Data:
                InvoiceNo: Unique Invoice Id,
                StockCode:  Unique Product Id,
                Product: Name of the Product,
                Quantity: Units of Product Sold,
                InvoiceDate: Date of the invoice generated,
                UnitPrice: Price per unit of the product,
                CustomerID: Unique ID of the customer,
                Country: Country,
                Revenue: Revenue of the Data
                '''

                chatBot = chatModel.start_chat(context=contextChatBot)
                getResponse = chatBot.send_message(
                    prompt, **params
                )
                print('Response =>', getResponse)
                # st.success(response)
                st.write(getResponse.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")


ui_text_prompt()
