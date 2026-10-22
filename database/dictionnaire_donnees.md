# Dictionnaire des données — Memora

## 1. Users

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant de l’utilisateur | Entier | Clé primaire | 1 |
| username | Nom d’utilisateur | Texte | Unique, non nul | alicebarka |
| email | Adresse email de l’utilisateur | Texte | Unique, non nul | alice@mail.com |
| password | Mot de passe chiffré | Texte | Non nul | pbkdf2_sha256... |
| role | Rôle de l’utilisateur | Texte | student / admin | student |
| is_active | Statut de vérification du compte | Booléen | true / false | true |

## 2. Folder

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant du dossier | Entier | Clé primaire | 1 |
| name | Nom du dossier | Texte | Non nul | Réseaux |
| created_at | Date de création | DateTime | Automatique | 2026-05-01 |
| user_id | Utilisateur propriétaire | Entier | Clé étrangère vers Users | 3 |

## 3. CoursePDF

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant du cours PDF | Entier | Clé primaire | 1 |
| title | Titre du cours | Texte | Non nul | Réseaux |
| subject | Matière ou catégorie du cours | Texte | Optionnel | Informatique |
| file | Chemin ou nom du fichier PDF | Texte | Non nul | reseaux.pdf |
| summary | Résumé généré par l’IA | Texte | Optionnel | Ce cours présente les protocoles réseau... |
| uploaded_at | Date d’importation | DateTime | Automatique | 2026-05-01 |
| user_id | Utilisateur propriétaire | Entier | Clé étrangère vers Users | 3 |
| folder_id | Dossier associé | Entier | Clé étrangère vers Folder, optionnel | 2 |

## 4. Deck

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant du deck | Entier | Clé primaire | 1 |
| title | Titre du deck | Texte | Non nul | Flashcards - Réseaux |
| description | Description du deck | Texte | Optionnel | Révision TCP/IP |
| created_at | Date de création | DateTime | Automatique | 2026-05-01 |
| user_id | Propriétaire du deck | Entier | Clé étrangère vers Users | 2 |
| course_pdf_id | PDF associé | Entier | Clé étrangère vers CoursePDF | 1 |

## 5. Flashcard

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant de la flashcard | Entier | Clé primaire | 1 |
| question | Question de la carte | Texte | Non nul | Qu’est-ce que TCP ? |
| answer | Réponse de la carte | Texte | Non nul | Un protocole de transport fiable |
| difficulty | Difficulté | Texte | easy / medium / hard | medium |
| created_at | Date de création | DateTime | Automatique | 2026-05-01 |
| deck_id | Deck associé | Entier | Clé étrangère vers Deck | 2 |

## 6. Quiz

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant du quiz | Entier | Clé primaire | 1 |
| title | Titre du quiz | Texte | Non nul | Quiz Réseaux |
| subject | Matière du quiz | Texte | Optionnel | Réseaux |
| created_at | Date de création | DateTime | Automatique | 2026-05-01 |
| deck_id | Deck associé | Entier | Clé étrangère vers Deck | 2 |

## 7. QuizQuestion

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant de la question | Entier | Clé primaire | 1 |
| question | Énoncé de la question | Texte | Non nul | Quel protocole utilise le port 80 ? |
| correct_answer | Bonne réponse | Texte | Non nul | HTTP |
| choices | Liste des choix proposés | Texte/JSON | Optionnel | ["HTTP","FTP","SMTP"] |
| quiz_id | Quiz associé | Entier | Clé étrangère vers Quiz | 1 |

## 8. QuizResult

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant du résultat du quiz | Entier | Clé primaire | 1 |
| score | Score obtenu | Entier | Non nul | 80 |
| correct_answers | Nombre de bonnes réponses | Entier | Non nul | 8 |
| passed_at | Date de passage | DateTime | Automatique | 2026-05-01 |
| user_id | Utilisateur associé | Entier | Clé étrangère vers Users | 1 |
| quiz_id | Quiz associé | Entier | Clé étrangère vers Quiz | 1 |

