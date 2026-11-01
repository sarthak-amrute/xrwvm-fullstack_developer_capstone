import React from 'react';

const Header = ({ user, onLogout }) => {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <a className="navbar-brand" href="/">&#9965; Best Cars Dealership</a>
      <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav">
        <span className="navbar-toggler-icon"></span>
      </button>
      <div className="collapse navbar-collapse" id="navbarNav">
        <ul className="navbar-nav ml-auto">
          <li className="nav-item"><a className="nav-link" href="/">Home</a></li>
          <li className="nav-item"><a className="nav-link" href="/static/About.html">About Us</a></li>
          <li className="nav-item"><a className="nav-link" href="/static/Contact.html">Contact Us</a></li>
          {user ? (
            <>
              <li className="nav-item"><span className="nav-link text-light">Welcome, {user}!</span></li>
              <li className="nav-item">
                <button className="btn btn-outline-light btn-sm mt-1 ml-2" onClick={onLogout}>Logout</button>
              </li>
            </>
          ) : (
            <>
              <li className="nav-item"><a className="nav-link" href="/login">Login</a></li>
              <li className="nav-item"><a className="nav-link" href="/register">Register</a></li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default Header;
