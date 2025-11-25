"""Simple agent/orchestrator that can be extended to call LLMs or external APIs.
Right now it triggers the local ingest script periodically (every 15 minutes).
"""
import subprocess, time, sys, os
from datetime import datetime

def run_ingest_once():
    print('Agent triggering ingest at', datetime.utcnow().isoformat())
    subprocess.run([sys.executable, 'ingest.py'])

if __name__ == '__main__':
    while True:
        try:
            run_ingest_once()
        except Exception as e:
            print('Agent error:', e)
        time.sleep(900)
