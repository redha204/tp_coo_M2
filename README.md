# COO_usine_boisson

Projet de Conception Orientée Objet - Gestion d'une usine de boissons

## Description

Application hybride Django/C++ pour la gestion d'une usine de production de boissons.

- **Backend Django** : API REST avec modèles de gestion (localisations, machines, produits, etc.)
- **Client C++** : Application cliente utilisant l'API avec classes C++ et smart pointers

## Structure

```
boissons/
├── high_level/     # Application Django avec modèles et API
├── low_level/      # Client C++ avec classes et requêtes HTTP
└── manage.py       # Script Django
```

## Installation

### Backend Django

```bash
source monenv/bin/activate
cd boissons
python manage.py migrate
python manage.py runserver
```

### Client C++

```bash
cd boissons/low_level
cmake -B build -S .
cmake --build build
./build/low_level
```

## API

L'API est accessible à `http://localhost:8000/api/`

Endpoints disponibles :
- `/api/<model>/<id>/` - Données basiques
- `/api/<model-name>/<id>/` - Données étendues avec relations

Exemple : `http://localhost:8000/api/localisation/1/`

## Technologies

- Python 3.12 + Django 5.2.7
- C++17 + CMake
- Libraries C++ : CPR (HTTP), nlohmann/json (JSON parsing)
- Smart pointers : `std::unique_ptr<>`, `std::optional<>`

## Auteurs

- Redha Aberkane
- Fawzi Hadjara

Master 2 ISTR

