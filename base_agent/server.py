
"""
Base Agent Web Server
Provides dashboard and API endpoints for agent monitoring
"""

from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime
from typing import Dict, Any

class AgentServer:
    def __init__(self, agent_name: str = "base-agent", port: int = 5000):
        self.app = Flask(__name__, 
                        template_folder='templates',
                        static_folder='static')
        self.agent_name = agent_name
        self.port = port
        self.setup_routes()
    
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def dashboard():
            """Main dashboard page"""
            return render_template('dashboard.html', agent_name=self.agent_name)
        
        @self.app.route('/api/metrics')
        def get_metrics():
            """Get agent performance metrics"""
            return jsonify(self.get_agent_metrics())
        
        @self.app.route('/api/baseline-results')
        def get_baseline_results():
            """Get baseline test results"""
            return jsonify(self.load_baseline_results())
        
        @self.app.route('/api/baseline-questions')
        def get_baseline_questions():
            """Get baseline questions organized by category"""
            return jsonify(self.load_baseline_questions())
        
        @self.app.route('/api/regulations/<state>')
        def get_regulations(state):
            """Get regulation data for a specific state"""
            return jsonify(self.load_state_regulations(state))
        
        @self.app.route('/api/status')
        def get_status():
            """Get agent status"""
            return jsonify({
                'agent': self.agent_name,
                'status': 'running',
                'timestamp': datetime.now().isoformat()
            })
    
    def get_agent_metrics(self) -> Dict[str, Any]:
        """Load and return agent metrics"""
        try:
            # Try to load baseline results for metrics
            baseline_results = self.load_baseline_results()
            if baseline_results and 'results' in baseline_results:
                total_tests = len(baseline_results['results'])
                passed_tests = sum(1 for r in baseline_results['results'] if r.get('passed', False))
                avg_response_time = sum(r.get('response_time', 0) for r in baseline_results['results']) / total_tests if total_tests > 0 else 1.0
                accuracy = (passed_tests / total_tests * 100) if total_tests > 0 else 0
                
                return {
                    'accuracy': f"{accuracy:.0f}%",
                    'response_time': f"{avg_response_time:.1f}s",
                    'confidence': '62%',
                    'tests_passed': f"{passed_tests}/{total_tests}",
                    'status': 'running',
                    'last_updated': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Error loading metrics: {e}")
        
        return {
            'accuracy': '0%',
            'response_time': '1.0s',
            'confidence': '62%',
            'tests_passed': '0/4',
            'status': 'needs setup',
            'last_updated': datetime.now().isoformat()
        }
    
    def load_baseline_results(self) -> Dict[str, Any]:
        """Load baseline test results"""
        # Try multiple paths for baseline results
        paths_to_try = [
            'baseline_results.json',
            os.path.join('..', 'baseline_results.json')
        ]
        
        for results_path in paths_to_try:
            if os.path.exists(results_path):
                try:
                    with open(results_path, 'r') as f:
                        return json.load(f)
                except Exception as e:
                    print(f"Error loading baseline results from {results_path}: {e}")
        return {}
    
    def load_baseline_questions(self) -> Dict[str, Any]:
        """Load baseline questions"""
        # Try multiple paths for baseline.json
        paths_to_try = [
            'baseline.json',
            os.path.join('..', 'baseline.json')
        ]
        
        for baseline_path in paths_to_try:
            if os.path.exists(baseline_path):
                try:
                    with open(baseline_path, 'r') as f:
                        return json.load(f)
                except Exception as e:
                    print(f"Error loading baseline questions from {baseline_path}: {e}")
        return {}
    
    def load_state_regulations(self, state: str) -> Dict[str, Any]:
        """Load regulation data for a specific state"""
        # Try multiple paths for regulations directory
        paths_to_try = [
            os.path.join('regulations', state, 'metadata.json'),
            os.path.join('..', 'regulations', state, 'metadata.json')
        ]
        
        for metadata_path in paths_to_try:
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, 'r') as f:
                        data = json.load(f)
                        
                    # Get list of available regulation URLs
                    regulation_dir = os.path.dirname(metadata_path)
                    urls = []
                    
                    # Check for mirrored domains
                    if 'mirrored_domains' in data:
                        for domain in data['mirrored_domains']:
                            domain_dir = os.path.join(regulation_dir, domain.replace('/', '_').replace(':', ''))
                            if os.path.exists(domain_dir):
                                urls.append({
                                    'title': f"Mirrored: {domain}",
                                    'url': f"https://{domain}",
                                    'local_path': domain_dir
                                })
                    
                    # Add main URL if available
                    if 'main_url' in data:
                        urls.append({
                            'title': 'Primary Regulation Site',
                            'url': data['main_url'],
                            'local_path': None
                        })
                    
                    return {
                        'state': state,
                        'name': data.get('name', state),
                        'agency': data.get('agency', 'Unknown Agency'),
                        'main_url': data.get('main_url'),
                        'last_updated': data.get('last_updated'),
                        'mirror_success': data.get('mirror_success', False),
                        'urls': urls
                    }
                except Exception as e:
                    print(f"Error loading regulations for {state}: {e}")
        
        return {
            'error': f'No regulation data found for state {state}'
        }
    
    def run(self, debug: bool = False):
        """Start the server"""
        print(f"Starting {self.agent_name} dashboard on http://0.0.0.0:{self.port}")
        self.app.run(host='0.0.0.0', port=self.port, debug=debug)

if __name__ == "__main__":
    server = AgentServer()
    server.run(debug=True)
