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

for i in {1..20}
do
    user=$(curl -s 'https://randomuser.me/api/?nat=fr')
    firstName=$(echo $user | jq -r '.results[0].name.first' | iconv -f utf8 -t ascii//TRANSLIT | tr -d ' ')
    lastName=$(echo $user | jq -r '.results[0].name.last' | iconv -f utf8 -t ascii//TRANSLIT | tr -d ' ')
    gender=$(echo $user | jq -r '.results[0].gender')
    if [ $gender = "male" ]; then
        gender="M"
    else
        gender="F"
    fi
    age=$(echo $user | jq -r '.results[0].dob.age')
    age=$(((age % 12) + 18))
    email="$firstName.$lastName$i@createRandomUser.sh"
    password="Panda666!"
    echo "Création de l'utilisateur $firstName $lastName ($gender, $age ans) avec l'email $email et le mot de passe $password"
    response=$(curl -s -X POST localhost:5000/api/auth/register -H "Content-Type: application/json" -d "{\"step\":1,\"firstname\":\"$firstName\",\"lastname\":\"$lastName\",\"gender\":\"$gender\",\"age\":$age,\"email\":\"$email\",\"password\":\"$password\"}")
    accessToken=$(echo $response | jq -r '.access_token')
    curl -s -X POST localhost:5000/api/auth/register -H "Content-Type: application/json" -H "Authorization: Bearer $accessToken" -d "{\"step\":2,\"city\":{\"lon\":7.3,\"lat\":47.75}, \"searching\":\"Friends\",\"commitment\":\"Short term\",\"frequency\":\"Daily\",\"weight\":\"< 50\",\"size\":\"< 150\",\"shape\":\"Skinny\",\"alcohol\":\"Never\",\"smoking\":false, \"diet\":\"Omnivor\"}"
    random_interests=$(shuf -e "${all_interests[@]}" -n 3 | jq -R . | jq -s .)
    curl -s -X POST localhost:5000/api/auth/register -H "Content-Type: application/json" -H "Authorization: Bearer $accessToken" -d "{\"step\":3,\"Culture\":$random_interests, \"description\":\"Lorem ipsum\"}"
    echo "Utilisateur créé avec succès. Access Token : $accessToken"
done