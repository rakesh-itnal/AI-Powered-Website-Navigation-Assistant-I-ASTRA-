/* ======================================= */
/*       I ASTRA ADVANCED INTELLIGENCE     */
/* ======================================= */

document.addEventListener("DOMContentLoaded", function () {

    const chatbot = document.getElementById("chatbot");
    const chatInput = document.getElementById("chat-input");
    const astraIcon = document.getElementById("astra-icon");

    if (!chatbot || !chatInput || !astraIcon) return;

    /* ========================= */
    /* 1️⃣ TOGGLE INPUT */
    /* ========================= */

    astraIcon.addEventListener("click", function () {
        if (chatInput.style.display === "none" || chatInput.style.display === "") {
            chatInput.style.display = "block";
            chatInput.focus();
        } else {
            chatInput.style.display = "none";
        }
    });


    /* ========================= */
    /* 2️⃣ INTENT DATABASE */
    /* ========================= */

    const intents = [

        { name: "home", url: "/", keywords: ["home","main","landing","start"] },

        { name: "services", url: "/services", keywords: ["service","services","solution","solutions","offerings","serv"] },

        { name: "careers", url: "/jobs", keywords: ["job","jobs","career","careers","carrer","vacancy","opening","hiring"] },

        { name: "about", url: "/about", keywords: ["about","company","team","management","director","hr"] },

        { name: "contact", url: "/contact", keywords: ["contact","email","phone","reach","location","office"] },

        { name: "whitepapers", url: "/whitepapers", keywords: ["whitepaper","whitepapers","research","report","paper"] },

        /* SERVICES DEEP */
        { name: "cloud", url: "/services#cloud", keywords: ["cloud","aws","azure","devops"] },
        { name: "ai", url: "/services#ai", keywords: ["ai","artificial","machine","learning","ml"] },
        { name: "cyber", url: "/services#cyber", keywords: ["cyber","security","bank","banking"] },
        { name: "consulting", url: "/services#consulting", keywords: ["consulting","advisory"] },

        /* CAREER DEEP */
        { name: "apply", url: "/jobs#apply", keywords: ["apply","application","resume","interview"] },

        /* WHITEPAPER DEEP */
        { name: "ai_white", url: "/whitepapers#ai", keywords: ["ai paper","enterprise ai"] },
        { name: "cloud_white", url: "/whitepapers#cloud", keywords: ["cloud paper","modernization"] },
        { name: "cyber_white", url: "/whitepapers#cyber", keywords: ["cyber banking","bank security"] },
        { name: "retail_white", url: "/whitepapers#retail", keywords: ["retail","analytics","retail data"] },
        { name: "health_white", url: "/whitepapers#health", keywords: ["health","medical"] },
        { name: "green_white", url: "/whitepapers#green", keywords: ["sustainable","green it"] }
    ];


    /* ========================= */
    /* 3️⃣ ADVANCED SCORING */
    /* ========================= */

    function wordSimilarity(a, b) {
        a = a.toLowerCase();
        b = b.toLowerCase();

        if (a === b) return 1;
        if (b.includes(a)) return 0.9;

        let matches = 0;
        for (let char of a) {
            if (b.includes(char)) matches++;
        }

        return matches / b.length;
    }

    function calculateIntentScore(userInput, intent) {

        const words = userInput.split(" ");
        let score = 0;

        words.forEach(word => {
            intent.keywords.forEach(keyword => {
                score += wordSimilarity(word, keyword);
            });
        });

        return score;
    }


    /* ========================= */
    /* 4️⃣ MAIN NAVIGATION */
    /* ========================= */

    /* ========================= */
/* 4️⃣ MAIN NAVIGATION */
/* ========================= */

chatInput.addEventListener("keypress", async function (e) {

    if (e.key === "Enter") {

        let userText = chatInput.value.trim();

        if (userText === "") return;

        try {

            const response = await fetch("/navigate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    text: userText
                })
            });

            const data = await response.json();

            console.log("AI Response:", data);

            if (data.url) {
                window.location.href = data.url;
            } else {
                alert("I ASTRA couldn't understand your request.");
            }

        } catch (error) {

            console.error("Navigation error:", error);
        }

        chatInput.value = "";
    }

});


    /* ========================= */
    /* 5️⃣ DRAGGING */
    /* ========================= */

    let offsetX, offsetY, isDragging = false;

    chatbot.addEventListener("mousedown", function (e) {
        isDragging = true;
        offsetX = e.clientX - chatbot.offsetLeft;
        offsetY = e.clientY - chatbot.offsetTop;
    });

    document.addEventListener("mousemove", function (e) {
        if (isDragging) {
            chatbot.style.left = (e.clientX - offsetX) + "px";
            chatbot.style.top = (e.clientY - offsetY) + "px";
            chatbot.style.right = "auto";
            chatbot.style.bottom = "auto";
        }
    });

    document.addEventListener("mouseup", function () {
        isDragging = false;
    });

    document.querySelectorAll('.fade-in').forEach(el => {
        el.classList.add('show');
    });

});