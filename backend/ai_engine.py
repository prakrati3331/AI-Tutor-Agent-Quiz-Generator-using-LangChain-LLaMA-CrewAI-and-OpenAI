import os
import json
import re
import logging
import httpx
from openai import OpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get API key and configuration from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://openrouter.ai/api/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "openai/gpt-3.5-turbo")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in the .env file.")


# Initialize the OpenAI client at module level
client = None



# In ai_engine.py, update the client initialization to include headers required by OpenRouter

def get_llm():
    global client
    try:
        if client is None:
            # Initialize the OpenAI client with proper configuration
            client = OpenAI(
                api_key=OPENAI_API_KEY,
                base_url=OPENAI_API_BASE,
                http_client=httpx.Client(
                    headers={
                        "Authorization": f"Bearer {OPENAI_API_KEY}",
                        "HTTP-Referer": "http://localhost:8000",
                        "Content-Type": "application/json"
                    }
                )
            )
        
        def generate_response(prompt):
            try:
                response = client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.error(f"Error generating response: {str(e)}")
                raise Exception(f"Failed to generate response: {str(e)}")
            
        return generate_response
    except Exception as e:
        logger.error(f"Error initializing LLM: {str(e)}")
        raise Exception(f"Failed to initialize AI model: {str(e)}")


# def get_llm():
#     global client
#     try:
#         if client is None:
#             # Initialize the OpenAI client with OpenRouter configuration
#             client = OpenAI(
#                 api_key=OPENAI_API_KEY,
#                 base_url=OPENAI_API_BASE,
#             )
        
#         def generate_response(prompt):
#             try:
#                 response = client.chat.completions.create(
#                     model=OPENAI_MODEL,
#                     messages=[{"role": "user", "content": prompt}],
#                     temperature=0.7
#                 )
#                 return response.choices[0].message.content
#             except Exception as e:
#                 logger.error(f"Error generating response: {str(e)}")
#                 raise Exception(f"Failed to generate response: {str(e)}")
            
#         return generate_response
#     except Exception as e:
#         logger.error(f"Error initializing LLM: {str(e)}")
#         raise Exception(f"Failed to initialize AI model: {str(e)}")

# Initialize the client when the module is imported
try:

   headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "HTTP-Referer": "http://localhost:8000",
        "Content-Type": "application/json"
    }

   client = OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_API_BASE,
        http_client=httpx.Client(headers=headers)
    )
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {str(e)}")
    raise


def generate_tutoring_response(subject, level, question, learning_style, background, language):
    """
    Generate a personalized tutoring response based on user preferences.

    Args:
         subject (str): The academic subject
         level (str): Learning level (Beginner, Intermediate, Advanced)
         question (str): User's specific question
         learning_style (str): Preferred learning style (visual Text-based, Hands-on)
         background (str): User's background knowledge
         language (str): Preferred language for response

    Returns:
         str: Formatted tutoring response
    """
    
    # Get LLM instance
    llm = get_llm()
    
    # Construct an effective prompt
    prompt = f"""
    You are a helpful tutor. Please provide a clear and concise explanation
    to the following question, tailored to the user's needs:
    
    Subject: {subject}
    Level: {level}
    Question: {question}
    Learning Style: {learning_style}
    Background: {background}
    Language: {language}
    
    Please provide a well-structured response that addresses the question
    while considering all the above factors.
    """

    try:
        # Generate response with error handling
        logger.info(f"Generating tutoring response for subject: {subject}, level: {level}")
        response = llm(prompt)

        # Post-process the response based on learning style
        return response
        
    except Exception as e:
        logger.error(f"Error generating tutoring response: {str(e)}")
        raise Exception(f"Error generating explanation: {str(e)}")


