#!/bin/bash
scriptPath=$(dirname "$(realpath "$0")")
cd "$scriptPath"
cols=$(tput cols)
cols=$((cols/2))

separator() {
    local name=$1
    echo -n "$name"
    for ((i=0; i<cols-${#name}; i++)); do
        if [ $i -eq $((cols-${#name}-1)) ]; then
            echo "-"
        else
            echo -n "-"
        fi
    done
}

separator "Database setup"
read -p "Do you want to start a database ? [Y(Yes)/N(No)/S(Skip)]: " userInput
if [ "$userInput" = "Y" ]; then
    echo "Starting database... searching file"
    if [ -f "database/docker/docker-compose.yml" ]; then
        echo "File found, starting database"
        docker-compose -f database/docker/docker-compose.yml up -d
    else
        echo "File not found, skipping step"
    fi
elif [ "$userInput" = "N" ]; then
    echo "Database not started"
    read -p "Do you want to stop a previously started database ? [Y(Yes)/N(No)]: " userInput
    if [ $userInput == "Y" ]; then
        echo "Stopping database... searching file"
        if [ -f "database/docker/docker-compose.yml" ]; then
            echo "File found, stopping database"
            docker-compose -f database/docker/docker-compose.yml down
        else
            echo "File not found, skipping step"
        fi
    elif [ $userInput == "N" ]; then
        echo "Database not stopped"
    else
        echo "Unknown input, skipping step"
    fi
elif [ "$userInput" = "S" ]; then
    echo "Skipping database setup"
else
    echo "Unknown input, skipping step"
fi
separator "Database setup end"
echo " "
separator "Backend setup"
read -p "Do you want to start the backend ? [Y(Yes)/N(No)]: " userInput
if [ $userInput == "Y" ]; then
    echo "Starting backend"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python3 app.py
elif [ $userInput == "N" ]; then
    echo "Backend not started"
else
    echo "Unknown input, end of the script"
fi
separator "Backend setup end"
