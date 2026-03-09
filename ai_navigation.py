from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Navigation dataset
navigation_data = [

# ---------------- HOME ----------------
{"text": "home main page homepage company homepage start page welcome page", "url": "/"},
{"text": "go to home page open main website dashboard landing page", "url": "/"},

# ---------------- SERVICES ----------------
{"text": "services technology services it services digital services enterprise solutions offerings", "url": "/services"},
{"text": "what services does company provide technology solutions consulting solutions", "url": "/services"},
{"text": "show me technology services and digital transformation services", "url": "/services"},

# -------- CLOUD SERVICES --------
{"text": "cloud services cloud computing aws azure devops kubernetes container cloud infrastructure hybrid cloud", "url": "/services#cloud"},
{"text": "cloud migration cloud modernization cloud platform engineering cloud architecture", "url": "/services#cloud"},
{"text": "i want information about cloud computing services", "url": "/services#cloud"},
{"text": "show cloud technology solutions and devops services", "url": "/services#cloud"},

# -------- AI SERVICES --------
{"text": "artificial intelligence ai machine learning deep learning data science predictive analytics", "url": "/services#ai"},
{"text": "ai solutions enterprise ai automation intelligent systems data analytics", "url": "/services#ai"},
{"text": "show ai technology and machine learning services", "url": "/services#ai"},
{"text": "where are artificial intelligence solutions", "url": "/services#ai"},

# -------- CYBER SECURITY --------
{"text": "cyber security cyber defence network security information security banking security firewall protection", "url": "/services#cyber"},
{"text": "cybersecurity solutions enterprise security security consulting cyber protection", "url": "/services#cyber"},
{"text": "show cyber security services and security consulting", "url": "/services#cyber"},

# -------- IT CONSULTING --------
{"text": "it consulting business consulting technology advisory digital strategy consulting enterprise consulting", "url": "/services#consulting"},
{"text": "technology consulting enterprise advisory transformation consulting", "url": "/services#consulting"},

# ---------------- CAREERS ----------------
{"text": "jobs careers hiring job openings vacancies recruitment work opportunities employment", "url": "/jobs"},
{"text": "apply for job submit resume career opportunities join company", "url": "/jobs"},
{"text": "show me available job openings and hiring positions", "url": "/jobs"},

# -------- APPLY SECTION --------
{"text": "apply job submit resume interview process recruitment process", "url": "/jobs#apply"},
{"text": "how to apply for job and recruitment steps", "url": "/jobs#apply"},

# ---------------- ABOUT ----------------
{"text": "about company about organization leadership directors hr team management", "url": "/about"},
{"text": "who are the managing directors and company leadership", "url": "/about"},
{"text": "information about company leadership team and employees", "url": "/about"},
{"text": "show me hr team and development team members", "url": "/about"},

# ---------------- CONTACT ----------------
{"text": "contact company contact office phone number email address office location", "url": "/contact"},
{"text": "how to reach company contact support office address", "url": "/contact"},
{"text": "company contact information and email address", "url": "/contact"},

# ---------------- WHITEPAPERS ----------------
{"text": "whitepapers research reports technical documents technology research papers", "url": "/whitepapers"},
{"text": "show research papers and industry whitepapers", "url": "/whitepapers"},

# -------- CLOUD WHITEPAPER --------
{"text": "cloud whitepaper cloud migration research cloud modernization cloud computing report", "url": "/whitepapers#cloud"},
{"text": "research paper on cloud infrastructure and cloud computing", "url": "/whitepapers#cloud"},
{"text": "show cloud technology research document", "url": "/whitepapers#cloud"},

# -------- AI WHITEPAPER --------
{"text": "artificial intelligence whitepaper ai enterprise research machine learning research paper", "url": "/whitepapers#ai"},
{"text": "ai automation research document artificial intelligence enterprise report", "url": "/whitepapers#ai"},
{"text": "show artificial intelligence research document", "url": "/whitepapers#ai"},

# -------- CYBER WHITEPAPER --------
{"text": "cyber security whitepaper banking cyber security research security technology report", "url": "/whitepapers#cyber"},
{"text": "research paper about cybersecurity in banking sector", "url": "/whitepapers#cyber"},

# -------- RETAIL WHITEPAPER --------
{"text": "retail analytics whitepaper retail data analytics business intelligence retail insights", "url": "/whitepapers#retail"},
{"text": "data analytics research for retail industry", "url": "/whitepapers#retail"},
{"text": "show retail analytics research paper", "url": "/whitepapers#retail"},

# -------- HEALTHCARE WHITEPAPER --------
{"text": "healthcare technology research healthcare digital transformation medical ai report", "url": "/whitepapers#health"},
{"text": "healthcare data analytics research medical artificial intelligence", "url": "/whitepapers#health"},

# -------- GREEN IT WHITEPAPER --------
{"text": "green technology sustainability green it research environmental computing report", "url": "/whitepapers#green"},
{"text": "research about sustainable technology and green computing", "url": "/whitepapers#green"},

]

