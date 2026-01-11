from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Get the base path for models
MODELS_PATH = os.path.join(os.path.dirname(__file__), 'models')

# Load the trained model and encoders
model = joblib.load(os.path.join(MODELS_PATH, 'welfare_model.pkl'))
encoders = joblib.load(os.path.join(MODELS_PATH, 'all_encoders.pkl'))

# Load doctor and hospital data
doctors_df = pd.read_csv(os.path.join(MODELS_PATH, 'All_Doctor list.csv'), encoding='latin-1')
hospitals_df = pd.read_csv(os.path.join(MODELS_PATH, 'All_Hospital list.csv'), encoding='latin-1')

# Load investment models (in backend folder, not models subfolder)
BACKEND_PATH = os.path.dirname(__file__)
investment_encoders = joblib.load(os.path.join(BACKEND_PATH, '1.pkl'))
investment_kmeans = joblib.load(os.path.join(BACKEND_PATH, '2.pkl'))

# Mapping from form values to encoder values
SEX_FORM_TO_ENCODER = {
    'male': 'M',
    'female': 'F'
}

EDUCATION_FORM_TO_ENCODER = {
    'no-education': 'Primary',
    'primary': 'Primary',
    'secondary': 'Secondary',
    'olevel': 'Secondary',
    'alevel': 'Diploma',
    'diploma': 'Diploma',
    'degree': 'Degree',
    'postgraduate': 'Postgraduate'
}

EMPLOYMENT_FORM_TO_ENCODER = {
    'unemployed': 'Unemployed',
    'student': 'Unemployed',
    'retired': 'Retired',
    'self-employed': 'Self-employed',
    'employed': 'Employed',
    'unable-to-work': 'Unemployed'
}

def find_specialists(medical_condition, symptoms):
    """Find relevant specialists based on medical condition and symptoms"""
    search_terms = f"{medical_condition} {symptoms}".lower()
    matching_specialists = []
    
    for _, row in doctors_df.iterrows():
        diseases = str(row['Diseases_Treated']).lower()
        matched_terms = [term for term in search_terms.split() if len(term) > 2 and term in diseases]
        if matched_terms:
            matching_specialists.append({
                'specialist': row['Specialist'],
                'treats': row['Diseases_Treated'][:150] + '...' if len(str(row['Diseases_Treated'])) > 150 else row['Diseases_Treated'],
                'matchScore': len(matched_terms)
            })
    
    # Sort by match score (best matches first)
    matching_specialists.sort(key=lambda x: x['matchScore'], reverse=True)
    
    # If no matches, return general practitioners
    if not matching_specialists:
        matching_specialists = [
            {'specialist': 'General Practitioner', 'treats': 'General health conditions, initial consultations', 'matchScore': 0},
            {'specialist': 'Internal Medicine Specialist', 'treats': 'General adult medical conditions', 'matchScore': 0}
        ]
    
    return matching_specialists[:5]  # Return top 5

def get_treatment_recommendations(medical_condition, symptoms):
    """Generate treatment recommendations based on condition and symptoms"""
    condition_lower = medical_condition.lower()
    symptoms_lower = symptoms.lower()
    
    treatments = []
    
    # Common condition-based treatments
    treatment_mapping = {
        'diabetes': [
            'Blood sugar monitoring and HbA1c tests',
            'Dietary consultation with a nutritionist',
            'Oral medication or insulin therapy as prescribed',
            'Regular foot and eye examinations',
            'Lifestyle modifications and exercise program'
        ],
        'heart': [
            'ECG and echocardiogram tests',
            'Blood pressure monitoring',
            'Cholesterol management medication',
            'Cardiac rehabilitation program',
            'Stress management and dietary changes'
        ],
        'hypertension': [
            'Regular blood pressure monitoring',
            'Antihypertensive medication as prescribed',
            'Low-sodium diet plan',
            'Regular cardiovascular exercise',
            'Stress reduction techniques'
        ],
        'fever': [
            'Blood tests to identify infection',
            'Antipyretic medication (paracetamol)',
            'Rest and adequate hydration',
            'Monitor temperature regularly',
            'Seek immediate care if fever persists over 3 days'
        ],
        'pain': [
            'Physical examination to identify source',
            'Pain management medication',
            'Physiotherapy if musculoskeletal',
            'Imaging tests if needed (X-ray, MRI)',
            'Follow-up consultation based on diagnosis'
        ],
        'respiratory': [
            'Chest X-ray and pulmonary function tests',
            'Bronchodilator or inhaler therapy',
            'Antibiotics if bacterial infection suspected',
            'Steam inhalation and rest',
            'Avoid smoking and pollutants'
        ],
        'skin': [
            'Dermatological examination',
            'Topical medications or creams',
            'Allergy tests if needed',
            'Skin biopsy for suspicious lesions',
            'Sun protection and skincare routine'
        ],
        'mental': [
            'Psychological assessment',
            'Counseling or therapy sessions',
            'Medication if recommended by psychiatrist',
            'Support group participation',
            'Stress management and lifestyle changes'
        ],
        'gastro': [
            'Endoscopy or colonoscopy if needed',
            'Dietary modifications',
            'Antacids or proton pump inhibitors',
            'Probiotic supplements',
            'Stress reduction and regular meal times'
        ]
    }
    
    # Find matching treatments
    for condition, treatment_list in treatment_mapping.items():
        if condition in condition_lower or condition in symptoms_lower:
            treatments.extend(treatment_list)
    
    # Add general treatments if none found
    if not treatments:
        treatments = [
            'Complete blood count (CBC) and basic metabolic panel',
            'Physical examination by a general physician',
            'Diagnostic tests based on symptoms',
            'Medication as prescribed by doctor',
            'Follow-up appointment for monitoring'
        ]
    
    return treatments[:6]  # Return up to 6 treatments