## 9. Availability

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant de disponibilité | Entier | Clé primaire | 1 |
| day | Jour disponible | Texte | Non nul | lundi |
| start_time | Heure de début | Heure | Non nul | 18:00 |
| end_time | Heure de fin | Heure | Non nul | 20:00 |
| user_id | Utilisateur associé | Entier | Clé étrangère vers Users | 1 |

## 10. RevisionPlan

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant du plan de révision | Entier | Clé primaire | 1 |
| title | Titre du planning de révision | Texte | Non nul | Planning examens |
| description | Description du planning | Texte | Optionnel | Révisions avant partiels |
| created_at | Date de création | DateTime | Automatique | 2026-05-01 |
| user_id | Utilisateur associé | Entier | Clé étrangère vers Users | 2 |

## 11. RevisionSession

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant de la session de révision | Entier | Clé primaire | 1 |
| revision_date | Date de la session | Date | Non nul | 2026-05-01 |
| start_time | Heure de début | Heure | Non nul | 18:00 |
| end_time | Heure de fin | Heure | Non nul | 20:00 |
| status | Statut de la session | Texte | planned / completed / cancelled | planned |
| revision_plan_id | Planning de révision associé | Entier | Clé étrangère vers RevisionPlan | 2 |
| deck_id | Deck associé | Entier | Clé étrangère vers Deck | 2 |

## 12. Todo

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant de la tâche | Entier | Clé primaire | 1 |
| title | Titre de la tâche | Texte | Non nul | Réviser chapitre 1 |
| description | Description de la tâche | Texte | Optionnel | Réviser les protocoles TCP/IP |
| due_date | Date limite | Date | Optionnel | 2026-05-10 |
| status | Statut de la tâche | Texte | todo / in_progress / done | todo |
| priority | Priorité de la tâche | Texte | low / medium / high | high |
| user_id | Utilisateur associé | Entier | Clé étrangère vers Users | 1 |
| revision_session_id | Session de révision associée | Entier | Clé étrangère vers RevisionSession, optionnel | 3 |

## 13. ForumPost

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant de la publication | Entier | Clé primaire | 1 |
| title | Titre de la publication | Texte | Non nul | Question sur TCP |
| content | Contenu de la publication | Texte | Non nul | Je n’ai pas compris la différence entre TCP et UDP |
| created_at | Date de publication | DateTime | Automatique | 2026-05-01 |
| user_id | Auteur de la publication | Entier | Clé étrangère vers Users | 1 |

## 14. ForumComment

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant du commentaire | Entier | Clé primaire | 1 |
| content | Contenu du commentaire | Texte | Non nul | TCP est fiable contrairement à UDP |
| created_at | Date de commentaire | DateTime | Automatique | 2026-05-01 |
| user_id | Auteur du commentaire | Entier | Clé étrangère vers Users | 2 |
| post_id | Publication associée | Entier | Clé étrangère vers ForumPost | 1 |

## 15. AIConversation

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant de la conversation IA | Entier | Clé primaire | 1 |
| title | Titre de la conversation | Texte | Non nul | Discussion sur les réseaux |
| scope | Portée de la recherche IA | Texte | global / course_pdf | course |
| created_at | Date de création | DateTime | Automatique | 2026-05-01 |
| user_id | Utilisateur associé | Entier | Clé étrangère vers Users | 1 |
| course_pdf_id | Cours ciblé par la conversation | Entier | Clé étrangère vers CoursePDF, optionnel | 3 |

## 16. AIMessage

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant du message IA | Entier | Clé primaire | 1 |
| role | Type d’émetteur du message | Texte | user / assistant | assistant |
| content | Contenu du message | Texte | Non nul | Explique-moi TCP |
| created_at | Date du message | DateTime | Automatique | 2026-05-01 |
| conversation_id | Conversation associée | Entier | Clé étrangère vers AIConversation | 1 |