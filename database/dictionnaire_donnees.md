# Dictionnaire des données — Memora

## 1.CoursePDF

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant du cours PDF | Entier | Clé primaire | 1 |
| title | Titre du cours | Texte | Non nul | Réseaux |
| file | Fichier PDF du cours | Fichier/Texte | Non nul | reseaux.pdf |
| uploaded_at | Date d’importation | DateTime | Automatique | 2026-05-01 |
| user_id | Utilisateur propriétaire | Entier | Clé étrangère vers User | 3 |

## 2.Deck
| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant du cours PDF | Entier | Clé primaire | 1 |
| title | Titre du cours | Texte | Non nul | Réseaux |
| description | Description du deck | Texte | Optionnel | Révision TCP/IP |
| created_at | Date de création | DateTime | Automatique | 2026-05-01 |
| user_id | Propriétaire du deck | Entier | Clé étrangère vers User | 2 |
| course_pdf_id | PDF associé | Entier | Clé étrangère vers CoursePDF | 1 |

## 3.Flashcard

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant flashcard | Entier | Clé primaire | 1 |
| question | Question de la carte | Texte | Non nul | Qu’est-ce TCP ? |
| answer | Réponse de la carte | Texte | Non nul | Protocole réseau |
| difficulty | Difficulté | Texte | easy/medium/hard | medium |
| created_at | Date création | DateTime | Automatique | 2026-05-01 |
| deck_id | Deck associé | Entier | Clé étrangère vers Deck | 2 |

## 4.Quiz

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant Quiz | Entier | Clé primaire | 1 |
| title | titre du quiz | Texte | Non nul | quiz d'histoire |
| created_at | Date création | DateTime | Automatique | 2026-05-01 |
| deck_id | Deck associé | Entier | Clé étrangère vers Deck | 2 |

## 5.QuizResult

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant du résultat du quiz | Entier | Clé primaire | 1 |
| score | Score du quiz | Entier | Non nul | 50 |
| correct_answers | Nombre de bonnes réponses | Entier | Non nul | 8 |
| passed_at | Date de passage | DateTime | Automatique | 2026-05-01 |
| user_id | Utilisateur associé | Entier | Clé étrangère vers User | 1 |
| quiz_id | Quiz associé | Entier | Clé étrangère vers Quiz | 1 |

## 6.Availability

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant de disponibilité | Entier | Clé primaire | 1 |
|  day | jour disponible | Texte | Non nul | lundi |
| start_time | Heure de début | Heure | Non nul | 18:00 |
| end_time | Heure de fin | Heure | Non nul | 20:00 |
| user_id | Utilisateur assoscié | Entier | Clé étrangère vers User | 1 |

## 7.RevisionPlan

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|

| id | Identifiant du plan de revision | Entier | Clé primaire | 1 |
|  title | titre du planning de revision | Texte | Non nul | planning de revision |
| created_at | Date création | DateTime | Automatique | 2026-05-01 |
| user_id | user associé | Entier | Clé étrangère vers User | 2 |

## 8.RevisionSession

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|

| id | Identifiant de la session de revision | Entier | Clé primaire | 1 |
| date | Date création | DateTime | Automatique | 2026-05-01 |
| start_time | Heure de début | Heure | Non nul | 18:00 |
| end_time | Heure de fin | Heure | Non nul | 20:00 |
| status | Statut de la session | Texte | planned / done / cancelled | planned |
| revision_plan_id, | planning de revision associé | Entier | Clé étrangère RevisionPlan | 2 |
| deck_id | deck associé | Entier | Clé étrangère vers Deck | 2 |

## 9. Todo

| Nom | Signification | Type | Contraintes | Exemple |
|---|---|---|---|---|
| id | Identifiant de la tâche | Entier | Clé primaire | 1 |
| title | Titre de la tâche | Texte | Non nul | Réviser chapitre 1 |
| description | Description de la tâche | Texte | Optionnel | Réviser les protocoles TCP/IP |
| due_date | Date limite | Date | Optionnel | 2026-05-10 |
| status | Statut de la tâche | Texte | todo / in_progress / done | todo |
| priority | Priorité de la tâche | Texte | low / medium / high | high |
| user_id | Utilisateur associé | Entier | Clé étrangère vers User | 1 |
| revision_session_id | Session de révision associée | Entier | Clé étrangère vers RevisionSession | 3 |

