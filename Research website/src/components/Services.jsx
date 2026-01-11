import ServiceCard from './ServiceCard';
import '../styles/Services.css';

export default function Services() {
  const services = [
    {
      id: 1,
      icon: '📈',
      title: 'Investment Recommender',
      description: 'Smart investment recommendations and financial planning assistance',
      link: 'family-support'
    },
    {
      id: 2,
      icon: '🏥',
      title: 'Health Services',
      description: 'Comprehensive healthcare and medical assistance programs',
      link: 'health-services'
    },
    {
      id: 3,
      icon: '🤖',
      title: 'AI-GIS Welfare Insights',
      description: 'AI-powered geographic insights for welfare program optimization',
      link: 'ai-gis-insights'
    },
    {
      id: 4,
      icon: '👴',
      title: 'Senior Care',
      description: 'Special programs and benefits for elderly citizens',
      link: 'senior-care'
    },
    {
      id: 5,
      icon: '💼',
      title: 'Employment Programs',
      description: 'Job training and employment assistance initiatives',
      link: 'employment'
    },
    {
      id: 6,
      icon: '🏠',
      title: 'Housing Assistance',
      description: 'Housing subsidies and accommodation programs',
      link: 'housing'
    }
  ];

  return (
    <section className="services" id="services">
      <div className="services-container">
        <h2>Our Services</h2>
        <p className="section-subtitle">
          Comprehensive welfare programs designed to improve the lives of all Sri Lankans
        </p>
        
        <div className="services-grid">
          {services.map(service => (
            <ServiceCard
              key={service.id}
              icon={service.icon}
              isImage={service.isImage}
              title={service.title}
              description={service.description}
              link={service.link}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
