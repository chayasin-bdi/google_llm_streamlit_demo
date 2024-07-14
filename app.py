import streamlit as st
import requests
import PyPDF2

url = 'http://localhost:5000/generate_content'
headers = {'Content-Type': 'application/json'}

with st.sidebar:
    # Streamlit input string
    input_role = st.radio(label="Select your role",
                    options=['cat','dog','upload file'],
                    captions=['answer as a cat', 'answer as a dog','answer as provided file'])
    answer_style = st.text_input("set your answer style","short answer, less than 50 words")

    # File uploader
    uploaded_file = st.file_uploader("Upload a file", type=["pdf"])

    # Include history checkbox
    include_history = st.checkbox("Include history")

# Process uploaded file if available
file_content = ''
if uploaded_file is not None:
    # Convert PDF to text
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    file_content = ""
    for page in pdf_reader.pages:
        file_content += page.extract_text()

    # Store converted text as a text file
    with open("uploaded_file.txt", "w") as f:
        f.write(file_content)

# Assign the roles
match input_role:
    case 'cat':
        role = 'answer as a cat'
    case 'dog':
        role = 'answer as a dog'
    case 'Tenten':
        if file_content:
            role = 'answer with the following data (or as the person in the following data): ' + file_content
        else:
            role = 'answer as no data since the file content is not uploaded'
    case _:
        role = 'normal answer'


st.title("💬 Tenten's Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello!!"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    if include_history:
        data = {
            'history': str(st.session_state.messages),
            'role': role,
            'answer_style': answer_style,
            'question': prompt,
        }
        print(data)
    else:
        data = {
            'role': role,
            'answer_style': answer_style,
            'question': prompt
        }
    response = requests.post(url, headers=headers, json=data)
    content = response.json()
    print(str(st.session_state.messages))
    st.session_state.messages.append({"role": "assistant", "content": content['content']})
    st.chat_message("assistant").write(content['content'])