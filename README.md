# Learning Helper Assistant

## Overview
The Learning Helper Assistant is an AI-powered educational platform that personalizes the learning experience. Users can upload any PDF book to learn its concepts through Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs). The system is designed for adaptive and user-centric learning.

## Features
- **Personalized Learning**: Dynamic paths tailored to user progress.
- **RAG Integration**: Combines retrieval-based and generative AI for accurate responses.
- **Chatbot Interaction**: Context-aware and interactive learning environment.
- **Custom Assessments**: Automated quiz and test generation.
- **Podcast Creation**: Converts learning modules into audio format.
- **Progress Tracking**: Monitors user advancement.

## Technologies Used
- **Backend**: Python Flask
- **Database**: SQLite (for user data), ChromaDB (for vector storage)
- **APIs**: Ollama & Groq for AI capabilities
- **Frontend**: HTML, CSS, and JavaScript (with Tailwind CSS for styling)

## Installation and Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/<username>/learning-helper-assistant.git
   cd learning-helper-assistant
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure API keys:
   - Obtain keys for Groq and Play.ai.
   - Add them to `models/config.py`.
4. Initialize the database:
   ```bash
   python models/db/db_init.py
   ```
5. Start the server:
   ```bash
   python main.py
   ```

## Usage
- **User Authentication**: Register or log in to access the platform.
- **Upload PDF**: Add course content for personalized learning paths.
- **Interactive Chat**: Engage with the chatbot for topic discussions and questions.
- **Take Tests**: Assess understanding through custom quizzes.
- **Generate Podcasts**: Convert learning topics into podcasts for accessibility.

## Directory Structure
```
└── Raviteja-5976-Learning-Helper-Assistant/
    ├── README.md
    ├── LICENSE
    ├── __init__.py
    ├── main.py
    ├── requirements.txt
    ├── chroma/
    ├── learning_helper_assistant/
    ├── models/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── config01.py
    │   ├── __pycache__/
    │   ├── authentication/
    │   │   ├── auth.py
    │   │   └── __pycache__/
    │   ├── db/
    │   │   ├── db_init.py
    │   │   └── __pycache__/
    │   ├── my_courses/
    │   │   ├── course_chat.py
    │   │   ├── course_embed.py
    │   │   ├── course_exam.py
    │   │   ├── course_podcast.py
    │   │   ├── courses.py
    │   │   └── __pycache__/
    │   └── rapid_learner/
    │       ├── rapid_chat.py
    │       └── __pycache__/
    └── templates/
        ├── base.html
        ├── course_chat.html
        ├── course_desc.html
        ├── course_exam.html
        ├── courses.html
        ├── courses_popup.html
        ├── index.html
        ├── login.html
        ├── rapid_chat.html
        ├── rapid_chat_popup.html
        └── register.html


## Future Scope
- Cross-platform compatibility for mobile devices.
- Enhanced AI capabilities for deeper insights.
- Integration with external learning platforms.

## Contribution
Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request.

## License
This project is licensed under the MIT License.

