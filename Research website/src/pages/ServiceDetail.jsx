import { useParams, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import '../styles/ServiceDetail.css';

// Sri Lankan districts with their coordinates for location-based recommendations
const sriLankanDistricts = [
  { value: 'colombo', label: 'Colombo' },
  { value: 'gampaha', label: 'Gampaha' },
  { value: 'kalutara', label: 'Kalutara' },
  { value: 'kandy', label: 'Kandy' },
  { value: 'matale', label: 'Matale' },
  { value: 'nuwara-eliya', label: 'Nuwara Eliya' },
  { value: 'galle', label: 'Galle' },
  { value: 'matara', label: 'Matara' },
  { value: 'hambantota', label: 'Hambantota' },
  { value: 'jaffna', label: 'Jaffna' },
  { value: 'kilinochchi', label: 'Kilinochchi' },
  { value: 'mannar', label: 'Mannar' },
  { value: 'mullaitivu', label: 'Mullaitivu' },
  { value: 'vavuniya', label: 'Vavuniya' },
  { value: 'trincomalee', label: 'Trincomalee' },
  { value: 'batticaloa', label: 'Batticaloa' },
  { value: 'ampara', label: 'Ampara' },
  { value: 'kurunegala', label: 'Kurunegala' },
  { value: 'puttalam', label: 'Puttalam' },
  { value: 'anuradhapura', label: 'Anuradhapura' },
  { value: 'polonnaruwa', label: 'Polonnaruwa' },
  { value: 'badulla', label: 'Badulla' },
  { value: 'monaragala', label: 'Monaragala' },
  { value: 'ratnapura', label: 'Ratnapura' },
  { value: 'kegalle', label: 'Kegalle' }
];

// Medical specialties for recommendation
const medicalSpecialties = [
  { value: 'general', label: 'General Medicine' },
  { value: 'cardiology', label: 'Cardiology (Heart)' },
  { value: 'neurology', label: 'Neurology (Brain & Nerves)' },
  { value: 'orthopedics', label: 'Orthopedics (Bones & Joints)' },
  { value: 'pediatrics', label: 'Pediatrics (Children)' },
  { value: 'gynecology', label: 'Gynecology & Obstetrics' },
  { value: 'dermatology', label: 'Dermatology (Skin)' },
  { value: 'ophthalmology', label: 'Ophthalmology (Eyes)' },
  { value: 'ent', label: 'ENT (Ear, Nose, Throat)' },
  { value: 'psychiatry', label: 'Psychiatry (Mental Health)' },
  { value: 'oncology', label: 'Oncology (Cancer)' },
  { value: 'urology', label: 'Urology' },
  { value: 'gastroenterology', label: 'Gastroenterology (Digestive)' },
  { value: 'pulmonology', label: 'Pulmonology (Lungs)' },
  { value: 'endocrinology', label: 'Endocrinology (Diabetes/Hormones)' },
  { value: 'nephrology', label: 'Nephrology (Kidneys)' },
  { value: 'rheumatology', label: 'Rheumatology (Arthritis)' },
  { value: 'dentistry', label: 'Dentistry' },
  { value: 'physiotherapy', label: 'Physiotherapy' },
  { value: 'emergency', label: 'Emergency Care' }
];

const serviceDetails = {
  'family-support': {
    id: 1,
    icon: '📈',
    title: 'Investment Recommender',
    shortDesc: 'Smart investment recommendations and financial planning assistance',
    fullDesc: 'Our intelligent investment recommendation system helps you make informed financial decisions. Using advanced analytics, we provide personalized investment advice tailored to your financial goals, risk tolerance, and current economic situation.',
    benefits: [
      'Personalized investment recommendations',
      'Risk assessment and portfolio analysis',
      'Financial goal planning',
      'Market trend insights',
      'Savings optimization strategies',
      'Retirement planning assistance'
    ],
    eligibility: [
      'Sri Lankan citizenship',
      'Age 18 and above',
      'Valid identification',
      'Registered with the platform'
    ],
    contact: '+94 11 234 5678'
  },
  'health-services': {
    id: 2,
    icon: '🏥',
    title: 'Health Services',
    shortDesc: 'Comprehensive healthcare and medical assistance programs',
    fullDesc: 'We provide comprehensive healthcare services to ensure every Sri Lankan has access to quality medical care. Our health services program covers preventive care, treatment, and rehabilitation services. The healthcare recommender system analyzes user data and eligibility criteria to suggest suitable healthcare and welfare services, improving decision-making, accessibility, and personalized service delivery.',
    benefits: [
      'Free medical consultations',
      'Subsidized medications',
      'Hospital treatment coverage',
      'Preventive health checkups',
      'Maternal and child health services',
      'Mental health support'
    ],
    eligibility: [
      'Low-income families',
      'Chronic disease patients',
      'Pregnant women and children',
      'Senior citizens',
      'Persons with disabilities'
    ],
    contact: '+94 11 234 5679'
  },
  'ai-gis-insights': {
    id: 3,
    icon: '🤖',
    title: 'AI-GIS Welfare Insights',
    shortDesc: 'AI-powered geographic insights for welfare program optimization',
    fullDesc: 'AI and GIS-based welfare insights analyze geographic and demographic data to identify service gaps, optimize resource allocation, and support data-driven decision-making for improved social welfare planning.',
    benefits: [
      'Predictive analytics for welfare needs',
      'Geographic mapping of underserved areas',
      'Resource allocation optimization',
      'Real-time data visualization',
      'Community vulnerability assessment',
      'Program impact analysis'
    ],
    eligibility: [
      'Government welfare departments',
      'Policy makers and researchers',
      'NGOs and community organizations',
      'District and divisional offices',
      'Welfare program administrators'
    ],
    contact: '+94 11 234 5680'
  },
  'senior-care': {
    id: 4,
    icon: '👴',
    title: 'Senior Care',
    shortDesc: 'Special programs and benefits for elderly citizens',
    fullDesc: 'We honor and support our senior citizens through comprehensive care programs that ensure dignity, health, and social inclusion in their golden years.',
    benefits: [
      'Monthly pension support',
      'Free healthcare services',
      'Senior citizen care centers',
      'Home care assistance',
      'Social activities and engagement',
      'Emergency support services'
    ],
    eligibility: [
      'Age 60 and above',
      'Sri Lankan citizens',
      'Income below specified threshold',
      'No family support (optional)'
    ],
    contact: '+94 11 234 5681'
  },
  'employment': {
    id: 5,
    icon: '💼',
    title: 'Employment Programs',
    shortDesc: 'Job training and employment assistance initiatives',
    fullDesc: 'We help individuals gain skills and secure meaningful employment through comprehensive training programs and job placement assistance.',
    benefits: [
      'Vocational training courses',
      'Skill development programs',
      'Job placement assistance',
      'Interview coaching',
      'Subsidy for job seekers',
      'Entrepreneurship support'
    ],
    eligibility: [
      'Age 18-60',
      'Unemployed or underemployed',
      'Sri Lankan citizens',
      'Willing to undergo training'
    ],
    process: [
      '1. Registration with employment office',
      '2. Skills assessment',
      '3. Course enrollment',
      '4. Training completion',
      '5. Job placement assistance'
    ],
    contact: '+94 11 234 5682'
  },
  'housing': {
    id: 6,
    icon: '🏠',
    title: 'Housing Assistance',
    shortDesc: 'Housing subsidies and accommodation programs',
    fullDesc: 'Everyone deserves a safe and adequate home. Our housing assistance program provides subsidies, loans, and accommodation support to low-income families.',
    benefits: [
      'Housing subsidies',
      'Low-interest housing loans',
      'Land allocation programs',
      'Repair and maintenance grants',
      'Emergency shelter assistance',
      'Slum upgrading programs'
    ],
    eligibility: [
      'Low-income families',
      'Homeless individuals',
      'Families living in substandard housing',
      'Disaster-affected people'
    ],
    process: [
      '1. Apply with housing documents',
      '2. Property assessment',
      '3. Income verification',
      '4. Loan/subsidy approval',
      '5. Disbursement and monitoring'
    ],
    contact: '+94 11 234 5683'
  }
};

export default function ServiceDetail() {
  const { serviceId } = useParams();
  const navigate = useNavigate();
  const service = serviceDetails[serviceId];
  
  const [formData, setFormData] = useState({
    fullName: '',
    nic: '',
    email: '',
    phone: '',
    age: '',
    district: '',
    monthlyIncome: '',
    savingsAmount: '',
    investmentGoal: '',
    riskTolerance: '',
    investmentDuration: ''
  });
  
  const [formSubmitted, setFormSubmitted] = useState(false);
  const [investmentRecommendations, setInvestmentRecommendations] = useState(null);
  const [isLoadingInvestment, setIsLoadingInvestment] = useState(false);

  // Health Services Form State
  const [healthFormData, setHealthFormData] = useState({
    fullName: '',
    age: '',
    gender: '',
    phone: '',
    email: '',
    district: '',
    familySize: '',
    monthlyIncome: '',
    educationLevel: '',
    employmentStatus: '',
    medicalCondition: '',
    symptoms: '',
    symptomsDescription: ''
  });
  
  const [healthFormSubmitted, setHealthFormSubmitted] = useState(false);
  const [recommendations, setRecommendations] = useState(null);
  const [isLoadingRecommendations, setIsLoadingRecommendations] = useState(false);

  // Senior Care Form State
  const [seniorFormData, setSeniorFormData] = useState({
    fullName: '',
    age: '',
    gender: '',
    nic: '',
    phone: '',
    district: '',
    livingStatus: '',
    mobilityLevel: ''
  });
  const [seniorFormSubmitted, setSeniorFormSubmitted] = useState(false);

  const handleSeniorInputChange = (e) => {
    const { name, value } = e.target;
    setSeniorFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSeniorFormSubmit = (e) => {
    e.preventDefault();
    console.log('Senior Care Form Data:', seniorFormData);
    setSeniorFormSubmitted(true);
    
    // Don't auto-reset - let user download forms at their own pace
  };

  const handleHealthInputChange = (e) => {
    const { name, value } = e.target;
    setHealthFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleHealthFormSubmit = async (e) => {
    e.preventDefault();
    setIsLoadingRecommendations(true);
    
    console.log('Health Services Form Data:', healthFormData);
    
    try {
      // Send data to ML model API
      const response = await fetch('http://localhost:5000/api/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(healthFormData),
      });
      
      const result = await response.json();
      console.log('API Response:', result);
      
      if (result.success) {
        setRecommendations(result.recommendations);
      } else {
        setRecommendations({
          eligibility: 'Error',
          message: result.error || 'An error occurred while processing your request.',
        });
      }
    } catch (error) {
      console.error('Error:', error);
      setRecommendations({
        eligibility: 'Error',
        message: 'Could not connect to the server. Please make sure the backend is running.',
      });
    }
    
    setIsLoadingRecommendations(false);
    setHealthFormSubmitted(true);
  };

  const resetHealthForm = () => {
    setHealthFormData({
      fullName: '',
      age: '',
      gender: '',
      phone: '',
      email: '',
      district: '',
      familySize: '',
      monthlyIncome: '',
      educationLevel: '',
      employmentStatus: '',
      medicalCondition: '',
      symptoms: '',
      symptomsDescription: ''
    });
    setHealthFormSubmitted(false);
    setRecommendations(null);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileChange = (e) => {
    setFormData(prev => ({
      ...prev,
      documents: e.target.files[0]
    }));
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    setIsLoadingInvestment(true);
    console.log('Investment Form Data:', formData);
    
    try {
      const response = await fetch('http://localhost:5000/api/investment-recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      const result = await response.json();
      console.log('Investment API Response:', result);
      
      if (result.success) {
        setInvestmentRecommendations(result.recommendations);
        setFormSubmitted(true);
      } else {
        alert('Error getting recommendations. Please try again.');
      }
    } catch (error) {
      console.error('Investment API Error:', error);
      alert('Could not connect to server. Please ensure the backend is running.');
    } finally {
      setIsLoadingInvestment(false);
    }
  };

  if (!service) {
    return (
      <div className="service-detail-container">
        <div className="not-found">
          <h1>Service Not Found</h1>
          <p>The service you're looking for doesn't exist.</p>
          <button className="btn btn-primary" onClick={() => navigate('/')}>
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="service-detail">
      <div className="service-detail-container">
        {/* Back Button */}
        <button className="back-btn" onClick={() => navigate('/')}>
          ← Back to Services
        </button>

        {/* Header */}
        <div className="detail-header">
          <div className="detail-icon">
            {service.isImage ? (
              <img src={service.icon} alt={service.title} />
            ) : (
              service.icon
            )}
          </div>
          <h1>{service.title}</h1>
          <p className="detail-subtitle">{service.shortDesc}</p>
        </div>

        {/* Full Description */}
        <section className="detail-section">
          <h2>Overview</h2>
          <p>{service.fullDesc}</p>
        </section>

        {/* Benefits */}
        <section className="detail-section">
          <h2>Key Benefits</h2>
          <ul className="benefits-list">
            {service.benefits.map((benefit, index) => (
              <li key={index}>
                <span className="check-mark">✓</span>
                {benefit}
              </li>
            ))}
          </ul>
        </section>

        {/* Eligibility */}
        <section className="detail-section">
          <h2>Eligibility Criteria</h2>
          <ul className="eligibility-list">
            {service.eligibility.map((criterion, index) => (
              <li key={index}>
                <span className="criterion-mark">•</span>
                {criterion}
              </li>
            ))}
          </ul>
        </section>

        {/* Process */}
        {service.process && service.process.length > 0 && (
        <section className="detail-section">
          <h2>Application Process</h2>
          <div className="process-steps">
            {service.process.map((step, index) => (
              <div key={index} className="process-step">
                <div className="step-number">{index + 1}</div>
                <p>{step}</p>
              </div>
            ))}
          </div>
        </section>
        )}

        {/* Contact */}
        <section className="detail-section contact-section">
          <h2>Get Started</h2>
          <p>
            For more information about this service, please contact us:
          </p>
          <div className="contact-box">
            <p className="contact-phone">
              <strong>📞 Phone:</strong> {service.contact}
            </p>
            <p className="contact-email">
              <strong>📧 Email:</strong> info@welfare.lk
            </p>
          </div>
          <button className="btn btn-primary" onClick={() => navigate('/#contact')}>
            Contact Us
          </button>
        </section>

        {/* Investment Recommender Form */}
        {serviceId === 'family-support' && (
          <section className="detail-section application-section">
            <h2>📊 Get Your Investment Plan</h2>
            <p className="form-intro">
              Fill out the form below to receive personalized investment recommendations based on your financial profile. All fields marked with * are required.
            </p>
            
            {formSubmitted ? (
              <div className="investment-results">
                {isLoadingInvestment ? (
                  <div className="loading-recommendations">
                    <div className="loading-spinner"></div>
                    <p>Analyzing your financial profile...</p>
                  </div>
                ) : investmentRecommendations ? (
                  <div className="recommendations-container">
                    {/* Investor Profile */}
                    <div className="investor-profile">
                      <div className="profile-header">
                        <div className="result-icon">💼</div>
                        <h3>Your Investor Profile: {investmentRecommendations.segment}</h3>
                      </div>
                      <div className="profile-stats">
                        <div className="stat-item">
                          <span className="stat-label">Risk Profile</span>
                          <span className="stat-value">{investmentRecommendations.risk_profile}</span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-label">Monthly Income</span>
                          <span className="stat-value">Rs. {investmentRecommendations.monthly_income?.toLocaleString()}</span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-label">Suggested Monthly Investment</span>
                          <span className="stat-value highlight">Rs. {investmentRecommendations.suggested_monthly_investment?.toLocaleString()}</span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-label">Recommended Savings Rate</span>
                          <span className="stat-value">{investmentRecommendations.recommended_savings_rate}</span>
                        </div>
                      </div>
                    </div>

                    {/* Investment Options */}
                    <div className="recommendation-section">
                      <h4>📈 Recommended Investment Options</h4>
                      <div className="investment-cards">
                        {investmentRecommendations.investment_options?.map((option, index) => (
                          <div key={index} className={`investment-card risk-${option.risk.toLowerCase().replace(/\s+/g, '-')}`}>
                            <div className="investment-header">
                              <h5>{option.name}</h5>
                              <span className={`risk-badge ${option.risk.toLowerCase().replace(/\s+/g, '-')}`}>{option.risk} Risk</span>
                            </div>
                            <p className="investment-type">{option.type}</p>
                            <p className="investment-desc">{option.description}</p>
                            <div className="investment-details">
                              <div className="detail-item">
                                <span className="label">Expected Return:</span>
                                <span className="value">{option.expected_return}</span>
                              </div>
                              <div className="detail-item">
                                <span className="label">Min Investment:</span>
                                <span className="value">{option.min_investment}</span>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Goal Advice */}
                    <div className="advice-section">
                      <h4>🎯 Goal-Specific Advice</h4>
                      <p>{investmentRecommendations.goal_advice}</p>
                    </div>

                    {/* Duration Tip */}
                    <div className="advice-section">
                      <h4>⏱️ Investment Duration Tip</h4>
                      <p>{investmentRecommendations.duration_tip}</p>
                    </div>

                    {/* Reset Button */}
                    <button 
                      className="btn btn-secondary" 
                      onClick={() => {
                        setFormSubmitted(false);
                        setInvestmentRecommendations(null);
                      }}
                    >
                      ← Get New Recommendations
                    </button>
                  </div>
                ) : (
                  <div className="form-success">
                    <span className="success-icon">✅</span>
                    <h3>Investment Profile Submitted!</h3>
                    <p>Reference Number: <strong>INV-{Date.now().toString().slice(-8)}</strong></p>
                  </div>
                )}
              </div>
            ) : (
              <form className="application-form" onSubmit={handleFormSubmit}>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="fullName">Full Name *</label>
                    <input
                      type="text"
                      id="fullName"
                      name="fullName"
                      value={formData.fullName}
                      onChange={handleInputChange}
                      placeholder="Enter your full name"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="nic">NIC Number *</label>
                    <input
                      type="text"
                      id="nic"
                      name="nic"
                      value={formData.nic}
                      onChange={handleInputChange}
                      placeholder="e.g., 200012345678"
                      required
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="email">Email Address *</label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      placeholder="your.email@example.com"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="phone">Phone Number *</label>
                    <input
                      type="tel"
                      id="phone"
                      name="phone"
                      value={formData.phone}
                      onChange={handleInputChange}
                      placeholder="+94 XX XXX XXXX"
                      required
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="age">Age *</label>
                    <input
                      type="number"
                      id="age"
                      name="age"
                      value={formData.age}
                      onChange={handleInputChange}
                      placeholder="e.g., 35"
                      min="18"
                      max="100"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="district">District *</label>
                    <select
                      id="district"
                      name="district"
                      value={formData.district}
                      onChange={handleInputChange}
                      required
                    >
                      <option value="">Select District</option>
                      {sriLankanDistricts.map(district => (
                        <option key={district.value} value={district.value}>
                          {district.label}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="monthlyIncome">Monthly Income (LKR) *</label>
                    <input
                      type="number"
                      id="monthlyIncome"
                      name="monthlyIncome"
                      value={formData.monthlyIncome}
                      onChange={handleInputChange}
                      placeholder="e.g., 75000"
                      min="0"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="savingsAmount">Available Savings (LKR) *</label>
                    <input
                      type="number"
                      id="savingsAmount"
                      name="savingsAmount"
                      value={formData.savingsAmount}
                      onChange={handleInputChange}
                      placeholder="e.g., 500000"
                      min="0"
                      required
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="investmentGoal">Investment Goal *</label>
                    <select
                      id="investmentGoal"
                      name="investmentGoal"
                      value={formData.investmentGoal}
                      onChange={handleInputChange}
                      required
                    >
                      <option value="">Select Goal</option>
                      <option value="retirement">Retirement Planning</option>
                      <option value="wealth-growth">Wealth Growth</option>
                      <option value="education">Children's Education</option>
                      <option value="home-purchase">Home Purchase</option>
                      <option value="emergency-fund">Emergency Fund</option>
                      <option value="passive-income">Passive Income</option>
                      <option value="business">Business Investment</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label htmlFor="riskTolerance">Risk Tolerance *</label>
                    <select
                      id="riskTolerance"
                      name="riskTolerance"
                      value={formData.riskTolerance}
                      onChange={handleInputChange}
                      required
                    >
                      <option value="">Select Risk Level</option>
                      <option value="conservative">Conservative (Low Risk)</option>
                      <option value="moderate">Moderate (Balanced)</option>
                      <option value="aggressive">Aggressive (High Risk)</option>
                    </select>
                  </div>
                </div>

                <div className="form-group full-width">
                  <label htmlFor="investmentDuration">Investment Duration *</label>
                  <select
                    id="investmentDuration"
                    name="investmentDuration"
                    value={formData.investmentDuration}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="">Select Duration</option>
                    <option value="short">Short Term (1-3 years)</option>
                    <option value="medium">Medium Term (3-7 years)</option>
                    <option value="long">Long Term (7+ years)</option>
                  </select>
                </div>

                <div className="form-agreement">
                  <label>
                    <input type="checkbox" required />
                    <span>I understand that investment recommendations are for informational purposes only and past performance does not guarantee future results.</span>
                  </label>
                </div>

                <button type="submit" className="btn btn-primary submit-application">
                  Get Investment Recommendations
                </button>
              </form>
            )}
          </section>
        )}

        {/* Health Services Recommendation Form */}
        {serviceId === 'health-services' && (
          <section className="detail-section health-recommendation-section">
            <h2>🏥 Check Your Health Welfare Eligibility</h2>
            <p className="form-intro">
              Fill out the form below to check if you're eligible for government health welfare services. Our system will analyze your information and provide personalized recommendations.
            </p>
            
            {healthFormSubmitted ? (
              <div className="recommendation-results">
                {isLoadingRecommendations ? (
                  <div className="loading-recommendations">
                    <div className="loading-spinner"></div>
                    <p>Analyzing your information...</p>
                  </div>
                ) : recommendations ? (
                  <div className="recommendations-container">
                    {/* Eligibility Status */}
                    <div className={`eligibility-status ${recommendations.eligibility === 'Eligible' ? 'eligible' : 'not-eligible'}`}>
                      <div className="status-header">
                        <div className="result-icon">{recommendations.eligibility === 'Eligible' ? '✅' : 'ℹ️'}</div>
                        <h3>{recommendations.eligibility === 'Eligible' ? 'You Are Eligible for Welfare Services!' : 'Welfare Eligibility Status'}</h3>
                      </div>
                      <p className="confidence">Confidence: {recommendations.confidence}%</p>
                      <p className="message">{recommendations.message}</p>
                    </div>

                    {/* Recommended Hospitals */}
                    {recommendations.hospitals && recommendations.hospitals.length > 0 && (
                      <div className="recommendation-section hospitals-section">
                        <h4>🏥 Nearest Hospitals in Your District</h4>
                        <div className="hospitals-grid">
                          {recommendations.hospitals.map((hospital, index) => (
                            <div key={index} className={`hospital-card ${hospital.type.toLowerCase()}`}>
                              <div className="hospital-type-badge">{hospital.type}</div>
                              <h5>{hospital.name}</h5>
                              <p className="hospital-note">{hospital.note}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Recommended Doctors/Specialists */}
                    {recommendations.specialists && recommendations.specialists.length > 0 && (
                      <div className="recommendation-section specialists-section">
                        <h4>👨‍⚕️ Recommended Specialists</h4>
                        <div className="specialists-list">
                          {recommendations.specialists.map((specialist, index) => (
                            <div key={index} className="specialist-card">
                              <div className="specialist-rank">#{index + 1}</div>
                              <div className="specialist-info">
                                <h5>{specialist.specialist}</h5>
                                <p><strong>Treats:</strong> {specialist.treats}</p>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Treatment Recommendations */}
                    {recommendations.treatments && recommendations.treatments.length > 0 && (
                      <div className="recommendation-section treatments-section">
                        <h4>💊 Recommended Treatments</h4>
                        <ul className="treatments-list">
                          {recommendations.treatments.map((treatment, index) => (
                            <li key={index}>{treatment}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Next Steps for Eligible Users */}
                    {recommendations.eligibility === 'Eligible' && recommendations.nextSteps && (
                      <div className="recommendation-section next-steps-section">
                        <h4>📋 Next Steps to Apply</h4>
                        <ol className="next-steps-list">
                          {recommendations.nextSteps.map((step, index) => (
                            <li key={index}>{step}</li>
                          ))}
                        </ol>
                      </div>
                    )}

                    {/* Benefits for Eligible Users */}
                    {recommendations.eligibility === 'Eligible' && recommendations.benefits && (
                      <div className="recommendation-section benefits-section">
                        <h4>🎁 Your Benefits</h4>
                        <ul className="benefits-list">
                          {recommendations.benefits.map((benefit, index) => (
                            <li key={index}>{benefit}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Alternatives for Not Eligible Users */}
                    {recommendations.eligibility === 'Not Eligible' && recommendations.alternatives && (
                      <div className="recommendation-section alternatives-section">
                        <h4>💡 Alternative Options</h4>
                        <ul className="alternatives-list">
                          {recommendations.alternatives.map((alt, index) => (
                            <li key={index}>{alt}</li>
                          ))}
                        </ul>
                        {recommendations.note && (
                          <p className="note">{recommendations.note}</p>
                        )}
                      </div>
                    )}
                  </div>
                ) : null}
                
                <button className="btn btn-secondary" onClick={resetHealthForm}>
                  Check Again
                </button>
              </div>
            ) : (
              <form className="health-form application-form" onSubmit={handleHealthFormSubmit}>
                {/* Personal Information Section */}
                <div className="form-section-header">
                  <h3>👤 Personal Information</h3>
                </div>
                
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="health-fullName">Full Name *</label>
                    <input
                      type="text"
                      id="health-fullName"
                      name="fullName"
                      value={healthFormData.fullName}
                      onChange={handleHealthInputChange}
                      placeholder="Enter your full name"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="health-age">Age *</label>
                    <input
                      type="number"
                      id="health-age"
                      name="age"
                      value={healthFormData.age}
                      onChange={handleHealthInputChange}
                      placeholder="e.g., 35"
                      min="0"
                      max="120"
                      required
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="health-gender">Gender *</label>
                    <select
                      id="health-gender"
                      name="gender"
                      value={healthFormData.gender}
                      onChange={handleHealthInputChange}
                      required
                    >
                      <option value="">Select Gender</option>
                      <option value="male">Male</option>
                      <option value="female">Female</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label htmlFor="health-phone">Phone Number *</label>
                    <input
                      type="tel"
                      id="health-phone"
                      name="phone"
                      value={healthFormData.phone}
                      onChange={handleHealthInputChange}
                      placeholder="+94 XX XXX XXXX"
                      required
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="health-email">Email Address</label>
                    <input
                      type="email"
                      id="health-email"
                      name="email"
                      value={healthFormData.email}
                      onChange={handleHealthInputChange}
                      placeholder="your.email@example.com"
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="health-district">District *</label>
                    <select
                      id="health-district"
                      name="district"
                      value={healthFormData.district}
                      onChange={handleHealthInputChange}
                      required
                    >
                      <option value="">Select District</option>
                      {sriLankanDistricts.map(district => (
                        <option key={district.value} value={district.value}>
                          {district.label}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Eligibility Information Section */}
                <div className="form-section-header">
                  <h3>📊 Eligibility Information</h3>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="health-familySize">Number of Family Members *</label>
                    <input
                      type="number"
                      id="health-familySize"
                      name="familySize"
                      value={healthFormData.familySize}
                      onChange={handleHealthInputChange}
                      placeholder="e.g., 4"
                      min="1"
                      max="20"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="health-monthlyIncome">Monthly Household Income (LKR) *</label>
                    <select
                      id="health-monthlyIncome"
                      name="monthlyIncome"
                      value={healthFormData.monthlyIncome}
                      onChange={handleHealthInputChange}
                      required
                    >
                      <option value="">Select Income Range</option>
                      <option value="below-25000">Below Rs. 25,000</option>
                      <option value="25000-50000">Rs. 25,000 - 50,000</option>
                      <option value="50000-100000">Rs. 50,000 - 100,000</option>
                      <option value="100000-200000">Rs. 100,000 - 200,000</option>
                      <option value="above-200000">Above Rs. 200,000</option>
                    </select>
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="health-educationLevel">Education Level *</label>
                    <select
                      id="health-educationLevel"
                      name="educationLevel"
                      value={healthFormData.educationLevel}
                      onChange={handleHealthInputChange}
                      required
                    >
                      <option value="">Select Education Level</option>
                      <option value="no-education">No Formal Education</option>
                      <option value="primary">Primary School</option>
                      <option value="secondary">Secondary School</option>
                      <option value="olevel">O/L Completed</option>
                      <option value="alevel">A/L Completed</option>
                      <option value="diploma">Diploma</option>
                      <option value="degree">Bachelor's Degree</option>
                      <option value="postgraduate">Postgraduate</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label htmlFor="health-employmentStatus">Employment Status *</label>
                    <select
                      id="health-employmentStatus"
                      name="employmentStatus"
                      value={healthFormData.employmentStatus}
                      onChange={handleHealthInputChange}
                      required
                    >
                      <option value="">Select Status</option>
                      <option value="employed">Employed</option>
                      <option value="self-employed">Self-Employed</option>
                      <option value="unemployed">Unemployed</option>
                      <option value="retired">Retired</option>
                      <option value="student">Student</option>
                      <option value="unable-to-work">Unable to Work</option>
                    </select>
                  </div>
                </div>

                {/* Medical Information Section */}
                <div className="form-section-header">
                  <h3>🩺 Medical Information (Optional)</h3>
                </div>

                <div className="form-group full-width">
                  <label htmlFor="health-medicalCondition">Current Medical Condition/Concern</label>
                  <input
                    type="text"
                    id="health-medicalCondition"
                    name="medicalCondition"
                    value={healthFormData.medicalCondition}
                    onChange={handleHealthInputChange}
                    placeholder="e.g., Diabetes, Heart Problem, Back Pain, None"
                  />
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="health-symptoms">Main Symptoms</label>
                    <select
                      id="health-symptoms"
                      name="symptoms"
                      value={healthFormData.symptoms}
                      onChange={handleHealthInputChange}
                    >
                      <option value="">Select Symptom (if any)</option>
                      <option value="none">No Current Symptoms</option>
                      <option value="pain">Pain/Ache</option>
                      <option value="fever">Fever/Temperature</option>
                      <option value="breathing">Breathing Difficulty</option>
                      <option value="digestive">Digestive Issues</option>
                      <option value="fatigue">Fatigue/Weakness</option>
                      <option value="chronic">Chronic Condition</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                </div>

                <div className="form-group full-width">
                  <label htmlFor="health-symptomsDescription">Additional Details</label>
                  <textarea
                    id="health-symptomsDescription"
                    name="symptomsDescription"
                    value={healthFormData.symptomsDescription}
                    onChange={handleHealthInputChange}
                    placeholder="Any additional information about your health situation..."
                    rows="3"
                  />
                </div>

                <div className="form-agreement">
                  <label>
                    <input type="checkbox" required />
                    <span>I certify that all information provided is true and accurate. I understand that this is a preliminary eligibility check and final determination will be made by authorized officials.</span>
                  </label>
                </div>

                <button type="submit" className="btn btn-primary submit-application" disabled={isLoadingRecommendations}>
                  {isLoadingRecommendations ? 'Checking Eligibility...' : 'Check Eligibility'}
                </button>
              </form>
            )}
          </section>
        )}

        {/* Senior Care Registration Form */}
        {serviceId === 'senior-care' && (
          <section className="detail-section senior-care-section">
            <h2>👴 Senior Care Registration</h2>
            <p className="form-intro">
              Register a senior citizen for our care programs. Please provide accurate information to help us serve them better.
            </p>
            
            {seniorFormSubmitted ? (
              <div className="form-success">
                <span className="success-icon">✅</span>
                <h3>Registration Submitted Successfully!</h3>
                <p>Reference Number: <strong>SC-{Date.now().toString().slice(-8)}</strong></p>
              </div>
            ) : (
              <form className="application-form senior-form" onSubmit={handleSeniorFormSubmit}>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="senior-fullName">Full Name *</label>
                    <input
                      type="text"
                      id="senior-fullName"
                      name="fullName"
                      value={seniorFormData.fullName}
                      onChange={handleSeniorInputChange}
                      placeholder="Enter full name"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="senior-nic">NIC Number *</label>
                    <input
                      type="text"
                      id="senior-nic"
                      name="nic"
                      value={seniorFormData.nic}
                      onChange={handleSeniorInputChange}
                      placeholder="e.g., 123456789V"
                      required
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="senior-age">Age *</label>
                    <input
                      type="number"
                      id="senior-age"
                      name="age"
                      value={seniorFormData.age}
                      onChange={handleSeniorInputChange}
                      placeholder="e.g., 65"
                      min="60"
                      max="120"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="senior-gender">Gender *</label>
                    <select
                      id="senior-gender"
                      name="gender"
                      value={seniorFormData.gender}
                      onChange={handleSeniorInputChange}
                      required
                    >
                      <option value="">Select Gender</option>
                      <option value="male">Male</option>
                      <option value="female">Female</option>
                    </select>
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="senior-phone">Phone Number *</label>
                    <input
                      type="tel"
                      id="senior-phone"
                      name="phone"
                      value={seniorFormData.phone}
                      onChange={handleSeniorInputChange}
                      placeholder="+94 XX XXX XXXX"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="senior-district">District *</label>
                    <select
                      id="senior-district"
                      name="district"
                      value={seniorFormData.district}
                      onChange={handleSeniorInputChange}
                      required
                    >
                      <option value="">Select District</option>
                      {sriLankanDistricts.map(district => (
                        <option key={district.value} value={district.value}>
                          {district.label}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="senior-livingStatus">Living Status *</label>
                    <select
                      id="senior-livingStatus"
                      name="livingStatus"
                      value={seniorFormData.livingStatus}
                      onChange={handleSeniorInputChange}
                      required
                    >
                      <option value="">Select Living Status</option>
                      <option value="alone">Living Alone</option>
                      <option value="with-spouse">With Spouse</option>
                      <option value="with-family">With Family</option>
                      <option value="care-home">In Care Home</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label htmlFor="senior-mobilityLevel">Mobility Level *</label>
                    <select
                      id="senior-mobilityLevel"
                      name="mobilityLevel"
                      value={seniorFormData.mobilityLevel}
                      onChange={handleSeniorInputChange}
                      required
                    >
                      <option value="">Select Mobility Level</option>
                      <option value="independent">Fully Independent</option>
                      <option value="some-assistance">Needs Some Assistance</option>
                      <option value="wheelchair">Uses Wheelchair</option>
                      <option value="bedridden">Bedridden</option>
                    </select>
                  </div>
                </div>

                <div className="form-agreement">
                  <label>
                    <input type="checkbox" required />
                    <span>I confirm that the information provided is accurate and consent to a welfare officer visit for verification.</span>
                  </label>
                </div>

                <button type="submit" className="btn btn-primary submit-application">
                  Submit Registration
                </button>
              </form>
            )}

            {/* Download Forms Section - Only shows after registration */}
            {seniorFormSubmitted && (
              <div className="download-forms-section">
                <h3>📄 Download Application Forms</h3>
                <p>Thank you for registering! Download these official forms for future use. Print and fill them out to apply for additional benefits.</p>
                <div className="download-cards">
                  <div className="download-card">
                    <div className="download-icon">📋</div>
                    <h4>Pension Form</h4>
                    <p>Senior Citizen Pension Application for monthly allowance benefits</p>
                    <a href="/forms/pension-form.html" download="Pension_Application_Form.html" className="btn btn-download">
                      ⬇️ Download Form
                    </a>
                  </div>
                  <div className="download-card">
                    <div className="download-icon">📝</div>
                    <h4>Aswesuma Form</h4>
                    <p>Aswesuma Welfare Benefit Scheme application for eligible families</p>
                    <a href="/forms/aswesuma-form.html" download="Aswesuma_Application_Form.html" className="btn btn-download">
                      ⬇️ Download Form
                    </a>
                  </div>
                </div>
              </div>
            )}
          </section>
        )}
      </div>
    </div>
  );
}
