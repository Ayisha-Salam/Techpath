import json
import random
from copy import deepcopy
from pathlib import Path
from urllib.parse import quote_plus
from uuid import uuid4


TRAIT_LABELS = {
    "AT": "Analytical thinking",
    "CR": "Creativity",
    "PS": "Problem solving",
    "CU": "Curiosity",
    "AD": "Attention to detail",
    "CO": "Communication",
    "LE": "Leadership",
    "TW": "Teamwork",
    "EM": "Empathy",
    "AP": "Adaptability",
    "RE": "Resilience",
    "SD": "Self-discipline",
    "OR": "Organization",
    "ST": "Strategic thinking",
    "RT": "Risk tolerance",
    "IN": "Innovation",
    "DM": "Decision making",
    "TA": "Technical aptitude",
    "BA": "Business awareness",
    "LA": "Learning agility",
}


QUESTIONS = [
    "I enjoy understanding how complex systems operate and finding ways to improve them.",
    "I enjoy solving difficult problems even when the solution is not immediately obvious.",
    "I often look for patterns and connections that others may miss.",
    "I enjoy experimenting with new ideas and approaches.",
    "I quickly adapt when plans or circumstances change unexpectedly.",
    "I prefer organizing my tasks before starting work.",
    "I enjoy helping people understand difficult concepts.",
    "I feel comfortable taking responsibility for important decisions.",
    "I enjoy learning technologies or skills that are completely new to me.",
    "I often think about how existing products or systems can be improved.",
    "I notice small errors and inconsistencies that others often overlook.",
    "I enjoy projects that require both technical and creative thinking.",
    "I usually consider long-term consequences before making decisions.",
    "I remain focused on important goals even when progress is slow.",
    "I enjoy collaborating with people who have different viewpoints.",
    "I enjoy understanding why people make certain choices.",
    "I enjoy troubleshooting technical issues until I find the root cause.",
    "I am comfortable making decisions when all information is not available.",
    "I enjoy taking initiative when working in a group.",
    "I enjoy exploring opportunities that involve uncertainty and calculated risk.",
    "I enjoy balancing technical requirements with practical or business needs.",
    "I actively seek feedback to improve my performance.",
    "I can stay productive when working under pressure.",
    "I often think of multiple possible solutions before choosing one.",
    "I enjoy understanding both the technical details and the bigger picture of a project.",
]

