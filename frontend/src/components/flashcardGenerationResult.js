export function buildFlashcardGenerationResult(result = {}) {
  const generatedCount = Number(result.generated_count ?? result.cards_count ?? 0);
  const requestedCount = Number(result.requested_count ?? generatedCount);

  if (generatedCount === 0) {
    return {
      mood: "encouraging",
      title: "Je n'ai pas trouvé assez de contenu 😔",
      message: "Essaie avec un document plus complet ou modifie les options de génération.",
    };
  }

  if (generatedCount < requestedCount) {
    return {
      mood: "thinking",
      title: "J'ai trouvé moins d'informations que prévu 🤔",
      message: `Ton document ne contenait pas assez de contenu exploitable pour créer ${requestedCount} flashcards. J'en ai généré ${generatedCount} avec les informations disponibles.`,
    };
  }

  return {
    mood: "celebrating",
    title: "C'est prêt ! 🎉",
    message: `J'ai créé ${generatedCount} flashcards à partir de ton document. Bonne révision !`,
  };
}
