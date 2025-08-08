app_js_content_with_css_import = """
import React, { useState } from 'react';
import './App.css'; // Import the CSS file

function App() {
  const [name, setName] = useState('');
  const [dietaryLifestyle, setDietaryLifestyle] = useState('');
  const [goals, setGoals] = useState('');
  const [specificGoal, setSpecificGoal] = useState('');
  const [particularNotes, setParticularNotes] = useState('');
  const [goalDate, setGoalDate] = useState(null); // Using null for initial state
  const [investment, setInvestment] = useState('');
  const [age, setAge] = useState(0); // Using 0 for initial state
  const [details, setDetails] = useState(null); // Using null for initial state
  const [plan, setPlan] = useState(null); // Using null for initial state
  const [showWarning, setShowWarning] = useState(false);

  const handleGeneratePlan = () => {
    if (name && dietaryLifestyle && goals && specificGoal && particularNotes && goalDate && investment && age > 0) {
      const userDetails = {
        "Dietary Lifestyle": dietaryLifestyle,
        "Goal(s)": goals,
        "Specific Goal": specificGoal,
        "Particular Notes/Specifications": particularNotes,
        "Projected Goal Date": goalDate ? goalDate.toLocaleDateString('en-US') : null,
        "Preferred Investment Range": investment,
        "Age": age
      };
      setDetails(userDetails);
      setShowWarning(false);
      
    } else {
      setDetails(null);
      setPlan(null);
      setShowWarning(true);
    }
  };

  return (
    <div>
      <h1>Personalized Diet & Fitness Planner</h1>

      <div>
        <label>What is your name, or what should we call you?</label>
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Enter name" />
        {name && <p style={{ color: 'green' }}>Hi {name}! Welcome to the community! Let's get started.</p>}
      </div>

      {name && (
        <div>
          <div>
            <label>What is your dietary lifestyle? (e.g., vegetarian, vegan, non-vegetarian, no restrictions)</label>
            <input type="text" value={dietaryLifestyle} onChange={(e) => setDietaryLifestyle(e.target.value)} placeholder="Enter dietary lifestyle" />
          </div>

          <div>
            <label>What is your aim with this platform?</label>
            <select value={goals} onChange={(e) => setGoals(e.target.value)}>
              <option value="">Select goal</option>
              <option value="fitness">fitness</option>
              <option value="health">health</option>
              <option value="weight-management">weight-management</option>
            </select>
            {goals === "fitness" && <p>Looks like you want to improve your fitness levels. Good for you!</p>}
            {goals === "health" && <p>Looks like you want to improve your health. Good for you!</p>}
            {goals === "weight-management" && <p>Looks like you want to work on your weight. Good for you!</p>}
          </div>

          {goals && (
            <div>
              <div>
                <label>What is your specific goal?</label>
                <input type="text" value={specificGoal} onChange={(e) => setSpecificGoal(e.target.value)} placeholder="Enter specific goal" />
              </div>

              <div>
                <label>Any specific area of your body or any further specifications?</label>
                <input type="text" value={particularNotes} onChange={(e) => setParticularNotes(e.target.value)} placeholder="Enter specifications" />
              </div>

              <div>
                <label>What is your goal date?</label>
                 {/* Input type="date" gives a string in YYYY-MM-DD format */}
                 <input type="date" onChange={(e) => setGoalDate(new Date(e.target.value))} />
              </div>

              <div>
                <label>How much are you willing to invest per month? (e.g., $100-$200)</label>
                <input type="text" value={investment} onChange={(e) => setInvestment(e.target.value)} placeholder="Enter investment range" />
              </div>

              <div>
                <label>Lastly, what is your age?</label>
                <input type="number" value={age} onChange={(e) => setAge(parseInt(e.target.value))} min="0" step="1" placeholder="Enter age" />
                {age > 0 && age <= 1 && <p>You are in the infant category.</p>}
                {age >= 1 && age < 13 && <p>You are in the child category.</p>}
                {age >= 13 && age < 18 && <p>You are in the teenager category.</p>}
                {age >= 18 && <p>You fall under the adult category.</p>}
              </div>

              <button onClick={handleGeneratePlan}>Generate My Plan</button>

              {showWarning && <p style={{ color: 'red' }}>Please fill in all the fields to generate your personalized plan.</p>}

              {details && (
                <div>
                  <h2>Here is what you provided:</h2>
                  <pre>{JSON.stringify(details, null, 2)}</pre> {/* Use pre and JSON.stringify for displaying JSON */}
                </div>
              )}

              {plan && (
                <div>
                  <h2>Your Customized Plan:</h2>
                  <p>{plan}</p>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {!name && <p style={{ color: 'orange' }}>Please enter your name to start.</p>}
    </div>
  );
}

export default App;
"""

print(app_js_content_with_css_import)
