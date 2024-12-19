
# informations globales sur les endpoints :

tout les endpoints commencent par un /api.

la liste d'endpoints va etre presente sous cette forme :

#### /exemple (type de requete (GET/POST)) : description courte
    details (si necessaire) :
        plus de details au sujet de cet endpoint
    Infos a envoyer (si necessaire) :
        -   nom classique de la var (nom de la var utilise dans le backend) : details si necessaire
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

# ENDPOINTS disponnibles

(si un bug est trouve, merci de l'indiquer dans le fichier bugsBackend.txt)

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
        - sexe (sexe)


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
        - sexe (sexe)
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
            - LIST_BOIT
            - LIST_ALIM
    Infos a envoyer :
        - fumeur (fumeur) : booleen
        - boit (boit)
        - alimentation (alimentation)

#### /account/modifyBodyInfo (POST) : modifie les valeurs de la categorie corps (taille, poids, corpulance)
    details:
        pour connaitre les valeurs disponnibles pour la taille, le poids et la corpu regarder le retour api de /getBodyInfo, ou le fichier config/userGlobal.py
        nom des valeurs dans le fichier :
            - LIST_CORPU
            - LIST_ALIM
    Infos a envoyer :
        - fumeur (fumeur) : booleen
        - boit (boit)
        - alimentation (alimentation)

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
        - fumeur : valeurs disponibles pour la var fumeur
        - boit : valeurs disponibles pour la var boit
        - alimentation : valeurs disponibles pour la valeur alimentation

#### /getBodyInfo (GET) : meme chose que pour getSanity mais pour getBodyInfo
    valeurs retournes : 
        - body_info : liste de champs obligatoires pour un modifyBodyInfo
        - corpulance : valeurs disponibles pour la var corpulance
        - poids : poids min et max possible
        - taille : taille min et max possible