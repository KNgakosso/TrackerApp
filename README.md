# Tracking

Tracking est une application web permettant de **rechercher et suivre des médias**, notamment des anime et des mangas.

## Démo

**[Accéder à l'application en ligne](https://trackerapp-jach.onrender.com/tracking)**

## Fonctionnalités

* Recherche d'anime et de mangas
* Consultation des informations d'un média
* Suivi de la progression
* Attribution d'une note et d'une classification
* Création et gestion de watchlists
* Récupération des informations depuis une API externe
* Sauvegarde des médias en base de données

## Technologies

* **Python**
* **Django**
* **pytest**

## Architecture

Le projet est organisé en plusieurs couches afin de séparer les responsabilités et de limiter les dépendances entre elles.

```text
Views
  │
  ▼
Use cases
  │
  ├───────────────┐
  ▼               ▼
Storage services  Tenrai services
  │               │
  ▼               ▼
ORM layer         API client
  │               │
  ▼               ▼
Django ORM       API externe
```

### Domain

Les classes du domaine représentent les objets métier de l'application (`Media`, `Anime`, `Manga`, `Watchlist`, etc.) indépendamment de Django.

### ORM

Une couche dédiée encapsule les interactions avec les modèles Django. Elle permet de ne pas exposer directement les modèles et méthodes Django aux couches supérieures.

### Services

Les services de stockage et d'intégration transforment les données techniques en objets du domaine et fournissent une interface indépendante de l'implémentation sous-jacente.

### Use cases

Les use cases portent la logique applicative et orchestrent les différentes opérations nécessaires à une fonctionnalité.

### Views

Les views gèrent les requêtes HTTP, les formulaires et la présentation des données via les templates Django.

## Tests

Le projet utilise **pytest** pour tester les différentes couches de l'application.

Les tests comprennent notamment :

* des tests unitaires de la logique applicative ;
* des tests d'intégration avec la base de données ;
* des tests des interactions avec les services externes via des mocks.

L'objectif est de tester les différentes responsabilités sans rendre l'ensemble de la suite de tests dépendante de l'API externe.

## Installation

```bash
git clone <URL_DU_REPOSITORY>
cd tracking

python -m venv .venv
source .venv/bin/activate  # Linux / macOS
# .venv\Scripts\activate   # Windows

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

Les variables d'environnement nécessaires au projet doivent être configurées avant le lancement.

## Statut

Projet personnel en cours de développement.
