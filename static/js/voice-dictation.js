document.addEventListener("DOMContentLoaded", () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        document.querySelectorAll(".voice-dictation-btn").forEach((btn) => {
            btn.disabled = true;
            btn.classList.add("opacity-30", "cursor-not-allowed");
            btn.title = "Dictée vocale non supportée par ce navigateur";
        });
        return;
    }

    let recognition = null;
    let activeButton = null;
    let activeTextarea = null;

    const stopListening = () => {
        if (recognition) recognition.stop();
    };

    const setListeningStyle = (btn, listening) => {
        btn.classList.toggle("bg-red-500", listening);
        btn.classList.toggle("text-white", listening);
        btn.classList.toggle("bg-slate-100", !listening);
        btn.classList.toggle("text-slate-500", !listening);
        btn.classList.toggle("animate-pulse", listening);
    };

    document.addEventListener("click", (evt) => {
        const btn = evt.target.closest(".voice-dictation-btn");
        if (!btn) return;
        evt.preventDefault();

        const textarea = document.getElementById(btn.dataset.target);
        if (!textarea) return;

        if (activeButton === btn) {
            stopListening();
            return;
        }

        if (activeButton) {
            stopListening();
        }

        recognition = new SpeechRecognition();
        recognition.lang = "fr-FR";
        recognition.interimResults = false;
        recognition.continuous = false;

        activeButton = btn;
        activeTextarea = textarea;
        setListeningStyle(btn, true);

        recognition.addEventListener("result", (event) => {
            const transcript = Array.from(event.results)
                .map((result) => result[0].transcript)
                .join(" ")
                .trim();
            if (!transcript) return;
            const separator = activeTextarea.value && !activeTextarea.value.endsWith(" ") ? " " : "";
            activeTextarea.value += separator + transcript;
        });

        recognition.addEventListener("end", () => {
            setListeningStyle(btn, false);
            activeButton = null;
            activeTextarea = null;
        });

        recognition.addEventListener("error", () => {
            setListeningStyle(btn, false);
            activeButton = null;
            activeTextarea = null;
        });

        recognition.start();
    });
});
