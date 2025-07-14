import React, { useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

const Main = ({
    messages,
    input,
    setInput,
    handleSend,
    handleImageChange,
    imagePreview,
    setImagePreview
}) => {
    const messagesEndRef = useRef(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    return (
        <main className="chatgpt-main">
            <div className="chatgpt-messages">
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`chatgpt-message ${msg.sender === 'user' ? 'user' : 'bot'}`}
                    >
                        <div className="avatar">
                            {msg.sender === 'user' ? (
                                <i className="fa fa-user" style={{ fontSize: 28, color: 'var(--color-message-user)' }} aria-label="User"></i>
                            ) : (
                                <i className="fa fa-robot" style={{ fontSize: 28, color: '#6c757d' }} aria-label="Bot"></i>
                            )}
                        </div>
                        <div className="bubble">
                            {msg.text && (
                                msg.sender === 'bot' ?
                                    <ReactMarkdown>{msg.text}</ReactMarkdown> :
                                    <span>{msg.text}</span>
                            )}
                            {msg.image && (
                                <img
                                    src={msg.image}
                                    alt="uploaded"
                                    className="chatgpt-image"
                                />
                            )}
                        </div>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>
            <form className="chatgpt-input-area" onSubmit={handleSend}>
                <label className="chatgpt-upload-btn" title="Upload image">
                    <input
                        type="file"
                        accept="image/*"
                        style={{ display: 'none' }}
                        onChange={handleImageChange}
                    />
                    <i className="fa fa-upload" style={{ fontSize: 22 }}></i>
                </label>
                <input
                    type="text"
                    className="chatgpt-input"
                    placeholder="Type your message..."
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    autoFocus
                />
                <button className="chatgpt-send-btn" type="submit">
                    <i className="fa fa-paper-plane" style={{ fontSize: 22 }}></i>
                </button>
            </form>
            {imagePreview && (
                <div className="chatgpt-image-preview">
                    <img src={imagePreview} alt="Preview" />
                    <button onClick={() => setImagePreview(null)}>Remove</button>
                </div>
            )}
        </main>
    );
};

export default Main;