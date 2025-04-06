import random
import json

# Define expanded cities and specialties
cities = [
    # Major metro cities
    "Mumbai", "Delhi", "Bengaluru", "Kolkata", "Chennai", "Hyderabad", "Pune", "Ahmedabad", 
    "Coimbatore", "Kochi", "Thiruvananthapuram", "Madurai", "Visakhapatnam", "Kozhikode", 
    "Surat", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore", "Bhopal", "Patna", "Vadodara", 
    "Guwahati", "Chandigarh", "Mysore", "Tiruchirappalli", "Bhubaneswar"
]

specialties = [
    "Cardiologist", "Neurologist", "Dermatologist", "Orthopedist", 
    "Pediatrician", "Gynecologist", "General Physician", 
    "ENT Specialist", "Pulmonologist", "Psychiatrist",
    "Endocrinologist", "Ophthalmologist", "Urologist", "Allergist",
    "Rheumatologist", "Gastroenterologist", "Hematologist", "Oncologist",
    "Nephrologist", "Plastic Surgeon", "Diabetologist"
]

first_names = [
    'Amit', 'Priya', 'Rahul', 'Neha', 'Vikram', 'Sunita', 'Rajesh', 'Anjali', 'Deepak', 'Meera',
    'Ravi', 'Ananya', 'Arun', 'Kavita', 'Sanjay', 'Divya', 'Arjun', 'Pooja', 'Ajay', 'Shikha',
    'Suresh', 'Kiran', 'Rohan', 'Nisha', 'Vijay', 'Smita', 'Karthik', 'Shreya', 'Mahesh', 'Namrata',
    'Vivek', 'Asha', 'Prakash', 'Renuka', 'Aditya', 'Jaya', 'Mohan', 'Shalini', 'Venkat', 'Latha'
]

last_names = [
    'Sharma', 'Gupta', 'Patel', 'Reddy', 'Kumar', 'Verma', 'Singh', 'Chopra', 'Joshi', 'Malhotra',
    'Rao', 'Iyer', 'Shah', 'Nair', 'Kapoor', 'Jayaraman', 'Banerjee', 'Das', 'Muthu', 'Sengupta',
    'Menon', 'Ranganathan', 'Pillai', 'Agarwal', 'Chatterjee', 'Naidu', 'Bose', 'Deshmukh', 'Trivedi', 'Krishnan',
    'Mukherjee', 'Hegde', 'Murthy', 'Shenoy', 'Patil', 'Dutta', 'Deshpande', 'Saxena', 'Goswami', 'Kulkarni'
]

hospitals = [
    'Apollo Hospital', 'Fortis Healthcare', 'Max Hospital', 'AIIMS', 'Manipal Hospital',
    'Narayana Health', 'Medanta', 'Kokilaben Hospital', 'Lilavati Hospital', 'Tata Memorial',
    'Sri Ramachandra', 'CMC Vellore', 'Jaslok Hospital', 'MGM Healthcare', 'Columbia Asia',
    'Ruby Hall Clinic', 'Hinduja Hospital', 'Wockhardt Hospital', 'Care Hospital', 'Sterling Hospital',
    'Global Hospitals', 'Aster Medcity', 'Artemis Hospital', 'BLK Hospital', 'Rainbow Children\'s Hospital'
]

sub_specialties = [
    "General", "Diabetes Specialist", "Cosmetic Specialist", "Pediatric", 
    "Interventional", "Geriatric", "Sports Medicine", "Preventive Care",
    "Critical Care", "Trauma Specialist", "Minimally Invasive", "Holistic Medicine",
    "Fertility Specialist", "Addiction Medicine", "Pain Management", "Transplant Specialist"
]

# Generate any number of fictitious doctor profiles
doctors = []
for i in range(1, 900):  # Generate 500 doctor profiles
    doctor = {
        "id": i,
        "name": f"Dr. {random.choice(first_names)} {random.choice(last_names)}",
        "specialty": random.choice(specialties),
        "sub_specialty": random.choice(sub_specialties),
        "location": f"{random.choice(cities)}, India",
        "hospital": random.choice(hospitals),
        "experience": random.randint(5, 30),
        "fees": random.randint(500, 3000),
        "rating": round(random.uniform(3.5, 5.0), 1),
        "recommendedBy": f"{random.randint(80, 99)}%",
        "reviewCount": random.randint(50, 800),
        "availability": random.sample(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], random.randint(2, 5)),
        "contact": f"+91-{random.randint(7000000000, 9999999999)}",
        "languages_spoken": random.sample(["English", "Hindi", "Tamil", "Telugu", "Marathi", "Bengali", "Gujarati", "Kannada", "Malayalam", "Punjabi", "Urdu", "Odia"], random.randint(2, 4)),
        "telemedicine_available": random.choice(["Yes", "No"]),
        "emergency_services_available": random.choice(["Yes", "No"])
    }
    doctors.append(doctor)

# Convert to JSON format
doctors_json = json.dumps({"doctors": doctors}, indent=4)

# Save to a file
with open("expanded_doctor_database.json", "w") as file:
    file.write(doctors_json)

print("Doctor database generated successfully!")
