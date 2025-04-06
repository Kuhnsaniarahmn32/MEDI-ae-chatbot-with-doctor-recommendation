# MEDI-AI Chatbot: Symptom to Specialist Recommendation

MedAI is an AI-powered healthcare chatbot that connects patients with the right medical specialists based on symptom analysis.

## Why MedAI?

MedAI was developed to address critical healthcare access challenges that many people face. When relocating to a new city, finding trustworthy healthcare providers is often difficult and time-consuming. Similarly, people from areas with limited healthcare infrastructure struggle to identify quality specialists they can trust.

Our application connects patients with the best and most recommended doctors in specific specialties, helping users avoid potentially fraudulent practitioners. By providing comprehensive doctor information including authentic patient reviews, transparent fee structures, available appointment dates, and communication options, MedAI empowers patients to make informed healthcare decisions regardless of their location or familiarity with local medical services.

## Problem Statement

Many patients struggle to determine which type of specialist doctor they need to consult based on their symptoms. MedAI solves this by analyzing user-provided symptoms, determining the appropriate medical specialty, and recommending qualified doctors in the patient's location with transparent information about fees, ratings, and experience.

## Features

- Natural language symptom analysis
- Location-based doctor recommendations
- Emergency situation detection
- Specialist matching based on symptom severity
- Doctor comparison by ratings, fees, and experience
- Interactive chat interface with suggestion buttons
- Dark mode support
- Multi-turn conversations with context retention
- Responsive design for mobile and desktop use

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: JSON (symptoms and doctor information)
- **NLP**: Custom symptom analysis algorithm
- **Responsive Design**: Media queries and Bootstrap grid system

## Setup Instructions

1. Clone the repository


2. Create a virtual environment :
python -m venv venv
.\venv\Scripts\Activate  (for vs code)

3. install the dependencies : pip install flask
   
4. Generate the doctor database:
   python expanded_doctor_database.py

5. Run the application:
   python app.py
   
6. Open a web browser and navigate to:
http://127.0.0.1:5000/

## Project Structure

- `app.py` - Main Flask application with routing and chatbot logic
- `expanded_doctor_database.py` - Script to generate doctor profiles
- `expanded_doctor_database.json` - Database of doctor information
- `templates/`
- `land_pg1.html` - Landing page with chatbot introduction
- `cht_pg1.html` - Chat interface for symptom analysis

## User Flow
1. User visits the landing page and learns about the chatbot's capabilities
2. User initiates chat and describes symptoms in natural language
3. System analyzes symptoms to determine appropriate specialist
4. User provides location information 
5. System recommends relevant specialists in that location
6. User can compare doctors based on ratings, fees, and experience
7. User can filter and sort results to find the most suitable doctor


## Key Differentiators

- **Symptom-to-Specialist Mapping**: Unlike general doctor directories, MedAI specifically matches symptoms to relevant specialists
- **Emergency Detection**: Identifies potentially urgent medical conditions and provides immediate guidance
- **Location-Specific Results**: Only shows doctors available in the user's specified location
- **Transparent Comparison**: Allows users to make informed decisions based on multiple factors
- **Natural Language Understanding**: No need for medical terminology - describe symptoms in your own words

## Contributors

- Kuhnsaniarahmn32



## Future Enhancements

- **Appointment Scheduling**: Direct integration with doctor calendars for real-time booking
- **Multi-language Support**: Extending the chatbot to support regional languages
- **Voice Interface**: Adding speech recognition for hands-free interaction
- **Medical History Integration**: Secure storage of patient history for more personalized recommendations
- **Insurance Coverage Filtering**: Showing doctors who accept specific insurance plans
- **Telemedicine Integration**: Direct video consultation capabilities with recommended specialists
- **Machine Learning Improvements**: Continuous enhancement of symptom analysis accuracy
- **Mobile App Version**: Native applications for iOS and Android
- **Specialist Verification System**: Enhanced verification of doctor credentials
- **Patient Community Features**: Reviews and experiences from patients with similar symptoms