QUESTION_SETS = {
    "set-1": QUESTIONS,
    "set-2": [
        "I enjoy identifying weaknesses in a process and finding ways to strengthen it.",
        "I can remain focused on a task even when distractions are present.",
        "I enjoy learning how different technologies interact with each other.",
        "I am comfortable explaining my ideas to a group of people.",
        "I often consider multiple perspectives before forming an opinion.",
        "I enjoy solving puzzles, logic problems, or technical challenges.",
        "I take responsibility when mistakes occur and work to correct them.",
        "I enjoy working on projects that require both creativity and structure.",
        "I can quickly understand new tools, systems, or software.",
        "I prefer making decisions based on facts rather than assumptions.",
        "I enjoy collaborating with others to achieve shared goals.",
        "I remain productive even when deadlines are tight.",
        "I enjoy exploring ideas that could improve future products or services.",
        "I carefully verify information before acting on it.",
        "I am comfortable leading discussions when a team lacks direction.",
        "I enjoy understanding why systems fail and how to prevent future issues.",
        "I can adapt my communication style to different people and situations.",
        "I enjoy setting long-term goals and planning how to achieve them.",
        "I am willing to take calculated risks when potential rewards justify them.",
        "I enjoy analyzing data to uncover useful insights.",
        "I actively seek opportunities to improve professional skills.",
        "I enjoy balancing technical requirements with customer or business needs.",
        "I stay calm and make decisions effectively during unexpected situations.",
        "I often suggest new ideas that could improve team performance.",
        "I enjoy understanding both the details of a problem and its broader impact.",
    ],
    "set-3": [
        "I enjoy building relationships that help achieve long-term goals.",
        "I can evaluate multiple options and choose the best course of action.",
        "I enjoy documenting my work so others can easily understand it.",
        "I often think ahead and anticipate potential problems.",
        "I like automating or simplifying repetitive tasks.",
        "I enjoy exploring how data can be used to solve real-world problems.",
        "I can manage multiple tasks without compromising quality.",
        "I enjoy negotiating and finding win-win solutions.",
        "I enjoy reverse-engineering problems to understand their root cause.",
        "I am comfortable working in fast-paced environments.",
        "I enjoy designing systems or processes from scratch.",
        "I like keeping up with industry trends and emerging technologies.",
        "I pay attention to security and privacy in everything I do.",
        "I enjoy presenting ideas and influencing others.",
        "I can learn from failure and use it to improve.",
        "I enjoy thinking about how technology can solve societal challenges.",
        "I like testing things thoroughly to ensure they work as expected.",
        "I can explain complex ideas in simple terms.",
        "I enjoy collaborating across different teams or departments.",
        "I am proactive in identifying opportunities for improvement.",
        "I enjoy estimating risks and preparing contingency plans.",
        "I remain organized even when managing complex projects.",
        "I enjoy mentoring or coaching others.",
        "I enjoy learning by doing hands-on projects.",
        "I always look for ways to deliver more value to users or customers.",
    ],
    "set-4": [
        "I enjoy discovering patterns in large amounts of information.",
        "I can understand how different business processes connect with each other.",
        "I enjoy investigating unusual activities to find their source.",
        "I enjoy advising others on how technology can improve their work.",
        "I enjoy creating prompts that generate useful and creative AI outputs.",
        "I prefer making decisions based on evidence rather than assumptions.",
        "I enjoy understanding customer needs before proposing solutions.",
        "I am curious about how digital systems can be exploited or protected.",
        "I enjoy presenting technical ideas to non-technical audiences.",
        "I frequently experiment with new AI tools and technologies.",
        "I can quickly identify inefficiencies in a workflow or process.",
        "I enjoy coordinating different teams to achieve a common objective.",
        "I pay close attention to security, compliance, and data integrity.",
        "I enjoy evaluating multiple solution options before making recommendations.",
        "I enjoy refining prompts until AI responses become highly accurate.",
        "I enjoy transforming raw data into meaningful business insights.",
        "I can remain objective when analyzing sensitive information.",
        "I enjoy understanding how technology decisions affect business outcomes.",
        "I am comfortable learning new software platforms without much guidance.",
        "I enjoy investigating digital evidence to reconstruct events.",
        "I can balance innovation with practical business requirements.",
        "I enjoy helping organizations solve complex technology challenges.",
        "I actively seek opportunities to improve AI-generated results.",
        "I enjoy creating structured processes that improve efficiency.",
        "I enjoy combining analytical thinking with creativity to solve problems.",
    ],
    "set-5": [
        "I enjoy identifying assumptions that could cause a project to fail.",
        "I often combine ideas from unrelated areas to solve problems.",
        "I prefer understanding the purpose behind a rule before following it.",
        "I can remain productive when project requirements change frequently.",
        "I enjoy comparing long-term consequences before choosing an approach.",
        "I can recognize when a team is losing momentum and help restore focus.",
        "I frequently notice opportunities for improvement that others overlook.",
        "I enjoy converting broad goals into clear action plans.",
        "I look for recurring causes behind repeated mistakes or failures.",
        "I enjoy studying how successful organizations achieve consistent performance.",
        "I am willing to make difficult decisions when others hesitate.",
        "I enjoy identifying dependencies that could delay a project's success.",
        "I enjoy finding practical applications for newly emerging technologies.",
        "I naturally consider how decisions affect different stakeholders.",
        "I can maintain accuracy while processing large amounts of information.",
        "I enjoy identifying bottlenecks that slow down progress.",
        "I enjoy exploring alternative methods even when the current approach works adequately.",
        "I can determine which information is most important when facing information overload.",
        "I enjoy helping people reach agreement during disagreements.",
        "I am interested in understanding how small changes can create significant outcomes.",
        "I enjoy designing methods that make work easier for others.",
        "I can evaluate opportunities even when complete information is unavailable.",
        "I enjoy investigating how decisions made in one area affect results in another.",
        "I continue improving a solution even after it meets minimum requirements.",
        "I enjoy integrating technical knowledge with human needs to create effective solutions.",
    ],
}


