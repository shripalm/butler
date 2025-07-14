import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import OpenWebUI from './components/OpenWebUI';
import Header from './components/Header';
import Home from "./components/Home";

const randomImages = [
  'https://picsum.photos/seed/1/600/300',
  'https://picsum.photos/seed/2/600/300',
  'https://picsum.photos/seed/3/600/300',
  'https://picsum.photos/seed/4/600/300',
  'https://picsum.photos/seed/5/600/300',
];

function getRandomImage() {
  return randomImages[Math.floor(Math.random() * randomImages.length)];
}

// Support page example
const Support = () => (
  <div className="container text-center py-5">
    <h2 className="mb-4 dentsu-heading">Support</h2>
    <img src={getRandomImage()} alt="Random" className="img-fluid rounded shadow" />
  </div>
);

function App() {
  // Theme state moved here
  const [dark, setDark] = useState(() => {
    const stored = localStorage.getItem('theme');
    if (stored === 'dark') return true;
    if (stored === 'light') return false;
    return window.matchMedia &&
      window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  useEffect(() => {
    localStorage.setItem('theme', dark ? 'dark' : 'light');
    document.body.classList.toggle('dark-theme', dark);
  }, [dark]);

  return (
    <Router>
      <Header dark={dark} setDark={setDark} />
      <Routes>
        <Route path="/" element={<Home dark={dark} />} />
        <Route path="/generate" element={<OpenWebUI />} />
        <Route path="/support" element={<Support />} />
      </Routes>
    </Router>
  );
}

export default App;