def find_hospitals(district, is_eligible):
    """Find hospitals in the user's district"""
    # Normalize district name for matching
    district_normalized = district.lower().replace('-', ' ').title()
    
    # Filter hospitals by district
    district_hospitals = hospitals_df[hospitals_df['District'].str.lower() == district_normalized.lower()]
    
    if district_hospitals.empty:
        # Try partial match
        district_hospitals = hospitals_df[hospitals_df['District'].str.lower().str.contains(district.lower()[:4])]
    
    hospitals_list = []
    
    if is_eligible:
        # Prioritize government hospitals for eligible users
        govt_hospitals = district_hospitals[district_hospitals['Type'] == 'Government']
        private_hospitals = district_hospitals[district_hospitals['Type'] == 'Private']
        
        for _, row in govt_hospitals.head(3).iterrows():
            hospitals_list.append({
                'name': row['Hospital'],
                'type': 'Government',
                'note': 'Free/subsidized care available'
            })
        
        for _, row in private_hospitals.head(2).iterrows():
            hospitals_list.append({
                'name': row['Hospital'],
                'type': 'Private',
                'note': 'Paid services'
            })
    else:
        # Show all hospitals for non-eligible users
        for _, row in district_hospitals.head(5).iterrows():
            hospitals_list.append({
                'name': row['Hospital'],
                'type': row['Type'],
                'note': 'Subsidized rates available' if row['Type'] == 'Government' else 'Paid services'
            })
    
    # If no hospitals found, provide general info
    if not hospitals_list:
        hospitals_list = [
            {'name': 'District General Hospital', 'type': 'Government', 'note': 'Visit your nearest district hospital'},
            {'name': 'Local Private Hospital', 'type': 'Private', 'note': 'Contact local healthcare providers'}
        ]
    
    return hospitals_list

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Backend is running'})

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    """
    Receive form data and return ML model predictions with hospital/doctor recommendations
    """
    try:
        data = request.json
        print("Received data:", data)
        
        # Extract form data
        age = int(data.get('age', 0))
        gender = data.get('gender', 'male')
        family_size = int(data.get('familySize', 1))
        district = data.get('district', 'colombo')
        medical_condition = data.get('medicalCondition', '')
        symptoms = data.get('symptoms', '')
        symptoms_description = data.get('symptomsDescription', '')
        
        # Handle income - convert from range to numeric
        income_str = data.get('monthlyIncome', '25000-50000')
        income_mapping = {
            'below-25000': 15000,
            '25000-50000': 37500,
            '50000-100000': 75000,
            '100000-200000': 150000,
            'above-200000': 250000
        }
        monthly_income = income_mapping.get(income_str, 50000)
        
        # Encode categorical variables using the new encoders
        sex_encoded = encoders['sex'].transform([SEX_FORM_TO_ENCODER.get(gender, 'M')])[0]
        education_value = EDUCATION_FORM_TO_ENCODER.get(data.get('educationLevel', 'secondary'), 'Secondary')
        education_encoded = encoders['education'].transform([education_value])[0]
        employment_value = EMPLOYMENT_FORM_TO_ENCODER.get(data.get('employmentStatus', 'employed'), 'Employed')
        employment_encoded = encoders['employment'].transform([employment_value])[0]
        
        # Create feature array: ['Age', 'Sex', 'Family_Size', 'Monthly_Income', 'Education_Level', 'Employment_Status']
        features = np.array([[age, sex_encoded, family_size, monthly_income, education_encoded, employment_encoded]])
        
        print(f"Features: {features}")
        
        # Get prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0]
        
        # Decode the prediction using welfare encoder
        result = encoders['welfare'].inverse_transform([prediction])[0]
        confidence = float(max(probability) * 100)
        
        print(f"Prediction: {result}, Confidence: {confidence}%")
        
        is_eligible = result == 'Eligible'
        
        # Find relevant specialists based on medical condition
        specialists = find_specialists(medical_condition, f"{symptoms} {symptoms_description}")
        
        # Find hospitals in user's district
        hospitals = find_hospitals(district, is_eligible)
        
        # Get treatment recommendations
        treatments = get_treatment_recommendations(medical_condition, f"{symptoms} {symptoms_description}")
        
        # Generate comprehensive recommendations
        if is_eligible:
            recommendations = {
                'eligibility': 'Eligible',
                'confidence': round(confidence, 1),
                'message': 'Congratulations! Based on your information, you are eligible for health welfare services.',
                'specialists': specialists,
                'hospitals': hospitals,
                'treatments': treatments,
                'nextSteps': [
                    'Visit your nearest Divisional Secretariat office',
                    'Bring your National ID card and income proof',
                    'Complete the official application form',
                    'A social worker will verify your eligibility'
                ],
                'benefits': [
                    'Free medical consultations at government hospitals',
                    'Subsidized medications',
                    'Free or reduced-cost treatments',
                    'Priority access to specialist care'
                ]
            }
        else:
            recommendations = {
                'eligibility': 'Not Eligible',
                'confidence': round(confidence, 1),
                'message': 'Based on your current information, you may not qualify for subsidized health welfare services. However, here are your healthcare recommendations:',
                'specialists': specialists,
                'hospitals': hospitals,
                'treatments': treatments,
                'alternatives': [
                    'Consider private health insurance options',
                    'Check with your employer for health benefits',
                    'Government hospitals still offer subsidized rates',
                    'Explore community health programs'
                ],
                'note': 'Eligibility criteria may change. Please visit your local Divisional Secretariat for a formal assessment.'
            }
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================
# CHATBOT FUNCTIONALITY
# ============================================

