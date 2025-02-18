#!/bin/bash

json_data=$(curl -s 'localhost:5000/api/getInformations/interests')

# Vérifier si les données sont vides
if [ -z "$json_data" ]; then
    echo "Aucun intérêt récupéré."
    exit 1
fi

all_interests=()
while IFS= read -r interest; do
    all_interests+=("$interest")
done < <(echo "$json_data" | jq -r '.interests[][]')

max_jobs=100
count=0 
max_loop=100

if (( max_loop % 2 != 0 )); then
    ((max_loop++))
fi

if [[ $max_jobs -gt $max_loop ]]; then
    max_jobs=$max_loop
fi

failed_file=$(mktemp)
echo 0 > "$failed_file"

increment_failed_count() {
    (
        flock -x 200
        echo $(( $(cat "$failed_file") + 1 )) > "$failed_file"
    ) 200>"$failed_file.lock"
}

startTime=$(date +%s)

batch_size=5000  # Taille d'un batch
remaining=$max_loop  # Nombre total d'utilisateurs à créer
batch_start=0

while (( remaining > 0 )); do
    current_batch=$(( remaining > batch_size ? batch_size : remaining ))  # Limite à 5000 max

    echo "LOG : Récupération d'un batch de $current_batch utilisateurs..."
    users=$(curl -s "https://randomuser.me/api/?nat=fr&results=$current_batch")

    for i in $(seq 0 $((current_batch - 1))); do
        (
            user=$(echo "$users" | jq ".results[$i]")
            firstName=$(echo "$user" | jq -r '.name.first' | iconv -f utf8 -t ascii//TRANSLIT | tr -d ' ')
            lastName=$(echo "$user" | jq -r '.name.last' | iconv -f utf8 -t ascii//TRANSLIT | tr -d ' ')
            gender=$(echo "$user" | jq -r '.gender')

            if [[ -z "$firstName" || -z "$lastName" ]]; then
                echo "Erreur : utilisateur invalide."
                increment_failed_count
                exit 1
            fi

            if [ "$gender" = "male" ]; then
                gender="M"
            else
                gender="F"
            fi

            age=$(echo "$user" | jq -r '.dob.age')
            age=$(((age % 12) + 18))
            email="$firstName.$lastName$((batch_start + i))@createRandomUser.sh"
            password="Panda666!"

            echo "Création de $email"
            response=$(curl -s -X POST localhost:5000/api/auth/register -H "Content-Type: application/json" -d "{\"step\":1,\"firstname\":\"$firstName\",\"lastname\":\"$lastName\",\"hetero\":false,\"gender\":\"$gender\",\"age\":$age,\"email\":\"$email\",\"password\":\"$password\"}")

            accessToken=$(echo "$response" | jq -r '.access_token')

            if [[ -z "$accessToken" || "$accessToken" == "null" ]]; then
                echo "Échec de récupération du token."
                increment_failed_count
                exit 1
            fi

            curl -s -X POST localhost:5000/api/auth/register -H "Content-Type: application/json" -H "Authorization: Bearer $accessToken" -d "{\"step\":2,\"city\":{\"lon\":7.3,\"lat\":47.75}, \"searching\":\"Friends\",\"commitment\":\"Short term\",\"frequency\":\"Daily\",\"weight\":\"< 50\",\"size\":\"< 150\",\"shape\":\"Skinny\",\"alcohol\":\"Never\",\"smoking\":false, \"diet\":\"Omnivor\"}"

            random_interests=$(shuf -e "${all_interests[@]}" -n 3 | jq -R . | jq -s .)

            curl -s -X POST localhost:5000/api/auth/register -H "Content-Type: application/json" -H "Authorization: Bearer $accessToken" -d "{\"step\":3,\"Culture\":$random_interests, \"description\":\"Lorem ipsum\"}"

            echo "Utilisateur $email créé avec succès."
        ) &  # Exécuter en parallèle

        count=$((count + 1))
        if (( count % max_jobs == 0 )); then
            wait
            actualTime=$(date +%s)
            echo "LOG : Création de $count utilisateurs terminée avec $(cat "$failed_file") échecs. Temps écoulé : $((actualTime - startTime)) secondes."
        fi
    done

    wait  # S'assurer que tous les utilisateurs du batch sont créés avant de continuer

    batch_start=$((batch_start + current_batch))  # Mettre à jour le compteur global
    remaining=$((remaining - current_batch))  # Réduire le nombre restant à traiter
done

endTime=$(date +%s)

echo "LOG : Création terminée avec $(cat "$failed_file") échecs."
echo "LOG : Temps d'exécution : $((endTime - startTime)) secondes"