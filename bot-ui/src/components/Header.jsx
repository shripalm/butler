import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import dentsuLogoLight from '../dentsu-4light.png';
import dentsuLogoDark from '../dentsu-4dark.png';

const navLinks = [
    { to: '/', label: 'Home' },
    { to: '/generate', label: 'Generate' },
    { to: '/support', label: 'Support' }
];

const lightTheme = {
    '--color-bg': '#f5f7fa',
    '--color-bg-alt': '#e9eafc',
    '--color-header': '#fff',
    '--color-message-bg': '#e0e7ff',
    '--color-message-bg-user': '#fffbe7',
    '--color-message-user': '#ff6c22',
    '--color-message-bot': '#3b3b3b',
    '--color-input-bg': '#fff',
    '--color-input-bg-focus': '#f0f4ff',
    '--color-send-btn': '#6c63ff',
    '--color-send-btn-hover': '#4834d4',
    '--color-upload-btn': '#6c63ff',
    '--color-upload-btn-hover': '#ff6c22',
    '--color-avatar-border': '#6c63ff',
    '--color-avatar-user-border': '#ff6c22',
    '--color-shadow': 'rgba(0,0,0,0.08)',
    '--color-shadow-strong': 'rgba(0,0,0,0.12)',
    '--color-white': '#fff'
};

const darkTheme = {
    '--color-bg': '#23272f',
    '--color-bg-alt': '#393053',
    '--color-header': '#181a20',
    '--color-message-bg': '#635985',
    '--color-message-bg-user': '#393053',
    '--color-message-user': '#00C4FF',
    '--color-message-bot': '#F8EDFF',
    '--color-input-bg': '#23272f',
    '--color-input-bg-focus': '#393053',
    '--color-send-btn': '#00C4FF',
    '--color-send-btn-hover': '#00a3cc',
    '--color-upload-btn': '#00C4FF',
    '--color-upload-btn-hover': '#FF6C22',
    '--color-avatar-border': '#00C4FF',
    '--color-avatar-user-border': '#FF6C22',
    '--color-shadow': 'rgba(0,0,0,0.08)',
    '--color-shadow-strong': 'rgba(0,0,0,0.12)',
    '--color-white': '#fff'
};

const applyTheme = (themeObj) => {
    Object.entries(themeObj).forEach(([key, value]) => {
        document.documentElement.style.setProperty(key, value);
    });
};