QUESTION_TRAITS = [
    {"AT": 1.0, "PS": 0.7, "TA": 0.5},
    {"PS": 1.0, "RE": 0.6, "AT": 0.5},
    {"AT": 1.0, "CU": 0.6},
    {"CR": 1.0, "IN": 0.8, "RT": 0.3},
    {"AP": 1.0, "RE": 0.5},
    {"OR": 1.0, "SD": 0.7},
    {"CO": 1.0, "EM": 0.6},
    {"LE": 0.8, "DM": 1.0},
    {"LA": 1.0, "CU": 0.7, "TA": 0.4},
    {"IN": 1.0, "ST": 0.6, "CR": 0.4},
    {"AD": 1.0, "SD": 0.4},
    {"CR": 0.8, "TA": 0.7, "PS": 0.5},
    {"ST": 1.0, "DM": 0.5},
    {"SD": 0.8, "RE": 1.0},
    {"TW": 1.0, "CO": 0.5, "AP": 0.3},
    {"EM": 1.0, "BA": 0.3},
    {"PS": 0.9, "TA": 1.0, "AD": 0.5},
    {"DM": 0.8, "RT": 1.0, "AP": 0.3},
    {"LE": 1.0, "TW": 0.5},
    {"RT": 1.0, "IN": 0.5},
    {"BA": 1.0, "ST": 0.5, "TA": 0.4},
    {"LA": 0.8, "RE": 0.4, "CO": 0.3},
    {"RE": 1.0, "AP": 0.7, "SD": 0.4},
    {"CR": 0.8, "PS": 1.0, "DM": 0.4},
    {"ST": 0.8, "TA": 0.7, "BA": 0.7},
]

QUESTION_TRAIT_SETS = {set_id: QUESTION_TRAITS for set_id in QUESTION_SETS}
GENERATED_QUESTION_TRAIT_SETS = {}

QUESTIONS_PER_SECTION = 5
REQUIRED_TRAITS = set(TRAIT_LABELS)


def get_question_set(set_id: str):
    return QUESTION_SETS.get(set_id)


def get_question_traits(set_id: str):
    return QUESTION_TRAIT_SETS.get(set_id) or GENERATED_QUESTION_TRAIT_SETS.get(set_id)


def _section_entries():
    entries = []
    for section_index, set_id in enumerate(QUESTION_SETS):
        section_questions = QUESTION_SETS[set_id]
        section_traits = QUESTION_TRAIT_SETS[set_id]
        section = []
        for question_index, question in enumerate(section_questions):
            section.append(
                {
                    "id": (section_index * len(section_questions)) + question_index + 1,
                    "text": question,
                    "section": set_id,
                    "traits": section_traits[question_index],
                }
            )
        entries.append(section)
    return entries


def _covered_traits(selection: list[dict]) -> set[str]:
    return {trait for question in selection for trait in question["traits"]}


