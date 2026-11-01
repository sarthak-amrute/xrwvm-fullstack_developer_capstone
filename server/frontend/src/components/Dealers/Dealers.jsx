import React, { useState, useEffect } from 'react';
import './Dealers.css';

const Dealers = ({ user }) => {
  const [dealers, setDealers] = useState([]);
  const [states, setStates] = useState([]);
  const [selectedState, setSelectedState] = useState('All');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDealers();
  }, []);

  const fetchDealers = async (state = 'All') => {
    setLoading(true);
    try {
      const url = state === 'All' ? '/djangoapp/get_dealers' : `/djangoapp/get_dealers/${state}`;
      const response = await fetch(url);
      const data = await response.json();
      setDealers(data.dealers || []);
      if (state === 'All') {
        const uniqueStates = [...new Set((data.dealers || []).map(d => d.state))].sort();
        setStates(uniqueStates);
      }
    } catch (err) {
      console.error('Error fetching dealers:', err);
    }
    setLoading(false);
  };

  const handleStateChange = (e) => {
    const state = e.target.value;
    setSelectedState(state);
    fetchDealers(state);
  };

  return (
    <div>
      <div className="hero-banner text-center text-white py-5">
        <h1 className="display-4">Find Your Perfect Car</h1>
        <p className="lead">Browse our dealership locations across the United States</p>
      </div>
      <div className="container py-4">
        <div className="row mb-4">
          <div className="col-md-4">
            <select className="form-control" value={selectedState} onChange={handleStateChange}>
              <option value="All">All States</option>
              {states.map(state => <option key={state} value={state}>{state}</option>)}
            </select>
          </div>
        </div>
        {loading ? (
          <div className="text-center py-5"><div className="spinner-border text-primary"></div></div>
        ) : (
          <div className="row">
            {dealers.map(dealer => (
              <div key={dealer.id} className="col-md-4 mb-4">
                <div className="card dealer-card h-100">
                  <div className="card-body">
                    <h5 className="card-title">{dealer.full_name}</h5>
                    <p className="text-muted"><i className="fas fa-map-marker-alt"></i> {dealer.city}, {dealer.state}</p>
                    <p className="text-muted"><i className="fas fa-phone"></i> {dealer.zip}</p>
                    <a href={`/dealer/${dealer.id}`} className="btn btn-outline-primary btn-sm">View Details</a>
                    {user && (
                      <a href={`/postreview/${dealer.id}`} className="btn btn-primary btn-sm ml-2">Review Dealer</a>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dealers;