# Precompute embeddings
texts = [item["text"] for item in navigation_data]
embeddings = model.encode(texts)

def find_best_match(user_input: str):

    text = user_input.lower()

    # ---------- CONTENT TYPE DETECTION ----------
    content_keywords = {
        "whitepapers": ["whitepaper", "whitepapers", "research", "paper", "report", "study", "document","read", "see", "open", "show", "view", "display", "check",
                        "explore", "learn", "discover", "look at", "find", "search","download", "access", "study", "review" "analysis", "technical paper",
                        "technical document", "research document", "industry research","AI in Enterprise 2026",
                        "technology research", "insights", "technology insights","Cloud Modernization Strategy",
                        "case study", "industry report", "knowledge article","Cyber Security in Banking","Data Analytics for Retail","Healthcare Digital Transformation","Sustainable IT Infrastructure","download pdf"],
        "services": ["service", "services", "solution", "solutions", "technology", "platform","providings","provides","provide",
                        "service", "services",
                        "solution", "solutions",
                        "offering", "offerings",
                        "technology services",
                        "technology solutions",
                        "enterprise services",
                        "enterprise solutions",
                        "digital services",
                        "digital transformation",
                        "it services",
                        "platform services",
                        "technology capabilities",
                        "what you provide",
                        "what company provides",
                        "company services",
                        "business solutions",
                        "technology offerings"
                                                ],
        "jobs": ["job", "jobs", "career", "careers", "vacancy", "hiring", "recruitment","benifits","growth","job benefits","employee","benefits","recruitment",
                "recruiting","join",
                "job role",
                "positions",],
        "about": ["about", "company", "leadership", "team", "management","scope","about",
                    "about us",
                    "about company",
                    "company information",
                    "company overview",
                    "company profile",
                    "organization information",
                    "who are you",
                    "who is this company",
                    "about organization",
                    "company details",
                    "company background","directors","developer","tester",
                    "company introduction"],
        "contact": ["contact", "phone", "email", "office", "reach","how to contact",
                    "how can i reach you","how do i contact company","where is your office","where are you located","how to reach office",
                    "support","customer support","help","help desk","assistance","technical support","phone","phone number",
                    "call","call company","contact number","mobile number","telephone","email",
                    "email address","contact","contact us","contact company","contact information","contact details","get in touch",
                    "reach us","reach company","connect with us","send email","company email","support email",]
    }

    detected_content = None

    for content, words in content_keywords.items():
        for word in words:
            if word in text:
                detected_content = content
                break
        if detected_content:
            break


    # ---------- TOPIC DETECTION ----------
    topic_keywords = {
        "cloud": ["cloud", "aws", "azure", "kubernetes", "devops", "container"],
        "ai": ["ai", "artificial intelligence", "machine learning", "deep learning", "data science"],
        "cyber": ["cyber", "security", "cybersecurity", "firewall", "banking security"],
        "consulting": ["consulting", "advisory", "strategy"],
        "retail": ["retail", "shopping", "commerce", "retail analytics"],
        "health": ["health", "healthcare", "medical", "hospital"],
        "green": ["green", "sustainability", "environment", "green computing"]
    }

    detected_topic = None

    for topic, words in topic_keywords.items():
        for word in words:
            if word in text:
                detected_topic = topic
                break
        if detected_topic:
            break


    # ---------- COMBINE RESULT ----------
    if detected_content and detected_topic:
        return f"/{detected_content}#{detected_topic}"

    if detected_content:
        return f"/{detected_content}"


    # ---------- AI SEMANTIC SEARCH ----------
    user_embedding = model.encode([user_input])
    similarities = cosine_similarity(user_embedding, embeddings)[0]

    best_index = np.argmax(similarities)
    best_score = similarities[best_index]

    # If AI is unsure → go to home
    if best_score < 0.35:
        return "/"

    return navigation_data[best_index]["url"]