def _repair_trait_coverage(selection: list[dict], sections: list[list[dict]], rng: random.Random) -> list[dict]:
    selected_ids = {question["id"] for question in selection}

    # Start from a random 5-per-section sample, then make targeted same-section
    # swaps only for missing traits. This keeps most of the original random draw
    # intact while guaranteeing every trait can contribute to scoring.
    while True:
        missing_traits = REQUIRED_TRAITS - _covered_traits(selection)
        if not missing_traits:
            return selection

        best_swap = None
        best_missing_count = len(missing_traits)
        shuffled_missing = list(missing_traits)
        rng.shuffle(shuffled_missing)

        for missing_trait in shuffled_missing:
            candidates = [
                candidate
                for section in sections
                for candidate in section
                if candidate["id"] not in selected_ids and missing_trait in candidate["traits"]
            ]
            rng.shuffle(candidates)

            for candidate in candidates:
                same_section_selected = [
                    question for question in selection if question["section"] == candidate["section"]
                ]
                rng.shuffle(same_section_selected)

                for removable in same_section_selected:
                    trial = [
                        candidate if question["id"] == removable["id"] else question
                        for question in selection
                    ]
                    trial_missing_count = len(REQUIRED_TRAITS - _covered_traits(trial))
                    if trial_missing_count < best_missing_count:
                        best_missing_count = trial_missing_count
                        best_swap = (removable, candidate)
                        if trial_missing_count == 0:
                            break
                if best_missing_count == 0:
                    break
            if best_missing_count == 0:
                break

        if not best_swap:
            raise ValueError("Unable to build an assessment with full trait coverage")

        removable, candidate = best_swap
        selection = [
            candidate if question["id"] == removable["id"] else question
            for question in selection
        ]
        selected_ids.remove(removable["id"])
        selected_ids.add(candidate["id"])


def generate_assessment_question_set() -> tuple[str, list[dict]]:
    sections = _section_entries()
    rng = random.SystemRandom()

    for _ in range(100):
        selection = [
            question
            for section in sections
            for question in rng.sample(section, QUESTIONS_PER_SECTION)
        ]
        try:
            selection = _repair_trait_coverage(selection, sections, rng)
            break
        except ValueError:
            continue
    else:
        raise ValueError("Unable to build an assessment with full trait coverage")

    selection.sort(key=lambda question: question["id"])

    question_set_id = f"generated-{uuid4().hex}"
    GENERATED_QUESTION_TRAIT_SETS[question_set_id] = [
        deepcopy(question["traits"]) for question in selection
    ]
    return question_set_id, [
        {"id": index + 1, "source_id": question["id"], "text": question["text"]}
        for index, question in enumerate(selection)
    ]


