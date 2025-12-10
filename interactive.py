"""
Vibeyf-AI - Mode Interactif Console
Permet à l'utilisateur de remplir le questionnaire directement dans la console
"""
from services.questionnaire_service import QuestionnaireService
from main import VibeyfAI


def main():
    """Point d'entrée pour le mode interactif"""
    print("\n" + "="*70)
    print("  🎵 VIBEYF-AI - MODE INTERACTIF")
    print("="*70)
    
    vibey = VibeyfAI(use_gemini=True)
    
    # Créer le questionnaire
    questionnaire = QuestionnaireService()
    
    # Afficher le questionnaire complet
    questionnaire.afficher_questionnaire()
    
    # Demander confirmation avant de commencer
    print("\n" + "="*70)
    input("Appuyez sur Entrée pour commencer à répondre...")
    
    # Collecter les réponses en mode interactif
    reponses = questionnaire.collecter_reponses_console()
    
    # Demander un ID utilisateur (optionnel)
    print("\n" + "="*70)
    print("Souhaitez-vous sauvegarder avec un identifiant personnalisé ?")
    user_id = input("Votre ID (laissez vide pour auto) : ").strip()
    if not user_id:
        user_id = None
    
    resultat = vibey.executer_recommandation_complete(reponses, user_id=user_id)
    
    # Afficher les résultats
    vibey.afficher_recommandations(resultat)
    
    # Proposer de recommencer
    print("\n" + "="*70)
    reponse = input("\nVoulez-vous faire une nouvelle recommandation ? (o/n) : ").strip().lower()
    if reponse in ['o', 'oui', 'y', 'yes']:
        print("\n" * 2)
        main()  # Récursion pour recommencer
    else:
        print("\n✨ Merci d'avoir utilisé Vibeyf-AI ! À bientôt ! 🎵")
        print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Interruption utilisateur. Au revoir ! 👋")
    except Exception as e:
        print(f"\n\n❌ Erreur inattendue: {e}")
        print("Veuillez vérifier votre configuration et réessayer.")
