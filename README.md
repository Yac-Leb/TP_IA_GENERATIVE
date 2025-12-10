# 🎵 Vibeyf-AI - Système de Recommandation Musicale Intelligent

Système de recommandation musicale basé sur l'analyse sémantique NLP (SBERT) et l'intelligence artificielle générative (Gemini API). Ce projet combine des techniques avancées de traitement du langage naturel avec un scoring pondéré pour proposer des recommandations musicales personnalisées.

## 📋 Table des Matières

- [Présentation](#présentation)
- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Structure du Projet](#structure-du-projet)
- [Exigences Fonctionnelles](#exigences-fonctionnelles)
- [Technologies](#technologies)

## 🎯 Présentation

Vibeyf-AI est un système backend de recommandation musicale qui analyse les préférences utilisateur exprimées en langage naturel pour proposer des playlists, genres, moods et ambiances musicales correspondant parfaitement à leurs attentes.

### Thématique
Recommandation musicale basée sur :
- Description d'ambiance ou mood en langage naturel
- Préférences musicales (échelle de Likert)
- Artistes ou genres préférés

### Référentiel Musical
Le système comprend :
- **Genres** : Extraction depuis Spotify-2000 dataset
- **Moods** : 10 moods définis (joyeux, triste, énergique, calme, etc.)
- **Ambiances** : 10 ambiances contextuelles
- **Playlists** : Générées par décennie, mood et niveau d'énergie
- **Artistes** : Base de données enrichie

## ✨ Fonctionnalités

### ✅ EF1 : Acquisition de la Donnée
- **Questionnaire hybride** avec questions Likert (1-5) et questions ouvertes
- **8 questions Likert** : énergie, calme, danse, valence, acoustique, intensité, rythme, ouverture
- **5 questions ouvertes** : mood, contexte, artistes, genres, émotions
- **Stockage structuré** en JSON

### ✅ EF2 : Moteur NLP Sémantique (Coût Zéro)
- **Modèle SBERT** : `paraphrase-multilingual-MiniLM-L12-v2` (multilingue français/anglais)
- **Embeddings vectoriels** pour référentiel et requêtes utilisateur
- **Similarité cosinus** pour mesurer la correspondance sémantique
- **Cache des embeddings** pour performances optimales

### ✅ EF3 : Système de Scoring et Recommandation
- **Formule de score pondérée** :
  - 50% Similarité sémantique (SBERT)
  - 20% Correspondance de mood
  - 20% Préférences Likert
  - 10% Caractéristiques audio (BPM, énergie, etc.)
- **Top 3 recommandations** globales + tops par catégorie
- **Analyse détaillée** avec scores décomposés

### ✅ EF4 : Augmentation par GenAI (Usage Stratégique)
- **EF4.1 - Enrichissement conditionnel** : Textes courts (<5 mots) enrichis via Gemini
- **EF4.2 - Plan de progression** : Recommandations personnalisées avec éléments à explorer
- **EF4.3 - Synthèse executive** : Justification et mise en contexte des recommandations

## 🏗️ Architecture

```
Vibeyf-AI/
│
├── config/
│   └── config.py              # Configuration centrale (API keys, paramètres)
│
├── data/
│   └── Spotify-2000.csv       # Dataset musical
│
├── services/
│   ├── referentiel_service.py # Construction du référentiel musical
│   ├── questionnaire_service.py # Gestion des questionnaires
│   ├── nlp_service.py         # Moteur NLP avec SBERT
│   ├── scoring_service.py     # Système de scoring pondéré
│   └── gemini_service.py      # Intégration API Gemini
│
├── main.py                    # Point d'entrée principal
├── requirements.txt           # Dépendances Python
└── README.md                  # Documentation
```

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone https://github.com/votre-repo/Vibeyf-ai.git
cd Vibeyf-ai
```

2. **Créer un environnement virtuel** (recommandé)
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configuration de l'API Gemini**
```bash
copy .env.example .env
```
Éditer `.env` et ajouter votre clé API :
```
GEMINI_API_KEY=votre_clé_api_ici
```

Obtenir une clé API gratuite : [Google AI Studio](https://makersuite.google.com/app/apikey)

## ⚙️ Configuration

### Configuration principale (`config/config.py`)

```python
# Modèle SBERT
SBERT_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

# Recommandations
TOP_N_RECOMMENDATIONS = 3

# Enrichissement GenAI
MIN_WORDS_FOR_ENRICHMENT = 5

# Poids du scoring
WEIGHTS = {
    "semantic_similarity": 0.5,
    "mood_match": 0.2,
    "preference_likert": 0.2,
    "audio_features": 0.1
}
```

## 💻 Utilisation

### Utilisation Basique

```python
from main import VibeyAI

# Initialiser le système
vibey = VibeyAI(use_gemini=True)

# Préparer les réponses utilisateur
reponses = {
    "likert": {
        "q1_energie": 5,
        "q2_calme": 2,
        "q3_danse": 4,
        "q4_joyeux": 5,
        "q5_acoustique": 2,
        "q6_intensite": 4,
        "q7_rythme": 5,
        "q8_nouveaute": 4
    },
    "ouvertes": {
        "qo1_mood": "Musique énergique pour le sport",
        "qo2_contexte": "Salle de sport, running",
        "qo3_artistes": ["Foo Fighters", "The Killers"],
        "qo4_genres": ["rock", "alternative"],
        "qo5_emotions": "Énergie, motivation"
    }
}

# Obtenir les recommandations
resultat = vibey.executer_recommandation_complete(reponses)

# Afficher les résultats
vibey.afficher_recommandations(resultat)
```

### Exemple Complet

```bash
python main.py
```

Cela exécute un exemple complet avec des réponses prédéfinies et affiche :
- Top 3 recommandations globales
- Tops par catégorie (genre, mood, ambiance, playlist)
- Statistiques de scoring
- Synthèse GenAI
- Plan de progression personnalisé

### Construction du Référentiel

```bash
python services/referentiel_service.py
```

### Test des Services Individuels

```bash
# Test du moteur NLP
python services/nlp_service.py

# Test du système de scoring
python services/scoring_service.py

# Test du questionnaire
python services/questionnaire_service.py

# Test du service Gemini
python services/gemini_service.py
```

## 📁 Structure du Projet

### Fichiers de Configuration
- **config/config.py** : Configuration centrale, paramètres, mappings des moods
- **.env** : Variables d'environnement (clé API Gemini)

### Services
- **referentiel_service.py** : Construit et gère le référentiel musical à partir du CSV Spotify
- **questionnaire_service.py** : Gestion des questionnaires Likert et questions ouvertes
- **nlp_service.py** : Moteur d'embeddings SBERT et calcul de similarité cosinus
- **scoring_service.py** : Calcul des scores pondérés et génération des recommandations
- **gemini_service.py** : Intégration API Gemini pour enrichissement et génération

### Données
- **Spotify-2000.csv** : Dataset de 2000 chansons avec métadonnées audio
- **referentiel/** : Référentiel musical généré (JSON) et cache des embeddings
- **user_responses/** : Réponses utilisateur et résultats sauvegardés

## 📊 Exigences Fonctionnelles

### ✅ EF1 : Acquisition de la Donnée
- [x] Questionnaire hybride (Likert + questions ouvertes)
- [x] Structuration en JSON
- [x] Sauvegarde persistante

### ✅ EF2 : Moteur NLP Sémantique
- [x] Référentiel de connaissances musical
- [x] Modèle SBERT open-source local
- [x] Calcul de similarité cosinus
- [x] Cache des embeddings

### ✅ EF3 : Système de Scoring
- [x] Formule de score pondérée (4 composantes)
- [x] Top 3 recommandations globales
- [x] Recommandations par type
- [x] Statistiques détaillées

### ✅ EF4 : Augmentation GenAI
- [x] Enrichissement conditionnel (<5 mots)
- [x] Plan de progression personnalisé
- [x] Synthèse executive
- [x] Usage limité et stratégique (2 appels API max)

## 🛠️ Technologies

### Core NLP
- **sentence-transformers** : Modèles SBERT pour embeddings
- **transformers** : Backbone des modèles NLP
- **torch** : Framework PyTorch
- **scikit-learn** : Similarité cosinus

### Data Processing
- **pandas** : Manipulation des données Spotify
- **numpy** : Calculs numériques

### GenAI
- **google-generativeai** : API Gemini de Google

### Utilities
- **python-dotenv** : Gestion des variables d'environnement

## 📈 Performance

- **Temps d'initialisation** : ~10-30 secondes (chargement du modèle SBERT)
- **Temps de recommandation** : ~1-3 secondes (avec cache des embeddings)
- **Temps avec GenAI** : +3-5 secondes (2 appels API Gemini)

## 🎓 Méthodologie

### Analyse Sémantique
1. **Encoding** : Transformation des textes en vecteurs via SBERT
2. **Similarité** : Calcul de la similarité cosinus entre requête et référentiel
3. **Ranking** : Tri par score décroissant

### Scoring Pondéré
```
Score Global = 0.5 × Similarité Sémantique
             + 0.2 × Mood Match
             + 0.2 × Préférences Likert
             + 0.1 × Audio Features
```

### Usage GenAI
- **Enrichissement** : Usage conditionnel (texte court uniquement)
- **Synthèse** : 1 appel API pour résumer les recommandations
- **Plan** : 1 appel API pour le plan de progression

## 📝 Format des Résultats

```json
{
  "user_id": "20231209_143022",
  "timestamp": "2023-12-09T14:30:22",
  "texte_utilisateur_original": "Musique énergique pour le sport",
  "texte_enrichi": "...",
  "recommandations": {
    "top_3": [
      {
        "rang": 1,
        "type": "mood",
        "nom": "Énergique",
        "score_global": 0.87,
        "details_scores": { ... }
      }
    ],
    "top_par_type": { ... },
    "statistiques": { ... }
  },
  "rapport_genai": {
    "synthese": "...",
    "plan_progression": "..."
  }
}
```

## 🤝 Contribution

Ce projet a été développé dans le cadre d'un projet académique sur les systèmes de recommandation NLP et GenAI.

## 📄 License

Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🔗 Ressources

- [Sentence-BERT Documentation](https://www.sbert.net/)
- [Google Gemini API](https://ai.google.dev/)
- [Spotify Dataset](https://www.kaggle.com/datasets/iamsumat/spotify-top-2000s-mega-dataset)

---

**Développé avec ❤️ pour Vibeyf-AI**