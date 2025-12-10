"""
Utilitaires pour le système de recommandation
"""
import json
from pathlib import Path
from typing import Any, Dict


def charger_json(filepath: Path) -> Dict[str, Any]:
    """Charge un fichier JSON"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def sauvegarder_json(data: Dict[str, Any], filepath: Path):
    """Sauvegarde des données en JSON"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def formater_score(score: float) -> str:
    """Formate un score pour affichage"""
    return f"{score:.3f}"


def normaliser_texte(texte: str) -> str:
    """Normalise un texte (minuscules, espaces)"""
    return " ".join(texte.lower().strip().split())
