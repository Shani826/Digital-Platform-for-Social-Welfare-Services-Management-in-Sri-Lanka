import { useState, useEffect } from 'react';
import '../styles/HeroSection.css';

export default function HeroSection() {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const images = ['/1.jpg', '/2.jpg', '/3.jpg'];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentImageIndex((prevIndex) => (prevIndex + 1) % images.length);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <section className="hero" id="home">
      {/* Fullscreen blurred background images */}
      <div className="hero-background">
        {images.map((image, index) => (
          <div
            key={index}
            className={`hero-bg-image ${index === currentImageIndex ? 'active' : ''}`}
            style={{ backgroundImage: `url(${image})` }}
          />
        ))}
        <div className="hero-overlay"></div>
      </div>

      <div className="hero-container">
        <div className="hero-content">
          <h1>Welfare Services for All Sri Lankans</h1>
          <p>"A centralized digital platform for social welfare service management in Sri Lanka, enabling efficient service delivery, transparent processes, and secure, easy access for citizens."</p>
          <div className="hero-buttons">
            <button 
              className="btn btn-primary"
              onClick={() => document.getElementById('services').scrollIntoView({ behavior: 'smooth' })}
            >
              Get Started
            </button>
          </div>
        </div>
      </div>

      {/* Creative wave bottom edge */}
      <div className="hero-wave">
        <svg viewBox="0 0 1440 120" preserveAspectRatio="none">
          <path d="M0,60 C360,120 720,0 1080,60 C1260,90 1380,90 1440,60 L1440,120 L0,120 Z" fill="#f8f9fa"/>
        </svg>
      </div>
    </section>
  );
}
