import pandas as pd
import streamlit as st


def get_senders(participants):
    sender = []
    for participant in participants:
        sender.append(participant['name'])
    return sender
