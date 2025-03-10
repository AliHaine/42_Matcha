cd "$(dirname "$0")"
cd ..
echo "Starting backend"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt > /dev/null
python3 run.py
deactivate
echo "Backend stopped"