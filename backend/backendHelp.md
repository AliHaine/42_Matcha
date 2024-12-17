
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

# ENDPOINTS disponnibles

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
    Infos a envoyer :
        - fumeur (fumeur) : booleen
        - boit (boit)
        - alimentation (alimentation)
