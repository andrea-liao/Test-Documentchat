import streamlit as st
import pandas as pd
from openai import OpenAI

# Show title and description.
st.title(" CSV Data Analysis with OpenAI")
st.write(
    "Upload a CSV file and ask a question about the data – GPT will analyze it! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🔑")
else:
    # Create an OpenAI client
    client = OpenAI(api_key=openai_api_key)
    
    # Let the user upload a CSV file
    uploaded_file = st.file_uploader("Upload a CSV file", type=("csv"))
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("### Preview of Uploaded Data:")
        st.dataframe(df.head())
        
        # Convert DataFrame to a string representation (limit rows for token efficiency)
        csv_string = df.to_csv(index=False)
        
        # Ask the user for a question
        question = st.text_area(
            "Now ask a question about the data!",
            placeholder="What insights can you draw from this data?",
        )
        
        if question:
            # Process the uploaded file and question
            messages = [
                {
                    "role": "user",
                    "content": f"""Here's a dataset:
                    ```csv
                    {csv_string[:5000]}  # Limit input size for token efficiency
                    ```
                    
                    Now, answer this question: {question}""",
                }
            ]
            
            # Generate an answer using OpenAI API
            stream = client.chat.completions.create(
                model="gpt-4-turbo",  # Use GPT-4-turbo for better reasoning
                messages=messages,
                stream=True,
            )
            
            # Stream the response
            st.write("### AI's Analysis:")
            st.write_stream(stream)