def _create_tutoring_prompt(subject, level, question, learning_style, background, language):
    """Helper function to create a well-structured tutoring prompt"""
     
    # Build the prompt with all necessary context and instruction 
    prompt = f"""
    You are an expert tutor in {subject} at the {level} level.

    STUDENT PROFILE:
    - Background knowledge: {background}
    - Learning style preferences: {learning_style}
    - Language preference: {language}

    QUESTION:
    {question}

    INSTRUCTIONS:
    1. Provide a clear, educational explanation that directly addresses the question
    2. Tailor your explanation to a {background} student at {level} level
    3. Use {language} as the primary language
    4. Format your response with appropriate markdown for readability

    LEARNING STYLE ADAPTATIONS:
    - For Visual learners: Include description of visual concepts, diagrams, or mental models
    - For Text-based learners: Provide clear, structured explanations with defined concepts
    - For Hands-on learners: Include practical examples, exercises, or applications

    Your explanations should be educational, accurate, and engaging.
    """
    return prompt

def _format_tutoring_response(content, learning_style):  # Fixed parameter name
    """Helper function to format the tutoring response based on learning style"""
    if learning_style == "Visual":  # Fixed variable name
        return content + "\n\n*Note: Visualize these concepts as you read for better retention.*"
    elif learning_style == "Hands-on":  # Now using the correct variable name
        return content + "\n\n*Tip: Try working through the examples yourself to reinforce your learning.*"
    else:
        return content


def _create_quiz_prompt(subject, level, num_questions):
    """Helper function to create a well-structured quiz generation prompt"""
    return f"""
    You are an expert quiz creator for {subject} at the {level} level.
    
    TASK:
    Create {num_questions} multiple-choice questions about {subject} suitable for a {level} level student.
    
    REQUIREMENTS:
    1. Each question should have 4 possible answers (a, b, c, d)
    2. Only one correct answer per question
    3. Include an explanation for the correct answer
    4. Questions should cover different aspects of {subject}
    5. Format your response as a JSON array of question objects
    
    RESPONSE FORMAT:
    [
        {{
            "question": "Sample question?",
            "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "correct_answer": "a",
            "explanation": "Explanation of why this is the correct answer"
        }}
    ]
    
    Generate the quiz questions now:
    """


def generate_quiz(subject, level, num_questions):
    """Helper function to create  a well-structured quiz generation prompt"""

    return f"""
    Create a {level}-level quiz on {subject} with exactly {num_questions} multiple-choice questions.

    INSTRUCTIONS:
    1. Each question should be appropriate for {level} level students
    2. Each question must have exactly 4 answer options (A, B, C, D)
    3. Clearly indicate the correct answer
    4. Cover diverse aspects of {subject}

    FORMAT YOUR RESPONSE AS JSON:
    ```json
    [
      {{
        "question": "Question text",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_answer": "Option A",
        "explanation": "Breif explanation of why this answer is correct"
      }},
      ...
    ]
    ```
    IMPORTANT: Make sure to return valid JSON that can be parsed.
    Do not include any text outside the JSON array.
    Include a breif explanation for each correct answer.
    """




def _create_fallback_quiz(subject, num_questions):
    """Helper function to create a fallback quiz if parsing fails"""

    logger.warning(f"Using feedback quiz for {subject}")
    return [
        {
            "question": f"Sample {subject} question #{i+1}",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": "Option A",
            "explanation": "This is a fallback explanation."
        }
        for i in range (num_questions)
    ]


def _validate_quiz_data(quiz_data):
    """Helper function to validate quiz data structure"""

    if not isinstance(quiz_data, list):
        raise ValueError("Quiz data must be a list of questions")

    for question in quiz_data:
        if not isinstance(question, dict):
            raise ValueError("Each quiz item must be a dictionary")

        if not all(key in question for key in ["question", "options", "correct_answer"]):
            raise ValueError("Each quiz item must have question, options, correct_answer")

    if not isinstance(question["options"], list) or len(question["options"]) !=4:
        raise ValueError("Each question must have exactly 4 options")




