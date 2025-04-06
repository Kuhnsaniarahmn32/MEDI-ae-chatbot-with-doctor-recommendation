from flask import Flask, request, jsonify, render_template
import json
import re
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
SPECIALTIES = [
    "Neurologist", "Gastroenterologist", "Cardiologist", "Dermatologist",
    "ENT Specialist", "General Physician", "Orthopedist", "Pulmonologist",
    "Urologist", "Allergist", "Endocrinologist", "Ophthalmologist",
    "Rheumatologist", "Psychiatrist", "Gynecologist"
]

# Expanded locations across India
INDIA_LOCATIONS = [
    # Major metro cities
    "Mumbai", "Delhi", "Bengaluru", "Kolkata", "Chennai", "Hyderabad", "Pune", "Ahmedabad", "Patna",
    "Coimbatore", "Kochi", "Thiruvananthapuram", "Madurai", "Visakhapatnam", "Kozhikode", "Malappuram",
    # Additional major cities
    "Surat", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore", "Bhopal", "Vadodara", "Ludhiana", 
    "Agra", "Nashik", "Faridabad", "Ghaziabad", "Rajkot", "Varanasi", "Srinagar", "Amritsar",
    "Prayagraj", "Guwahati", "Chandigarh", "Jodhpur", "Mysore", "Tiruchirappalli", "Bhubaneswar",
    # Major states
    "Maharashtra", "Tamil Nadu", "Karnataka", "Uttar Pradesh", "Gujarat", "West Bengal", "Rajasthan",
    "Kerala", "Punjab", "Haryana", "Telangana", "Andhra Pradesh", "Bihar", "Odisha", "Assam",
    # Additional states & union territories
    "Madhya Pradesh", "Chhattisgarh", "Jharkhand", "Uttarakhand", "Himachal Pradesh", 
    "Jammu and Kashmir", "Meghalaya", "Manipur", "Mizoram", "Nagaland", "Tripura", "Sikkim", "Goa",
    "Puducherry", "Ladakh", "Andaman and Nicobar Islands", "Lakshadweep",
    # Delhi areas
    "Pahar Ganj", "Connaught Place", "Karol Bagh", "Lajpat Nagar",
    "Dwarka", "Rohini", "Saket", "Pitampura", "Vasant Kunj", "Janakpuri"
]

SYMPTOM_INDICATORS = [
    'pain', 'ache', 'sore', 'hurt', 'discomfort', 'fever', 'cough',
    'headache', 'nausea', 'vomiting', 'dizziness', 'weakness',
    'breathing', 'chest', 'heart', 'blood', 'bleeding', 'severe',
    'difficulty', 'problem', 'issue', 'symptom', 'feeling', 'sick',
    'attack', 'infection', 'disease', 'condition', 'disorder'
]

CARDIAC_INDICATORS = [
    'chest pain', 'heart pain', 'chest pressure', 'heart attack', 'heartattack',
    'chest tightness', 'palpitation', 'racing heart', 'irregular heartbeat',
    'heavy heart', 'cardiac', 'cardiovascular'
]

BREATHING_INDICATORS = [
    'shortness of breath', 'difficulty breathing', "can't breathe",
    'trouble breathing', 'breathlessness'
]

SEVERE_INDICATORS = ["severe", "extreme", "unbearable", "worst", "intense", "excruciating"]
MODERATE_INDICATORS = ["moderate", "uncomfortable", "distressing", "significant"]

# Initialize Flask app
app = Flask(__name__)

# Store conversation states
conversation_states = {}

