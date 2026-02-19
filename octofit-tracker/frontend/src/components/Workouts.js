import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Get the codespace name from the current hostname or use localhost for local development
    const hostname = window.location.hostname;
    const isCodespaces = hostname.includes('app.github.dev');
    const apiUrl = isCodespaces 
      ? `https://${hostname.replace(/-(3000|8000)/, '-8000')}/api/workouts/`
      : 'http://localhost:8000/api/workouts/';
    console.log('Workouts component - Fetching from API endpoint:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts component - Fetched data:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        console.log('Workouts component - Processed workouts data:', workoutsData);
        setWorkouts(workoutsData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Workouts component - Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="container mt-4"><p>Loading workouts...</p></div>;
  if (error) return <div className="container mt-4"><p>Error: {error}</p></div>;

  return (
    <div className="container mt-4">
      <h2>Workout Suggestions</h2>
      <div className="row">
        {workouts.map(workout => (
          <div key={workout.id} className="col-md-6 mb-3">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">{workout.name}</h5>
                <p className="card-text">{workout.description}</p>
                <ul className="list-group list-group-flush">
                  <li className="list-group-item">
                    <strong>Type:</strong> {workout.workout_type}
                  </li>
                  <li className="list-group-item">
                    <strong>Duration:</strong> {workout.duration} minutes
                  </li>
                  <li className="list-group-item">
                    <strong>Difficulty:</strong> {workout.difficulty}
                  </li>
                  <li className="list-group-item">
                    <strong>Calories:</strong> {workout.calories_estimate}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Workouts;
