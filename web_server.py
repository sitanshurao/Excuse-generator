from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
from generator import ExcuseGenerator
from apology_generator import ApologyGenerator
from proof_generator import ProofGenerator
from emergency_system import EmergencySystem
from history_manager import HistoryManager
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize generators
excuse_gen = ExcuseGenerator()
apology_gen = ApologyGenerator()
proof_gen = ProofGenerator()
emergency_sys = EmergencySystem()
history_mgr = HistoryManager()

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_content():
    """Generate content based on user input"""
    try:
        data = request.json
        gen_type = data.get('type')
        scenario = data.get('scenario')
        tone = data.get('tone')
        urgency = data.get('urgency', 'medium')
        
        if gen_type == 'excuse':
            content = excuse_gen.generate_excuse(scenario, urgency, tone)
        elif gen_type == 'apology':
            content = apology_gen.generate_apology(scenario, tone)
        elif gen_type == 'proof':
            # Generate proof documents
            doc_proof = proof_gen.generate_document(scenario)
            location_proof = proof_gen.generate_location_log()
            
            content = f"""
            <div class="proof-section">
                <h3>📋 Supporting Documentation Package</h3>
                
                <div class="proof-item">
                    <h4>1. {doc_proof['title']}</h4>
                    <p><strong>Date:</strong> {doc_proof['date']}</p>
                    <p><strong>Name:</strong> {doc_proof['name']}</p>
                    <p><strong>Details:</strong> {doc_proof['details']}</p>
                    <p><strong>Authorized by:</strong> {doc_proof['signature']}</p>
                </div>
                
                <div class="proof-item">
                    <h4>2. Location Verification</h4>
                    <p><strong>Timestamp:</strong> {location_proof['timestamp']}</p>
                    <p><strong>Location:</strong> {location_proof['address']}</p>
                    <p><strong>Coordinates:</strong> {location_proof['latitude']}, {location_proof['longitude']}</p>
                </div>
                
                <div class="proof-item">
                    <h4>3. Chat Screenshot</h4>
                    <p>Chat proof image has been generated and saved as 'chat_proof.png'</p>
                </div>
            </div>
            """
            
            # Generate and save chat screenshot
            chat_img = proof_gen.generate_chat_screenshot(f"Excuse for {scenario}")
            chat_img.save("static/chat_proof.png")
        
        # Save to history
        history_mgr.add_excuse(content, scenario, [gen_type, tone, urgency])
        
        return jsonify({
            'success': True,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/emergency', methods=['POST'])
def simulate_emergency():
    """Simulate emergency scenario"""
    try:
        data = request.json
        scenario = data.get('scenario', 'general')
        
        # Simulate emergency call
        emergency_sys.simulate_emergency_call("Emergency Contact")
        
        # Generate emergency message
        emergency_msg = emergency_sys.send_emergency_text(
            "Family Member", 
            f"Urgent {scenario} situation"
        )
        
        content = f"""
        <div class="result-item" style="border-left-color: #dc3545; background: #f8d7da;">
            <h3>🚨 Emergency Simulation Active</h3>
            <p><strong>Status:</strong> Emergency contact simulation initiated</p>
            <p><strong>Time:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
            <p><strong>Scenario:</strong> {scenario}</p>
        </div>
        
        <div class="result-item">
            <h3>📞 Emergency Communication</h3>
            <p><strong>Message Sent:</strong> {emergency_msg}</p>
            <p><strong>Status:</strong> Delivered</p>
        </div>
        """
        
        # Save to history
        history_mgr.add_excuse(content, scenario, ['emergency', 'urgent', 'high'])
        
        return jsonify({
            'success': True,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get generation history"""
    try:
        limit = request.args.get('limit', 10, type=int)
        history = history_mgr.get_history(limit)
        return jsonify({
            'success': True,
            'history': history
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    """Get favorite excuses"""
    try:
        favorites = history_mgr.get_favorites()
        return jsonify({
            'success': True,
            'favorites': favorites
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/toggle-favorite', methods=['POST'])
def toggle_favorite():
    """Toggle favorite status of an excuse"""
    try:
        data = request.json
        timestamp = data.get('timestamp')
        success = history_mgr.toggle_favorite(timestamp)
        
        return jsonify({
            'success': success,
            'message': 'Favorite status updated' if success else 'Item not found'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Create templates and static directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)