import { useEffect, useMemo, useRef, useState } from "react";
import flashcard from "/src/assets/flashcard.png";
import { getDecks, uploadCoursePDF, generateFlashcardsFromCourse } from "../../services/api";
import {
  ChevronLeft,
  ChevronRight,
  Plus,
  RotateCcw,
  Sparkles,
  Layers,
  Search,
  Shuffle,
  UploadCloud,
  Trash2,
} from "lucide-react";

const initialDecks = []

function Flashcards() {
  const fileInputRef = useRef(null);
  const [mode, setMode] = useState("study");
  const [decks, setDecks] = useState(initialDecks);
  const [deckId, setDeckId] = useState(null);
  const [search, setSearch] = useState("");
  const [idx, setIdx] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [progress, setProgress] = useState({ hard: 0, good: 0, easy: 0 });
  const [shuffledCards, setShuffledCards] = useState([]);

  

  useEffect(() => {
    async function loadDecks() {
      try {
        const data = await getDecks();

        if (Array.isArray(data) && data.length > 0) {
  setDecks(data);
  setDeckId(data[0].id);
} else {
  setDecks([]);
  setDeckId(null);
}
      } catch (error) {
        console.error("Erreur lors du chargement des flashcards :", error);
        setDecks([]);
  setDeckId(null);
      }
    }

    loadDecks();
  }, []);

  const filteredDecks = useMemo(
    () =>
      decks.filter((deck) =>
        deck.title.toLowerCase().includes(search.toLowerCase())
      ),
    [decks, search]
  );

  const deck = decks.find((d) => d.id === deckId);
  const activeCards =
  shuffledCards.length > 0 ? shuffledCards : deck?.cards || [];

  const card = activeCards[idx];
  const total = activeCards.length || 0;
  const finished = idx >= total;


  useEffect(() => {
    setIdx(0);
    setFlipped(false);
    setProgress({ hard: 0, good: 0, easy: 0 });
    setShuffledCards([]);
  }, [deckId]);

   if (!deck) {
  return (
    <div className="p-8 max-w-[1500px] mx-auto text-[#1E293B]">

      <input
        ref={fileInputRef}
        type="file"
        accept="application/pdf"
        hidden
        onChange={(e) => handlePdf(e.target.files)}
      />

      <header className="flex items-end justify-between gap-5 mb-8">
        <div>
          <p className="text-xs font-extrabold uppercase tracking-wider text-[#8B6CF6]">
            Mémorisation espacée
          </p>
          <h1 className="text-5xl font-extrabold tracking-tight mt-1">
            Flashcards
          </h1>
          <p className="text-slate-500 mt-2">
            Aucun deck pour le moment. Génère tes premières flashcards depuis un PDF.
          </p>
        </div>
      </header>

      <PdfGenerator onClick={() => window.location.href = "/courses"} />
    </div>
  );
}
  const restart = () => {
    setIdx(0);
    setFlipped(false);
    setProgress({ hard: 0, good: 0, easy: 0 });
  };

  const shuffleCards = () => {
  const shuffled = [...deck.cards].sort(() => Math.random() - 0.5);

  setShuffledCards(shuffled);
  setIdx(0);
  setFlipped(false);
};

  const handleRate = (kind) => {
    setProgress((prev) => ({ ...prev, [kind]: prev[kind] + 1 }));
    setFlipped(false);
    setTimeout(() => setIdx((i) => i + 1), 200);
  };

  const handlePdf = async (files) => {
    const pdf = Array.from(files || []).find((file) =>
      file.name.toLowerCase().endsWith(".pdf")
    );

    if (!pdf) return alert("Choisis un fichier PDF.");

    try {
      const savedCourse = await uploadCoursePDF(pdf);

      await generateFlashcardsFromCourse(savedCourse.id);

      const data = await getDecks();

      setDecks(data);
      setDeckId(data[0].id);
      setMode("study");

      if (fileInputRef.current) fileInputRef.current.value = "";
    } catch (error) {
      console.error(error);
      alert("Erreur pendant la génération des flashcards.");
    }
  };


  return (
    <div className="p-8 max-w-[1500px] mx-auto text-[#1E293B]">
      <input
        ref={fileInputRef}
        type="file"
        accept="application/pdf"
        hidden
        onChange={(e) => handlePdf(e.target.files)}
      />

      <header className="flex items-end justify-between gap-5 mb-8">
        <div>
          <p className="text-xs font-extrabold uppercase tracking-wider text-[#8B6CF6]">
            Mémorisation espacée
          </p>
          <h1 className="text-5xl font-extrabold tracking-tight mt-1">
            Flashcards
          </h1>
          <p className="text-slate-500 mt-2">
            Concentre-toi ! Memi t’accompagne.
          </p>
        </div>

        <button
          onClick={() => setMode("pdf")}
          className="h-12 px-5 rounded-2xl bg-[#8B6CF6] text-white font-bold flex items-center gap-2 shadow-lg hover:bg-[#7C3AED]"
        >
          <Plus size={20} />
          Nouvelles flashcards
        </button>
      </header>

      <div className="inline-flex bg-white border border-slate-100 rounded-3xl p-2 shadow-sm mb-7">
        <button
          onClick={() => setMode("study")}
          className={`px-6 py-3 rounded-2xl font-bold ${mode === "study" ? "bg-[#8B6CF6] text-white" : "text-[#1E293B]"
            }`}
        >
          🃏 Mes flashcards
        </button>

        <button
          onClick={() => setMode("pdf")}
          className={`px-6 py-3 rounded-2xl font-bold ${mode === "pdf" ? "bg-[#8B6CF6] text-white" : "text-[#1E293B]"
            }`}
        >
          📄 Générer depuis PDF
        </button>
      </div>

      {mode === "pdf" ? (
  <PdfGenerator onClick={() => window.location.href = "/courses"} />
) : (
        <div className="grid lg:grid-cols-[360px_1fr] gap-7">
          <aside>
            <div className="relative mb-4">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Rechercher des flashcard..."
                className="w-full h-12 rounded-2xl border border-slate-200 bg-white pl-12 pr-4 outline-none focus:ring-2 focus:ring-[#8B6CF6]/40"
              />
            </div>

            <div className="bg-white rounded-3xl border border-slate-100 p-3">
              {filteredDecks.map((d) => (
                <div
  key={d.id}
  onClick={() => setDeckId(d.id)}
  className={`relative w-full text-left p-4 rounded-2xl flex gap-4 transition cursor-pointer ${d.id === deckId ? "bg-[#8B6CF6]/10" : "hover:bg-slate-50"
    }`}
>
                  <div
                    className="w-12 h-12 rounded-2xl text-white flex items-center justify-center"
                    style={{ background: d.color }}
                  >
                    <Layers />
                  </div>

<button
  onClick={async (e) => {
    e.stopPropagation();

    try {
      const token = localStorage.getItem("token");

await fetch(
  `http://127.0.0.1:8000/api/courses/flashcards/delete/${d.id}/`,
  {
    method: "DELETE",
    headers: {
      Authorization: `Token ${token}`,
    },
  }
);

      const updatedDecks = decks.filter((deck) => deck.id !== d.id);

      setDecks(updatedDecks);

      if (updatedDecks.length > 0) {
        setDeckId(updatedDecks[0].id);
      }

    } catch (error) {
      console.error(error);
    }
  }}
  className="absolute top-4 right-4 text-red-400 hover:text-red-600 transition"
>
  <Trash2 size={18} />
</button>

                  <div>
                    <h3
                      className={`font-extrabold ${d.id === deckId ? "text-[#8B6CF6]" : ""
                        }`}
                    >
                      {d.title}
                    </h3>
                    <p className="text-sm text-slate-400">
                      {d.subject} · {d.cards.length} cartes
                    </p>

                    <div className="flex gap-2 mt-2">
                      <span className="text-xs bg-emerald-50 text-emerald-600 px-2 py-1 rounded-full font-bold">
                        {d.mastered} maîtrisées
                      </span>
                      <span className="text-xs bg-amber-50 text-amber-600 px-2 py-1 rounded-full font-bold">
                        {d.due} à revoir
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </aside>


          <section>
            <div className="bg-white rounded-3xl border border-slate-100 p-5 mb-5">
              <div className="flex justify-between items-center">
                <h2 className="font-extrabold">{deck.title}</h2>
                <div className="flex items-center gap-4 text-sm text-slate-400 font-bold">
                  <button onClick={restart} className="hover:text-[#8B6CF6]">
                    Recommencer
                  </button>
                  <button
  onClick={shuffleCards}
  className="hover:text-[#8B6CF6] flex items-center gap-1"
>
                    <Shuffle size={16} /> Mélanger
                  </button>
                  <span>{Math.min(idx + 1, total)} / {total}</span>
                  
                </div>
              </div>

              <div className="h-2 bg-slate-100 rounded-full mt-4 overflow-hidden">
                <div
                  className="h-full rounded-full"
                  style={{
                    width: `${Math.min((idx / total) * 100, 100)}%`,
                    background: deck.color,
                  }}
                />
              </div>
            </div>

            {!finished ? (
              <>
                <div
                  onClick={() => setFlipped(!flipped)}
                  className="h-[420px] cursor-pointer [perspective:1200px]"
                >
                  <div
                    className={`relative h-full w-full transition-transform duration-700 ease-out [transform-style:preserve-3d] ${flipped ? "[transform:rotateY(180deg)]" : ""
                      }`}
                  >
                    {/* QUESTION */}
                    <div
                      className="absolute inset-0 rounded-[34px] border border-slate-100 shadow-xl flex flex-col items-center justify-center text-center p-10 overflow-hidden [backface-visibility:hidden]"
                      style={{
                        background: `linear-gradient(135deg, ${deck.color}18, #ffffff 55%, ${deck.color}10)`,
                      }}
                    >
                      <div
                        className="absolute -top-24 -left-24 w-72 h-72 rounded-full blur-3xl opacity-30"
                        style={{ background: deck.color }}
                      />

                      <p className="relative uppercase text-sm font-extrabold text-slate-400">
                        Question
                      </p>

                      <h2 className="relative mt-6 text-2xl md:text-3xl font-extrabold text-[#1E293B] leading-snug max-w-3xl">
                        {card.front}
                      </h2>

                      <p className="relative mt-8 text-slate-400">
                        Clique pour révéler la réponse
                      </p>
                    </div>

                    {/* RÉPONSE */}
                    <div
                      className="absolute inset-0 rounded-[34px] shadow-xl flex flex-col items-center justify-center text-center p-10 overflow-hidden text-white [backface-visibility:hidden] [transform:rotateY(180deg)]"
                      style={{
                        background: `linear-gradient(135deg, ${deck.color}, #A78BFA)`,
                      }}
                    >
                      <div className="absolute -top-24 -right-24 w-72 h-72 rounded-full bg-white/20 blur-3xl" />

                      <p className="relative uppercase text-sm font-extrabold text-white/80">
                        Réponse
                      </p>

                      <div className="relative mt-6 max-h-[250px] overflow-y-auto px-4">
                        <h2 className="text-xl md:text-2xl font-bold leading-relaxed">
                          {card.back}
                        </h2>
                      </div>

                      <p className="relative mt-8 text-white/80">
                        Clique pour revoir la question
                      </p>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4 mt-6">
                  <RateButton
                    onClick={() => handleRate("hard")}
                    label="Difficile"
                    hint="Je l’ai oubliée"
                    color="#EF4444"
                    bg="bg-red-50"
                  />
                  <RateButton
                    onClick={() => handleRate("good")}
                    label="Bien"
                    hint="Avec un effort"
                    color="#3B82F6"
                    bg="bg-blue-50"
                  />
                  <RateButton
                    onClick={() => handleRate("easy")}
                    label="Facile"
                    hint="Sans hésiter"
                    color="#10B981"
                    bg="bg-emerald-50"
                  />
                </div>

                <div className="flex justify-between mt-5 text-slate-400 font-semibold">
                  <button onClick={() => setIdx((i) => Math.max(0, i - 1))}>
                    <ChevronLeft size={16} className="inline" /> Précédente
                  </button>

                  <button
                    onClick={() => setIdx((i) => Math.min(total - 1, i + 1))}
                  >
                    Suivante <ChevronRight size={16} className="inline" />
                  </button>
                </div>
              </>
            ) : (
              <div className="bg-white rounded-3xl border border-slate-100 p-12 text-center">
                <h2 className="text-3xl font-extrabold">Bravo, flashcards terminé 🎉</h2>
                <p className="text-slate-500 mt-2">
                  Difficile : {progress.hard} · Bien : {progress.good} · Facile :{" "}
                  {progress.easy}
                </p>
                <button
                  onClick={restart}
                  className="mt-6 bg-[#1E293B] text-white px-6 py-3 rounded-2xl font-bold"
                >
                  Recommencer
                </button>
              </div>
            )}
          </section>
        </div>
      )}
    </div>
  );
}

function PdfGenerator({ onClick }) {
  return (
    <div>
      <section className="rounded-[34px] bg-gradient-to-br from-[#8B6CF6] to-[#C084FC] text-white p-8 mb-7 relative overflow-hidden">
        <p className="font-bold flex items-center gap-2">
          <Sparkles size={18} /> IA Memi
        </p>
        <h2 className="text-3xl font-extrabold mt-3">
          Génère tes flashcards depuis un PDF
        </h2>
        <p className="text-white/80 mt-2">
          Upload ton cours et Memi crée des cartes automatiquement.
        </p>
        <img
          src={flashcard}
          alt="Flashcard mascot"
          className="absolute right-10 top-8 w-28 h-28 object-contain drop-shadow-xl hover:scale-110 transition duration-300"
        />
      </section>

      <section
        onClick={onClick}
        className="h-[260px] rounded-[34px] border-2 border-dashed border-[#8B6CF6]/30 bg-white/60 flex flex-col items-center justify-center cursor-pointer"
      >
        <UploadCloud size={42} className="text-[#8B6CF6]" />
        <h3 className="font-extrabold text-xl mt-4">
          Clique pour uploader ton PDF
        </h3>
        <p className="text-slate-400 mt-1">
          Memi générera les flashcards automatiquement.
        </p>
      </section>
    </div>
  );
}

function RateButton({ onClick, label, hint, color, bg }) {
  return (
    <button
      onClick={onClick}
      className={`${bg} rounded-2xl p-5 text-left hover:-translate-y-0.5 transition`}
      style={{ color }}
    >
      <div className="font-extrabold text-xl">{label}</div>
      <div className="text-sm mt-1 opacity-80">{hint}</div>
    </button>
  );
}

export default Flashcards;