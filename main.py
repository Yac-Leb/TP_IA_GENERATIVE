"""
Système de Recommandation Musicale Vibeyf-AI
Point d'entrée principal du backend
"""
import json
from pathlib import Path
from datetime import datetime

from services.referentiel_service import ReferentielMusical
from services.questionnaire_service import QuestionnaireService
from services.nlp_service import MoteurNLP
from services.scoring_service import SystemeScoring
from services.gemini_service import GeminiService
from config.config import RESPONSES_DIR


class VibeyfAI:
    """Classe principale orchestrant tout le système de recommandation"""
    
    def __init__(self, use_gemini: bool = True):
        """
        Initialise le système complet
        
        Args:
            use_gemini: Activer ou non l'intégration Gemini
        """
        print("\n" + "="*70)
        print("  VIBEYF-AI - SYSTÈME DE RECOMMANDATION MUSICALE")
        print("="*70)
        
        self.referentiel = ReferentielMusical()
        self.moteur_nlp = MoteurNLP()
        
        if not self.moteur_nlp.charger_cache():
            textes_ref = self.referentiel.get_all_semantic_texts()
            self.moteur_nlp.preparer_referentiel(textes_ref)
        
        self.scoring = SystemeScoring()
        self.questionnaire = QuestionnaireService()
        self.use_gemini = use_gemini
        self.gemini = GeminiService() if use_gemini else None
        
        print("✓ Système initialisé\n")
    
    def executer_recommandation_complete(
        self,
        reponses_utilisateur: dict,
        user_id: str = None
    ) -> dict:
        """
        Exécute le processus complet de recommandation
        
        Args:
            reponses_utilisateur: Réponses au questionnaire
            user_id: Identifiant utilisateur (optionnel)
            
        Returns:
            Dictionnaire complet avec recommandations et analyses
        """
        if user_id is None:
            user_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print("\n🎵 Génération de vos recommandations...\n")
        
        reponses_structurees = self.questionnaire.collecter_reponses_dict(
            reponses_utilisateur
        )
        self.questionnaire.sauvegarder_reponses(reponses_structurees, user_id)
        
        texte_utilisateur = self.questionnaire.extraire_texte_semantique(
            reponses_structurees
        )
        
        texte_enrichi = texte_utilisateur
        if self.use_gemini and self.gemini and self.gemini.model:
            try:
                texte_enrichi = self.gemini.enrichir_texte_court(texte_utilisateur)
            except:
                pass
        
        elements_avec_similarite = self.moteur_nlp.obtenir_scores_detailles(
            texte_enrichi
        )
        
        preferences_audio = self.questionnaire.extraire_preferences_audio(
            reponses_structurees
        )
        
        genres_preferes = self.questionnaire.extraire_genres_preferes(
            reponses_structurees
        )
        
        niveau_ouverture = self.questionnaire.extraire_niveau_ouverture(
            reponses_structurees
        )
        
        elements_scores = self.scoring.calculer_scores_elements(
            elements_avec_similarite,
            preferences_audio,
            texte_enrichi,
            moods_detectes=None,
            genres_preferes=genres_preferes,
            niveau_ouverture=niveau_ouverture
        )
        
        recommandations = self.scoring.generer_recommandations(
            elements_scores,
            top_n=3
        )
        
        rapport_genai = None
        if self.use_gemini and self.gemini and self.gemini.model:
            try:
                rapport_genai = self.gemini.generer_rapport_complet(
                    recommandations,
                    texte_utilisateur,
                    texte_enrichi
                )
            except:
                pass
        
        # Construire le résultat final
        resultat = {
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            'texte_utilisateur_original': texte_utilisateur,
            'texte_enrichi': texte_enrichi if texte_enrichi != texte_utilisateur else None,
            'preferences_audio': preferences_audio,
            'recommandations': {
                'top_3': [
                    {
                        'rang': i + 1,
                        'type': r['type'],
                        'id': r['id'],
                        'nom': r['data'].get('nom', r['id']),
                        'artiste': r['data'].get('artiste', '') if r['type'] == 'chanson' else None,
                        'genre': r.get('genre', r['data'].get('genre', '')) if r['type'] == 'chanson' else None,
                        'description': r['data'].get('description', ''),
                        'score_global': r['scores']['global'],
                        'details_scores': r['scores'],
                        'data': r['data']
                    }
                    for i, r in enumerate(recommandations['top_recommandations'])
                ],
                'top_par_type': {
                    type_elem: [
                        {
                            'type': e['type'],
                            'id': e['id'],
                            'nom': e['data'].get('nom', e['id']),
                            'score': e['scores']['global']
                        }
                        for e in elements
                    ]
                    for type_elem, elements in recommandations['top_par_type'].items()
                },
                'statistiques': recommandations['statistiques']
            },
            'rapport_genai': rapport_genai
        }
        
        self._sauvegarder_resultat(resultat, user_id)
        
        return resultat
    
    def _sauvegarder_resultat(self, resultat: dict, user_id: str):
        """Sauvegarde le résultat complet"""
        output_path = RESPONSES_DIR / f"resultat_{user_id}.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(resultat, f, ensure_ascii=False, indent=2)
    
    def afficher_recommandations(self, resultat: dict):
        """Affiche les recommandations de manière formatée"""
        print("\n" + "="*70)
        print("  RÉSULTATS DE LA RECOMMANDATION")
        print("="*70)
        
        # Top 3
        print("\n🎵 TOP 3 RECOMMANDATIONS:")
        print("-"*70)
        for reco in resultat['recommandations']['top_3']:
            type_icon = "🎵" if reco['type'] == 'chanson' else "📁"
            print(f"\n{reco['rang']}. {type_icon} [{reco['type'].upper()}] {reco['nom']}")
            
            # Affichage spécial pour les chansons
            if reco['type'] == 'chanson' and 'artiste' in reco:
                print(f"   Artiste: {reco['artiste']}")
                if 'genre' in reco:
                    print(f"   Genre: {reco['genre']}")
            
            print(f"   Score: {reco['score_global']:.3f}")
            
            # Description si disponible
            if reco.get('description') and reco['type'] != 'chanson':
                print(f"   {reco['description'][:100]}...")
            
            details = reco.get('details_scores', {})
            boost_text = " 🌟 GENRE PRÉFÉRÉ" if details.get('genre_boost', 0) > 0 else ""
            print(f"   Détails: Sémantique={details.get('similarite_semantique', 0):.2f} | "
                  f"Mood={details.get('mood_match', 0):.2f} | "
                  f"Préférences={details.get('preference_likert', 0):.2f}{boost_text}")
        
        # Statistiques
        stats = resultat['recommandations']['statistiques']
        print("\n" + "="*70)
        print("📊 STATISTIQUES:")
        print(f"  - Score moyen: {stats['score_moyen']:.3f}")
        print(f"  - Score maximum: {stats['score_max']:.3f}")
        print(f"  - Éléments évalués: {stats['nombre_elements_evalues']}")
        
        # Rapport GenAI
        if resultat.get('rapport_genai'):
            print("\n" + "="*70)
            print("🤖 SYNTHÈSE GENAI:")
            print("-"*70)
            print(resultat['rapport_genai']['synthese'])
            
            print("\n" + "="*70)
            print("📈 PLAN DE PROGRESSION:")
            print("-"*70)
            print(resultat['rapport_genai']['plan_progression'])
        
        print("\n" + "="*70)