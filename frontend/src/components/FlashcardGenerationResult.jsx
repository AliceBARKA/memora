import { MemiGuide } from "./AnimatedMemi";

export function FlashcardGenerationResult({ result, className = "" }) {
  if (!result) return null;

  return (
    <MemiGuide
      mood={result.mood}
      eyebrow="Résultat de la génération"
      title={result.title}
      message={result.message}
      compact
      className={className}
    />
  );
}
