import streamlit as st
from difflib import SequenceMatcher

# Page config
st.set_page_config(
    page_title="Social Welfare Assistant",
    page_icon="💬",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(to bottom right, #EFF6FF, #E0E7FF);
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    .user-message {
        background-color: #6366F1;
        color: white;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px 0;
        text-align: right;
    }
    .bot-message {
        background-color: white;
        color: #1F2937;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Knowledge Base from English PDF
knowledge_base = {
    'programs_available': 'This platform provides information on financial aid, health, education, and social support programs.',
    'eligibility': 'Eligibility depends on income, family size, age, and health condition. Citizens meeting government criteria can apply.',
    'create_account': 'Register using your NIC, mobile number, and email address.',
    'multiple_benefits': 'Yes, if you meet the eligibility criteria.',
    'platform_free': 'Yes, the platform is completely free for all users.',
    'how_to_apply': 'Select the program and submit the online application.',
    'ai_decision': 'No, AI only assists. Final decisions are made by authorities.',
    'appeal_decision': 'Yes, users can submit an appeal through the platform.',
    'online_application': 'Yes, all applications are online.',
    'required_documents': 'NIC and proof of income are required.',
    'edit_application': 'Yes, you can edit before final submission.',
    'approval_time': 'Usually 2 to 4 weeks.',
    'check_status': 'Check via your account dashboard.',
    'eligibility_criteria': 'Based on income, family size, age, and health condition.',
    'not_eligible': 'Eligibility criteria were not met.',
    'data_secure': 'Yes, data is securely stored and kept confidential.',
    'language_sinhala': 'Yes, Sinhala is supported.',
    'language_tamil': 'Yes, Tamil is supported.',
    'language_english': 'Yes, English is supported.',
    'support_247': 'Yes, chatbot support is available 24/7.',
    'elderly_friendly': 'Yes, it is simple, easy, and user-friendly.',
    'forgot_password': 'Use the "Forgot Password" option to reset.',
    'change_details': 'Yes, you can update through account/profile settings.',
    'upload_later': 'Yes, you can upload documents before approval.',
    'file_formats': 'PDF, JPG, and PNG formats are accepted.',
    'save_draft': 'Yes, you can save and continue later.',
    'notifications': 'Yes, via SMS and email.',
    'mobile_friendly': 'Yes, mobile-friendly design.',
    'internet_required': 'Yes, internet is required.',
    'apply_for_others': 'Yes, with proper authorization.',
    'after_submission': 'Application is reviewed by officials.',
    'cancel_application': 'Yes, you can cancel before approval.',
    'contact_support': 'Through chatbot or help desk.',
    'voice_support': 'Not yet, planned for future.',
    'update_income': 'Yes, through profile settings.',
    'benefits_transfer': 'Yes, benefits are transferred digitally to bank accounts when applicable.',
    'change_program': 'Yes, you can change before submission.',
    'ai_reject': 'No, AI only assists review. Authorities make final decisions.',
    'eligibility_reasons': 'Yes, shown in application status.',
    'family_size': 'Yes, family size is important and affects eligibility.',
    'reapply': 'Yes, you can reapply after correcting details.',
    'login_anytime': 'Yes, 24/7 access.',
    'data_sharing': 'No, data will not be shared and is kept confidential.',
    'delete_account': 'Yes, via support request.',
    'training': 'Yes, user guides and training are available.',
    'updates_shown': 'Yes, updates are shown on dashboard.',
    'government_approved': 'Yes, officially approved by government.',
    'feedback': 'Yes, feedback option is available.',
    'previous_applications': 'Yes, visible in your account dashboard.',
    'track_multiple': 'Yes, all applications are visible in dashboard.',
}

# Enhanced keywords mapping for better matching
keywords = {
    'programs_available': ['programs', 'available', 'welfare programs', 'what programs', 'which programs', 'services'],
    'eligibility': ['eligible', 'eligibility', 'who can apply', 'qualify', 'criteria', 'requirements'],
    'create_account': ['create account', 'register', 'sign up', 'registration', 'how to register'],
    'multiple_benefits': ['multiple', 'more than one', 'several benefits', 'multiple benefits'],
    'platform_free': ['free', 'cost', 'charge', 'payment', 'pay'],
    'how_to_apply': ['how to apply', 'apply', 'application process', 'submit application'],
    'ai_decision': ['ai decision', 'artificial intelligence', 'ai make', 'final decision'],
    'appeal_decision': ['appeal', 'challenge', 'dispute', 'disagree'],
    'online_application': ['online', 'internet application', 'apply online'],
    'required_documents': ['documents', 'required', 'need', 'submit', 'papers', 'what documents'],
    'edit_application': ['edit', 'change', 'modify', 'update application'],
    'approval_time': ['how long', 'time', 'duration', 'when', 'approval time'],
    'check_status': ['status', 'check', 'track', 'progress'],
    'eligibility_criteria': ['criteria', 'based on', 'determined', 'how decide'],
    'not_eligible': ['not eligible', 'rejected', 'denied', 'why not'],
    'data_secure': ['secure', 'safe', 'security', 'data protection', 'privacy'],
    'language_sinhala': ['sinhala', 'sinhala language'],
    'language_tamil': ['tamil', 'tamil language'],
    'language_english': ['english', 'english language'],
    'support_247': ['support', '24/7', 'help', 'assistance', 'available'],
    'elderly_friendly': ['elderly', 'old people', 'senior', 'easy to use'],
    'forgot_password': ['forgot password', 'reset password', 'lost password'],
    'change_details': ['change details', 'update details', 'personal details', 'contact information'],
    'upload_later': ['upload later', 'documents later'],
    'file_formats': ['format', 'file type', 'accepted files'],
    'save_draft': ['draft', 'save', 'continue later'],
    'notifications': ['notification', 'alert', 'notify', 'inform'],
    'mobile_friendly': ['mobile', 'phone', 'smartphone'],
    'internet_required': ['internet', 'wifi', 'connection'],
    'apply_for_others': ['apply for', 'someone else', 'family member', 'behalf'],
    'after_submission': ['after submit', 'what happens', 'next step'],
    'cancel_application': ['cancel', 'withdraw', 'remove application'],
    'contact_support': ['contact', 'support', 'help desk'],
    'voice_support': ['voice', 'audio', 'speech'],
    'update_income': ['income', 'update income', 'salary'],
    'benefits_transfer': ['transfer', 'payment', 'receive', 'bank'],
    'change_program': ['change program', 'switch program'],
    'ai_reject': ['ai reject', 'ai decline'],
    'eligibility_reasons': ['why eligible', 'reasons', 'explain eligibility'],
    'family_size': ['family size', 'family members', 'household'],
    'reapply': ['reapply', 'apply again', 'rejected'],
    'login_anytime': ['login', 'access', 'anytime'],
    'data_sharing': ['share data', 'data shared'],
    'delete_account': ['delete', 'remove account', 'close account'],
    'training': ['training', 'guide', 'tutorial', 'help'],
    'updates_shown': ['updates', 'dashboard'],
    'government_approved': ['government', 'approved', 'official'],
    'feedback': ['feedback', 'suggestion', 'comment'],
    'previous_applications': ['previous', 'past applications', 'history'],
    'track_multiple': ['multiple applications', 'track multiple', 'several applications'],
}

def similarity_score(str1, str2):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def find_answer(question):
    """Find answer using keyword matching and similarity scoring"""
    q = question.lower()
    best_match = None
    best_score = 0
    
    # First try exact keyword matching
    for category, words in keywords.items():
        for word in words:
            if word in q:
                score = len(word) / len(q)  # Prefer longer matches
                if score > best_score:
                    best_score = score
                    best_match = category
    
    # If no good match, try similarity scoring
    if best_score < 0.3:
        for category, words in keywords.items():
            for word in words:
                score = similarity_score(q, word)
                if score > best_score and score > 0.5:
                    best_score = score
                    best_match = category
    
    if best_match:
        return knowledge_base[best_match]
    
    return "I'm sorry, I don't have an answer to that question. Please try rephrasing or ask about:\n- Available programs\n- Eligibility criteria\n- How to apply\n- Required documents\n- Application status"

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
            'role': 'assistant',
            'content': 'Hello! 👋 I\'m the Social Welfare Assistant. I can help you with information about welfare programs, eligibility, applications, and more. What would you like to know?'
        }
    ]

# Header
st.title("💬 Social Welfare Assistant")
st.markdown("**Your Guide to Welfare Programs and Benefits**")
st.divider()

# Quick questions
st.markdown("#### Quick Questions:")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📋 Available Programs"):
        question = "What programs are available?"
        st.session_state.messages.append({'role': 'user', 'content': question})
        response = find_answer(question)
        st.session_state.messages.append({'role': 'assistant', 'content': response})
        st.rerun()
    
    if st.button("✅ Eligibility"):
        question = "Who is eligible?"
        st.session_state.messages.append({'role': 'user', 'content': question})
        response = find_answer(question)
        st.session_state.messages.append({'role': 'assistant', 'content': response})
        st.rerun()

with col2:
    if st.button("📝 How to Apply"):
        question = "How do I apply?"
        st.session_state.messages.append({'role': 'user', 'content': question})
        response = find_answer(question)
        st.session_state.messages.append({'role': 'assistant', 'content': response})
        st.rerun()
    
    if st.button("📄 Required Documents"):
        question = "What documents are required?"
        st.session_state.messages.append({'role': 'user', 'content': question})
        response = find_answer(question)
        st.session_state.messages.append({'role': 'assistant', 'content': response})
        st.rerun()

with col3:
    if st.button("⏱️ Approval Time"):
        question = "How long does approval take?"
        st.session_state.messages.append({'role': 'user', 'content': question})
        response = find_answer(question)
        st.session_state.messages.append({'role': 'assistant', 'content': response})
        st.rerun()
    
    if st.button("📊 Check Status"):
        question = "How to check status?"
        st.session_state.messages.append({'role': 'user', 'content': question})
        response = find_answer(question)
        st.session_state.messages.append({'role': 'assistant', 'content': response})
        st.rerun()

st.divider()

# Display chat messages
for message in st.session_state.messages:
    if message['role'] == 'user':
        st.markdown(f'<div class="user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">🤖 {message["content"]}</div>', unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type your question here...")

if user_input:
    # Add user message
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    
    # Get bot response
    response = find_answer(user_input)
    st.session_state.messages.append({'role': 'assistant', 'content': response})
    
    # Rerun to update chat
    st.rerun()

# Sidebar with information
with st.sidebar:
    st.markdown("### 📚 About")
    st.info("This chatbot provides information about social welfare programs including financial aid, health, education, and social support.")
    
    st.markdown("### 🎯 Topics I Can Help With:")
    st.markdown("""
    - Available welfare programs
    - Eligibility requirements
    - Application process
    - Required documents
    - Account registration
    - Application status
    - Support and contact info
    - Platform features
    """)
    
    st.markdown("### 💡 Tips:")
    st.success("Try asking questions like:\n- 'What programs are available?'\n- 'How do I apply?'\n- 'What documents do I need?'\n- 'How long does approval take?'")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = [
            {
                'role': 'assistant',
                'content': 'Hello! 👋 I\'m the Social Welfare Assistant. I can help you with information about welfare programs, eligibility, applications, and more. What would you like to know?'
            }
        ]
        st.rerun()

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #6B7280; font-size: 12px;'>
   </div>
""", unsafe_allow_html=True)