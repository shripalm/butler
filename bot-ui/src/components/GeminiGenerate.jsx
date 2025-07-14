import React, { useState } from "react";

const GEMINI_API_KEY = "AIzaSyAW3bf6TFoHUjXQoaUMubn1y3dyLejhgZA";
const GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent";

export default function GeminiGenerate() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResponse("");
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
      } else {
        setResponse(
          data.candidates?.[0]?.content?.parts?.[0]?.text || "No response"
        );
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "2rem auto", padding: 24, background: "#fff", borderRadius: 8, boxShadow: "0 2px 8px #eee" }}>
      <h2>Gemini 2.0 Flash Chat</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: 16 }}>
        <textarea
          value={input}
          onChange={e => setInput(e.target.value)}
          rows={4}
          style={{ width: "100%", marginBottom: 8 }}
          placeholder="Ask Gemini something..."
        />
        <br />
        <button type="submit" disabled={loading || !input.trim()}>
          {loading ? "Generating..." : "Generate"}
        </button>
      </form>
      {error && <div style={{ color: "red" }}>{error}</div>}
      {response && (
        <div style={{ marginTop: 16, whiteSpace: "pre-wrap", background: "#f6f6f6", padding: 12, borderRadius: 4 }}>
          <strong>Gemini:</strong> {response}
        </div>
      )}
    </div>
  );
}
