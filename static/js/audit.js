document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("composants-container");
    const addButton = document.getElementById("add-composant");
    const template = document.getElementById("composant-template");

    if (!container || !addButton || !template) return;

    const renumber = () => {
        container.querySelectorAll(".composant-row").forEach((row, i) => {
            const label = row.querySelector(".composant-label");
            if (label) label.textContent = `Composant #${i + 1}`;
        });
    };

    const bindRemove = (row) => {
        const removeBtn = row.querySelector(".remove-composant");
        removeBtn.addEventListener("click", () => {
            if (container.querySelectorAll(".composant-row").length <= 1) {
                return; // toujours garder au moins un composant
            }
            row.remove();
            renumber();
        });
    };

    container.querySelectorAll(".composant-row").forEach(bindRemove);

    let nextIndex = container.querySelectorAll(".composant-row").length;

    addButton.addEventListener("click", () => {
        const fragment = template.content.cloneNode(true);
        const html = fragment.querySelector(".composant-row").outerHTML.replaceAll(
            "__INDEX__",
            String(nextIndex)
        );

        const wrapper = document.createElement("div");
        wrapper.innerHTML = html.trim();
        const newRow = wrapper.firstElementChild;

        container.appendChild(newRow);
        bindRemove(newRow);
        renumber();
        nextIndex += 1;

        newRow.scrollIntoView({ behavior: "smooth", block: "center" });
    });
});