def _parse_quiz_response(response_content, subject, num_questions):
    """Helper function to parse and validate the quiz response"""

    try:
        # Try to find JSON content using regex
        json_match = re.search(r'```json\s*(\[[\s\S]*?\])\s*```', response_content)

        if json_match:
            # Extract JSON from code block
            quiz_json = json_match.group(1)
        else:
            # Try to find raw JSON array
            json_match = re.search(r'\[\s*\{.*\}\s*\]', response_content, re.DOTALL)
            if json_match:
                quiz_json = json_match.group(0)
            else:
                # Assume the entire response is JSON
                quiz_json = response_content
        # Parse the JSON 
        quiz_data = json.loads(quiz_json)

        # Validate the data structure
        _validate_quiz_data(quiz_data)

        # Ensure we have the requested number of questions
        if len(quiz_data) > num_questions:
            quiz_date = quiz_data[:num_questions]

        # Add explanation field if missing
        for question in quiz_data:
            if "explanation" not in question:
                question["explanation"] = f"The correct answer is {question['correct_answer']}."

        return quiz_data

    except (json.json.JSONDecodeError, ValueError) as e:
        logger.error(f"Error parsing quiz response: {str(e)}")

        # Create a fallback quiz if parsing fails
        return _create_fallback_quiz(subject, num_questions)



def generate_quiz(subject, level, num_questions=5, reveal_answer=True):
    """
    Generate a quiz with multiple-choice questions based on subject and level.

    Args:
        subject (str): The academic subject
        level (str): Learning level (Beginner, Intermediate, Advanced)
        num_questions (int): Number of questions to generate
        reveal_answer (bool): Whether to format the response with hidden answers that can be revealed 

    Returns:
         dict: Contains quiz data (list of questions) and formatted HTML if reveal_answer is True
    """

    try:
        # Get LLM response
        llm = get_llm()

        # Create a structured prompt for quiz generation
        prompt = _create_quiz_prompt(subject, level, num_questions)

        # Generate response using the chat completions API
        logger.info(f"Generating quiz for subject: {subject}, level: {level}, questions: {num_questions}")
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": f"You are an expert quiz creator for {subject} at the {level} level."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        response_content = response.choices[0].message.content

        # Parse and validate the response
        quiz_data = _parse_quiz_response(response_content, subject, num_questions)

        # Format the quiz with hidden answers if requested 
        if reveal_answer:
            formatted_quiz = _format_quiz_with_reveal(quiz_data)
            return {
                "quiz": quiz_data,  # Changed from quiz_data to quiz to match frontend expectation
                "formatted_quiz": formatted_quiz
            }
        else:
            return {
                "quiz": quiz_data  # Changed from quiz_data to quiz to match frontend expectation
            }

    except Exception as e:
        logger.error(f"Error generating quiz: {str(e)}")
        raise Exception(f"Failed to generate quiz: {str(e)}")