from difflib import SequenceMatcher
import re

# Knowledge Base - English (Expanded)
knowledge_base_en = {
    # Conversational responses
    'greeting': "Hello! 👋 I'm the Welfare Services Assistant. How can I help you today?",
    'greeting_morning': "Good morning! ☀️ I'm here to help you with welfare services. What would you like to know?",
    'greeting_afternoon': "Good afternoon! 🌤️ How can I assist you today?",
    'greeting_evening': "Good evening! 🌙 I'm here to help. What can I do for you?",
    'how_are_you': "I'm doing great, thank you for asking! 😊 I'm here and ready to help you with any questions about welfare services. How can I assist you?",
    'who_are_you': "I'm the Welfare Services Assistant, a chatbot designed to help you with information about government welfare programs in Sri Lanka. I can answer questions about eligibility, how to apply, health services, education support, and more!",
    'what_can_you_do': "I can help you with:\n\n📋 Information about welfare programs\n✅ Checking eligibility requirements\n📝 How to apply for services\n📄 Required documents\n🏥 Health services information\n📚 Education support\n💰 Financial aid programs\n📊 Application status\n\nJust ask me anything!",
    'thanks': "You're welcome! 😊 Is there anything else I can help you with?",
    'bye': "Goodbye! 👋 Thank you for chatting with me. Take care and feel free to come back anytime!",
    'ok': "Great! 👍 Let me know if you have any other questions.",
    'yes': "Alright! What would you like to know more about?",
    'no': "Okay, no problem! If you need help later, just ask. 😊",
    'help': "I'm here to help! You can ask me about:\n\n• Available welfare programs\n• Eligibility requirements\n• How to apply\n• Required documents\n• Health services\n• Education support\n• Financial aid\n• Application status\n\nWhat would you like to know?",
    'name': "I'm the Welfare Services Assistant! 🤖 You can call me your friendly welfare helper. I'm here to assist you with information about government welfare programs in Sri Lanka.",
    
    # Service information
    'programs_available': 'Our platform offers several welfare programs:\n\n🏥 **Health Services** - Free medical consultations, subsidized medications, hospital treatment coverage\n\n📚 **Education Support** - Scholarships, free textbooks, tutorial classes, higher education assistance\n\n💰 **Financial Aid** - Monthly allowances, emergency funds, livelihood support\n\n📈 **Investment Recommender** - Financial planning and investment guidance\n\n👴 **Senior Care** - Elderly support services and pension assistance',
    'eligibility': 'Eligibility for welfare services depends on:\n\n• **Income Level** - Monthly household income\n• **Family Size** - Number of dependents\n• **Age** - Specific programs have age requirements\n• **Health Condition** - For health-related programs\n• **Employment Status** - Current employment situation\n\nYou can check your eligibility by visiting our Health Services page and filling out the eligibility form.',
    'create_account': 'To register on our platform:\n\n1. Click on the Login/Register button\n2. Enter your NIC (National Identity Card) number\n3. Provide your mobile number and email\n4. Create a password\n5. Verify your account via SMS/email\n\nRegistration is completely FREE!',
    'how_to_apply': 'To apply for welfare services:\n\n1. Go to the **Services** page\n2. Select the program you need (Health, Education, Financial Aid, etc.)\n3. Click "Learn More" to view details\n4. Fill out the eligibility/application form\n5. Submit required documents\n6. Wait for approval (2-4 weeks)\n\nYou can track your application status in your dashboard.',
    'required_documents': 'Required documents for most applications:\n\n📄 **National Identity Card (NIC)** - Original or certified copy\n📄 **Proof of Income** - Salary slips, bank statements, or Grama Niladhari certificate\n📄 **Family Certificate** - For family-based benefits\n📄 **Medical Reports** - For health-related programs\n📄 **Birth Certificate** - For age verification\n\nAccepted formats: PDF, JPG, PNG (max 5MB each)',
    'health_services': 'Our Health Services program offers:\n\n✅ Free medical consultations at government hospitals\n✅ Subsidized medications (up to 80% discount)\n✅ Hospital treatment coverage\n✅ Preventive health checkups\n✅ Maternal and child health services\n✅ Mental health support\n\nTo check if you qualify, visit the Health Services page and fill out the eligibility form. Our AI system will recommend suitable hospitals and doctors based on your condition.',
    'education_support': 'Our Education Support program includes:\n\n🎓 Full and partial scholarships\n📚 Free textbooks and school supplies\n💻 Laptop/tablet provision for students\n📖 Tutorial and extra classes\n🍽️ School meal programs\n🎯 Higher education assistance\n\nEligible students from low-income families can apply through the Services page.',
    'financial_aid': 'Financial Aid programs available:\n\n💵 Monthly welfare allowances\n🆘 Emergency financial assistance\n🏠 Housing support\n👴 Senior citizen pensions\n👨‍👩‍👧‍👦 Family support payments\n💼 Livelihood and self-employment support\n\nBenefits are transferred directly to your bank account.',
    'approval_time': 'Application processing times:\n\n⏱️ **Initial Review**: 3-5 working days\n⏱️ **Document Verification**: 1-2 weeks\n⏱️ **Final Approval**: 2-4 weeks total\n\nYou will receive SMS and email notifications about your application status. You can also track progress in your dashboard.',
    'check_status': 'To check your application status:\n\n1. Log in to your account\n2. Go to your Dashboard\n3. View "My Applications" section\n4. Click on any application to see detailed status\n\nStatus types: Pending → Under Review → Approved/Rejected',
    'contact_support': 'Need help? Contact us through:\n\n💬 **This Chatbot** - Available 24/7\n📞 **Hotline**: 1919 (Government helpline)\n📧 **Email**: support@welfare.gov.lk\n🏢 **In Person**: Visit your nearest Divisional Secretariat office\n\nOffice hours: Monday-Friday, 8:30 AM - 4:30 PM',
    'data_secure': 'Your data is completely secure:\n\n🔒 All data is encrypted\n🔒 Stored on government-secured servers\n🔒 Not shared with third parties\n🔒 Compliant with data protection laws\n\nOnly authorized officials can access your information for processing applications.',
    'platform_free': 'Yes! This platform is 100% FREE.\n\n✅ No registration fees\n✅ No application fees\n✅ No hidden charges\n✅ All services are government-funded\n\n⚠️ Beware of scammers asking for money!',
    'languages': 'Our platform supports:\n\n🇱🇰 **Sinhala** (සිංහල)\n🇱🇰 **Tamil** (தமிழ்)\n🇬🇧 **English**\n\nYou can switch languages from the settings.',
    'investment': 'Our Investment Recommender service helps you with:\n\n📈 Financial planning advice\n💰 Savings optimization strategies\n🏦 Bank account recommendations\n📊 Investment options guidance\n👴 Retirement planning assistance\n\nThis service is available to all registered users.',
    'senior_care': 'Senior Care services for elderly citizens:\n\n👴 Pension assistance\n🏥 Priority healthcare access\n🏠 Elderly home support\n💊 Medication subsidies\n🚗 Transportation assistance\n👨‍👩‍👧 Caregiver support programs',
    'appeal': 'If your application is rejected, you can appeal:\n\n1. Log in to your account\n2. Go to the rejected application\n3. Click "Submit Appeal"\n4. Provide additional documents or explanation\n5. Wait for re-evaluation (1-2 weeks)\n\nYou can also visit your Divisional Secretariat for assistance.',
}

