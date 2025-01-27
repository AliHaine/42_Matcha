# informations globales sur les endpoints :

tout les endpoints commencent par un /api.

la liste d'endpoints va etre presente sous cette forme :

#### /exemple (type de requete (GET/POST)) : description courte
    details (si necessaire) :
        plus de details au sujet de cet endpoint
    Infos a envoyer (si necessaire) :
        -   nom classique de la var (nom de la var utilise par le backend) : details si necessaire
    Infos retournes (si necessaire) :
        - nom de var : detail du contenu

tout les endpoints qui ont /account dans leur path necessitent que l'utilisateur soit authentifie (a l'exception de register et login)

toutes les endpoints /account retournent constamment une valeur 'Success' a true ou false pour indiquer si l'operation s'est bien deroulee, si success est a false, une variable 'Error' est normalement constamment passe en meme temps

exemple :
    - si reussite:
        - Success = true
    - si echec :
        - Success = false
        - Error = message d'erreur de la part du serveur

### informations annexes avant la suite
    Pour lancer le backend rapidement lancer le script launchBackend.sh et suivre les infos indiques
    Si ca veut creer 30 utilisateurs randoms correct pour les tests lancer le script createRandomUsers.sh avec le back de lance

# ENDPOINTS disponnibles

(si un bug est trouve, merci de l'indiquer dans le fichier bugsBackend.txt)


#### /account/checkMissingFields (GET) : regarde si le profil a ete correcement complete ou non et retourne les erreurs s'il y en a


#### /account/register (POST) : permet d'enregistrer un utilisateur
    details :
        cree l'utilisateur si les informations sont valides, si tout est ok l'authentifie directement
    Infos a envoyer :
        - prenom (firstName)
        - nom (lastName)
        - email (email)
        - mot de passe (password)
        - confirmation de mot de passe (passwordConfirm)
        - age (age)
        - sexe (sex)


#### /account/login (POST) : permet de se connecter a un compte
    Infos a envoyer :
        - email (email)
        - mot de passe (password)

#### /account/logout (GET) : permet de se deconnecter du compte actuel

#### /account/modifyPersonnalInfo (POST) : permet de modifier les valeurs de base du profil (nom, prenom, age, sexe, email, mot de passe)
    details :
        lors d'une requete sur cet endpoint le mot de passe est obligatoire pour faire une modification, peu importe quel est la valeur modifiee. Aucune des autres infos est obligatoire (si laisse vide ne change pas la valeur sur la bdd)
    Infos a envoyer :
        - prenom (firstName)
        - nom (lastName)
        - age (age)
        - sexe (sex)
        - email (email)
        - mot de passe (password)
        - nouveau mot de passe (newPassword)
        - confirmation du nouveau mot de passe (newPasswordConfirm) : obligatoire si new password


#### /account/getUser (GET) : retourne les informations "basique" de l'utilisateur
    Infos retournes :
        - firstName : prenom enregistre de la personne
        - lastName : nom enregistre de la personne
        - email : email enregistre de la personne
        - description : description enregistre de la personne

#### /account/modifyDescription (POST) : permet de modifier la description de l'utilisateur
    Infos a envoyer :
        - description (description)

#### /account/modifyInterests (POST) : change les centres d'interet de l'utilisateur
    details :
        lors de la requete les valeurs passes sont verifies, si elles sont valide la liste d'interets actuelle de l'utilisateur est supprime et les valeurs passees ajoutes
    
    Infos a envoyer :
        - centres d'interets (interests) : un tableau de string contenant les interets que l'utilisateur souhaite avoir

#### /account/modifySanity (POST) : modifie les valeurs de la categorie sante (fumeur, boit, alimentation)
    details:
        pour connaitre les valeurs disponnibles pour boit et alimentation regarder le retour api de /getSanity, ou le fichier config/userGlobal.py
        nom des valeurs dans le fichier :
            - LIST_DRINK
            - LIST_DIET
    Infos a envoyer :
        - fumeur (smoking) : booleen
        - boit (drink)
        - alimentation (diet)

#### /account/modifyBodyInfo (POST) : modifie les valeurs de la categorie corps (taille, poids, corpulance)
    details:
        pour connaitre les valeurs disponnibles pour la taille, le poids et la corpu regarder le retour api de /getBodyInfo, ou le fichier config/userGlobal.py
        nom des valeurs dans le fichier :
            - LIST_CORPU
            - MAX/MIN_WEIGHT
            - MAX/MIN_HEIGHT
    Infos a envoyer :
        - taille (height) : int
        - poids (weight) : int
        - corpulence (corpu)
    
#### /account/modifyIdealRelation (POST) : modifie les valeurs de la categorie relation (recherche, engagement, frequence)
    details :
        pour connaitre les valeurs dispo regarder le retour api de getIdealRelation ou le fichier config/userGlobal.py
        nom des valeurs dans le fichier :
            - LIST_RESEARCH
            - LIST_ENGAGEMENT
            - LIST_FREQUENCY
    Infos a envoyer :
        - recherche (research)
        - engagement (engagement)
        - frequence (frequency)

#### /registerRequirements (GET) : permet de recuperer les principaux details verifies lors d'un register
    Infos retournes :
        - allowed_characters : liste de caracteres autorises dans le nom et prenom
        - password_requirements : caracteristiques minimales du mot de passe (taille min, nombre de digits, majuscule et minuscules)
        - required_fields : liste de champs obligatoires pour enregistrer un utilisateur

#### /getInterests (GET) : donne la liste de tout les interets existant sur la bdd actuellement
    valeurs retournes :
        - interests : liste des interets

#### /getSanity (GET) : donne les vals obligatoires a envoyer lors d'un modifySanity et donne les valeurs disponnibles pour chaque champs
    valeurs retournes :
        - sanity : liste de champs obligatoires pour un modify sanity
        - smoking : valeurs disponibles pour la var fumeur
        - drink : valeurs disponibles pour la var boit
        - diet : valeurs disponibles pour la valeur alimentation

#### /getBodyInfo (GET) : meme chose que pour getSanity mais pour getBodyInfo
    valeurs retournes : 
        - body_info : liste de champs obligatoires pour un modifyBodyInfo
        - corpu : valeurs disponibles pour la var corpulance
        - weight : poids min et max possible
        - height : taille min et max possible

#### /getIdealRelation (GET) : meme chose que getSanity mais avec les infos pour relations
    valeurs retournes :
        - ideal_relation : liste des champs obligatoires pour modifyIdealRelation
        - research : liste des valeurs dispo
        - engagement : liste des valeurs dispo
        - frequency : liste des valeurs dispo

#### /account/profiles/\<id> (GET) : permet de recuperer les informations publiques d'un profil
    valeurs retournes :
        - nom (lastName)
        - prenom (firstName)
        - email (email) (peut etre le supprime car unsafe et useless ?)
        - description (description)
        - sexe (sexe)
        - age
        - cat sante (health) : les trois infos de la categorie sante
        - cat corps (body) : les trois infos de la categorie corps
        - cat relation (lookingFor) : les trois infos de la categorie relation
        - interets (interests) : c'est un tableau, au cas ou


#### /matcha (GET) : endpoint retournant les profils pour le home
    details :
        un argument peut etre passe qui est nbProfiles, permettant de recevoir plus ou moins de profils que la valeur par defaut (qui est actuellement 8)
    valeurs retournes :
        - Success : si tout c'est bien passe
        - matcha : tableau d'utilisateurs

#### /account/location (POST) : pas encore setup mais aura pour vocation d;enregistrer la localisation de l'utilisateur

#### /profile_pics/nom_de_l'image (GET) : retourne l'image de profil demande (pour l'instant faut mettre l'extension du fichier mais je vais fix ca)

#### /account/uploadProfilePic (POST) : upload la photo de profil envoye
    infos a envoyer :
        - un fichier "file" qui est une image

#### /account/deleteProfilePic (POST) : permet de supprimer une photo de profil demande
    infos a envoyer :
        - photoNumber a envoyer sous forme d'un argument qui est le numero de photo qui sera supprime
