import React, { useState } from 'react';
import Main from './Main';

const GEMINI_API_KEY = "AIzaSyAW3bf6TFoHUjXQoaUMubn1y3dyLejhgZA";
const GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent";

const OpenWebUI = () => {
    const [messages, setMessages] = useState([
        { sender: 'bot', text: 'Hello! How can I help you today?' }
    ]);
    const [input, setInput] = useState('');
    const [imagePreview, setImagePreview] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim() && !imagePreview) return;

        if (input.trim()) {
            setMessages(msgs => [...msgs, { sender: 'user', text: input }]);
            setLoading(true);
            setError("");
            try {
                const res = await fetch(`${GEMINI_ENDPOINT}?key=${GEMINI_API_KEY}`,
                    {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            contents: [
                                { parts: [{ text: input }] }
                            ]
                        })
                    }
                );
                const data = await res.json();
                if (!res.ok) {
                    setError(data.error?.message || "Unknown error");
                    setMessages(msgs => [...msgs, { sender: 'bot', text: '[Error: ' + (data.error?.message || 'Unknown error') + ']' }]);
                } else {
                    setMessages(msgs => [
                        ...msgs,
                        { sender: 'bot', text: data.candidates?.[0]?.content?.parts?.[0]?.text || "No response" }
                    ]);
                }
            } catch (err) {
                setError(err.message);
                setMessages(msgs => [...msgs, { sender: 'bot', text: '[Error: ' + err.message + ']' }]);
            } finally {
                setLoading(false);
            }
        }

        if (imagePreview) {
            setMessages(msgs => [
                ...msgs,
                { sender: 'user', image: imagePreview }
            ]);
            setTimeout(() => {
                setMessages(msgs => [
                    ...msgs,
                    { sender: 'bot', text: "Nice image! (Image handling is a demo only)" }
                ]);
            }, 700);
            setImagePreview(null);
        }

        setInput('');
    };

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setImagePreview(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    return (
        <div className="chatgpt-ui">
            <Main
                messages={messages}
                input={input}
                setInput={setInput}
                handleSend={handleSend}
                handleImageChange={handleImageChange}
                imagePreview={imagePreview}
                setImagePreview={setImagePreview}
                loading={loading}
                error={error}
            />
        </div>
    );
};

export default OpenWebUI;