# Extended keywords for better matching
keywords_en = {
    # Conversational keywords
    'greeting': ['hello', 'hi', 'hey', 'hii', 'hiii', 'helo', 'hellow', 'greetings', 'howdy', 'sup', 'yo'],
    'greeting_morning': ['good morning', 'morning'],
    'greeting_afternoon': ['good afternoon', 'afternoon'],
    'greeting_evening': ['good evening', 'evening', 'good night'],
    'how_are_you': ['how are you', 'how r u', 'how are u', 'hows it going', 'how is it going', 'whats up', "what's up", 'how do you do', 'are you ok', 'are you good', 'you good', 'how u doing'],
    'who_are_you': ['who are you', 'what are you', 'are you a bot', 'are you human', 'are you real', 'are you ai', 'bot or human', 'who r u'],
    'what_can_you_do': ['what can you do', 'what do you do', 'how can you help', 'what can you help with', 'your capabilities', 'what are your features', 'help me'],
    'thanks': ['thank', 'thanks', 'thank you', 'thankyou', 'thx', 'ty', 'appreciate', 'grateful', 'cheers'],
    'bye': ['bye', 'goodbye', 'good bye', 'see you', 'see ya', 'later', 'exit', 'quit', 'close', 'end', 'take care', 'cya'],
    'ok': ['ok', 'okay', 'k', 'kk', 'got it', 'understood', 'i see', 'alright', 'right'],
    'yes': ['yes', 'yeah', 'yep', 'yup', 'sure', 'of course', 'definitely', 'certainly'],
    'no': ['no', 'nope', 'nah', 'not really', 'no thanks', 'no thank you', "that's all", 'nothing'],
    'help': ['help', 'assist', 'support me', 'i need help', 'can you help', 'need assistance'],
    'name': ['your name', 'whats your name', "what's your name", 'who is this', 'name please'],
    
    # Service keywords
    'programs_available': ['programs', 'available', 'welfare', 'services', 'what programs', 'which programs', 'what services', 'offer', 'provide', 'list programs', 'show programs', 'all services'],
    'eligibility': ['eligible', 'eligibility', 'who can apply', 'qualify', 'am i eligible', 'can i apply', 'requirements', 'do i qualify', 'check eligibility'],
    'create_account': ['create account', 'register', 'sign up', 'registration', 'how to register', 'new account', 'open account', 'join', 'signup'],
    'how_to_apply': ['how to apply', 'apply', 'application process', 'submit application', 'how do i apply', 'application', 'apply for', 'want to apply', 'need to apply', 'start application'],
    'required_documents': ['documents', 'required documents', 'what documents', 'papers', 'paperwork', 'need to submit', 'upload', 'nic', 'proof', 'certificate'],
    'health_services': ['health', 'medical', 'doctor', 'hospital', 'treatment', 'healthcare', 'medicine', 'clinic', 'sick', 'illness', 'disease', 'checkup', 'consultation'],
    'education_support': ['education', 'school', 'scholarship', 'study', 'university', 'college', 'student', 'learn', 'books', 'tuition', 'exam', 'degree'],
    'financial_aid': ['financial', 'money', 'allowance', 'funds', 'cash', 'payment', 'aid', 'assistance', 'loan', 'grant', 'welfare money', 'monthly payment'],
    'approval_time': ['how long', 'time', 'duration', 'when', 'approval time', 'waiting', 'how many days', 'how many weeks', 'processing time', 'take'],
    'check_status': ['status', 'check status', 'track', 'progress', 'where is my application', 'my application', 'application status', 'update', 'result'],
    'contact_support': ['contact', 'support', 'help desk', 'call', 'reach', 'phone', 'email', 'hotline', 'office', 'speak to someone', 'human', 'agent'],
    'data_secure': ['secure', 'safe', 'security', 'data protection', 'privacy', 'confidential', 'data', 'information safe', 'protect'],
    'platform_free': ['free', 'cost', 'charge', 'fee', 'payment', 'pay', 'price', 'how much', 'expensive'],
    'languages': ['language', 'sinhala', 'tamil', 'english', 'translate', 'change language'],
    'investment': ['investment', 'invest', 'savings', 'financial planning', 'retirement', 'pension planning', 'money management'],
    'senior_care': ['senior', 'elderly', 'old age', 'pension', 'retired', 'elder', 'grandparent', 'old people'],
    'appeal': ['appeal', 'rejected', 'denied', 'reapply', 'reconsider', 'not approved', 'failed', 'try again'],
    'thanks': ['thank', 'thanks', 'thank you', 'appreciate', 'grateful', 'thx'],
    'bye': ['bye', 'goodbye', 'see you', 'exit', 'quit', 'close', 'end'],
}

