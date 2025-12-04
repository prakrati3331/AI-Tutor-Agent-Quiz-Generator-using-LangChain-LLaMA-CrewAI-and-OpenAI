import streamlit as st
import requests
import uuid
import random
from streamlit.components.v1 import html

# Page configuration
st.set_page_config(page_title="AI Tutor", layout="wide")

# Backend connection check function
def check_backend_connection():
    try:
        response = requests.get("http://127.0.0.1:8000/health")
        if response.status_code == 200:
            return True, "✅ Backend is connected!"
        return False, f"❌ Backend error: {response.text}"
    except Exception as e:
        return False, f"❌ Cannot connect to backend: {str(e)}"

# App title and header
st.title("AI-Powered Tutor & Quiz App")

# Sidebar
with st.sidebar:
    st.header("Learning Preferences")
    subject = st.selectbox("Select Subject", ["Mathematics", "Physics", "Computer Science", "History", "Biology", "Programming"])
    level = st.selectbox("Select Learning Level", ["Beginner", "Intermediate", "Advanced"])
    learning_style = st.selectbox("Learning Style", ["Visual", "Text-based", "Hands-on"])
    language = st.selectbox("Preferred Language", ["English", "Hindi", "Spanish", "French"])
    background = st.selectbox("Background Knowledge", ["Beginner", "Some knowledge", "Experienced"])

    # Connection status
    if st.button("🔌 Check Backend Connection"):
        success, message = check_backend_connection()
        if success:
            st.success(message)
        else:
            st.error(message)

# Main content area
API_ENDPOINT = "http://127.0.0.1:8000"

# Tabs for Question and Quiz
tab1, tab2 = st.tabs(["Ask a Question", "Take a Quiz"])

with tab1:
    st.header("Ask Your Question")
    question = st.text_area("What would you like to learn today?", "Explain Newton's Second Law of Motion.")
    
    if st.button("Get Answer"):
        try:
            response = requests.post(
                f"{API_ENDPOINT}/tutor",
                json={
                    "subject": subject,
                    "level": level,
                    "learning_style": learning_style,
                    "language": language,
                    "background": background,
                    "question": question
                }
            )
            if response.status_code == 200:
                st.success("Here's your personalized explanation:")
                st.markdown(response.json().get("response", "No response from server"), unsafe_allow_html=True)
            else:
                st.error(f"Error from server: {response.text}")
        except Exception as e:
            st.error(f"Error getting explanation: {str(e)}")
            st.info(f"Make sure the backend server is running at {API_ENDPOINT}")

with tab2:
    st.header("Take a Quiz")
    
    # Add quiz controls in columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        num_questions = st.slider("Number of Questions", min_value=1, max_value=10, value=5)
    
    with col2:
        quiz_button = st.button("Generate Quiz", use_container_width=True)
    
    if quiz_button:
        with st.spinner("Creating quiz questions..."):
            try:
                # Request quiz with interactive answer reveal format
                response = requests.post(f"{API_ENDPOINT}/quiz", json={
                    "subject": subject,
                    "level": level,
                    "num_questions": num_questions,
                    "reveal_format": True
                })
                
                if response.status_code == 200:
                    response_data = response.json()
                    st.success("Quiz generated! Try answering these questions:")

                    # Check if we have formatted quiz HTML
                    if "formatted_quiz" in response_data and response_data["formatted_quiz"]:
                        # Display using HTML component
                        html(response_data["formatted_quiz"], height=num_questions * 300)
                    # Check if we have quiz data
                    elif "quiz" in response_data and response_data["quiz"]:
                        # Fallback to simple display if formatted quiz isn't available
                        for i, q in enumerate(response_data["quiz"]):
                            with st.expander(f"Question {i+1}: {q['question']}", expanded=True):
                                # Generate a random session ID to avoid conflicts between questions
                                session_id = str(uuid.uuid4())

                                # Display options as radio buttons
                                selected = st.radio(
                                    "Select your answer:", 
                                    q["options"], 
                                    key=f"q_{session_id}",
                                    index=None  # No default selection
                                )

                                # Check answer button
                                if st.button("Check Answer", key=f"check_{session_id}"):
                                    if selected == q["correct_answer"]:
                                        st.success(f"Correct! {q.get('explanation', '')}")
                                    else:
                                        st.error(f"Incorrect. The correct answer is: {q['correct_answer']}")
                    else:
                        st.error("Unexpected response format from the server")
                else:
                    st.error(f"Error from server: {response.text}")

            except Exception as e:
                st.error(f"Error generating quiz: {str(e)}")
                st.info(f"Make sure the backend server is running at {API_ENDPOINT}")
