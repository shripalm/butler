import React, { useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import dentsuLogoLight from '../dentsu-4light.png';
import dentsuLogoDark from '../dentsu-4dark.png';

// Animated count-up hook
function useCountUp(to, duration = 1200) {
    const ref = useRef();
    useEffect(() => {
        let start = 0;
        const end = typeof to === "number" ? to : parseInt(to.replace(/\D/g, ""));
        const increment = end / (duration / 16);
        let current = start;
        let frame;
        function animate() {
            current += increment;
            if (current < end) {
                ref.current.textContent = Math.floor(current).toLocaleString();
                frame = requestAnimationFrame(animate);
            } else {
                ref.current.textContent = typeof to === "number" ? to : to;
            }
        }
        animate();
        return () => cancelAnimationFrame(frame);
    }, [to, duration]);
    return ref;
}

// Dentsu stats for "At a Glance"
const stats = [
    { label: "Countries", value: "145+", icon: "fa-globe" },
    { label: "Employees", value: 65000, icon: "fa-users" },
    { label: "Founded", value: 1901, icon: "fa-building" },
    { label: "Clients", value: "11,000+", icon: "fa-handshake" },
];

// Dentsu values/vision
const values = [
    {
        title: "Innovation",
        desc: "Pioneering new solutions for a digital-first world.",
        icon: "fa-lightbulb"
    },
    {
        title: "Collaboration",
        desc: "Working together globally for client success.",
        icon: "fa-people-group"
    },
    {
        title: "Diversity",
        desc: "Embracing diverse perspectives and talents.",
        icon: "fa-earth-asia"
    },
    {
        title: "Sustainability",
        desc: "Driving positive change for society and the planet.",
        icon: "fa-leaf"
    }
];

const ActionButtons = () => (
    <div className="d-flex justify-content-center gap-3 my-4">
        <Link to="/generate" className="btn btn-primary">
            Try Generate
        </Link>
        <Link to="/support" className="btn btn-secondary">
            Support
        </Link>
    </div>
);

const Home = ({ dark }) => {
    const employeeRef = useCountUp(65000);

    return (
        <>
            <div className="home-bg" />
            <div className="container py-5" style={{ position: "relative", zIndex: 1 }}>
                <div className="text-center mb-5">
					<img
                        src={dark ? dentsuLogoDark : dentsuLogoLight}
                        alt="Dentsu Logo"
                        style={{
                            height: 60,
                            borderRadius: 8,
                            marginBottom: 16,
                        }}
                    />
                    <h2 className="mb-3 dentsu-heading">Welcome to Dentsu AI</h2>
                    <p className="lead text-dentsu">
                        Dentsu is a global leader in marketing, media, and digital
                        transformation. Explore our AI-powered solutions and discover how we
                        drive innovation for brands worldwide.
                    </p>
                    {/* Button pair below intro paragraph */}
                    <ActionButtons />
                </div>

                {/* Dentsu at a Glance - Animated Stats */}
                <div className="row g-4 mb-5 justify-content-center">
                    {stats.map((stat, idx) => (
                        <div
                            className="col-6 col-md-3"
                            key={stat.label}
                            style={{ animation: `fadeInUp 0.6s ${0.1 * idx + 0.2}s both` }}
                        >
                            <div className="card h-100 shadow border-0 text-center glance-card">
                                <div className="card-body">
                                    <i className={`fa ${stat.icon} mb-2`} style={{ fontSize: 32, color: "var(--color-send-btn)" }}></i>
                                    <h3 className="fw-bold mb-1" style={{ color: "var(--color-message-user)" }}>
                                        {stat.label === "Employees"
                                            ? <span ref={employeeRef} /> // animated count up
                                            : stat.value}
                                    </h3>
                                    <div className="text-muted small">{stat.label}</div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Dentsu Values/Vision */}
                <div className="mb-5">
                    <h4 className="mb-4 text-center dentsu-heading" style={{ letterSpacing: 1 }}>Our Values</h4>
                    <div className="row g-4 justify-content-center">
                        {values.map((v, idx) => (
                            <div
                                className="col-12 col-md-6 col-lg-3"
                                key={v.title}
                                style={{ animation: `fadeInUp 0.7s ${0.2 * idx + 0.3}s both` }}
                            >
                                <div className="card h-100 border-0 shadow-sm text-center value-card">
                                    <div className="card-body">
                                        <i className={`fa ${v.icon} mb-3`} style={{ fontSize: 28, color: "var(--color-message-bot)" }}></i>
                                        <h5 className="fw-bold mb-2">{v.title}</h5>
                                        <p className="text-muted small">{v.desc}</p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* What can Dentsu AI do for you */}
                <div className="mt-5 text-center">
                    <h4 className="mb-3 text-dentsu">
                        What can Dentsu AI do for you?
                    </h4>
                    <ul className="list-unstyled text-dentsu">
                        <li style={{ animation: "fadeInLeft 0.7s 0.2s both" }}>🤖 Generate creative content and ideas</li>
                        <li style={{ animation: "fadeInLeft 0.7s 0.4s both" }}>📊 Analyze marketing data and trends</li>
                        <li style={{ animation: "fadeInLeft 0.7s 0.6s both" }}>🌐 Enhance customer experiences with AI</li>
                        <li style={{ animation: "fadeInLeft 0.7s 0.8s both" }}>🚀 Accelerate your brand's digital transformation</li>
                    </ul>
                    {/* Button pair below list */}
                    <ActionButtons />
                </div>
            </div>
        </>
    );
};

export default Home;