DOMAIN_WEIGHTS = {
    "Software Development": {"PS": 15, "TA": 12, "AT": 10, "AD": 10, "SD": 8, "LA": 6},
    "Web Development": {"CR": 10, "PS": 10, "CO": 10, "TA": 10, "AP": 10, "TW": 8},
    "Mobile App Development": {"PS": 12, "TA": 12, "AT": 9, "CR": 8, "AP": 10, "LA": 6},
    "Data Analytics": {"AT": 15, "PS": 12, "AD": 12, "TA": 12, "SD": 9, "ST": 8},
    "Artificial Intelligence & Machine Learning": {"AT": 15, "PS": 15, "TA": 14, "AD": 10, "LA": 8, "IN": 7},
    "Cybersecurity": {"AT": 15, "PS": 15, "AD": 15, "TA": 20, "CU": 10, "RE": 5},
    "Cloud Computing": {"PS": 13, "TA": 15, "AT": 12, "AD": 12, "AP": 10, "LA": 7},
    "DevOps & Site Reliability Engineering": {"PS": 14, "TA": 18, "AT": 12, "LE": 10, "AP": 10, "TW": 8},
    "Networking": {"PS": 12, "TA": 18, "AT": 10, "AD": 10, "CO": 8, "CU": 8},
    "Database Management": {"AT": 13, "AD": 15, "TA": 15, "PS": 10, "OR": 7, "SD": 6},
    "UI/UX Design": {"CR": 20, "CO": 15, "EM": 15, "PS": 10, "IN": 8, "AD": 5},
    "QA & Software Testing": {"AD": 25, "PS": 15, "AT": 10, "TA": 10, "SD": 8, "RE": 6},
    "Game Development": {"CR": 18, "PS": 15, "TA": 18, "IN": 10, "TW": 8, "CU": 8},
    "Embedded Systems & IoT": {"TA": 25, "PS": 15, "AT": 12, "AD": 12, "CU": 8, "SD": 6},
    "Blockchain Development": {"AT": 15, "PS": 15, "TA": 20, "CU": 8, "SD": 5, "IN": 5},
    "AR/VR Development": {"CR": 15, "PS": 10, "CU": 10, "IN": 10, "TA": 10, "AP": 8},
    "Robotics & Automation": {"AT": 12, "PS": 12, "TA": 12, "AD": 10, "CU": 8, "SD": 6},
    "IT Support & System Administration": {"PS": 12, "CO": 10, "TA": 12, "AD": 10, "AP": 8, "RE": 6},
    "Product Management": {"CO": 12, "LE": 10, "EM": 10, "BA": 10, "ST": 10, "DM": 8},
    "Project Management": {"CO": 12, "LE": 10, "OR": 10, "TW": 8, "AP": 8, "DM": 8},
    "Business Intelligence": {"AT": 12, "PS": 10, "BA": 10, "AD": 10, "CO": 8, "TA": 8},
    "Enterprise Systems (ERP/CRM)": {"AT": 10, "AD": 10, "TA": 10, "TW": 8, "OR": 8, "AP": 8},
    "Digital Forensics": {"AT": 12, "PS": 12, "AD": 12, "TA": 12, "SD": 8, "RE": 8},
    "IT Consulting": {"CO": 12, "LE": 10, "PS": 10, "AT": 10, "DM": 8, "BA": 8},
    "Generative AI & Prompt Engineering": {"CR": 12, "IN": 12, "AT": 10, "PS": 10, "TA": 10, "CU": 8},
}


ROADMAP_DATA_PATH = Path(__file__).resolve().parent / "roadmap.json"

CATEGORY_BY_DOMAIN = {
    "Software Development": "development",
    "Web Development": "development",
    "Mobile App Development": "development",
    "Data Analytics": "data",
    "Artificial Intelligence & Machine Learning": "data",
    "Cybersecurity": "infrastructure",
    "Cloud Computing": "infrastructure",
    "DevOps & Site Reliability Engineering": "infrastructure",
    "Networking": "infrastructure",
    "Database Management": "data",
    "UI/UX Design": "creative",
    "Quality Assurance & Software Testing": "development",
    "Game Development": "creative",
    "Embedded Systems & IoT": "hardware",
    "Blockchain Development": "development",
    "AR/VR Development": "creative",
    "Robotics & Automation": "hardware",
    "IT Support & System Administration": "infrastructure",
    "Product Management": "business",
    "Project Management": "business",
    "Business Intelligence": "data",
    "Enterprise Systems (ERP/CRM)": "business",
    "Digital Forensics": "infrastructure",
    "IT Consulting": "business",
    "Generative AI & Prompt Engineering": "data",
}

ICON_BY_DOMAIN = {
    "Software Development": "code",
    "Web Development": "browser",
    "Mobile App Development": "mobile",
    "Data Analytics": "chart",
    "Artificial Intelligence & Machine Learning": "spark",
    "Cybersecurity": "shield",
    "Cloud Computing": "cloud",
    "DevOps & Site Reliability Engineering": "cycle",
    "Networking": "network",
    "Database Management": "database",
    "UI/UX Design": "pen",
    "Quality Assurance & Software Testing": "check",
    "Game Development": "game",
    "Embedded Systems & IoT": "chip",
    "Blockchain Development": "blocks",
    "AR/VR Development": "cube",
    "Robotics & Automation": "robot",
    "IT Support & System Administration": "tools",
    "Product Management": "compass",
    "Project Management": "calendar",
    "Business Intelligence": "dashboard",
    "Enterprise Systems (ERP/CRM)": "building",
    "Digital Forensics": "search",
    "IT Consulting": "briefcase",
    "Generative AI & Prompt Engineering": "wand",
}

