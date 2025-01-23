#!/bin/zsh

interests=$(curl -s 'localhost:8000/api/getInterests' | jq -r '.interests[]')
sanity=$(curl -s 'localhost:8000/api/getSanity')
alim=$(echo $sanity | jq -r '.alimentation[]')
boit=$(echo $sanity | jq -r '.boit[]')
bodyInfo=$(curl -s 'localhost:8000/api/getBodyInfo')
corpulence=$(echo $bodyInfo | jq -r '.corpulence[]')
idealRelation=$(curl -s 'localhost:8000/api/getIdealRelation')
engagement=$(echo $idealRelation | jq -r '.engagement[]')
frequence=$(echo $idealRelation | jq -r '.frequence[]')
recherche=$(echo $idealRelation | jq -r '.recherche[]')
# Vérifier si des intérêts ont été récupérés
if [ -z "$interests" ]; then
    echo "Aucun intérêt récupéré."
    exit 1
fi
if [ -z "$sanity" ]; then
    echo "Aucun element sanity récupéré."
    exit 1
fi
if [ -z "$alim" ]; then
    echo "Aucun element alimentation récupéré."
    exit 1
fi
if [ -z "$boit" ]; then
    echo "Aucun element boit récupéré."
    exit 1
fi
if [ -z "$bodyInfo" ]; then
    echo "Aucun element bodyInfo récupéré."
    exit 1
fi
if [ -z "$corpulence" ]; then
    echo "Aucun element corpulence récupéré."
    exit 1
fi
if [ -z "$idealRelation" ]; then
    echo "Aucun element idealRelation récupéré."
    exit 1
fi
if [ -z "$engagement" ]; then
    echo "Aucun element engagement récupéré."
    exit 1
fi
if [ -z "$frequence" ]; then
    echo "Aucun element frequence récupéré."
    exit 1
fi
if [ -z "$recherche" ]; then
    echo "Aucun element recherche récupéré."
    exit 1
fi

# Convertir les intérêts en tableau Bash
while IFS= read -r line; do
    interests_array+=("$line")
done <<< "$interests"
while IFS= read -r line; do
    alim_array+=("$line")
done <<< "$alim"
while IFS= read -r line; do
    boit_array+=("$line")
done <<< "$boit"
while IFS= read -r line; do
    corpulence_array+=("$line")
done <<< "$corpulence"
while IFS= read -r line; do
    engagement_array+=("$line")
done <<< "$engagement"
while IFS= read -r line; do
    frequence_array+=("$line")
done <<< "$frequence"
while IFS= read -r line; do
    recherche_array+=("$line")
done <<< "$recherche"

for i in {1..5}
do
    user=$(curl -s 'https://randomuser.me/api/?nat=fr')
    # echo $user
    firstName=$(echo $user | jq -r '.results[0].name.first' | iconv -f utf8 -t ascii//TRANSLIT | tr -d ' ')
    lastName=$(echo $user | jq -r '.results[0].name.last' | iconv -f utf8 -t ascii//TRANSLIT | tr -d ' ')
    sexe=$(echo $user | jq -r '.results[0].gender')
    if [ $sexe = "male" ]; then
        sexe="H"
    else
        sexe="F"
    fi
    age=$(echo $user | jq -r '.results[0].dob.age')
    age=$(((age % 12) + 18))
    email="$firstName.$lastName$i@createRandomUser.sh"
    password="Panda666!"
    echo "User: $firstName $lastName $sexe $age $email $password"
    curl -X POST localhost:8000/api/account/register -c temp.txt  -H "Content-Type: application/json" -d "{\"firstName\":\"$firstName\",\"lastName\":\"$lastName\",\"sexe\":\"$sexe\",\"age\":$age,\"email\":\"$email\",\"password\":\"$password\",\"passwordConfirm\":\"$password\"}"
    num_select=5
    userInterests=$(printf "%s\n" "${interests_array[@]}" | shuf -n $num_select | jq -R -s -c 'split("\n")[:-1]')
    echo "Interests: $userInterests"
    curl -X POST localhost:8000/api/account/modifyInterests -b temp.txt -H "Content-Type: application/json" -d "{\"interests\":$userInterests}"
    # description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus non eros sed massa consequat vestibulum ut ac odio. Quisque in risus ac elit dictum blandit. Proin efficitur eros quis lacinia posuere. Proin rutrum blandit leo id elementum. Sed sollicitudin risus vitae nunc vehicula, vel luctus tellus mollis. Donec bibendum sapien nunc, ac mollis dui varius mattis. Nullam id nisl pellentesque, imperdiet ipsum at, mollis ante. Proin at venenatis dolor."
    description="test"
    curl -X POST localhost:8000/api/account/modifyDescription -b temp.txt -H "Content-Type: application/json" -d "{\"description\":\"$description\"}"
    userAlim=$(printf "%s\n" "${alim_array[@]}" | shuf -n 1)
    userBoit=$(printf "%s\n" "${boit_array[@]}" | shuf -n 1)
    userFume=$(shuf -n 1 -e true false)
    echo "Alim: $userAlim Boit: $userBoit Fume: $userFume"
    curl -X POST localhost:8000/api/account/modifySanity -b temp.txt -H "Content-Type: application/json" -d "{\"alimentation\":\"$userAlim\",\"boit\":\"$userBoit\",\"fumeur\":$userFume}"
    userPoids=$(shuf -n 1 -e 50 60 70 80 90 100)
    userTaille=$(shuf -n 1 -e 150 160 170 180 190 200)
    userCorpulence=$(printf "%s\n" "${corpulence_array[@]}" | shuf -n 1)
    echo "Poids: $userPoids Taille: $userTaille Corpulence: $userCorpulence"
    curl -X POST localhost:8000/api/account/modifyBodyInfo -b temp.txt -H "Content-Type: application/json" -d "{\"poids\":$userPoids,\"taille\":$userTaille,\"corpulence\":\"$userCorpulence\"}"
    userEngagement=$(printf "%s\n" "${engagement_array[@]}" | shuf -n 1)
    userFrequence=$(printf "%s\n" "${frequence_array[@]}" | shuf -n 1)
    userRecherche=$(printf "%s\n" "${recherche_array[@]}" | shuf -n 1)
    echo "Engagement: $userEngagement Frequence: $userFrequence Recherche: $userRecherche"
    curl -X POST localhost:8000/api/account/modifyIdealRelation -b temp.txt -H "Content-Type: application/json" -d "{\"engagement\":\"$userEngagement\",\"frequence\":\"$userFrequence\",\"recherche\":\"$userRecherche\"}"
done