# Keywords for Sinhala matching
keywords_si = {
    'programs': ['වැඩසටහන්', 'වැඩසටහන', 'ප්‍රතිලාභ', 'සේවා'],
    'eligibility': ['සුදුසුකම්', 'අයදුම්', 'ප්‍රතිපත්ති'],
    'register': ['ලියාපදිංචි', 'ගිණුමක්'],
    'free': ['නොමිලේ', 'මිල'],
    'apply': ['අයදුම්', 'යොදන්නේ'],
    'documents': ['ලේඛන', 'අවශ්‍ය'],
    'time': ['කාලය', 'කොපමණ', 'දින', 'සති'],
    'status': ['තත්ත්වය', 'බලන්නේ'],
    'support': ['සහාය', 'උදව්'],
    'health': ['සෞඛ්‍ය', 'වෛද්‍ය', 'රෝහල්'],
}

# Knowledge Base - Sinhala
knowledge_base_si = {
    'programs': 'මුල්‍ය, සෞඛ්‍ය, අධ්‍යාපන සහ සමාජ ප්‍රතිසාධන වැඩසටහන් ලබා ගත හැක.',
    'eligibility': 'ආදායම, පවුල් ප්‍රමාණය, වයස සහ සෞඛ්‍ය තත්ත්වය අනුව සුදුසුකම් තීරණය වේ.',
    'register': 'ජාතික හැඳුනුම්පත් අංකය, දුරකථන අංකය සහ ඊමේල් භාවිතා කර ලියාපදිංචි විය හැක.',
    'free': 'ඔව්, මෙම වේදිකාව සම්පූර්ණයෙන්ම නොමිලේ.',
    'apply': 'අදාල වැඩසටහන තෝරා අන්තර්ජාල අයදුම්පත්‍රය යොදන්න.',
    'documents': 'ජාතික හැඳුනුම්පත සහ ආදායම් සනාථ කිරීම අවශ්‍යයි.',
    'time': 'සාමාන්‍යයෙන් සති 2-4 ගතවේ.',
    'status': 'ඔබගේ ගිණුම ඇතුළත තත්ත්වය බලන්න.',
    'support': 'ඔව්, චැට්බෝට් සහාය 24/7 ලබා ගත හැක.',
    'health': 'සෞඛ්‍ය සේවා මගින් නොමිලේ වෛද්‍ය උපදේශන, සහනාධාර ඖෂධ, රෝහල් ප්‍රතිකාර ආවරණය ලබා දේ.',
}

