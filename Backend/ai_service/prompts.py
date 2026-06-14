import json


JSON_ONLY_SYSTEM = "Tu réponds uniquement avec un objet JSON valide, sans markdown."


def build_flashcards_prompt(text, count, difficulty="all", focus=""):
    difficulty_instruction = (
        "répartis les difficultés entre easy, medium et hard"
        if difficulty == "all"
        else f"toutes les cartes doivent avoir la difficulté {difficulty}"
    )
    focus_instruction = focus or "les notions les plus importantes du cours"
    return f"""
Tu es un assistant pédagogique expert en création de supports de révision.
Génère jusqu'à {count} flashcards distinctes et utiles à partir de cette section du cours.

Réponds uniquement avec:
{{"items": [{{"question": "question claire", "answer": "réponse précise", "difficulty": "easy"}}]}}

Contraintes:
- réponds uniquement en français
- difficulty doit être easy, medium ou hard; {difficulty_instruction}
- concentre-toi sur: {focus_instruction}
- privilégie les définitions, méthodes, mécanismes, concepts et relations
- ignore les détails administratifs, liens et bibliographies
- ne reformule pas deux fois la même question
- n'invente rien et retourne moins de cartes si la section manque de matière

Section du cours:
{text}
"""


def build_summary_facts_prompt(text, fact_count, instructions=""):
    focus = instructions or "les notions les plus importantes du cours"
    return f"""
Tu analyses une section d'un cours afin de préparer une synthèse globale.
Extrais uniquement les faits pédagogiques importants, précis et autonomes.

Contraintes:
- réponds en français et n'invente rien
- ignore les détails administratifs, liens et bibliographies
- privilégie définitions, relations, mécanismes, méthodes et conclusions
- fusionne les idées redondantes
- retourne au maximum {fact_count} faits
- consigne particulière: {focus}

Réponds uniquement avec:
{{"facts": ["fait important 1", "fait important 2"]}}

Section du cours:
{text}
"""


def build_summary_synthesis_prompt(facts, line_count, instructions=""):
    focus = instructions or "les notions les plus importantes du cours"
    return f"""
Tu es un assistant pédagogique expert en synthèse de cours.
Crée une fiche de révision cohérente uniquement à partir des faits vérifiés.

Contraintes:
- réponds en français et n'invente rien
- fusionne les doublons et organise les idées dans un ordre logique
- chaque ligne doit apporter une information différente et utile
- retourne jusqu'à {line_count} lignes, sans répétition pour remplir
- la dernière ligne doit commencer par "À retenir :"
- consigne particulière: {focus}

Réponds uniquement avec:
{{"lines": ["ligne 1", "ligne 2"]}}

Faits vérifiés:
{json.dumps(facts, ensure_ascii=False)}
"""


def build_quiz_prompt(flashcards, count, difficulty="medium", instructions=""):
    focus = instructions or "les notions les plus importantes"
    return f"""
Tu es un assistant pédagogique expert en création de QCM de révision.
Génère jusqu'à {count} questions distinctes à partir des flashcards fournies.

Réponds uniquement avec:
{{"items": [{{"question": "question claire", "choices": ["A", "B", "C", "D"], "correct_answer": "A", "explanation": "explication courte"}}]}}

Contraintes:
- réponds uniquement en français
- chaque question teste une notion différente
- chaque question a exactement 4 choix distincts
- correct_answer est exactement égal à un choix
- les mauvais choix sont plausibles mais faux
- ne répète ni question, ni ensemble de choix
- niveau attendu: {difficulty}
- consigne particulière: {focus}
- retourne moins de questions si les flashcards ne permettent pas d'en créer davantage

Flashcards:
{json.dumps(flashcards, ensure_ascii=False)}
"""


def build_personal_quiz_prompt(topic, count, difficulty="medium", instructions=""):
    focus = instructions or "couvrir les notions principales"
    return f"""
Tu es un assistant pédagogique expert en création de QCM.
Génère jusqu'à {count} questions distinctes sur le sujet fourni.

Réponds uniquement avec:
{{"items": [{{"question": "question claire", "choices": ["A", "B", "C", "D"], "correct_answer": "A", "explanation": "explication courte"}}]}}

Contraintes:
- réponds uniquement en français
- chaque question teste un aspect différent
- exactement 4 choix distincts et une seule bonne réponse
- correct_answer est exactement égal à un choix
- ne répète ni question, ni ensemble de choix
- niveau attendu: {difficulty}
- consigne particulière: {focus}

Sujet:
{topic}
"""


def build_pdf_question_prompt(context, question):
    return f"""
Tu es un assistant pédagogique.
Réponds à la question uniquement à partir des extraits du cours fournis.
Si la réponse n'y figure pas, réponds: "Je ne trouve pas cette information dans le cours."
Réponds en français, clairement, sans inventer.

Question:
{question}

Extraits pertinents du cours:
{context}
"""


def build_revision_plan_prompt(deck_title, flashcards, availabilities, exam_date, priority):
    return f"""
Tu es un assistant pédagogique spécialisé dans l'organisation des révisions.
Propose un planning réaliste utilisant uniquement les disponibilités fournies.

Réponds uniquement avec:
{{"sessions": [{{"day": "Lundi", "start_time": "18:00", "end_time": "19:00", "objective": "Réviser les notions principales", "session_type": "flashcards", "todo_title": "Réviser les cartes importantes", "todo_description": "Revoir les cartes difficiles", "todo_priority": "high"}}]}}

Contraintes:
- maximum 5 séances et aucune séance hors disponibilité
- session_type: flashcards, summary, quiz ou review
- todo_priority: low, medium ou high
- réponds en français

Deck: {deck_title}
Date d'examen: {exam_date}
Priorité: {priority}
Disponibilités: {json.dumps(availabilities, ensure_ascii=False)}
Flashcards représentatives: {json.dumps(flashcards, ensure_ascii=False)}
"""