const Header = ({ dark, setDark }) => {
    const location = useLocation();
    const [drawerOpen, setDrawerOpen] = useState(false);

    useEffect(() => {
        applyTheme(dark ? darkTheme : lightTheme);
        document.body.classList.toggle('dark-theme', dark);
        localStorage.setItem('theme', dark ? 'dark' : 'light');
    }, [dark]);

    // Close drawer on route change
    useEffect(() => {
        setDrawerOpen(false);
    }, [location.pathname]);

    // Prevent background scroll when drawer is open
    useEffect(() => {
        if (drawerOpen) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    }, [drawerOpen]);

    return (
        <header className="chatgpt-header">
            <div className="chatgpt-header-inner">
                <div className="chatgpt-header-title">
                    <Link to="/" className="d-flex align-items-center text-decoration-none">
                        <img
                            src={dark ? dentsuLogoDark : dentsuLogoLight}
                            alt="Dentsu Logo"
                            style={{ height: 32, marginRight: 10, borderRadius: 6, padding: 2 }}
                        />
                    </Link>
                </div>
                {/* Desktop nav */}
                <nav className="d-none d-md-block">
                    <ul className="nav nav-pills gap-2">
                        {navLinks.map(link => (
                            <li className="nav-item" key={link.to}>
                                <Link
                                    to={link.to}
                                    className={`nav-link px-3 py-1 rounded-pill fw-semibold ${
                                        location.pathname === link.to
                                            ? 'active text-white'
                                            : 'text-primary'
                                    }`}
                                    style={{
                                        background: location.pathname === link.to
                                            ? 'linear-gradient(90deg, var(--color-send-btn), var(--color-message-user))'
                                            : 'transparent',
                                        transition: 'background 0.2s, color 0.2s'
                                    }}
                                >
                                    {link.label}
                                </Link>
                            </li>
                        ))}
                    </ul>
                </nav>
                {/* Theme toggle */}
                <div className="d-none d-md-block align-items-center ms-3">
                    <div className="form-check form-switch m-0">
                        <input
                            className="form-check-input"
                            type="checkbox"
                            id="themeSwitch"
                            checked={dark}
                            onChange={() => setDark(d => !d)}
                            style={{ cursor: 'pointer' }}
                        />
                        <label htmlFor="themeSwitch" className="ms-2 mb-0" style={{ cursor: 'pointer' }}>
                            {dark
                                ? <i className="fa fa-moon" style={{ color: '#FFD700', fontSize: 20 }} aria-label="Dark" />
                                : <i className="fa fa-sun" style={{ color: '#FFA500', fontSize: 20 }} aria-label="Light" />
                            }
                        </label>
                    </div>
                </div>
                {/* Mobile menu button */}
                <button
                    className="btn btn-link d-md-none ms-auto"
                    style={{ fontSize: 26, color: 'var(--color-message-bot)' }}
                    onClick={() => setDrawerOpen(true)}
                    aria-label="Open menu"
                >
                    <i className="fa fa-bars"></i>
                </button>
            </div>
            {/* Drawer for mobile */}
            <div className={`mobile-drawer${drawerOpen ? ' open' : ''}`}>
                <div className="mobile-drawer-header d-flex justify-content-between align-items-center px-3 py-2">
                    <span style={{ fontWeight: 600, fontSize: 18 }}></span>
                    <button
                        className="btn btn-link"
                        style={{ fontSize: 26, color: 'var(--color-message-bot)' }}
                        onClick={() => setDrawerOpen(false)}
                        aria-label="Close menu"
                    >
                        <i className="fa fa-times"></i>
                    </button>
                </div>
                <ul className="nav flex-column px-3 mt-2">
                    {navLinks.map(link => (
                        <li className="nav-item" key={link.to}>
                            <Link
                                to={link.to}
                                className={`nav-link py-2 fw-semibold ${
                                    location.pathname === link.to
                                        ? 'active text-white'
                                        : 'text-primary'
                                }`}
                                style={{
                                    background: location.pathname === link.to
                                        ? 'linear-gradient(90deg, var(--color-send-btn), var(--color-message-user))'
                                        : 'transparent',
                                    borderRadius: 20,
                                    marginBottom: 4,
                                    fontSize: 18,
                                    transition: 'background 0.2s, color 0.2s'
                                }}
                                onClick={() => setDrawerOpen(false)}
                            >
                                {link.label}
                            </Link>
                        </li>
                    ))}
                </ul>
                <div className="px-3 py-2">
                    <div style={{ display: 'flex', justifyContent: 'center' }}>
                        <div className="form-check form-switch">
                            <input
                                className="form-check-input"
                                type="checkbox"
                                id="themeSwitchMobile"
                                checked={dark}
                                onChange={() => setDark(d => !d)}
                                style={{ cursor: 'pointer' }}
                            />
                            <label htmlFor="themeSwitchMobile" className="ms-2 mb-0" style={{ cursor: 'pointer' }}>
                                {dark
                                    ? <i className="fa fa-moon" style={{ color: '#FFD700', fontSize: 20 }} aria-label="Dark" />
                                    : <i className="fa fa-sun" style={{ color: '#FFA500', fontSize: 20 }} aria-label="Light" />
                                }
                            </label>
                        </div>
                    </div>
                </div>
            </div>
            {/* Overlay */}
            {drawerOpen && <div className="mobile-drawer-backdrop" onClick={() => setDrawerOpen(false)} />}
        </header>
    );
};

export default Header;