import React, { useState, useEffect } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Get the codespace name from the current hostname or use localhost for local development
    const hostname = window.location.hostname;
    const isCodespaces = hostname.includes('app.github.dev');
    const apiUrl = isCodespaces 
      ? `https://${hostname.replace(/-(3000|8000)/, '-8000')}/api/teams/`
      : 'http://localhost:8000/api/teams/';
    console.log('Teams component - Fetching from API endpoint:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Teams component - Fetched data:', data);
        // Handle both paginated (.results) and plain array responses
        const teamsData = data.results || data;
        console.log('Teams component - Processed teams data:', teamsData);
        setTeams(teamsData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Teams component - Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="container mt-4"><p>Loading teams...</p></div>;
  if (error) return <div className="container mt-4"><p>Error: {error}</p></div>;

  return (
    <div className="container mt-4">
      <h2>Teams</h2>
      <div className="row">
        {teams.map(team => (
          <div key={team.id} className="col-md-6 mb-3">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">{team.name}</h5>
                <p className="card-text">{team.description}</p>
                <p className="card-text">
                  <small className="text-muted">Created: {new Date(team.created_at).toLocaleDateString()}</small>
                </p>
                {team.members && team.members.length > 0 && (
                  <div>
                    <strong>Members:</strong> {team.members.join(', ')}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Teams;
