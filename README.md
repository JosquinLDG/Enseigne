# Enseigne
TD0 M2 MMAA INFO901 : Enseigne

## Description
Ce projet consiste à créer une application pour gérer une enseigne de matériel de sport disposant de plusieurs magasins en France. L'application permet de structurer les magasins en secteurs d'activités et en rayons, de gérer les vendeurs (affectation, suivi des ventes, fiches signalétiques) ainsi que les clients.

## Installation à partir d'un terminal

### Sur Linux et macOS
```bash
git clone https://github.com/titis73/Enseigne.git
cd Enseigne
python3 -m venv .venv # Évite d'installer dans l'environnement global
source .venv/bin/activate # Active l'environnement virtuel
pip install -e .  # Installe les dépendances
```

### Sur Windows
```powershell
git clone https://github.com/titis73/Enseigne.git
cd Enseigne
python3 -m venv .venv  # Évite d'installer dans l'environnement global
.\.venv\Scripts\Activate.ps1  # Active l'environnement virtuel
pip install -e . # Installe les dépendances
```

## Utilisation

Aprés avoir fait les etapes détaillé ci-dessus exécuter la commande suivante 
```console
enseigne
```

# Affichage des diagrammes UML

Les diagrammes UML sont écrits dans le langage [Mermaid](https://mermaid.js.org/intro/). 

Pour les visualiser directement dans votre navigateur à l'aide du script de documentation, vous pouvez exécuter les commandes suivantes dans votre console :

```bash
# Afficher le diagramme de classe
python3 ./doc/mermaid.py ./doc/class.mmd

# Afficher le diagramme de cas d'utilisation
python3 ./doc/mermaid.py ./doc/use_case.mmd

# Afficher le diagramme de séquence
python3 ./doc/mermaid.py ./doc/sequence.mmd
```

## Structure du projet
```text
Enseigne/
├── docs/                 # Documentation (Diagramme UML)
├── src/
│   └── enseigne/
│       ├── __init__.py   # Fichier d'initialisation des modules 
│       ├── __main__.py   # Fichier d'entrée de notre programme 
│       ├── module1.py    # Classe 1 
│       └── module2.py    # Classe 2
├── LICENSE               # Conditions d’utilisation de votre projet  
├── README.md             # Explication du projet  
└── pyproject.toml        # Fichier de configuration
└── .gitignore            # Liste des fichiers et dossiers non suivis par Git
```

## Organisation des membres

| Rôle | Personnes |
|----------|-------------|
| GITHUB | Mathis, Josquin |
| Dictionnaire | Jodie, Judith, Lilou, Anaïs |
| Diagramme UML (Use Case) | ???? |
| Diagramme UML (Séquence) | ???? |
| Diagramme UML (Classe) | Salihou + Mathis |
| Scrum Master |  Jodie + Séphora |
| Product Owner | Dimitri + Mathis |
| Programme principal | Josquin + Jodie |



| Classe | Personnes |
|----------|-------------|
| Vente | Anaïs |
| Client | Lilou |
| Achat| Séphora |
| Produit | Dimitri |
| ClasseMetier | Mathieu |
| Vendeur |  Assil |
| VendeurResponsable| Josquin |
| Rayon | Mathis |
| Activite | Yoliza |
| Magasin | Jodie |
| SiteInternet | Judith |



## Comment contribuer
*Note importante : On ne code jamais directement sur la branche principale. Le travail s'organise par version/semaine (ex: `S42` pour la semaine 42, puis `S46` pour la semaine suivante).*

1. Créez un compte sur [GitHub](https://github.com).
2. Forkez le projet depuis [Enseigne](https://github.com/titis73/Enseigne). Cliquez sur le bouton **Fork** en haut à droite de la page du dépôt GitHub, puis sur *Create fork*. Cette action va créer un dépôt `user_name/Enseigne` sur votre compte.
3. clonez votre propre dépôt sur votre machine : 
   ```bash
   git clone https://github.com/user_name/Enseigne
   ```
4. Placez-vous sur la branche de la semaine en cours (par exemple `S42`) :
   ```bash
   git checkout S42
   ```
5. Créez et basculez sur une nouvelle branche de travail personnelle en respectant la convention :
   - `feat/nom_de_la_feature` pour l'ajout d'une fonctionnalité
   - `fix/nom_du_fix` pour résoudre un bug
   
   Exemple :
   ```console
   git checkout -b feat/gestion-vendeurs
   ```
6. Ajoutez toutes vos modifications :
   ```console
   git add .
   ```
7. Enregistrez les modifications avec un message clair :
   ```console
   git commit -m "feat: ajout de la classe Vendeur"
   ```
8. Envoyez votre branche sur votre fork GitHub (Push) :
   ```console
   git push origin feat/gestion-vendeurs
   ```
9. Ouvrez une Pull Request (PR) :
   - Rendez-vous sur votre fork sur GitHub.
   - Cliquez sur **"Compare & pull request"**.
   - Ciblez la branche de la semaine correspondante sur le dépôt officiel (ex: fusionner votre branche vers la branche `S42` du dépôt officiel).
   - Créez la Pull Request pour relecture par les responsables GitHub.
10. Une fois la PR validée et fusionnée par les responsables, mettez à jour votre dépôt local :
   ```console
   git checkout S42
   git pull origin S42
   git branch -d feat/gestion-vendeurs
   ```

## Conventions d'écriture du code
- Le nom des classes utilise le **PascalCase**.
- Les méthodes, fonctions et variables utilisent le **snake_case**.
- Un seul fichier par classe, et le nom du fichier sera en snake_case (exemple : pour la classe `SecteurActivite`, le fichier s'appellera `secteur_activite.py`).
- Les fonctions et méthodes seront typées et documentées en utilisant le standard PEP 8 de Python.
  
  Exemple :
  ```python
  """
  Classe : ClassTemplate
  Module : 
  Description : Permet d'avoir une ossature pour toutes mes classes
  """
  class ClassTemplate:
      def __init__(self, aValeurAttribut01: type1, aValeurAttribut02: type2) -> None:
          """Constructeur de la classe ClassTemplate.
              
          Args:
              aValeurAttribut01: Description de aValeurAttribut01.
              aValeurAttribut02: Description de aValeurAttribut02.
          """
          self.attribut01 = aValeurAttribut01
          self.attribut02 = aValeurAttribut02

      def __str__(self) -> str:
          chaine = "Ma manière d'afficher la classe ClassTemplate\n"
          chaine += "attribut01=" + str(self.attribut01) + "\n"
          chaine += "attribut02=" + str(self.attribut02) + "\n"
          return chaine

      def action01(self, aValeurParametrage01: type2, aValeurParametrage02: type3) -> None:
          """Description de l'action01.
              
          Args:
              aValeurParametrage01: Description de aValeurParametrage01.
              aValeurParametrage02: Description de aValeurParametrage02.
          """
          print(str(self.attribut01) + " action01 avec les paramètres " + str(aValeurParametrage01) + ", " + str(aValeurParametrage02))
  ```
