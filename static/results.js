const resultsContent = document.querySelector("#results-content");
const missingResults = document.querySelector("#missing-results");
const feedbackForm = document.querySelector("#feedback-form");
const feedbackMessage = document.querySelector("#feedback-message");
const feedbackDomain = document.querySelector("#feedback-domain");
const storedResult = sessionStorage.getItem("techpathResults");

if (!storedResult) {
    missingResults.hidden = false;
} else {
    const result = JSON.parse(storedResult);
    const [top, ...alternatives] = result.recommendations;
    feedbackDomain.value = top.name;

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

if (feedbackForm) {
    feedbackForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const submitButton = feedbackForm.querySelector("button[type='submit']");
        const formData = new FormData(feedbackForm);
        const payload = {
            recommended_domain: formData.get("recommended_domain"),
            recommendation_relevance: formData.get("recommendation_relevance"),
            interest_level: formData.get("interest_level"),
            satisfaction_rating: Number(formData.get("satisfaction_rating")),
            user_comment: formData.get("user_comment") || "",
        };

        submitButton.disabled = true;
        feedbackMessage.textContent = "Submitting...";
        feedbackMessage.classList.remove("error");

        try {
            const response = await fetch("/api/feedback", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload),
            });
            if (!response.ok) throw new Error("Feedback could not be saved. Please try again.");
            feedbackForm.reset();
            feedbackDomain.value = payload.recommended_domain;
            feedbackMessage.textContent = "Thank you. Your feedback was submitted successfully.";
        } catch (error) {
            feedbackMessage.textContent = error.message;
            feedbackMessage.classList.add("error");
        } finally {
            submitButton.disabled = false;
        }
    });
}
