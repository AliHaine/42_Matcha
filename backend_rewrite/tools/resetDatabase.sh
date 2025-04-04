cd "$(dirname "$0")"
cd ..
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt > /dev/null
read -p "Do you want to init the db ? [y/n]: " userInput
userInput=$(echo $userInput | tr '[:upper:]' '[:lower:]')
if [ "$userInput" = "y" ]; then
    flask --app flask_backend init-db
fi