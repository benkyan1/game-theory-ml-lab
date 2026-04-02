from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import numpy as np
import json
from models.game import PrisonersDilemma
from models.ml_analyzer import GameTheoryMLAnalyzer
import plotly.graph_objs as go
import plotly.utils
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Initialize game and ML analyzer
game = PrisonersDilemma()
ml_analyzer = GameTheoryMLAnalyzer()

# Train ML model on startup
ml_analyzer.train_model()

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/game')
def game_page():
    """Interactive game page"""
    return render_template('game.html')

@app.route('/analysis')
def analysis_page():
    """Game theory analysis page"""
    nash = game.find_nash_equilibrium()
    pareto = game.calculate_pareto_optimal()
    
    return render_template('analysis.html', 
                         nash=nash, 
                         pareto=pareto)

@app.route('/ml-demo')
def ml_demo_page():
    """Machine learning demonstration page"""
    return render_template('ml_demo.html')

@app.route('/api/play', methods=['POST'])
def play_round():
    """Play a single round of Prisoner's Dilemma"""
    data = request.json
    action1 = data.get('action1')
    action2 = data.get('action2')
    
    if action1 not in ['cooperate', 'defect'] or action2 not in ['cooperate', 'defect']:
        return jsonify({'error': 'Invalid actions'}), 400
    
    payoff1, payoff2 = game.get_payoff(action1, action2)
    
    # Store in session history
    if 'game_history' not in session:
        session['game_history'] = []
    
    session['game_history'].append({
        'round': len(session['game_history']) + 1,
        'action1': action1,
        'action2': action2,
        'payoff1': payoff1,
        'payoff2': payoff2
    })
    session.modified = True
    
    return jsonify({
        'payoff1': payoff1,
        'payoff2': payoff2,
        'total_payoff1': sum(r['payoff1'] for r in session['game_history']),
        'total_payoff2': sum(r['payoff2'] for r in session['game_history']),
        'history': session['game_history']
    })

@app.route('/api/simulate', methods=['POST'])
def simulate_game():
    """Simulate repeated game with AI strategies"""
    data = request.json
    strategy1 = data.get('strategy1', 'tit_for_tat')
    strategy2 = data.get('strategy2', 'always_defect')
    n_rounds = data.get('rounds', 100)
    discount_factor = data.get('discount_factor', 0.9)
    
    results = game.simulate_repeated_game(n_rounds, strategy1, strategy2, discount_factor)
    
    # Create visualization data
    rounds = list(range(1, n_rounds + 1))
    p1_actions = [1 if a == 'cooperate' else 0 for a, _ in results['history']]
    p2_actions = [1 if a == 'cooperate' else 0 for _, a in results['history']]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=rounds, y=p1_actions, mode='lines+markers', 
                             name='Player 1 (Cooperation)', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=rounds, y=p2_actions, mode='lines+markers', 
                             name='Player 2 (Cooperation)', line=dict(color='blue')))
    fig.update_layout(title='Cooperation Over Time',
                     xaxis_title='Round',
                     yaxis_title='Cooperation (1=Cooperate, 0=Defect)',
                     yaxis=dict(tickvals=[0, 1], ticktext=['Defect', 'Cooperate']))
    
    return jsonify({
        'total_payoffs': results['total_payoffs'],
        'cooperation_rates': results['cooperation_rate'],
        'visualization': json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder),
        'history': results['history'][:20]  # Return first 20 rounds
    })

@app.route('/api/analyze-behavior', methods=['POST'])
def analyze_behavior():
    """Analyze player behavior using ML"""
    data = request.json
    history = data.get('history', [])
    
    if len(history) < 5:
        return jsonify({'error': 'Need at least 5 rounds for meaningful analysis'}), 400
    
    analysis = ml_analyzer.analyze_player_behavior(history)
    return jsonify(analysis)

@app.route('/api/predict-optimal', methods=['POST'])
def predict_optimal():
    """Predict optimal strategy using ML"""
    data = request.json
    payoffs = {
        'cooperate_reward': data.get('cooperate_reward', 3),
        'cooperate_punishment': data.get('cooperate_punishment', 0),
        'defect_reward': data.get('defect_reward', 5),
        'defect_punishment': data.get('defect_punishment', 1)
    }
    
    prediction = ml_analyzer.predict_optimal_strategy(payoffs)
    return jsonify(prediction)

@app.route('/api/nash-equilibrium', methods=['GET'])
def get_nash():
    """Get Nash equilibrium analysis"""
    nash = game.find_nash_equilibrium()
    return jsonify(nash)

@app.route('/api/reset-game', methods=['POST'])
def reset_game():
    """Reset game history"""
    session.pop('game_history', None)
    return jsonify({'status': 'reset'})

@app.route('/api/payoff-matrix', methods=['GET'])
def get_payoff_matrix():
    """Get current payoff matrix"""
    return jsonify({
        'matrix': [
            [game.get_payoff('cooperate', 'cooperate'),
             game.get_payoff('cooperate', 'defect')],
            [game.get_payoff('defect', 'cooperate'),
             game.get_payoff('defect', 'defect')]
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)