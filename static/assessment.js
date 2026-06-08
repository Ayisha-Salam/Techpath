const intro = document.querySelector("#assessment-intro");
const quizCard = document.querySelector("#quiz-card");
const beginButton = document.querySelector("#begin-assessment");
const questionText = document.querySelector("#question-text");
const questionCount = document.querySelector("#question-count");
const progressPercent = document.querySelector("#progress-percent");
const progressBar = document.querySelector("#progress-bar");
const ratingButtons = [...document.querySelectorAll("#rating-grid button")];
const previousButton = document.querySelector("#previous-question");
const nextButton = document.querySelector("#next-question");
const message = document.querySelector("#quiz-message");

let questions = [];
let answers = [];
let currentIndex = 0;
let questionSetId = null;

async function loadQuestions() {
    const previousSetId = localStorage.getItem("techpathLastQuestionSetId");
    const query = previousSetId ? `?exclude_set_id=${encodeURIComponent(previousSetId)}` : "";
    const response = await fetch(`/api/questions${query}`);
    if (!response.ok) throw new Error("Could not load the assessment.");
    const data = await response.json();
    questionSetId = data.question_set_id;
    localStorage.setItem("techpathLastQuestionSetId", questionSetId);
    questions = data.questions;
    answers = new Array(questions.length).fill(null);
}

function renderQuestion() {
    const question = questions[currentIndex];
    const progress = Math.round(((currentIndex + 1) / questions.length) * 100);

    questionText.textContent = question.text;
    questionCount.textContent = `Question ${currentIndex + 1} of ${questions.length}`;
    progressPercent.textContent = `${progress}% complete`;
    progressBar.style.width = `${progress}%`;
    previousButton.disabled = currentIndex === 0;
    nextButton.textContent = currentIndex === questions.length - 1 ? "See my results ->" : "Next question ->";
    message.textContent = "";

    ratingButtons.forEach((button) => {
        const selected = Number(button.dataset.value) === answers[currentIndex];
        button.classList.toggle("selected", selected);
        button.setAttribute("aria-checked", String(selected));
    });
}

async function submitAssessment() {
    nextButton.disabled = true;
    nextButton.textContent = "Calculating...";
    message.textContent = "";

    try {
        const response = await fetch("/api/assessment", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({answers, question_set_id: questionSetId}),
        });
        if (!response.ok) throw new Error("Your results could not be calculated.");
        const result = await response.json();
        sessionStorage.setItem("techpathResults", JSON.stringify(result));
        window.location.href = "/results";
    } catch (error) {
        message.textContent = error.message;
        nextButton.disabled = false;
        nextButton.textContent = "Try again";
    }
}

beginButton.addEventListener("click", async () => {
    beginButton.disabled = true;
    beginButton.textContent = "Preparing...";
    try {
        await loadQuestions();
        intro.hidden = true;
        quizCard.hidden = false;
        renderQuestion();
    } catch (error) {
        beginButton.disabled = false;
        beginButton.textContent = "Begin assessment ->";
        intro.querySelector(".privacy-note").textContent = error.message;
    }
});

ratingButtons.forEach((button) => {
    button.addEventListener("click", () => {
        answers[currentIndex] = Number(button.dataset.value);
        renderQuestion();
    });
});

previousButton.addEventListener("click", () => {
    if (currentIndex > 0) {
        currentIndex -= 1;
        renderQuestion();
    }
});

nextButton.addEventListener("click", () => {
    if (answers[currentIndex] === null) {
        message.textContent = "Choose one response before continuing.";
        return;
    }
    if (currentIndex === questions.length - 1) {
        submitAssessment();
        return;
    }
    currentIndex += 1;
    renderQuestion();
});
