import streamlit as st
import re
from urllib.parse import urlparse

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="TrustGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(37,99,235,0.12), transparent 25%),
        radial-gradient(circle at 90% 20%, rgba(6,182,212,0.08), transparent 25%),
        #07111f;
    color: #e5edf7;
}

[data-testid="stHeader"] {
    display: none;
}

[data-testid="stToolbar"] {
    display: none;
}

.main .block-container {
    max-width: 1350px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #081321;
    border-right: 1px solid rgba(148,163,184,0.12);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #f8fafc;
}

/* Main title */

.brand {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 5px;
}

.brand-icon {
    width: 52px;
    height: 52px;
    border-radius: 15px;
    background: linear-gradient(135deg, #2563eb, #06b6d4);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 27px;
    box-shadow: 0 10px 30px rgba(37,99,235,0.25);
}

.brand-name {
    font-size: 32px;
    font-weight: 800;
    color: #f8fafc;
}

.brand-sub {
    color: #8fa3b8;
    font-size: 14px;
    margin-bottom: 25px;
}

/* Cards */

.metric-card {
    background: linear-gradient(
        145deg,
        rgba(15,32,53,0.95),
        rgba(9,23,39,0.95)
    );
    border: 1px solid rgba(96,165,250,0.13);
    border-radius: 18px;
    padding: 20px;
    min-height: 125px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.18);
}

.metric-label {
    color: #7f94aa;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-value {
    color: #f8fafc;
    font-size: 25px;
    font-weight: 750;
    margin-top: 8px;
}

.metric-small {
    color: #60a5fa;
    font-size: 12px;
    margin-top: 5px;
}

/* Section */

.section-title {
    font-size: 24px;
    font-weight: 750;
    color: #f8fafc;
    margin-top: 30px;
    margin-bottom: 5px;
}

.section-sub {
    color: #8194a9;
    margin-bottom: 20px;
}

/* Evidence */

.evidence-card {
    background: #0b1a2b;
    border: 1px solid rgba(148,163,184,0.12);
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 10px;
}

.evidence-title {
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 5px;
}

.evidence-desc {
    color: #91a4b8;
    font-size: 13px;
}

/* Risk */

.risk-box {
    border-radius: 18px;
    padding: 25px;
    background: linear-gradient(
        145deg,
        #0c1d31,
        #091827
    );
    border: 1px solid rgba(96,165,250,0.15);
    margin: 15px 0 20px 0;
}

.risk-score {
    font-size: 48px;
    font-weight: 800;
    color: #f8fafc;
}

.risk-label {
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 1px;
}

/* Buttons */

.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid rgba(96,165,250,0.25);
    background: linear-gradient(135deg, #1d4ed8, #0891b2);
    color: white;
    font-weight: 700;
    min-height: 48px;
    transition: 0.2s;
}

.stButton > button:hover {
    border-color: #60a5fa;
    box-shadow: 0 8px 25px rgba(37,99,235,0.25);
}

/* Inputs */

textarea, input {
    background-color: #091827 !important;
    color: #e5edf7 !important;
}

div[data-baseweb="input"],
div[data-baseweb="textarea"] {
    border-radius: 12px !important;
}

/* Status */

.online {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(34,197,94,0.10);
    color: #4ade80;
    border: 1px solid rgba(34,197,94,0.2);
    padding: 7px 12px;
    border-radius: 20px;
    font-size: 12px;
}

.dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #22c55e;
}

/* Footer */

