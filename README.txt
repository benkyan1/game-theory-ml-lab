# 🎮 Prisoner's Dilemma - Interactive Game Theory Simulator

An interactive web application that demonstrates the classic Prisoner's Dilemma from game theory, built with Flask, Python, and modern web technologies.

## ✨ Features

- **Interactive Gameplay**: Play against an AI opponent using various strategies
- **Real-time Scoring**: Watch your scores update instantly
- **Strategy Analysis**: Get insights into your playing style and patterns
- **Nash Equilibrium**: Visualize game theory concepts in action
- **Beautiful UI**: Animated characters, feedback popups, and engaging design
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd game_theory_ui

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py


Access the Game
Open your browser and navigate to: http://127.0.0.1:5000

🎯 How to Play
Start the Game: Click "Start Playing" on the home page

Make Your Choice:

🤝 Cooperate: Stay silent, trust your partner

⚔️ Defect: Betray your partner for personal gain

Watch the Results: See how your choice affects both players' scores

Analyze Your Strategy: Click "Analyze Strategy" to get insights

Play Multiple Rounds: See how strategies evolve over time

📊 Game Theory Concepts
Payoff Matrix: (You, Opponent)

Both Cooperate: (3, 3) - Best for society

Cooperate/Defect: (0, 5) - You get betrayed

Defect/Cooperate: (5, 0) - You betray for gain

Both Defect: (1, 1) - Mutual destruction

Nash Equilibrium: (Defect, Defect) is the only stable outcome

Dominant Strategy: Defecting always gives better individual payoff

Pareto Optimal: (Cooperate, Cooperate) is best for both players

🧠 AI Strategies
The AI opponent uses Tit-for-Tat strategy:

Starts by cooperating

Then copies your previous move

Simple but powerful in repeated games

🔧 Technologies Used
Backend: Python, Flask, Flask-Session

Frontend: HTML5, CSS3, JavaScript, Bootstrap 5

Visualization: Font Awesome icons, custom animations

Game Theory: Custom implementation with NumPy