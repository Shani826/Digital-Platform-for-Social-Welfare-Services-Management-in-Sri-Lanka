import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar'
import HeroSection from './components/HeroSection'
import Services from './components/Services'
import About from './components/About'
import ContactForm from './components/ContactForm'
import Footer from './components/Footer'
import ChatBot from './components/ChatBot'
import ServiceDetail from './pages/ServiceDetail'
import ServicesPage from './pages/ServicesPage'
import AboutPage from './pages/AboutPage'
import ContactPage from './pages/ContactPage'
import LoginPage from './pages/LoginPage'
import './App.css'

function Home() {
  return (
    <>
      <HeroSection />
      <Services />
      <About />
      <ContactForm />
    </>
  );
}

function App() {
  return (
    <Router>
      <div className="app">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/services" element={<ServicesPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/contact" element={<ContactPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/service/:serviceId" element={<ServiceDetail />} />
        </Routes>
        <Footer />
        <ChatBot />
      </div>
    </Router>
  )
}

export default App
