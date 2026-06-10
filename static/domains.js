const searchInput = document.querySelector("#domain-search");
const cards = [...document.querySelectorAll(".domain-card")];
const filters = [...document.querySelectorAll(".filter-chip")];
const emptyState = document.querySelector("#empty-state");
let activeFilter = "all";

function updateDomains() {
    const query = searchInput ? searchInput.value.trim().toLowerCase() : "";
    let visibleCount = 0;

    cards.forEach((card) => {
        const category = (card.dataset.category || "").trim().toLowerCase();
        const searchableText = (card.dataset.search || "").toLowerCase();
        const categoryMatches = activeFilter === "all" || category === activeFilter;
        const searchMatches = !query || searchableText.includes(query);
        const visible = categoryMatches && searchMatches;
        card.hidden = !visible;
        if (visible) visibleCount += 1;
    });

    if (emptyState) emptyState.hidden = visibleCount !== 0;
}

filters.forEach((filter) => {
    filter.addEventListener("click", () => {
        filters.forEach((item) => {
            item.classList.remove("active");
            item.setAttribute("aria-pressed", "false");
        });
        filter.classList.add("active");
        filter.setAttribute("aria-pressed", "true");
        activeFilter = (filter.dataset.filter || "all").toLowerCase();
        updateDomains();
    });
});

if (searchInput) searchInput.addEventListener("input", updateDomains);
updateDomains();