def similarity_score(str1, str2):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def find_chatbot_answer(question, language='en'):
    """Find answer using improved keyword matching"""
    q = question.lower().strip()
    
    # Remove punctuation for better matching
    q_clean = re.sub(r'[^\w\s]', '', q)
    
    if language == 'si':
        knowledge_base = knowledge_base_si
        keywords = keywords_si
        default_response = 'මට සමාවෙන්න, මම එම ප්‍රශ්නයට පිළිතුරු දැනගෙන නැහැ. කරුණාකර වෙනත් ආකාරයකින් අහන්න.'
    else:
        knowledge_base = knowledge_base_en
        keywords = keywords_en
        default_response = "I'm sorry, I couldn't find a specific answer to that question. Here are some topics I can help with:\n\n• What programs are available?\n• Am I eligible for welfare?\n• How do I apply?\n• What documents are needed?\n• Health services information\n• Education support\n• Financial aid\n• How to contact support\n\nPlease try asking about one of these topics!"
    
    best_match = None
    best_score = 0
    
    # Method 1: Exact phrase matching (highest priority)
    for category, words in keywords.items():
        for word in words:
            if word in q_clean or word in q:
                # Longer matches get higher scores
                score = len(word) * 2
                if score > best_score:
                    best_score = score
                    best_match = category
    
    # Method 2: Word-by-word matching
    if best_score < 10:
        q_words = set(q_clean.split())
        for category, words in keywords.items():
            match_count = 0
            for word in words:
                word_parts = word.split()
                for part in word_parts:
                    if part in q_words:
                        match_count += 1
            if match_count > 0:
                score = match_count * 3
                if score > best_score:
                    best_score = score
                    best_match = category
    
    # Method 3: Similarity matching for fuzzy matching
    if best_score < 5:
        for category, words in keywords.items():
            for word in words:
                score = similarity_score(q_clean, word) * 10
                if score > best_score and score > 5:
                    best_score = score
                    best_match = category
    
    if best_match and best_match in knowledge_base:
        return knowledge_base[best_match]
    
    return default_response

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chatbot endpoint"""
    try:
        data = request.json
        message = data.get('message', '')
        language = data.get('language', 'en')
        
        response = find_chatbot_answer(message, language)
        
        return jsonify({
            'success': True,
            'response': response
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Investment Recommendation Endpoint
@app.route('/api/investment-recommend', methods=['POST'])
def investment_recommend():
    try:
        data = request.json
        
        # Extract form data
        age = int(data.get('age', 30))
        monthly_income = float(data.get('monthlyIncome', 50000))
        savings = float(data.get('savingsAmount', 100000))
        investment_goal = data.get('investmentGoal', 'wealth-growth')
        risk_tolerance = data.get('riskTolerance', 'moderate')
        investment_duration = data.get('investmentDuration', 'medium')
        
        # Prepare features for KMeans (income, age, encoded value)
        # Using sex encoding as placeholder - model expects 3 features
        sex_encoded = 0.5  # Neutral value
        features = np.array([[monthly_income, age, sex_encoded]])
        
        # Get cluster prediction (income-based segmentation)
        cluster = investment_kmeans.predict(features)[0]
        
        # Define investment recommendations based on cluster and preferences
        investment_plans = {
            0: {  # Low income cluster (~31,000 LKR)
                'segment': 'Conservative Saver',
                'recommended_savings_rate': '15-20%',
                'recommendations': [
                    {
                        'name': 'National Savings Bank Fixed Deposit',
                        'type': 'Fixed Deposit',
                        'risk': 'Low',
                        'expected_return': '8-10% p.a.',
                        'min_investment': 'Rs. 1,000',
                        'description': 'Safe government-backed savings with guaranteed returns'
                    },
                    {
                        'name': 'Employee Provident Fund (EPF)',
                        'type': 'Retirement Fund',
                        'risk': 'Low',
                        'expected_return': '9-12% p.a.',
                        'min_investment': 'Salary-based',
                        'description': 'Mandatory retirement savings with employer contribution'
                    },
                    {
                        'name': 'Post Office Savings',
                        'type': 'Savings Account',
                        'risk': 'Very Low',
                        'expected_return': '5-7% p.a.',
                        'min_investment': 'Rs. 500',
                        'description': 'Easily accessible savings with government guarantee'
                    }
                ]
            },
            1: {  # Medium income cluster (~82,000 LKR)
                'segment': 'Balanced Investor',
                'recommended_savings_rate': '20-30%',
                'recommendations': [
                    {
                        'name': 'Unit Trust Funds',
                        'type': 'Mutual Fund',
                        'risk': 'Medium',
                        'expected_return': '12-15% p.a.',
                        'min_investment': 'Rs. 5,000',
                        'description': 'Diversified portfolio managed by professionals'
                    },
                    {
                        'name': 'Corporate Debentures',
                        'type': 'Fixed Income',
                        'risk': 'Medium-Low',
                        'expected_return': '10-13% p.a.',
                        'min_investment': 'Rs. 25,000',
                        'description': 'Higher returns than FDs with moderate risk'
                    },
                    {
                        'name': 'Treasury Bonds',
                        'type': 'Government Securities',
                        'risk': 'Low',
                        'expected_return': '11-14% p.a.',
                        'min_investment': 'Rs. 10,000',
                        'description': 'Government-backed securities with steady returns'
                    },
                    {
                        'name': 'Gold Investment (ETF/Physical)',
                        'type': 'Commodity',
                        'risk': 'Medium',
                        'expected_return': '8-12% p.a.',
                        'min_investment': 'Rs. 10,000',
                        'description': 'Hedge against inflation and currency fluctuation'
                    }
                ]
            },
            2: {  # High income cluster (~129,000 LKR)
                'segment': 'Growth Investor',
                'recommended_savings_rate': '30-40%',
                'recommendations': [
                    {
                        'name': 'Colombo Stock Exchange (CSE) Stocks',
                        'type': 'Equity',
                        'risk': 'High',
                        'expected_return': '15-25% p.a.',
                        'min_investment': 'Rs. 50,000',
                        'description': 'Direct stock investment for long-term wealth growth'
                    },
                    {
                        'name': 'Real Estate Investment',
                        'type': 'Property',
                        'risk': 'Medium-High',
                        'expected_return': '10-20% p.a.',
                        'min_investment': 'Rs. 500,000',
                        'description': 'Land or property investment for capital appreciation'
                    },
                    {
                        'name': 'Equity Mutual Funds',
                        'type': 'Mutual Fund',
                        'risk': 'High',
                        'expected_return': '15-20% p.a.',
                        'min_investment': 'Rs. 25,000',
                        'description': 'Professionally managed stock portfolio'
                    },
                    {
                        'name': 'Dollar-Denominated Investments',
                        'type': 'Foreign Currency',
                        'risk': 'Medium-High',
                        'expected_return': '5-8% + FX gains',
                        'min_investment': '$500',
                        'description': 'Protect against LKR depreciation'
                    },
                    {
                        'name': 'Business/Startup Investment',
                        'type': 'Entrepreneurship',
                        'risk': 'Very High',
                        'expected_return': '20-50%+ p.a.',
                        'min_investment': 'Rs. 100,000+',
                        'description': 'High-risk, high-reward business opportunities'
                    }
                ]
            }
        }
        
        # Adjust recommendations based on risk tolerance
        base_recommendations = investment_plans.get(cluster, investment_plans[1])
        filtered_recommendations = []
        
        for rec in base_recommendations['recommendations']:
            risk_level = rec['risk'].lower()
            if risk_tolerance == 'conservative':
                if 'low' in risk_level or 'very low' in risk_level:
                    filtered_recommendations.append(rec)
            elif risk_tolerance == 'moderate':
                if 'high' not in risk_level or 'medium' in risk_level:
                    filtered_recommendations.append(rec)
            else:  # aggressive
                filtered_recommendations.append(rec)
        
        # If too few recommendations after filtering, add some back
        if len(filtered_recommendations) < 2:
            filtered_recommendations = base_recommendations['recommendations'][:3]
        
        # Calculate suggested monthly investment
        if risk_tolerance == 'conservative':
            savings_rate = 0.15
        elif risk_tolerance == 'moderate':
            savings_rate = 0.25
        else:
            savings_rate = 0.35
        
        suggested_monthly = int(monthly_income * savings_rate)
        
        # Investment duration tips
        duration_tips = {
            'short': 'Focus on liquid investments like Fixed Deposits and Treasury Bills that can be easily accessed within 1-3 years.',
            'medium': 'Balance between growth and security. Consider a mix of Unit Trusts and Corporate Debentures for 3-7 year goals.',
            'long': 'Maximize growth potential with equity investments and real estate. Time in market reduces volatility risk over 7+ years.'
        }
        
        # Goal-specific advice
        goal_advice = {
            'retirement': 'Prioritize EPF/ETF contributions and long-term equity investments. Consider pension plans for tax benefits.',
            'wealth-growth': 'Diversify across asset classes. Reinvest dividends and compound your returns over time.',
            'education': 'Start a dedicated education fund early. Consider child education insurance plans with guaranteed returns.',
            'home-purchase': 'Build a down payment fund in safe instruments. Aim for 20% of property value to avoid high interest.',
            'emergency-fund': 'Keep 6 months of expenses in easily accessible savings. NSB or high-yield savings accounts are ideal.',
            'passive-income': 'Focus on dividend-paying stocks, rental properties, and fixed income securities for regular income.',
            'business': 'Build capital gradually. Consider business loans with your savings as collateral for leverage.'
        }
        
        return jsonify({
            'success': True,
            'recommendations': {
                'segment': base_recommendations['segment'],
                'cluster': int(cluster),
                'monthly_income': monthly_income,
                'suggested_monthly_investment': suggested_monthly,
                'recommended_savings_rate': base_recommendations['recommended_savings_rate'],
                'investment_options': filtered_recommendations,
                'duration_tip': duration_tips.get(investment_duration, duration_tips['medium']),
                'goal_advice': goal_advice.get(investment_goal, goal_advice['wealth-growth']),
                'risk_profile': risk_tolerance.capitalize(),
                'current_savings': savings
            }
        })
        
    except Exception as e:
        print(f"Investment recommendation error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 50)
    print("Healthcare Recommender System Backend")
    print("=" * 50)
    print(f"Model loaded: RandomForestClassifier")
    print(f"Model features: {model.feature_names_in_}")
    print(f"Welfare classes: {encoders['welfare'].classes_}")
    print(f"Doctors database: {len(doctors_df)} specialists")
    print(f"Hospitals database: {len(hospitals_df)} hospitals")
    print("Chatbot: Enabled (English & Sinhala)")
    print("=" * 50)
    app.run(debug=False, port=5000, host='0.0.0.0')
