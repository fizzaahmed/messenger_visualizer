from io import StringIO
import streamlit as st
import pandas as pd
import numpy as np
import os
import json
#from common import get_senders

# define important variables
messages = []
senders  = []
message_data = pd.DataFrame()

def get_senders(participants):
    sender = []
    for participant in participants:
        sender.append(participant['name'])
    return sender


def basic_stats(jfile):
    with open(jfile) as json_file:
        input = json.load(json_file)
    
    # save messages
    messages = input["messages"]
    participants = input['participants']
    senders  = get_senders(participants)
  
    st.write("You've sent " + str(len(messages)) + " messages overall!")

    # find messages per person
    message_counts = {}
    for sender in senders:
        message_counts[sender] = 0
    for message in messages:
        message_counts[message["sender_name"]] += 1

    col1, col2 = st.columns(2)

    col1.subheader(senders[0])
    col2.subheader(senders[1])
    col1.subheader(message_counts[senders[0]])
    col2.subheader(message_counts[senders[1]])

    max_user = senders[0] if message_counts[senders[0]] > message_counts[senders[1]] else senders[1]

    st.write("Wow! It looks like " + max_user + " really likes to talk!")


def main():
    st.title("Welcome! To get started, upload your Messenger data file(JSON format only)")

    uploaded_file = st.file_uploader("Choose a file", type=['json'])
    if uploaded_file is not None:
        if not os.path.exists("data"):
            os.mkdir("data")
        new_path = os.path.join("data", "message.json")
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        saved_file = open(new_path, "w+")
        saved_file.write(stringio.read())

        st.write("Let's look at how many messages you've sent")
        basic_stats(new_path)


if __name__ == "__main__":
    main()