# Footer
st.markdown("---")
st.markdown("Powered by AI - Your Personal Learning Assistant")























# import streamlit as st
# import requests
# import uuid
# import random
# from streamlit.components.v1 import html


# # Page configuration
# st.set_page_config(page_title="AI Tutor", layout="wide")

# # App title
# st.title("AI-Powered Tutor & Quiz App")


# with st.sidebar:
         

#         # Add this after your existing sidebar code
#     if st.sidebar.button("🔌 Test Backend Connection"):
#         try:
#             response = requests.get("http://127.0.0.1:8000/health")
#             if response.status_code == 200:
#                 st.sidebar.success("✅ Backend is connected!")
#             else:
#                 st.sidebar.error(f"❌ Backend error: {response.text}")
#         except Exception as e:
#             st.sidebar.error(f"❌ Cannot connect to backend: {str(e)}")



#     st.header("Learning Preferences")
#     subject = st.selectbox("Select Subject", ["Mathematics", "Physics", "Computer Science", "History", "Biology", "Programming"])

#     level = st.selectbox("Select Learing Level", ["Beginner", "Intermediate", "Advanced"])

#     learning_style = st.selectbox("Learning Style", ["Visual", "Text-based", "Hands-on"])

#     language = st.selectbox("Preferred Language", ["English", "Hindi", "Spanish", "French"])

#     background = st.selectbox("Background Knowledge", ["Beginner", "Some knowledge", "Experienced"])




#     API_ENDPOINT = "http://127.0.0.1:8000"


#     tab1, tab2 = st.tabs(["Ask a Question", "Take a Quiz"])

#     with tab1:
#         # Main content area for tutoring
#         st.header("Ask Your Question")
#         question = st.text_area("What would you like to learn today?", "Explain Newton's Second Law of Motion.")


#         # Tutor section
#         if st.button("Get Explanation"):
#             with st.spinner("Generating personalized explanation..."):
#                 try:
#                     response = requests.post(f"{API_ENDPOINT}/tutor", json={
#                         "subject": subject,
#                         "level": level,
#                         "learning_style": learning_style,
#                         "language": language,
#                         "background": background,
#                         "question": question
#                     }).json()
#                     st.success("Here's your personalized explanation:")
#                     st.markdown(response["response"], unsafe_allow_html=True)
#                 except Exception as e:
#                     st.error(f"Error getting explanation: {str(e)}")
#                     st.info(f"Make sure the backend server is running at {API_ENDPOINT}")


# # Footer
# st.markdown("---")
# st.markdown("Powered by AI - Your Personal Learning Assistant")


# st.header("Test Your Knowledge")

# col1, col2 = st.columns([2, 1])

# with col1:
#     num_questions = st.slider("Number of Questions", min_value=1, max_value=10, value=5)

# with col2:
#     quiz_button = st.button("Generate Quiz", use_container_width=True)

# if quiz_button:
#     with st.spinner("Creating quiz questions..."):
#         try:
#             # Request quiz with interactive answer reveal format
#             response = requests.post(f"{API_ENDPOINT}/quiz", json={
#                 "subject": subject,
#                 "level": level,
#                 "num_questions": num_questions,
#                 "reveal_format": True
#             }).json()

#             st.success("Quiz generated! Try answering these questions:")

#             if "formatted_quiz" in response and response["formatted_quiz"]:
#                 # Display using HTML component
#                 html(response["formatted_quiz"], height=num_questions * 300)
#             else:
#                 # Fallback to simple display if formatted quiz isn't available
#                 for i, q in enumerate(response["quiz"]):
#                     with st.expander(f"Question {i+1}: {q ['question']}", expanded=True):
#                         # Generate a random session ID to avoid conflicts between questions
#                         session_id = str(uuid.uuid4())

#                         # Display options as radio buttons
#                         selected = st.radio(
#                             "Select your answer:", q["options"], key=f"q_{session_id}"
#                         )

#                         # Check answer button
#                         if st.button("Check Answer", key=f"check_{session_id}"):
#                             if selected == q["correct_answer"]:
#                                 st.success(f"Correct! {q.get('explanation', '')}")
#                             else:
#                                 st.error(f"Incorrect. The correct answer is: {q['correct_answer']}")

#         except Exception as e:
#             st.error(f"Error generating quiz: {str(e)}")
#             st.info(f"Make sure the backend server is running at {API_ENDPOINT}")


# # Footer
# st.markdown("---")
# st.markdown("Powered by AI - Your Personal Learning Assistant")

