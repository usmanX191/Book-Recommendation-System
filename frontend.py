import requests
import streamlit as st

# Set the page title and layout
st.set_page_config(page_title="Book Recommendation System", layout="centered")

# Initialize session state for user query, response, and thread ID
if "user_query" not in st.session_state:
    st.session_state["user_query"] = ""
if "response" not in st.session_state:
    st.session_state["response"] = ""
if "thread_id" not in st.session_state:
    # Call the backend to create a new thread
    # thread_response = requests.get("http://127.0.0.1:5000/thread")
    thread_response = requests.get(
        "https://book-recommendation-system-backend.replit.app/thread"
    )
    if thread_response.status_code == 200:
        st.session_state["thread_id"] = thread_response.json().get("thread_id")
    else:
        st.session_state["thread_id"] = None

# Main headline
st.title("Book Recommendation System")

# Input field for user query
user_query = st.text_input("Enter your query:", value=st.session_state["user_query"])
st.session_state["user_query"] = user_query  # Always sync the input with session state

# Buttons for sending and clearing input
col1, col2 = st.columns([9, 1])  # Adjust column widths for alignment
with col1:
    send_button = st.button("Send")
with col2:
    clear_button = st.button("Clear", key="clear_button")

# Handle "Clear" button functionality
if clear_button:
    st.session_state["user_query"] = ""  # Clear the text input
    st.session_state["response"] = ""  # Clear the response

# Handle "Send" button functionality
if send_button:
    if not st.session_state["user_query"]:
        st.warning("Please enter a query before sending.")  # Show warning if no input
    else:
        try:
            # API request to the backend
            api_response = requests.post(
                "https://book-recommendation-system-backend.replit.app/chat",
                json={
                    "query": st.session_state[
                        "user_query"
                    ],  # Use updated session state
                    "thread_id": st.session_state["thread_id"],
                },
            )
            if api_response.status_code == 200:
                st.session_state["response"] = api_response.json().get(
                    "response", "No response received."
                )
            else:
                st.session_state["response"] = (
                    f"Error: {api_response.status_code} - {api_response.text}"
                )
        except Exception as e:
            st.session_state["response"] = f"Failed to connect to API: {e}"

# Display the response
st.subheader("Response:")
st.write(st.session_state["response"])


# # Input field for user query
# user_query = st.text_input("Enter your query:", value=st.session_state["user_query"])

# # Buttons for sending and clearing input
# col1, col2 = st.columns([9, 1])  # Adjust column widths for alignment
# with col1:
#     send_button = st.button("Send")
# with col2:
#     clear_button = st.button("Clear", key="clear_button")

# # Handle "Clear" button functionality
# if clear_button:
#     st.session_state["user_query"] = ""  # Clear the text input
#     st.session_state["response"] = ""  # Clear the response
#     user_query = ""  # Reflect the cleared state in the input field

# # Handle "Send" button functionality
# if send_button:
#     if not user_query:
#         st.warning("Please enter a query before sending.")  # Show warning if no input
#     else:
#         st.session_state["user_query"] = user_query
#         try:
#             # API request to the backend
#             api_response = requests.post(
#                 "https://book-recommendation-system-backend.replit.app/chat",
#                 # "http://127.0.0.1:5000/chat",
#                 json={"query": user_query, "thread_id": st.session_state["thread_id"]},
#             )
#             if api_response.status_code == 200:
#                 st.session_state["response"] = api_response.json().get(
#                     "response", "No response received."
#                 )
#             else:
#                 st.session_state["response"] = (
#                     f"Error: {api_response.status_code} - {api_response.text}"
#                 )
#         except Exception as e:
#             st.session_state["response"] = f"Failed to connect to API: {e}"

# # Display the response
# st.subheader("Response:")
# st.write(st.session_state["response"])
