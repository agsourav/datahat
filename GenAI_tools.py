#In this Python script we shall learn to
# * Build generative AI tools using Hugging Face
# * Deploy it using streamlit

#Installation
#pip install transformers
#pip install streamlit
import transformers
from transformers import pipeline
import streamlit as st


st.title("Building Generative AI tool")

"""
The pipelines are a great and easy way to use models for inference. These pipelines are objects that abstract most of the 
complex code from the library, offering a simple API dedicated to several tasks, including Named Entity Recognition, 
Masked Language Modeling, Sentiment Analysis, Feature Extraction and Question Answering
"""

st.subheader("Converting text to speech")

text = st.text_input("enter your text here...", value="")

pipe = pipeline("text-to-speech", model="suno/bark-small", device="cuda")
print(pipe)
output = pipe(text)
st.audio(output["audio"], sample_rate=output["sampling_rate"])
