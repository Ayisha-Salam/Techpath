const resultsContent = document.querySelector("#results-content");
const missingResults = document.querySelector("#missing-results");
const storedResult = sessionStorage.getItem("techpathResults");

if (!storedResult) {
    missingResults.hidden = false;
} else {
    const result = JSON.parse(storedResult);
    const [top, ...alternatives] = result.recommendations;

    document.querySelector("#top-result").innerHTML = `
        <span class="domain-symbol">${top.name.split(" ").slice(0, 2).map((word) => word[0]).join("")}</span>
        <div>
            <span class="result-kicker">Your strongest match</span>
            <h2>${top.name}</h2>
            <p>${top.summary}</p>
            <a class="button button-light" href="/roadmap/${top.slug}">Open my roadmap →</a>
        </div>
        <div class="score-ring"><strong>${Math.round(top.score)}%</strong></div>
    `;

    document.querySelector("#recommendation-list").innerHTML = alternatives.map((domain, index) => `
        <div class="recommendation-row">
            <span class="rank-number">${index + 2}</span>
            <div><strong>${domain.name}</strong><small>${Math.round(domain.score)}% profile match</small></div>
            <a href="/roadmap/${domain.slug}">Roadmap →</a>
        </div>
    `).join("");

    document.querySelector("#trait-list").innerHTML = result.top_traits.map((trait) => `
        <div class="trait-item">
            <div class="trait-label"><span>${trait.name}</span><span>${Math.round(trait.score)}%</span></div>
            <div class="trait-meter"><span style="width: ${trait.score}%"></span></div>
        </div>
    `).join("");

    resultsContent.hidden = false;
}

