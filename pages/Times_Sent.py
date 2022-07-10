"""
Visualize the volume of messages sent per hour, with the option to filter by participant.
"""
import datetime
import pandas as pd
import json
from fb_message import get_senders
import streamlit as st

st.title("Message by Hour")
st.markdown("This chart shows the volume of messages sent during each hour by each participant.")

def convert_time(timestamp_ms):
    return datetime.datetime.fromtimestamp(timestamp_ms/1000.0)

def get_hour(time_datetime):
    return time_datetime.hour


messages_per_hour = {}

with open("data/message.json") as message_file:
    input = json.loads(message_file.read())
    messages = input["messages"]
message_data = pd.DataFrame(messages)



message_data['timestamp_ms'] = message_data['timestamp_ms'].apply(convert_time)
message_data['hour']         = message_data['timestamp_ms'].apply(get_hour)

hours      = range(0, 24)
senders    = get_senders(input["participants"])
times_sent = pd.DataFrame(0, index=senders, columns=hours)
for sender in senders:
    for hour in hours:
        times_sent.loc[sender, hour] = sum((message_data.sender_name==sender) & (message_data.hour==hour))

st.bar_chart(times_sent.T)

st.write("Total messages sent = " + str(len(messages)))


st.write("Messages sent from " + message_data.loc[: ,"timestamp_ms"].iloc[-1].strftime("%m/%d/%Y, %H:%M:%S") + 
                        " to " + message_data.loc[: ,"timestamp_ms"].iloc[0].strftime("%m/%d/%Y, %H:%M:%S"))