.footer {
    text-align: center;
    color: #53677d;
    font-size: 12px;
    margin-top: 50px;
    padding-top: 25px;
    border-top: 1px solid rgba(148,163,184,0.08);
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# ANALYSIS ENGINE
# =========================================================

def analyze_text(text):
    """
    Explainable rule-based text analysis.
    Returns score, level and evidence.
    """

    text_lower = text.lower()

    score = 0
    evidence = []

    rules = [
        (
            r"\b(urgent|immediately|act now|within \d+ hours?|last warning|final warning)\b",
            20,
            "Urgency / pressure language",
            "The content creates pressure to act quickly."
        ),
        (
            r"\b(payment|pay|send money|transfer|upi|refund fee|processing fee)\b",
            25,
            "Payment request",
            "The content mentions money, payment or transfer."
        ),
        (
            r"\b(otp|password|pin|cvv|card number|bank details|account number|login details)\b",
            30,
            "Sensitive information request",
            "The content references credentials or sensitive financial information."
        ),
        (
            r"\b(prize|winner|won|reward|lottery|cashback|free gift)\b",
            20,
            "Prize / reward language",
            "The content uses unexpected reward or prize claims."
        ),
        (
            r"(https?://|www\.)",
            15,
            "External link detected",
            "The content contains a web link."
        ),
        (
            r"\b(verify your account|verify account|account verification|confirm your account)\b",
            15,
            "Account verification request",
            "The content asks the user to verify or confirm an account."
        ),
        (
            r"\b(click here|click the link|open the link|tap here)\b",
            15,
            "Call-to-action link language",
            "The user is encouraged to follow a link."
        ),
        (
            r"\b(suspended|blocked|deactivated|locked)\b",
            15,
            "Account threat language",
            "The content warns of account suspension or restriction."
        ),
    ]

    found = set()

    for pattern, points, title, description in rules:
        if re.search(pattern, text_lower):
            key = title

            if key not in found:
                score += points
                evidence.append({
                    "title": title,
                    "description": description,
                    "points": points
                })
                found.add(key)

    score = min(score, 100)

    if score >= 60:
        level = "HIGH RISK"
        icon = "🔴"
    elif score >= 30:
        level = "SUSPICIOUS"
        icon = "🟠"
    else:
        level = "LOW RISK"
        icon = "🟢"

    return score, level, icon, evidence


# =========================================================
# URL ANALYZER
# =========================================================

def analyze_url(url):

    original = url.strip()

    if not original:
        return 0, "LOW RISK", "🟢", [], "Please enter a URL."

    if not re.match(r"^https?://", original.lower()):
        url_for_parse = "https://" + original
    else:
        url_for_parse = original

    try:
        parsed = urlparse(url_for_parse)
        hostname = parsed.hostname or ""
    except Exception:
        return 70, "HIGH RISK", "🔴", [{
            "title": "Invalid URL structure",
            "description": "The entered value could not be parsed as a normal web address.",
            "points": 70
        }], "The URL format appears invalid."

    score = 0
    evidence = []

    def add(title, description, points):
        nonlocal score
        evidence.append({
            "title": title,
            "description": description,
            "points": points
        })
        score += points

    if parsed.scheme != "https":
        add(
            "No HTTPS",
            "The URL does not use HTTPS.",
            20
        )

    if "@" in url_for_parse:
        add(
            "Username-style URL trick",
            "The URL contains '@', which can make the visible address confusing.",
            25
        )

    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", hostname):
        add(
            "IP address used as hostname",
            "The destination is represented directly by an IP address.",
            20
        )

    if len(original) > 100:
        add(
            "Unusually long URL",
            "The URL is considerably long and may deserve extra scrutiny.",
            15
        )

    suspicious_words = [
        "login",
        "verify",
        "secure",
        "account",
        "update",
        "claim",
        "reward",
        "free",
        "bonus",
        "wallet",
        "payment"
    ]

    matched_words = [
        word for word in suspicious_words
        if word in hostname.lower()
    ]

    if matched_words:
        add(
            "Sensitive / action-oriented domain wording",
            "The hostname contains words commonly associated with account or payment actions.",
            15
        )

    if hostname.count("-") >= 3:
        add(
            "Unusual domain structure",
            "The hostname contains multiple hyphens.",
            10
        )

    if len(hostname.split(".")) > 4:
        add(
            "Deep subdomain structure",
            "The hostname contains several subdomain levels.",
            10
        )

    score = min(score, 100)

    if score >= 60:
        level = "HIGH RISK"
        icon = "🔴"
    elif score >= 30:
        level = "SUSPICIOUS"
        icon = "🟠"
    else:
        level = "LOW RISK"
        icon = "🟢"

    message = f"Analyzed hostname: {hostname}"

    return score, level, icon, evidence, message


# =========================================================
# PAYMENT ANALYZER
# =========================================================

def analyze_payment(text):

    text_lower = text.lower()

    score = 0
    evidence = []

    checks = [
        (
            r"\b(upi|payment|transfer|send money|pay now|pay immediately)\b",
            25,
            "Payment instruction",
            "The request asks for or references a payment or transfer."
        ),
        (
            r"\b(otp|pin|cvv|card|bank|account number)\b",
            35,
            "Financial credential reference",
            "The request references sensitive banking or authentication information."
        ),
        (
            r"\b(refund|cashback|reward|prize|lottery)\b",
            20,
            "Financial incentive",
            "The request uses a refund, reward or prize as a reason for payment."
        ),
        (
            r"\b(urgent|immediately|now|today|last chance)\b",
            20,
            "Payment urgency",
            "The request creates pressure to complete the transaction quickly."
        ),
        (
            r"(https?://|www\.)",
            15,
            "Payment-related link",
            "A web link is included in the payment request."
        )
    ]

    for pattern, points, title, desc in checks:
        if re.search(pattern, text_lower):
            score += points
            evidence.append({
                "title": title,
                "description": desc,
                "points": points
            })

    score = min(score, 100)

    if score >= 60:
        level = "HIGH RISK"
        icon = "🔴"
    elif score >= 30:
        level = "SUSPICIOUS"
        icon = "🟠"
    else:
        level = "LOW RISK"
        icon = "🟢"

    return score, level, icon, evidence


# =========================================================
# EMAIL ANALYZER
# =========================================================

def analyze_email(subject, body):

    combined = f"{subject}\n{body}"

    score, level, icon, evidence = analyze_text(combined)

    if subject.strip():
        subject_lower = subject.lower()

        if re.search(r"\b(urgent|important|action required|final notice)\b", subject_lower):
            score = min(score + 15, 100)

            evidence.append({
                "title": "Attention-grabbing email subject",
                "description": "The subject uses language designed to prompt immediate attention.",
                "points": 15
            })

    if score >= 60:
        level = "HIGH RISK"
        icon = "🔴"
    elif score >= 30:
        level = "SUSPICIOUS"
        icon = "🟠"
    else:
        level = "LOW RISK"
        icon = "🟢"

    return score, level, icon, evidence


# =========================================================
# SCREENSHOT ANALYZER
# =========================================================

def analyze_screenshot(uploaded_file):

    if uploaded_file is None:
        return None

    filename = uploaded_file.name.lower()

    evidence = []
    score = 10

    suspicious_filename_words = [
        "payment",
        "otp",
        "verify",
        "reward",
        "account",
        "login",
        "refund",
        "winner",
        "bank"
    ]

    matches = [
        word for word in suspicious_filename_words
        if word in filename
    ]

    if matches:
        score += 25

        evidence.append({
            "title": "Suspicious filename indicators",
            "description": "The uploaded filename contains words associated with account, payment or reward activity.",
            "points": 25
        })

    evidence.append({
        "title": "Screenshot received",
        "description": "The screenshot has been successfully uploaded for analysis.",
        "points": 0
    })

    score = min(score, 100)

    if score >= 60:
        level = "HIGH RISK"
        icon = "🔴"
    elif score >= 30:
        level = "SUSPICIOUS"
        icon = "🟠"
    else:
        level = "LOW RISK"
        icon = "🟢"

    return score, level, icon, evidence


# =========================================================
# RESULT DISPLAY
# =========================================================

def display_result(score, level, icon, evidence, language="English"):

    st.markdown('<div class="section-title">Threat Assessment</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:

        st.markdown(
            f"""
            <div class="risk-box">
                <div class="risk-score">{score}%</div>
                <div class="risk-label">{icon} {level}</div>
                <div style="color:#71859b;margin-top:8px;font-size:13px;">
                    Explainable risk assessment
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            '<div class="section-title" style="margin-top:10px;">Evidence Found</div>',
            unsafe_allow_html=True
        )

        if evidence:

            for item in evidence:

                points = item["points"]

                points_text = f"+{points} risk" if points else "Signal detected"

                st.markdown(
                    f"""
                    <div class="evidence-card">
                        <div class="evidence-title">
                            🔎 {item["title"]}
                            <span style="float:right;color:#60a5fa;">
                                {points_text}
                            </span>
                        </div>
                        <div class="evidence-desc">
                            {item["description"]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.info(
                "No major suspicious indicators were detected by the current rule set."
            )

    st.markdown("### 🛡️ Recommended Safe Action")

    if score >= 60:

        st.error(
            "Avoid clicking links, sending money, or sharing passwords/OTP. "
            "Verify the request independently using an official source."
        )

    elif score >= 30:

        st.warning(
            "Pause before acting. Verify the sender, destination and request "
            "through an independent trusted channel."
        )

    else:

        st.success(
            "No major warning signals were detected. Still verify unexpected "
            "requests before sharing sensitive information."
        )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🛡️ TrustGuard AI")
    st.caption("Explainable Digital Threat Intelligence")

    st.markdown("---")

    st.markdown("### Analysis Tools")

    tool = st.radio(
        "Choose analyzer",
        [
            "💬 Message Analyzer",
            "🔗 URL Analyzer",
            "📧 Email Analyzer",
            "💳 Payment Request",
            "🌐 Website Checker",
            "🖼️ Screenshot Analyzer",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    language = st.selectbox(
        "Explanation Language",
        ["English", "Hindi"]
    )

    st.markdown("---")

    st.markdown(
        """
        <div class="online">
            <span class="dot"></span>
            System Online
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption("Rule-based explainable prototype")


# =========================================================
# DASHBOARD HEADER
# =========================================================

st.markdown(
    """
    <div class="brand">
        <div class="brand-icon">🛡️</div>
        <div class="brand-name">TrustGuard AI</div>
    </div>

    <div class="brand-sub">
        Explainable Digital Threat Detection • Detect the threat. Understand WHY.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DASHBOARD METRICS
# =========================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Detection</div>
            <div class="metric-value">Multi-Input</div>
            <div class="metric-small">Messages • URLs • Emails</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m2:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Method</div>
            <div class="metric-value">Explainable</div>
            <div class="metric-small">Evidence-based rules</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Signals</div>
            <div class="metric-value">8+</div>
            <div class="metric-small">Threat indicators</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m4:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">System</div>
            <div class="metric-value">Online</div>
            <div class="metric-small">Ready for analysis</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# MESSAGE ANALYZER
# =========================================================

if tool == "💬 Message Analyzer":

    st.markdown(
        '<div class="section-title">💬 Analyze a Suspicious Message</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-sub">Paste an SMS, WhatsApp message, DM or suspicious text to inspect its threat signals.</div>',
        unsafe_allow_html=True
    )

    message = st.text_area(
        "Message",
        height=190,
        placeholder=(
            "Example:\n"
            "Your account verification is pending. "
            "Verify your account immediately using the link below."
        )
    )

    if st.button("🔍 Analyze Message"):

        if message.strip():

            score, level, icon, evidence = analyze_text(message)

            display_result(
                score,
                level,
                icon,
                evidence,
                language
            )

            with st.expander("📄 View Analyzed Message"):
                st.write(message)

        else:
            st.warning("Please enter a message first.")


# =========================================================
# URL ANALYZER
# =========================================================

elif tool == "🔗 URL Analyzer":

    st.markdown(
        '<div class="section-title">🔗 Analyze a Suspicious URL</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-sub">Inspect the structure of a URL for common warning indicators.</div>',
        unsafe_allow_html=True
    )

    url = st.text_input(
        "Website URL",
        placeholder="https://example.com/login"
    )

    if st.button("🔎 Analyze URL"):

        if url.strip():

            score, level, icon, evidence, message = analyze_url(url)

            st.info(message)

            display_result(
                score,
                level,
                icon,
                evidence,
                language
            )

        else:
            st.warning("Please enter a URL.")


# =========================================================
# EMAIL ANALYZER
# =========================================================

elif tool == "📧 Email Analyzer":

    st.markdown(
        '<div class="section-title">📧 Analyze a Suspicious Email</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-sub">Analyze an email subject and body for suspicious language and requests.</div>',
        unsafe_allow_html=True
    )

    subject = st.text_input(
        "Email Subject",
        placeholder="Your account requires immediate verification"
    )

    body = st.text_area(
        "Email Body",
        height=220,
        placeholder="Paste the email body here..."
    )

    if st.button("📨 Analyze Email"):

        if subject.strip() or body.strip():

            score, level, icon, evidence = analyze_email(
                subject,
                body
            )

            display_result(
                score,
                level,
                icon,
                evidence,
                language
            )

        else:
            st.warning("Please enter an email subject or body.")


# =========================================================
# PAYMENT REQUEST
# =========================================================

elif tool == "💳 Payment Request":

    st.markdown(
        '<div class="section-title">💳 Analyze a Payment Request</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-sub">Check payment requests for money, credential, urgency and link-related signals.</div>',
        unsafe_allow_html=True
    )

    payment_text = st.text_area(
        "Payment Request",
        height=200,
        placeholder=(
            "Example:\n"
            "Your refund is pending. Pay the processing fee through UPI "
            "to receive your cashback immediately."
        )
    )

    if st.button("💰 Analyze Payment Request"):

        if payment_text.strip():

            score, level, icon, evidence = analyze_payment(
                payment_text
            )

            display_result(
                score,
                level,
                icon,
                evidence,
                language
            )

        else:
            st.warning("Please enter the payment request.")


# =========================================================
# WEBSITE CHECKER
# =========================================================

elif tool == "🌐 Website Checker":

    st.markdown(
        '<div class="section-title">🌐 Website Safety Checker</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-sub">Perform a local structural check of a website address.</div>',
        unsafe_allow_html=True
    )

    website = st.text_input(
        "Website Address",
        placeholder="https://example.com"
    )

    if st.button("🌐 Check Website"):

        if website.strip():

            score, level, icon, evidence, message = analyze_url(
                website
            )

            st.info(message)

            display_result(
                score,
                level,
                icon,
                evidence,
                language
            )

            st.caption(
                "Note: This prototype evaluates URL structure. "
                "It does not claim to prove that a website is safe or malicious."
            )

        else:
            st.warning("Please enter a website address.")


# =========================================================
# SCREENSHOT ANALYZER
# =========================================================

elif tool == "🖼️ Screenshot Analyzer":

    st.markdown(
        '<div class="section-title">🖼️ Analyze a Suspicious Screenshot</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-sub">Upload a screenshot of a suspicious digital message or request.</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload Screenshot",
        type=["png", "jpg", "jpeg"],
        help="Upload a screenshot for prototype analysis."
    )

    if uploaded_file:

        st.image(
            uploaded_file,
            caption="Uploaded Screenshot",
            use_container_width=True
        )

        if st.button("🖼️ Analyze Screenshot"):

            result = analyze_screenshot(uploaded_file)

            if result:

                score, level, icon, evidence = result

                display_result(
                    score,
                    level,
                    icon,
                    evidence,
                    language
                )

                st.info(
                    "Prototype note: the current screenshot analyzer "
                    "does not perform OCR or image-based semantic detection yet."
                )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        🛡️ TrustGuard AI • CODE SANGAM Prototype<br>
        Explainable digital threat analysis for safer decisions.
    </div>
    """,
    unsafe_allow_html=True
)