document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("signature-pad");
    const clearButton = document.getElementById("signature-clear");
    const hiddenInput = document.getElementById("signature");
    const form = canvas ? canvas.closest("form") : null;

    if (!canvas || !hiddenInput || !form) return;

    const ctx = canvas.getContext("2d");
    let drawing = false;
    let hasStroke = false;

    const resizeCanvas = () => {
        const ratio = window.devicePixelRatio || 1;
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * ratio;
        canvas.height = rect.height * ratio;
        ctx.scale(ratio, ratio);
        ctx.lineWidth = 2.5;
        ctx.lineCap = "round";
        ctx.strokeStyle = "#0f172a";
    };
    resizeCanvas();

    const pointFromEvent = (evt) => {
        const rect = canvas.getBoundingClientRect();
        const point = evt.touches ? evt.touches[0] : evt;
        return { x: point.clientX - rect.left, y: point.clientY - rect.top };
    };

    const start = (evt) => {
        evt.preventDefault();
        drawing = true;
        hasStroke = true;
        const { x, y } = pointFromEvent(evt);
        ctx.beginPath();
        ctx.moveTo(x, y);
    };

    const move = (evt) => {
        if (!drawing) return;
        evt.preventDefault();
        const { x, y } = pointFromEvent(evt);
        ctx.lineTo(x, y);
        ctx.stroke();
    };

    const stop = () => {
        drawing = false;
    };

    canvas.addEventListener("mousedown", start);
    canvas.addEventListener("mousemove", move);
    window.addEventListener("mouseup", stop);

    canvas.addEventListener("touchstart", start, { passive: false });
    canvas.addEventListener("touchmove", move, { passive: false });
    canvas.addEventListener("touchend", stop);

    clearButton.addEventListener("click", () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        hasStroke = false;
        hiddenInput.value = "";
    });

    form.addEventListener("submit", (evt) => {
        if (!hasStroke) {
            evt.preventDefault();
            alert("Merci de signer avant de valider l'audit.");
            return;
        }
        hiddenInput.value = canvas.toDataURL("image/png");
    });
});
