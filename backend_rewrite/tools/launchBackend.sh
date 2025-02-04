cd "$(dirname "$0")"
cd ..
# read -p "Did you started a database conforming to the backend setup (postgres db on port 6000) ? [y/n]: " userInput
# userInput=$(echo $userInput | tr '[:upper:]' '[:lower:]')
# if [ "$userInput" = "n" ]; then
#     ./tools/launchDatabase.sh
# fi
echo "Starting backend"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
read -p "Do you want to init the db ? [y/n]: " userInput
userInput=$(echo $userInput | tr '[:upper:]' '[:lower:]')
if [ "$userInput" = "y" ]; then
    flask --app flask-backend init-db
fi
flask --app flask-backend run --debug