DOMAIN_WEIGHT_ALIASES = {
    "Quality Assurance & Software Testing": "QA & Software Testing",
}

REQUIRED_ROADMAP_FIELDS = [
    "domain",
    "overview",
    "essentialQualities",
    "skillsRequired",
    "roadmapTimeline",
    "certifications",
    "careerOpportunities",
    "recommendedCourses",
    "expectedEntryLevelSalaryIndia",
    "expectedCompanies",
    "bestExams",
    "projectIdeas",
]


def slugify(name: str) -> str:
    return (
        name.lower()
        .replace("&", "and")
        .replace("/", "-")
        .replace("(", "")
        .replace(")", "")
        .replace(" ", "-")
        .replace("--", "-")
    )


def clean_text(value: str) -> str:
    return value.replace("aEUR'", "Rs ").replace("a,?", "Rs ").replace("₹", "\u20b9")


def require_list(record: dict, field: str) -> list:
    value = record.get(field, [])
    return value if isinstance(value, list) else []


def parse_timeline_item(item: str, index: int) -> dict:
    duration, _, title = item.partition(":")
    return {
        "stage": index + 1,
        "duration": clean_text(duration.strip()) if title else f"Stage {index + 1}",
        "title": clean_text(title.strip() if title else item),
    }


def course_links(domain_name: str, courses: list[str]) -> list[dict]:
    return [
        {
            "provider": "Course search",
            "title": clean_text(course),
            "url": f"https://www.coursera.org/search?query={quote_plus(course + ' ' + domain_name)}",
        }
        for course in courses
    ]


def validate_roadmap_record(record: dict) -> list[str]:
    return [field for field in REQUIRED_ROADMAP_FIELDS if field not in record]


def load_roadmap_records() -> list[dict]:
    records = json.loads(ROADMAP_DATA_PATH.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("roadmap.json must contain a list of domain roadmap objects")
    return records


def adapt_roadmap_record(record: dict) -> dict:
    name = clean_text(record["domain"])
    courses = [clean_text(course) for course in require_list(record, "recommendedCourses")]
    return {
        "id": record.get("id"),
        "name": name,
        "slug": slugify(name),
        "category": CATEGORY_BY_DOMAIN.get(name, "development"),
        "icon": ICON_BY_DOMAIN.get(name, "roadmap"),
        "summary": clean_text(record.get("overview", "")),
        "qualities": [clean_text(item) for item in require_list(record, "essentialQualities")],
        "skills": [clean_text(item) for item in require_list(record, "skillsRequired")],
        "roadmap": [
            parse_timeline_item(item, index)
            for index, item in enumerate(require_list(record, "roadmapTimeline"))
        ],
        "certifications": [clean_text(item) for item in require_list(record, "certifications")],
        "careers": [clean_text(item) for item in require_list(record, "careerOpportunities")],
        "courses": course_links(name, courses),
        "recommended_courses": courses,
        "salary": clean_text(record.get("expectedEntryLevelSalaryIndia", "Not specified")),
        "companies": [clean_text(item) for item in require_list(record, "expectedCompanies")],
        "exams": [clean_text(item) for item in require_list(record, "bestExams")],
        "projects": [clean_text(item) for item in require_list(record, "projectIdeas")],
        "missing_fields": validate_roadmap_record(record),
    }


DOMAINS = [adapt_roadmap_record(record) for record in load_roadmap_records()]


for new_name, old_name in DOMAIN_WEIGHT_ALIASES.items():
    if old_name in DOMAIN_WEIGHTS and new_name not in DOMAIN_WEIGHTS:
        DOMAIN_WEIGHTS[new_name] = DOMAIN_WEIGHTS.pop(old_name)


def get_domain_by_slug(slug: str):
    return next((domain for domain in DOMAINS if domain["slug"] == slug), None)