def _format_quiz_with_reveal(quiz_data):
    """
    Format quiz data into HTML with hidden answers that can be revealed on click.

    Args:
       quiz data (list): List of question dictionaries

    Returns:
        str: HTML string with quiz questions and hidden answers 
    """

    html = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <style>
          body {
            font-family: Arial, sans-serif;
            color: white;
            background-color: #121212;
          }

        .quiz-container {
           max-width: 800px;
           margin: 0 auto;
           padding: 20px;
        }

        .question {
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #444;
            border-radius: 10px;
            background-color: #1e1e2f;
        }

        .question h3 {
          margin-top: 0;
          color: #90caf9
        }

        .options {
          margin-left: 10px;
        }

        .option {
           margin: 10px 0;
           padding: 12px;
           border: 1px solid #555;
           border-radius: 6px;
           cursor: pointer;
           background-color: #2d2d44;
           transition: background-color 0.2s;
        }


        .option:hover {
           background-color: #3a3a5a;
        }

        .reveal-btn {
          background-color: #2196f3;
          color: white;
          border: none;
          padding: 10px 20px;
          border-radius: 5px;
          cursor: pointer;
          font-weight: bold;
          margin-top: 15px;
          transition: background-color 0.2s;
        }

        .reveal-btn:hover {
          background-color: #0d8bf2;
        }

        .answer-section {
          margin-top: 20px;
          border: 2px solid #ffeb3b;
          border-radius: 8px;
          padding: 0;
          overflow: hidden;
          display: none;
        }

        .answer-header {
          background-color: #ffeb3b:
          color: #000;
          padding: 10px;
          font-weight: bold;
          font-size: 16px;
          text-align: center;
        }
         
        .answer-content {
         padding: 15px;
         background-color: #1a237e;
        }

        .correct-answer {
           font-size: 18px;
           font-weight: bold;
           color: white;
           margin-bottom: 15px;  
        }

        .explanation {
          color: #e1f5fe;
          font-size: 16px;
          line-height: 1.5;
        }

        .selected-correct{
          background-color: #1b5e20 !important;
          border-color: #4caf50 !important;
        }

        .selected-incorrect {
          background-color: #b71c1c !important;
          border-color: #f44336 !important;
        }

      </style>

    </head>
    <body>
          <div class="quiz-container">
          <h2 style="color: #2196f3; text-align: center;
          margin-bottom: 30px;">Interactive Quiz</h2>
    """

    for i, question in enumerate(quiz_data, 1):
        option_letters = ["A", "B", "C", "D"]
        correct_index = question["options"].index(question["correct_answer"]) if question["correct_answer"] in question["options"] else 0

        html += f"""
             <div class="question" id="question-{i}">
                <h3>Question {i}</h3>
                <p>{question["question"]}</p>
                <div class="options">
        """

        for j, option in enumerate(question["options"]):
            is_correct = j == correct_index
            html += f"""
                <div class="option" id="option-{i}-{j}"
                onclick="selectOption({i}, {j}, {str(is_correct).lower()})">
                <strong>{option_letters[j]}.</strong>
                {option}
                </div>
            """

        html += f""" 
                </div>
                <button class="reveal-btn" onclick="revealAnswer({i})">SHOW ANSWER</button>
                <div class="answer-section" id="answer-{i}">
                    <div class="answer-header">CORRECT ANSWER</div>
                    <div class="answer-content">
                        <div class="correct-answer">
                            {option_letters[correct_index]}. {question["correct_answer"]}
                        </div>
                        <div class="explanation">{question.get("explanation", "")}</div>
                    </div>
                </div>
            </div>
        """

    html += """
           </div>
           <script>
               function selectOption(questionNum, optionNum, isCorrect) {
                   const questionId = `question-${questionNum}`;
                   const options = document.querySelectorAll(`#${questionId} .option`);

                   // Reset all options
                   options.forEach(option => {
                       option.className = 'option';
                   });

                   // Highlight selected option
                   const selectedOption = document.getElementById(`option-${questionNum}-${optionNum}`);
                   if (isCorrect === 'true') {
                       selectedOption.className = 'option selected-correct';
                   } else {
                       selectedOption.className = 'option selected-incorrect';
                       // Show answer if incorrect
                       revealAnswer(questionNum);
                   }
               }

               function revealAnswer(questionNum) {
                   const answerDiv = document.getElementById(`answer-${questionNum}`);
                   answerDiv.style.display = 'block';

                   // Scroll to answer
                   setTimeout(() => {
                       answerDiv.scrollIntoView({behavior: 'smooth', block: 'nearest'});
                   }, 100);

                   // Add animation for attention 
                   answerDiv.animate([
                       { transform: 'scale(1)', boxShadow: '0 0 0 rgba(255, 235, 59, 0)'},
                       { transform: 'scale(1.02)', boxShadow: '0 0 20px rgba(255, 235, 59, 0.7)'}, 
                       { transform: 'scale(1)', boxShadow: '0 0 10px rgba(255, 235, 59, 0.3)'}
                   ], {
                       duration: 1000,
                       iterations: 1
                   });
               }
           </script>
        </body>
        </html>
    """

    return html


# Export quiz to file (new function)
def export_quiz_to_html(quiz_data, file_path="quiz.html"):
    """ 
    Export the formatted quiz to an HTML file

    Args:
      quiz_data (list): List of questions dictionaries
      file_path (str): Path to save the HTML file
    """

    try:
        html_content = _format_quiz_with_reveal(quiz_data)

        with open(file_path, "w", encoding="utf-8") as f: f.write(html_content)

        logger.info(f"Quiz exported successfully to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error exporting quiz to HTML: {str(e)}")
        return False












