# ESIEE Network

ESIEE Network est une application web Django destinee aux etudiants ESIEE.
Le projet centralise plusieurs services campus dans une seule interface :

- publications et interactions entre etudiants,
- gestion d'evenements,
- carte du campus avec marqueurs d'evenements,
- messagerie privee,
- profils utilisateurs et recherche de comptes.

## Objectif

Le but du projet est de proposer un mini reseau social etudiant oriente campus.
Un utilisateur peut :

- creer un compte avec une adresse ESIEE,
- se connecter et gerer son profil,
- publier des annonces ou messages,
- aimer et commenter des publications,
- creer des evenements lies a un lieu du campus,
- visualiser ces evenements sur la carte,
- rechercher d'autres utilisateurs,
- envoyer des messages prives.

## Stack technique

- `Python`
- `Django`
- `SQLite`
- `Django Templates`
- `HTML / CSS`
- `Bootstrap 5`
- `Bootstrap Icons`
- `JavaScript`

## Structure du projet

Le projet est organise en apps Django :

- `users/`
  - authentification, inscription, verification email,
  - profils utilisateurs,
  - recherche d'utilisateurs,
  - systeme de follow,
  - messagerie privee.
- `posts/`
  - publications,
  - likes,
  - commentaires et reponses.
- `events/`
  - creation, modification, suppression et affichage d'evenements,
  - gestion des lieux officiels du campus.
- `maps/`
  - affichage de la carte ESIEE,
  - affichage des marqueurs d'evenements sur la carte.
- `templates/`
  - templates HTML globaux du projet.
- `static/`
  - fichiers statiques, dont CSS et image de la carte.
- `media/`
  - images uploades par les utilisateurs.

## Fonctionnalites principales

### Authentification

- inscription avec email ESIEE,
- verification email,
- connexion / deconnexion,
- reinitialisation du mot de passe.

### Publications

- creation de publication,
- modification / suppression,
- likes,
- commentaires et reponses.

### Evenements

- creation d'un evenement avec un lieu,
- affichage de la liste des evenements,
- detail d'un evenement,
- modification / suppression par le createur.

### Carte du campus

- carte statique ESIEE,
- lieux predefinis avec coordonnees en pourcentage,
- marqueurs d'evenements a venir ou en cours,
- popup d'information sur la carte.

### Utilisateurs et messagerie

- recherche d'autres comptes,
- consultation d'un profil public,
- suivi d'autres utilisateurs,
- messagerie privee entre comptes.

## Prerequis

- `Python 3.11+` recommande
- `pip`
- environnement virtuel recommande

## Installation

### 1. Cloner le projet

```powershell
git clone <url-du-repo>
cd Esiee_network
```

### 2. Creer et activer un environnement virtuel

Sous Windows PowerShell :

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Sous Linux / macOS :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dependances

```powershell
pip install -r requirements.txt
```

## Lancer le projet

### 1. Appliquer les migrations

```powershell
py manage.py migrate
```

### 2. Lancer le serveur de developpement

```powershell
py manage.py runserver
```

Le projet sera accessible ici :

```text
http://127.0.0.1:8000/
```

## Commandes utiles

### Creer un superutilisateur

```powershell
py manage.py createsuperuser
```

### Faire de nouvelles migrations

```powershell
py manage.py makemigrations
py manage.py migrate
```

### Verifier le projet

```powershell
py manage.py check
```

### Ouvrir le shell Django

```powershell
py manage.py shell
```

### Lancer les tests

```powershell
py manage.py test
```

## Routes principales

- `/` : page d'accueil
- `/signup/` : inscription
- `/login/` : connexion
- `/logout/` : deconnexion
- `/mon-profil/` : profil personnel
- `/profile/` : modification du profil
- `/search-users/` : recherche d'utilisateurs
- `/messages/` : liste des conversations
- `/messages/<username>/` : conversation avec un utilisateur
- `/posts/` : publications
- `/events/` : liste des evenements
- `/events/create/` : creation d'un evenement
- `/map/` : carte du campus
- `/admin/` : interface d'administration Django

## Configuration actuelle

Quelques points importants du projet :

- base de donnees : `SQLite` via `db.sqlite3`,
- utilisateur personnalise : `users.User`,
- fichiers medias servis depuis `media/` en mode `DEBUG`,
- backend email de developpement :
  - les emails sont affiches dans la console,
  - ils ne sont pas envoyes reellement en production.

## Comptes et verification email

L'inscription demande une adresse se terminant par :

```text
@edu.esiee.fr
```

Apres inscription :

- le compte est cree inactif,
- un email de verification est genere,
- en environnement de developpement, le lien est visible dans la console du serveur.

## Carte et evenements

Le systeme de carte fonctionne ainsi :

- un evenement est lie a un `Location`,
- chaque `Location` possede `x_percent` et `y_percent`,
- la page `/map/` affiche les evenements a venir ou en cours,
- les marqueurs sont positionnes sur l'image statique du campus.

## Arborescence minimale

```text
Esiee_network/
├── esiee_network/      # configuration Django
├── users/              # auth, profils, recherche, messages
├── posts/              # publications, likes, commentaires
├── events/             # evenements et lieux
├── maps/               # carte du campus
├── templates/          # templates HTML
├── static/             # CSS, images, assets
├── media/              # uploads utilisateurs
├── db.sqlite3          # base SQLite
├── manage.py
└── requirements.txt
```

## Conseils pour le developpement

- activer l'environnement virtuel avant toute commande Django,
- executer `py manage.py migrate` apres recuperation de nouvelles migrations,
- verifier la console lors des tests d'inscription ou de reset mot de passe,
- si une image statique ne change pas, faire un rafraichissement fort du navigateur.

## Limites actuelles

- base SQLite adaptee au developpement et a une petite charge,
- pas de temps reel pour la messagerie,
- backend email configure pour le developpement uniquement.

## Auteur / Contexte

Projet realise dans le cadre d'un travail collaboratif etudiant autour d'une plateforme campus ESIEE construite avec Django.
