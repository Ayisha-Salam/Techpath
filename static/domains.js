const searchInput = document.querySelector("#domain-search");
const cards = [...document.querySelectorAll(".domain-card")];
const filters = [...document.querySelectorAll(".filter-chip")];
const emptyState = document.querySelector("#empty-state");
let activeFilter = "all";

function updateDomains() {
    const query = searchInput.value.trim().toLowerCase();
    let visibleCount = 0;

    cards.forEach((card) => {
        const categoryMatches = activeFilter === "all" || card.dataset.category === activeFilter;
        const searchMatches = !query || card.dataset.search.includes(query);
        const visible = categoryMatches && searchMatches;
        card.hidden = !visible;
        if (visible) visibleCount += 1;
    });

    emptyState.hidden = visibleCount !== 0;
}

filters.forEach((filter) => {
    filter.addEventListener("click", () => {
        filters.forEach((item) => item.classList.remove("active"));
        filter.classList.add("active");
        activeFilter = filter.dataset.filter;
        updateDomains();
    });
});

searchInput.addEventListener("input", updateDomains);

