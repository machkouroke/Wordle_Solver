Wordle_Solver
============
Programme python permettant de résoudre le jeu Wordle en 3 coup en moyenne

![tempFileForShare_20220703-144805](https://user-images.githubusercontent.com/40785379/177042717-9dc861f5-2d49-4ba7-b0b1-fe73d2fcdc96.jpg)

<a href="https://buymeacoffee.com/machkouroke" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>


## Caractéristique
Ce programme permet de résoudre le populaire jeux de mots Wordle en 3 coup en moyenne(Ce qui est déja très bien pour épater vos camarade). 
Il se base sur un concept important de la théorie de l'information qu'est l'entropie. Ainsi pour un dictionnaire de mots données on vas rechercher à chaque étape du jeu quelle est le mot qui nous apporteras le plus d'informations en général. En effet l'entropie peut être considéré comme la moyenne des informations d'un mot données pour chaque possibilité du jeu


## Comment l'utiliser
- Cloner le répository avec:
```
git clone https://github.com/machkouroke/Wordle_Solver.git
```
- A la première exécution du programme ils vous seras demandé de choisir un dictionnaire (3 vous seront proposé de base). Pour ajouter votre propre dictionnaire veuillez voir la section <a href='#add_dico'>Ajouter votre propre dictionnaire.</a>
```
====Bienvenue sur le LOPWorld Solver====
Quel dictionnaire de mot vouliez vous utiliser
1 - Dictionnaire francais court (22740 mots)
2 - Dictionnaire francais long (208914 mots)
3 - Dictionnaire anglais (84100 mots)
Veuillez saisir votre choix:
```
- Le premier démarrage seras un peu lent car l'algorithme vas chercher le meilleurs mots dans le dictionnaire que vous lui aviez fournit 
- Après avoir trouvé le meilleur mots il vous seras demandé de le saisir dans votre jeu Wordle (vous pouviez en saisir un autre mais cela retarderas l'algorithme)
```
Le meilleur mot est:  jeton
Quel mot aviez-vous saisi: jeton
```
- Ensuite le pattern que vous auriez obtenu dans l'application vous seras demandé (j -> jaune, g -> gris, v -> vert)
```
Quelle est le model que vous aviez obtenue: (V:Vert, G:Gris, J:Jaune) gjgjg
---Recherche du meilleur mot de l'étape actuelle
Le meilleur mot est:  chope
Quel mot aviez-vous saisi:chope
Quelle est le model que vous aviez obtenue: (V:Vert, G:Gris, J:Jaune) jjjjv
---Recherche du meilleur mot de l'étape actuelle
Le meilleur mot est:  poche
Quel mot aviez-vous saisi: poche
Quelle est le model que vous aviez obtenue: (V:Vert, G:Gris, J:Jaune) vvvvv
```
- Le script s'arrêteras si vous saisisez 'vvvvv' qui signifie que le mot est trouvé ou 'stop' pour un arrêt prématuré
- On note qu'on peut encore faire mieux que l'algorithme en chosisant dans la liste des mots trouvé par l'algorithme le mot le plus fréquent car Wordle utilise des mots courants

---

## <span id="add_dico"> Ajouter votre propre dictionnaire <span>

Si le dictionnaire par défaut ne vous convient pas ou tout simplement ne comprends pas votre langue vous pouviez l'ajouter en suivant les étapes suivantes
- Copier le fichier contenat votre dictionnaire dans le dossier dico
- Ajouter son chemin dans le dictionnaire du code main en respectant les numéros
- Vous pouviez personnaliser le menu (Fonction menu) pour voir votre dictionnaire apparaitre dans le menu
- N'hésitez pas à partager votre dictionnaire avec nous en soumettant votre pull

---

