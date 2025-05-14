#!/usr/bin/env python
"""
This script starts the HealthBench Dashboard application.
"""

from dashboard.app import app

if __name__ == "__main__":
    print("Starting HealthBench Dashboard on http://localhost:5001")
    print("Press Ctrl+C to stop the server")
    app.run(debug=True, port=5001) 