def load_json_file(file_path, default_value):
    """Load JSON data from a file with error handling."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading {file_path}: {e}")
        return default_value

# Load data files
symptoms_data = load_json_file('datamed/symptoms_int.json', {"intents": [], "hierarchies": {}, "age_routing": {}, "gender_routing": {}})
doctors_data = load_json_file('expanded_doctor_database.json', {"doctors": []})

def preprocess_text(text):
    """Convert text to lowercase and remove punctuation."""
    return re.sub(r'[^\w\s]', '', text.lower())

def match_gender(text):
    """Identify gender from text."""
    text = text.lower()
    if any(word in text for word in ["female", "woman", "girl"]): return "female"
    if any(word in text for word in ["male", "man", "boy"]): return "male"
    return "unspecified"

def determine_severity(symptoms):
    """Determine symptom severity."""
    if any(indicator in symptoms for indicator in SEVERE_INDICATORS): return "severe"
    if any(indicator in symptoms for indicator in MODERATE_INDICATORS): return "moderate"
    return "mild"

def is_likely_symptoms(text):
    """Determine if text describes symptoms."""
    text = text.lower()
    
    # Check for symptom indicators
    has_symptom_words = any(indicator in text for indicator in SYMPTOM_INDICATORS)
    has_cardiac_words = any(indicator in text for indicator in CARDIAC_INDICATORS)
    has_breathing_words = any(indicator in text for indicator in BREATHING_INDICATORS)
    
    return has_symptom_words or has_cardiac_words or has_breathing_words

def is_likely_location(text):
    """Determine if text describes a location."""
    text = text.lower()
    
    # Check for direct location matches
    for location in INDIA_LOCATIONS:
        if location.lower() in text:
            return True
    
    # Check for location indicators
    location_indicators = ["in", "from", "at", "near", "location", "city", "area"]
    return any(indicator in text for indicator in location_indicators)

def extract_location(text):
    """Extract location from text."""
    text_lower = text.lower()
    
    # Check for direct location matches
    for location in INDIA_LOCATIONS:
        if location.lower() in text_lower:
            return location
    
    # Check for location patterns
    location_indicators = ["in", "from", "at", "near", "location is", "city is", "area is"]
    for indicator in location_indicators:
        if indicator in text_lower:
            parts = text_lower.split(indicator)
            if len(parts) > 1:
                potential_location = parts[1].strip()
                # Take first few words as potential location
                potential_location = ' '.join(potential_location.split()[:2])
                # Filter out common words and very short strings
                common_words = ["the", "a", "an", "and", "but", "or", "for", "with", "is", "am", "my"]
                if potential_location and potential_location not in common_words and len(potential_location) > 2:
                    return potential_location.title()
    
    return None

def recognizes_specialty_request(message):
    """Check if message contains a direct request for a specialist."""
    message = message.lower()
    specialty_map = {
        "cardiologist": "Cardiologist",
        "heart doctor": "Cardiologist",
        "heart specialist": "Cardiologist",
        "neurologist": "Neurologist",
        "gastroenterologist": "Gastroenterologist",
        "dermatologist": "Dermatologist",
        "ent": "ENT Specialist",
        "orthopedist": "Orthopedist",
        "pulmonologist": "Pulmonologist",
        "urologist": "Urologist",
        "allergist": "Allergist",
        "endocrinologist": "Endocrinologist",
        "ophthalmologist": "Ophthalmologist",
        "rheumatologist": "Rheumatologist",
        "psychiatrist": "Psychiatrist",
        "gynecologist": "Gynecologist"
    }
    
    for key, specialty in specialty_map.items():
        if key in message:
            return specialty
    
    return None

def detect_emergency(symptoms):
    """Check for critical cardiac/breathing symptoms."""
    symptoms = preprocess_text(symptoms)
    has_cardiac = any(indicator in symptoms for indicator in CARDIAC_INDICATORS)
    has_breathing = any(indicator in symptoms for indicator in BREATHING_INDICATORS)
    return has_cardiac or has_breathing  # Using OR for better sensitivity

def get_recommended_doctors(specialty, location=None, limit=5):
    """Get top-rated doctors matching specialty and location."""
    # Add debugging to track function calls
    print(f"Searching for {specialty} in {location}")
    
    if not location:
        # If no location provided, return top doctors of that specialty
        filtered = [d for d in doctors_data.get("doctors", []) if d.get("specialty") == specialty]
        return sorted(filtered, key=lambda x: x.get("rating", 0), reverse=True)[:limit], False
    else:
        # Normalize location for better matching
        location_lower = location.lower().strip()
        
        # Primary search: exact location match
        filtered = [d for d in doctors_data.get("doctors", []) 
                   if d.get("specialty") == specialty and 
                   location_lower in d.get("location", "").lower()]
        
        print(f"First filter - exact match: Found {len(filtered)} doctors")
        
        # If no matches, try with location as standalone word
        if not filtered:
            filtered = [d for d in doctors_data.get("doctors", []) 
                      if d.get("specialty") == specialty and
                      any(loc.lower() == location_lower for loc in d.get("location", "").lower().split(', '))]
            
            print(f"Second filter - word match: Found {len(filtered)} doctors")
        
        # Try with city variations
        if not filtered:
            # Add common variations of cities
            city_variations = {
                "delhi": ["delhi", "new delhi", "delhi ncr"],
                "mumbai": ["mumbai", "bombay"],
                "bangalore": ["bangalore", "bengaluru"],
                # Add more as needed
            }
            
            # Check if we have variations for this city
            variations = city_variations.get(location_lower, [location_lower])
            
            # Try matching with any variation
            filtered = [d for d in doctors_data.get("doctors", []) 
                      if d.get("specialty") == specialty and
                      any(var in d.get("location", "").lower() for var in variations)]
            
            print(f"Third filter - variations: Found {len(filtered)} doctors")
            
            # REMOVED: Final fallback to return doctors regardless of location
            # Instead, signal that no location match was found
            if not filtered:
                print(f"No doctors found for {specialty} in {location}")
                return [], True
        
        # Return sorted results
        return sorted(filtered, key=lambda x: x.get("rating", 0), reverse=True)[:limit], False

def analyze_symptoms(symptoms_text, gender='unspecified'):
    """Analyze symptoms and determine appropriate specialty."""
    try:
        symptoms = preprocess_text(symptoms_text)
        severity = determine_severity(symptoms)
        gender = gender if gender != 'unspecified' else match_gender(symptoms_text)
        
        # Emergency detection
        if detect_emergency(symptoms):
            return {
                "specialty": "Cardiologist",
                "severity": "severe",
                "is_emergency": True,
                "matched_symptoms": [s for s in CARDIAC_INDICATORS + BREATHING_INDICATORS if s in symptoms]
            }
        
        # Symptom pattern matching
        for intent in symptoms_data.get("intents", []):
            if any(pattern in symptoms for pattern in intent.get("patterns", [])):
                specialty = intent.get("responses", ["General Physician"])[0]
                if intent.get("severity_mapping"):
                    specialty = intent["severity_mapping"].get(severity, specialty)
                return {
                    "specialty": specialty,
                    "severity": severity,
                    "matched_symptoms": [p for p in intent["patterns"] if p in symptoms]
                }
        
        return {"specialty": "General Physician", "severity": severity}
    
    except Exception as e:
        logging.error(f"Symptom analysis error: {str(e)}")
        return {"specialty": "General Physician"}

@app.route('/')
def home():
    return render_template('land_pg1.html')

@app.route('/chat')
def chat():
    return render_template('cht_pg1.html')

@app.route('/chat_api', methods=['POST'])
def handle_chat():
    
    user_id = request.json.get('user_id', f"user_{os.urandom(4).hex()}")
    message = request.json.get('message', '').strip()
    
    # Initialize or get conversation state
    state = conversation_states.setdefault(user_id, {
        'stage': 'greeting',
        'location': None,
        'symptoms': None,
        'gender': 'unspecified'
    })
    
    # Add debugging to track conversation state
    print(f"Message: '{message}', Current state: {state}")
    
    # Extract gender if provided
    current_gender = state.get('gender')
    state['gender'] = match_gender(message) if match_gender(message) != 'unspecified' else current_gender
    
    # Check for location update
    if is_likely_location(message) and not is_likely_symptoms(message):
        location = extract_location(message)
        if location:
            old_location = state.get('location')
            state['location'] = location
            
            # If we already have symptoms, process them with new location
            if state.get('symptoms'):
                analysis = analyze_symptoms(state['symptoms'], state.get('gender'))
                doctors, location_match_failed = get_recommended_doctors(analysis['specialty'], state['location'])
                
                location_msg = f"I've updated your location to {state['location']}. "
                
                if analysis.get('is_emergency'):
                    return jsonify(
                        response=f"{location_msg}⚠️ EMERGENCY: Please seek immediate care! Here are cardiologists:",
                        doctors=doctors,
                        is_emergency=True,
                        conversation_complete=True
                    )
                
                if not doctors:
                    return jsonify(
                        response=f"{location_msg}No {analysis['specialty']} specialists found in {state['location']}. Please try a different location.",
                        doctors=[],
                        conversation_complete=True
                    )
                
                return jsonify(
                    response=f"{location_msg}Recommended {analysis['specialty']} specialists:",
                    doctors=doctors,
                    conversation_complete=True
                )
            else:
                state['stage'] = 'get_symptoms'
                return jsonify(response=f"I've set your location to {location}. Please describe your symptoms.")
    
    # Check for direct specialty request
    requested_specialty = recognizes_specialty_request(message)
    if requested_specialty:
        doctors, location_match_failed = get_recommended_doctors(requested_specialty, state.get('location'))
        
        if not doctors:
            if location_match_failed:
                return jsonify(
                    response=f"No {requested_specialty} specialists found in {state.get('location', 'your area')}. Please try a different location.",
                    doctors=[],
                    conversation_complete=True
                )
            else:
                return jsonify(
                    response=f"No {requested_specialty} specialists found in our database.",
                    doctors=[],
                    conversation_complete=True
                )
        
        return jsonify(
            response=f"Recommended {requested_specialty} specialists:",
            doctors=doctors,
            conversation_complete=True
        )
    
    # Handle conversation flow
    if state['stage'] == 'greeting':
        state['stage'] = 'get_symptoms'
        return jsonify(response="Hello! I'm MedAI. Please describe your symptoms or health concerns.")
    
    elif state['stage'] == 'get_symptoms':
        if is_likely_symptoms(message):
            state['symptoms'] = message
            
            # If location is already provided, process
            if state.get('location'):
                analysis = analyze_symptoms(state['symptoms'], state.get('gender'))
                doctors, location_match_failed = get_recommended_doctors(analysis['specialty'], state['location'])
                
                if analysis.get('is_emergency'):
                    return jsonify(
                        response="⚠️ EMERGENCY: Please seek immediate care! Here are cardiologists:",
                        doctors=doctors,
                        is_emergency=True,
                        conversation_complete=True
                    )
                
                if not doctors:
                    return jsonify(
                        response=f"No {analysis['specialty']} specialists found in {state['location']}. Please try a different location or specialty.",
                        doctors=[],
                        conversation_complete=True
                    )
                
                return jsonify(
                    response=f"Recommended {analysis['specialty']} specialists:",
                    doctors=doctors,
                    conversation_complete=True
                )
            else:
                state['stage'] = 'get_location'
                return jsonify(response="Thank you. Which city or state in India are you located?")
        else:
            # Not recognizable as symptoms, might be location
            location = extract_location(message)
            if location:
                state['location'] = location
                return jsonify(response=f"I've set your location to {location}. Please describe your symptoms.")
            else:
                return jsonify(response="I couldn't understand your symptoms. Please describe what health issues you're experiencing.")
    
    elif state['stage'] == 'get_location':
        location = extract_location(message)
        if location:
            state['location'] = location
        else:
            # If we can't extract a specific location, use the message as-is
            state['location'] = message
        
        # Process symptoms with location
        analysis = analyze_symptoms(state['symptoms'], state.get('gender'))
        doctors, location_match_failed = get_recommended_doctors(analysis['specialty'], state['location'])
        
        if analysis.get('is_emergency'):
            return jsonify(
                response="⚠️ EMERGENCY: Please seek immediate care! Here are cardiologists:",
                doctors=doctors,
                is_emergency=True,
                conversation_complete=True
            )
        
        if not doctors:
            return jsonify(
                response=f"No {analysis['specialty']} specialists found in {state['location']}. Please try a different location or specialty.",
                doctors=[],
                conversation_complete=True
            )
        
        return jsonify(
            response=f"Recommended {analysis['specialty']} specialists:",
            doctors=doctors,
            conversation_complete=True
        )
    
    # If user provides symptoms at any point, process them
    if is_likely_symptoms(message):
        state['symptoms'] = message
        
        # If we don't have location yet, ask for it
        if not state.get('location'):
            state['stage'] = 'get_location'
            return jsonify(response="Thank you. Which city or state in India are you located?")
        
        # Process with existing location
        analysis = analyze_symptoms(state['symptoms'], state.get('gender'))
        doctors, location_match_failed = get_recommended_doctors(analysis['specialty'], state['location'])
        
        if analysis.get('is_emergency'):
            return jsonify(
                response="⚠️ EMERGENCY: Please seek immediate care! Here are cardiologists:",
                doctors=doctors,
                is_emergency=True,
                conversation_complete=True
            )
        
        if not doctors:
            return jsonify(
                response=f"No {analysis['specialty']} specialists found in {state['location']}. Please try a different location or specialty.",
                doctors=[],
                conversation_complete=True
            )
        
        return jsonify(
            response=f"Recommended {analysis['specialty']} specialists:",
            doctors=doctors,
            conversation_complete=True
        )
    
    # Fallback
    return jsonify(response="I didn't understand that. Please tell me your symptoms or location.", conversation_complete=False)

@app.route('/analyze', methods=['POST'])
def api_analyze():
    data = request.json
    analysis = analyze_symptoms(
        data.get('symptoms', ''),
        data.get('gender', 'unspecified')
    )
    doctors, location_match_failed = get_recommended_doctors(analysis['specialty'], data.get('location'))
    
    if not doctors and location_match_failed:
        analysis["message"] = f"No {analysis['specialty']} specialists found in {data.get('location')}."
    
    return jsonify({**analysis, "doctors": doctors})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
