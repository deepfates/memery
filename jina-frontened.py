import streamlit as st
import requests

# Set up some defaults
endpoint = 'http://0.0.0.0:45678/search'
top_k = 10 # Number of results to return

def get_data(query: str, endpoint: str, top_k: int) -> dict:
    headers = {
        "Content-Type": "application/json",
    }

    data = '{"top_k":' + str(top_k) + ',"mode":"search","data":["' + query + '"]}'

    response = requests.post(endpoint, headers=headers, data=data)
    content = response.json()

    matches = content["data"]["docs"][0]["matches"]

    return matches


# layout
max_width = 1200
padding = 2


st.markdown(
    f"""
<style>
    .reportview-container .main .block-container{{
        max-width: {max_width}px;
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }}
    .reportview-container .main {{
        color: "#111";
        background-color: "#eee";
    }}
</style>
""",
    unsafe_allow_html=True,
)

# Setup sidebar
st.sidebar.title("Settings")
endpoint = st.sidebar.text_input(label="Endpoint", value=endpoint)
top_k = st.sidebar.number_input(label="Top K", value=top_k, step=1)
output_format = st.sidebar.selectbox(label="Output format", options=["Plain text", "JSON", "Images"])

st.title("Simple Jina Search Frontend")

query = st.text_input(
    label="Your search term"
)

if st.button(label="Search"):
    if not query:
        st.markdown("Please enter a query")
    else:

        matches = get_data(query=query, endpoint=endpoint, top_k=top_k)
        if output_format == "JSON":
            st.json(matches)
        elif output_format == "Plain text":
            for match in matches:
                st.markdown(f"- {match['uri']}")
        elif output_format == "Images":
            for match in matches:
                st.image(match['uri'])