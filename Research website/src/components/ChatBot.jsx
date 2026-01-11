import { useState, useRef, useEffect } from 'react';
import '../styles/ChatBot.css';

const ChatBot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hello! 👋 I'm the Welfare Services Assistant. I can help you with information about welfare programs, eligibility, applications, and more. What would you like to know?"
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const quickQuestions = [
    { text: '📋 Available Programs', question: 'What programs are available?' },
    { text: '✅ Eligibility', question: 'Who is eligible for welfare services?' },
    { text: '📝 How to Apply', question: 'How do I apply for welfare services?' },
    { text: '🏥 Health Services', question: 'What health services are available?' },
  ];

  const handleSendMessage = async (message) => {
    if (!message.trim()) return;

    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: message }]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message, language: 'en' }),
      });

      const data = await response.json();
      
      if (data.success) {
        setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
      } else {
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: "I'm sorry, I'm having trouble connecting. Please try again later." 
        }]);
      }
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: "I'm sorry, I'm having trouble connecting to the server. Please make sure the backend is running." 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    handleSendMessage(inputValue);
  };

  const handleQuickQuestion = (question) => {
    handleSendMessage(question);
  };

  const handleClose = () => {
    setIsOpen(false);
    // Clear chat history and reset to initial message
    setMessages([
      {
        role: 'assistant',
        content: "Hello! 👋 I'm the Welfare Services Assistant. I can help you with information about welfare programs, eligibility, applications, and more. What would you like to know?"
      }
    ]);
    setInputValue('');
  };

  return (
    <>
      {/* Chat Button */}
      <button 
        className={`chat-button ${isOpen ? 'hidden' : ''}`}
        onClick={() => setIsOpen(true)}
        aria-label="Open chat"
      >
        <span className="chat-icon">💬</span>
        <span className="chat-tooltip">Chat with us!</span>
      </button>

      {/* Chat Window */}
      <div className={`chat-window ${isOpen ? 'open' : ''}`}>
        {/* Header */}
        <div className="chat-header">
          <div className="chat-header-info">
            <span className="chat-avatar">🤖</span>
            <div>
              <h4>Welfare Assistant</h4>
              <span className="chat-status">Online</span>
            </div>
          </div>
          <button className="chat-close" onClick={handleClose}>
            ✕
          </button>
        </div>

        {/* Messages */}
        <div className="chat-messages">
          {messages.map((msg, index) => (
            <div key={index} className={`chat-message ${msg.role}`}>
              {msg.role === 'assistant' && <span className="message-avatar">🤖</span>}
              <div className="message-content">
                {msg.content}
              </div>
              {msg.role === 'user' && <span className="message-avatar">👤</span>}
            </div>
          ))}
          {isLoading && (
            <div className="chat-message assistant">
              <span className="message-avatar">🤖</span>
              <div className="message-content typing">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Quick Questions */}
        <div className="quick-questions">
          {quickQuestions.map((q, index) => (
            <button 
              key={index} 
              className="quick-question-btn"
              onClick={() => handleQuickQuestion(q.question)}
            >
              {q.text}
            </button>
          ))}
        </div>

        {/* Input */}
        <form className="chat-input-form" onSubmit={handleSubmit}>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your question..."
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading || !inputValue.trim()}>
            ➤
          </button>
        </form>
      </div>
    </>
  );
};

export default ChatBot;
