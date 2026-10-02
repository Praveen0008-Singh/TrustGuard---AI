# 🛡️ TrustGuard AI

### Don't just detect the threat. Understand WHY.

TrustGuard AI is an explainable digital threat detection prototype built to help users understand **why suspicious digital content may be risky**, instead of simply showing a "Scam" or "Safe" label.

It analyzes messages, URLs, emails, payment requests, websites, and uploaded screenshots using explainable detection rules and presents the detected evidence through a simple cybersecurity dashboard.

---

## 🚀 Key Features

### 💬 Message Analyzer
Analyze suspicious SMS, WhatsApp messages, DMs, and other text content.

Detects indicators such as:
- Urgency and pressure
- Payment requests
- OTP/password references
- Account verification requests
- Suspicious links
- Prize or reward claims
- Account suspension warnings

### 🔗 URL Analyzer
Analyzes a URL's structure and identifies potentially suspicious characteristics such as:
- Missing HTTPS
- IP-based destinations
- Unusual URL length
- Suspicious domain wording
- Unusual domain structure
- Deep subdomains

### 📧 Email Analyzer
Analyze email subjects and body content for suspicious patterns and social-engineering indicators.

### 💳 Payment Request Analyzer
Checks payment-related messages for:
- Payment or transfer requests
- UPI references
- OTP/PIN/CVV references
- Banking information requests
- Refund/reward claims
- Urgency

### 🌐 Website Checker
Performs a structural analysis of a website address and highlights potential warning indicators.

> Note: The current prototype performs URL-based structural analysis. It does not claim to prove whether a website is completely safe or malicious.

### 🖼️ Screenshot Analyzer
Allows users to upload screenshots of suspicious digital content.

The current prototype provides basic upload-level analysis, with more advanced OCR and image understanding planned for future versions.

---

## 📊 Explainable Risk Assessment

TrustGuard AI does not only provide a final risk label.

It shows:

**Risk Score → Detected Evidence → Reason → Recommended Action**

### Risk Levels

| Score | Level |
|---|---|
| 🟢 0–29 | Low Risk |
| 🟠 30–59 | Suspicious |
| 🔴 60–100 | High Risk |

The score is generated from detected threat indicators in the current rule-based prototype.

---

## 🔎 How It Works

```text
              USER INPUT
                  │
                  ▼
        ┌──────────────────┐
        │ Content Analysis │
        └────────┬─────────┘
                 │
                 ▼
       ┌────────────────────┐
       │ Threat Indicators  │
       └─────────┬──────────┘
                 │
                 ▼
       ┌────────────────────┐
       │ Explainable Score  │
       └─────────┬──────────┘
                 │
          ┌──────┴──────┐
          ▼             ▼
      Evidence       Risk Level
          │             │
          └──────┬──────┘
                 ▼
          Safe Action
