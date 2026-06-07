from urllib.parse import quote_plus


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


DOMAIN_SEEDS = [
    ("Software Development", "development", "code", "Build reliable software applications and systems.", ["Python or Java", "Data structures", "OOP", "Git", "APIs"], ["Programming foundations", "Build console applications", "Learn databases and APIs", "Ship a portfolio project"], ["Software Engineer", "Backend Developer", "Application Developer"], "4-12 LPA"),
    ("Web Development", "development", "browser", "Create accessible, responsive websites and web applications.", ["HTML", "CSS", "JavaScript", "React", "Backend APIs"], ["Web foundations", "Interactive interfaces", "Backend and databases", "Deploy a full-stack project"], ["Frontend Developer", "Backend Developer", "Full-stack Developer"], "3-12 LPA"),
    ("Mobile App Development", "development", "mobile", "Design and build applications for Android and iOS.", ["Kotlin", "Flutter", "Dart", "Mobile UI", "Firebase"], ["Programming basics", "Mobile interface design", "Data and device APIs", "Publish a complete app"], ["Android Developer", "Flutter Developer", "Mobile Engineer"], "4-12 LPA"),
    ("Data Analytics", "data", "chart", "Turn raw data into insights that support decisions.", ["Excel", "SQL", "Python", "Statistics", "Power BI"], ["Spreadsheet analysis", "SQL and statistics", "Python and dashboards", "Complete a business case study"], ["Data Analyst", "Reporting Analyst", "Business Analyst"], "4-10 LPA"),
    ("Artificial Intelligence & Machine Learning", "data", "spark", "Create predictive and intelligent systems from data.", ["Python", "Linear algebra", "Machine learning", "Deep learning", "MLOps"], ["Python and mathematics", "Classical ML projects", "Neural networks", "Deploy an ML application"], ["ML Engineer", "AI Engineer", "Data Scientist"], "6-18 LPA"),
    ("Cybersecurity", "infrastructure", "shield", "Protect systems, networks, and data from digital threats.", ["Linux", "Networking", "Security fundamentals", "SIEM", "Ethical hacking"], ["Network and OS basics", "Security labs", "Detection and response", "Build a defensive portfolio"], ["Security Analyst", "SOC Analyst", "Penetration Tester"], "4-12 LPA"),
    ("Cloud Computing", "infrastructure", "cloud", "Build and operate scalable services on cloud platforms.", ["Linux", "Networking", "AWS or Azure", "Containers", "Infrastructure as code"], ["Infrastructure basics", "Core cloud services", "Containers and automation", "Deploy a production-style system"], ["Cloud Engineer", "Cloud Administrator", "Solutions Associate"], "5-14 LPA"),
    ("DevOps & Site Reliability Engineering", "infrastructure", "cycle", "Automate delivery and keep software systems dependable.", ["Linux", "Git", "Docker", "Kubernetes", "CI/CD"], ["Linux and scripting", "Containers and pipelines", "Kubernetes and monitoring", "Operate a deployed service"], ["DevOps Engineer", "SRE Associate", "Platform Engineer"], "6-18 LPA"),
    ("Networking", "infrastructure", "network", "Design, connect, and troubleshoot computer networks.", ["TCP/IP", "Routing", "Switching", "Cisco tools", "Network security"], ["Network fundamentals", "Routing and switching labs", "Security and automation", "Prepare for CCNA"], ["Network Engineer", "NOC Engineer", "Network Administrator"], "3-9 LPA"),
    ("Database Management", "data", "database", "Design, secure, and optimize the data layer of applications.", ["SQL", "DBMS", "PostgreSQL", "Data modelling", "Backup and recovery"], ["Relational foundations", "Advanced SQL", "Administration and tuning", "Build a database project"], ["Database Administrator", "SQL Developer", "Database Engineer"], "4-10 LPA"),
    ("UI/UX Design", "creative", "pen", "Research and design useful, inclusive digital experiences.", ["Figma", "User research", "Wireframing", "Prototyping", "Design systems"], ["Visual design basics", "UX research methods", "Prototype and test", "Publish case studies"], ["UI Designer", "UX Designer", "Product Designer"], "4-12 LPA"),
    ("QA & Software Testing", "development", "check", "Improve product quality through systematic testing.", ["Test design", "Bug tracking", "Selenium", "API testing", "Automation"], ["Testing principles", "Manual and API testing", "Automation frameworks", "Test a complete application"], ["QA Engineer", "Automation Tester", "Test Analyst"], "3-9 LPA"),
    ("Game Development", "creative", "game", "Build interactive game experiences for multiple platforms.", ["C#", "Unity", "Game design", "3D basics", "Version control"], ["Programming and game loops", "Unity fundamentals", "Systems and polish", "Publish a playable game"], ["Game Developer", "Gameplay Programmer", "Technical Designer"], "4-12 LPA"),
    ("Embedded Systems & IoT", "hardware", "chip", "Combine hardware and software to create connected devices.", ["Embedded C", "Microcontrollers", "Arduino", "Sensors", "IoT protocols"], ["Electronics and C", "Microcontroller labs", "Connectivity and RTOS", "Build an IoT prototype"], ["Embedded Engineer", "Firmware Engineer", "IoT Developer"], "4-11 LPA"),
    ("Blockchain Development", "development", "blocks", "Create decentralized applications and smart contracts.", ["Solidity", "Ethereum", "Web3", "Smart contracts", "Security"], ["Distributed systems basics", "Solidity contracts", "DApp integration", "Audit and deploy a project"], ["Blockchain Developer", "Smart Contract Engineer", "Web3 Developer"], "6-18 LPA"),
    ("AR/VR Development", "creative", "cube", "Develop immersive applications for learning, work, and play.", ["Unity", "C#", "3D interaction", "ARCore", "XR toolkit"], ["3D and programming basics", "Unity interaction", "AR/VR prototypes", "Create an immersive portfolio"], ["XR Developer", "Unity Developer", "AR Engineer"], "4-14 LPA"),
    ("Robotics & Automation", "hardware", "robot", "Create intelligent machines and automated systems.", ["Python", "C++", "Electronics", "ROS", "Control systems"], ["Programming and electronics", "Sensors and actuators", "ROS and controls", "Build an autonomous prototype"], ["Robotics Engineer", "Automation Engineer", "Controls Engineer"], "4-12 LPA"),
    ("IT Support & System Administration", "infrastructure", "tools", "Keep devices, users, servers, and workplace IT running.", ["Windows", "Linux", "Networking", "Active Directory", "Scripting"], ["Hardware and OS basics", "Networks and troubleshooting", "Server administration", "Run a home lab"], ["IT Support Engineer", "System Administrator", "NOC Engineer"], "3-8 LPA"),
    ("Product Management", "business", "compass", "Guide digital products from user problem to measurable outcome.", ["Product discovery", "Analytics", "Agile", "Roadmapping", "Stakeholder management"], ["Business and UX basics", "Discovery and metrics", "Product case studies", "Lead a student product"], ["Associate Product Manager", "Product Analyst", "Product Owner"], "6-18 LPA"),
    ("Project Management", "business", "calendar", "Plan and coordinate technical work across people and timelines.", ["Agile", "Scrum", "Jira", "Risk management", "Documentation"], ["Team and planning basics", "Agile delivery", "Tools and risk control", "Manage a real project"], ["Project Coordinator", "PMO Analyst", "Scrum Master"], "4-12 LPA"),
    ("Business Intelligence", "data", "dashboard", "Build dashboards and models that explain business performance.", ["SQL", "Power BI", "Tableau", "Excel", "Data modelling"], ["Excel and SQL", "Dashboard principles", "DAX and modelling", "Publish a BI portfolio"], ["BI Analyst", "Power BI Developer", "Reporting Analyst"], "4-12 LPA"),
    ("Enterprise Systems (ERP/CRM)", "business", "building", "Configure platforms that connect core business processes.", ["SAP or Salesforce", "SQL", "Business analysis", "Workflows", "Documentation"], ["Business process basics", "Choose an ERP or CRM", "Configuration projects", "Prepare for platform certification"], ["ERP Consultant", "CRM Administrator", "Implementation Associate"], "4-14 LPA"),
    ("Digital Forensics", "infrastructure", "search", "Investigate digital evidence and reconstruct cyber incidents.", ["Operating systems", "Networking", "Forensic tools", "Incident response", "Report writing"], ["OS and network basics", "Security foundations", "Forensic labs", "Complete an investigation case"], ["Forensics Analyst", "Incident Response Analyst", "Cyber Investigator"], "4-12 LPA"),
    ("IT Consulting", "business", "briefcase", "Help organizations solve business problems with technology.", ["Business analysis", "Presentation", "Cloud basics", "Data analysis", "Project coordination"], ["Technology and business basics", "Structured problem solving", "Case studies", "Build a consulting portfolio"], ["Technology Analyst", "IT Consultant", "Implementation Consultant"], "5-15 LPA"),
    ("Generative AI & Prompt Engineering", "data", "wand", "Build useful workflows and products with generative AI.", ["Python", "Prompt design", "LLM basics", "APIs", "RAG"], ["Python and AI foundations", "Prompt evaluation", "Build RAG and tool workflows", "Deploy a responsible AI app"], ["GenAI Developer", "AI Automation Specialist", "LLM App Developer"], "5-18 LPA"),
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


def course_links(domain_name: str) -> list[dict]:
    query = quote_plus(domain_name)
    return [
        {
            "provider": "NPTEL",
            "title": f"Explore {domain_name} courses",
            "url": f"https://nptel.ac.in/courses?searchText={query}",
        },
        {
            "provider": "Coursera",
            "title": f"Learn {domain_name}",
            "url": f"https://www.coursera.org/search?query={query}",
        },
    ]


DOMAINS = [
    {
        "name": name,
        "slug": slugify(name),
        "category": category,
        "icon": icon,
        "summary": summary,
        "skills": skills,
        "roadmap": [
            {"stage": index + 1, "title": step, "duration": duration}
            for index, (step, duration) in enumerate(
                zip(steps, ["0-3 months", "3-6 months", "6-12 months", "12+ months"])
            )
        ],
        "careers": careers,
        "salary": salary,
        "courses": course_links(name),
    }
    for name, category, icon, summary, skills, steps, careers, salary in DOMAIN_SEEDS
]


def get_domain_by_slug(slug: str):
    return next((domain for domain in DOMAINS if domain["slug"] == slug), None)

