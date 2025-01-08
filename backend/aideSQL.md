## INFORMATIONS IMPORTANTES

postgresql est sensible a la casse

Les commandes sql sont toujours ecrit en full maj et se finissent obligatoirement par un ';'

pour se connecter a la bdd au cas ou :
- ne pas oublier de lancer la bdd
- rentrer dans la bdd : docker exec -it [nom du docker] psql [nom de la bdd] [utilisateur utilise]

commandes utiles : 
- \c [bdd name] : permet de se connecter a une bdd diff
- \dt : affiche toutes les tables existantes sur la bdd actuelle


### CREATE TABLE [nom de la table] (nomCol type, ...);

creer une table du nom que on lui a indiquer et de lui dire quelle va contenir les colonnes indiques entre parantheses

(create peut creer d'autres trucs mais pas encore touche)

### INSERT INTO [nom de la table] (nomCol, ...) VALUES (val, ...);

permet d'inserer des valeurs dans la table correspondantes

### SELECT [quoi select] FROM [nom de la table];

quoi select :
- '*' : donnes toutes les colonnes de la table
- nom d'une col : donne juste la col  correspondant au nom

### DELETE FROM [nom de la table]

supprime tout le contenu de la table sans supprimer la table

#### WHERE [nom de col] = 'valeur'

where peut etre rajouter a coup sur apres le delete et select indique au dessus

where permet d'apppliquer les commandes que sur les elements filtres par where

exemple : 
DELETE FROM users WHERE name = 'test';

la commande va supprimer uniquement les elements qui ont la colonne name a la valeur test de la table users

### DROP TABLE [nom de la table];

supprime completement une table de la bdd

