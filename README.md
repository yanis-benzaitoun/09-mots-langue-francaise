> [!CAUTION]
> Ce travail s'effectue dans [l'environnement Github](https://perso.esiee.fr/~courivad/courses/utils/misc-01-github-environment.html)

# Les mots de la langue française

[Le français](https://fr.wikipedia.org/wiki/Fran%C3%A7ais) est une langue indo-européenne de la famille des langues romanes. Le français est parlé, en 2018, sur tous les continents par environ 300 millions de personnes.

L'objectif est ici d'écrire un ensemble de fonctions permettant de manipuler les mots de la langue française.

Le fichier ``main.py`` contient :

- un ensemble de fonctions secondaires détaillées ci après ;
- la fonction principale ``main()`` dont le rôle est de faire appel aux fonctions secondaires pour vérifier leur bon fonctionnement.

Les données utilisées pour cet exercice sont contenues dans le fichier ``corpus.txt``. Il contient environ 336000 mots tirés du [corpus textuel](https://fr.wikipedia.org/wiki/Linguistique_de_corpus) de la langue française.

## Lecture des données

Ecrire la fonction secondaire ``read_data()`` qui prend en argument un nom de fichier et retourne son contenu sous la forme d'une liste de `n` mots si le fichier comporte `n` lignes.

> [!TIP]
> Les mots contenus dans le fichier sont suivis d'un caractère spécial `\n` (retour à la ligne) qu'il conviendra de retirer. Pour effectuer cette opération, quelle est [la méthode de chaine de caractère](https://docs.python.org/3/library/stdtypes.html#string-methods) la plus adaptée ?

### Application

Utiliser les fonctions `main()` et `read_data()` pour rechercher les mots en position ``24499``, ``28281``, ``57305``, ``118091``, ``199316``, ``223435``, ``336455``. 

Ça devrait vous faire penser à un célèbre personnage de bande dessinée.

## L'ensemble des mots

Le mot "ensemble" est ici pris dans son acception [mathématique](https://fr.wikipedia.org/wiki/Ensemble), c'est à dire comme "un rassemblement d’objets distincts".

Ecrire la fonction secondaire `ensemble_mots()` qui prend en argument un nom de fichier et retourne un [set](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset) de ces mots.

> [!TIP]
> Cette fonction doit être écrite sans duplication de code, et donc faire appel à `read_data()`. Le constructeur de [set](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset) prend en argument une séquence, c’est à dire un objet itérable.

> [!TIP]
> La recherche dans une `list` possède de piètres performances. Dans les pires cas (le mot recherché est présent mais en dernière position, ou le mot recherché n'est pas présent) il faut balayer toute la liste, et la complexité algorithmique est en $\Theta(n)$. Le [`set`](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset) est ici beaucoup plus adapté. La complexité algorithmique de la recherche est cette fois en $\Theta(1)$. Au détriment il est vrai d'un encombrement mémoire plus important.

### Application

Utiliser les fonctions `main()` et `ensemble_mots()` ainsi que l'opérateur `in` pour vérifier la présence ou non des mots "chronophage", "procrastinateur", "dangerosité", et "gratifiant" dans la liste. 

Comme pour la `list`, l'écriture de l'appartenance pour un `set` fait appel à l'opérateur `in`.

## Les mots de n lettres

Ecrire une fonction `mots_de_n_lettres()` qui prend en argument un ensemble ([`set`](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)) de `mots` et un nombre entier `n` et retourne le sous ensemble des mots de `n` lettres.

### Application

Le jeu de [Scrabble](https://fr.wikipedia.org/wiki/Scrabble) accorde un bonus de 50 points lorsque le joueur parvient à placer la totalité de ses 7 lettres sur le plateau.

Utiliser les fonctions `main()` et `mots_de_n_lettres()` pour rechercher le nombre de mots de ``7`` lettres dans le fichier utilisé. Combien y en a t-il ? 

Utiliser la fonction [`random.sample()`](https://docs.python.org/3/library/random.html#random.sample) pour en afficher quelques uns. 

Effectuer la même opération pour d'autres longueurs de mots. En utilisant le code prédéfini utilisé dans l'exercice sur les suites de Syracuse, sauriez vous tracer le nombre de mots du corpus en fonction de leur longueur ?

## Mots spéciaux

Dans la version française du [Scrabble](https://fr.wikipedia.org/wiki/Scrabble), certaines lettres rares rapportent plus de points que d'autres et il peut être intéressant de connaître les mots qui les utilisent.

Ecrire une fonction `mots_avec()` qui prend en argument un ensemble ([`set`](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)) de `mots` et une chaine de caractères `s` et retourne le sous ensemble des mots comprenant la chaine `s`.

### Application

Utiliser les fonctions `main()` et `mots_avec()` pour rechercher le nombre de mots contenant la lettre `k` dans le fichier utilisé. 

Utiliser la fonction [`random.sample()`](https://docs.python.org/3/library/random.html#random.sample) pour en afficher quelques uns. 

Même question pour la chaine `oo`.

## Recherche complexe

Les [`set`](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset) sont des structures de données très puissantes pour réaliser des [opérations ensemblistes](https://fr.wikipedia.org/wiki/Alg%C3%A8bre_des_parties_d%27un_ensemble).

Ecrire une fonction `cherche1()` qui prend en argument un ensemble ([`set`](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)) de `mots`, une chaine de caractères `start`, une chaine de caractères `stop`, un nombre de lettres `n`  et retourne le sous ensemble des mots de `n` lettres commmençant par `start` et terminant par `stop`.

> [!TIP]
> Les méthodes [`str.startswith`](https://docs.python.org/3/library/stdtypes.html#str.startswith) et [`str.endswith`](https://docs.python.org/3/library/stdtypes.html#str.endswith) seront utiles.

### Application

Utiliser ` main()` et les fonctions secondaires pour trouver les mots :
- de 14 lettres commençant par un `z` ;
- de 18 lettres se terminant par un `z` ;
- de 17 lettres commençant par ``sur``, se terminant par ``ons`` et comportant un ``x``;

## Recherche plus complexe

Ecrire une fonction `cherche2()` qui prend en argument :

- un ensemble ([`set`](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)) de `mots` ;
- une liste de chaines de caractères `lstart` ;
- une liste de chaines de caractères `lmid` ;
- une liste de chaines de caractères `lstop` ;
- un entier nmin, le nombre minimal de lettres dans le mot
- un entier nmax, le nombre maximal de lettres dans le mot
- et retourne le sous ensemble des mots :
  - de longueur comprise entre  `nmin` et `nmax` ;
  - commençant par une chaine de caractères présente dans `lstart` ;
  - comportant une chaine de caractères présente dans `lmid`, qui n'est ni au début, ni à la fin du mot ;
  - se terminant par une chaine de caractères présente dans `lstop`.

### Application

Utiliser les fonctions `main()` et `cherche2()` pour trouver les mots de 8 à 12 lettres commençant par une consonne, se terminant par une voyelle et comportant un ``ç``.

<!-- START INSERT -->

## To do

1️⃣ Ecrire (ou modifier) le code de la fonction secondaire.

2️⃣ Si nécessaire, ajouter (ou modifier) les appels à la fonction secondaire logés dans la fonction principale ``main()``. Cela permet de tester la fonction secondaire sur quelques cas simples.

3️⃣ Exécuter le programme depuis le terminal. Tant que la fonction secondaire ne retourne pas les résultats attendus, répéter le cycle 1️⃣ 2️⃣ 3️⃣.

    $ python main.py

4️⃣ Lorsque les résultats obtenus à l'étape 3️⃣ sont satisfaisants, soumettre le code à une procédure de test plus robuste, les tests unitaires.

    $ pytest .python

Le score de test ``ST`` obtenu est le pourcentage de tests réussis. Tant que certains tests échouent, répéter le cycle 1️⃣ 2️⃣ 3️⃣ 4️⃣

5️⃣ Lorsque le score de test ``ST`` est satisfaisant, s'intéresser à la [qualité du code](https://perso.esiee.fr/~courivad/courses/utils/sources/python-23-codequality.html).

    $ pylint main.py

Si le score de qualité ``SQ`` n'est pas maximal, répéter l'étape 5️⃣ en tenant compte des messages dans le terminal

6️⃣ Lorsque les scores ``ST`` et ``SQ`` sont satisfaisants, initialiser les variables d'environnement fournies dans BlackBoard puis pusher le travail pour évaluation

    $ git add .
    $ git commit -m "un message explicatif"
    $ git push

> [!CAUTION]
En cas de soumissions multiples, seule la première est prise en compte.

<!-- END INSERT -->
