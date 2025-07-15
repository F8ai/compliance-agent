
#!/usr/bin/env python3
"""
Start the compliance agent dashboard server
"""

import sys
import os

# Add base_agent to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'base_agent'))

from base_agent.server import AgentServer

if __name__ == "__main__":
    # Create server instance for compliance agent
    server = AgentServer(agent_name="compliance-agent", port=5000)
    
    print("🚀 Starting Compliance Agent Dashboard...")
    print("📊 Dashboard will be available at: http://0.0.0.0:5000")
    print("🔄 Auto-refreshes every 30 seconds")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        server.run(debug=False)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
