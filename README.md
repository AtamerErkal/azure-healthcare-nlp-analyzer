# Healthcare NLP Analyzer
**Azure AI-102 Portfolio Project**

## 🎯 Project Goal
Medical text analysis using Azure AI Language services for healthcare AI applications in clinical settings.

## 🏥 Use Cases
- **Medical Entity Recognition:** Extract diseases, medications, dosages, procedures
- **PII Detection & Redaction:** Protect patient privacy (names, IDs, dates)
- **Clinical Translation:** English ↔ German medical terminology
- **Speech-to-Text:** Convert voice clinical notes to structured text

## 🛠️ Tech Stack
- **Azure AI Language** (NER, PII, sentiment)
- **Azure AI Speech** (STT, TTS)
- **Azure Translator** (EN ↔ DE medical terms)
- **Python 3.10**
- **Microsoft Foundry**

## 📦 Setup Instructions

### Prerequisites
- Python 3.10+
- Azure subscription with AI Services resource
- Git

### Installation
```bash
# Clone repository
git clone https://github.com/AtamerErkal/azure-healthcare-nlp-analyzer.git
cd azure-healthcare-nlp-analyzer

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Azure credentials
```

### Run Tests
```bash
python src/test_connection.py
```

## 📊 Project Roadmap

### Planned Features
- 🌟 FHIR-compliant output (HL7 standard)
- 🌟 Web UI with real-time entity highlighting
- 🌟 Batch document processing (100+ files)
- 🌟 Confidence score dashboard
- 🌟 Medical glossary (EN-DE terminology mapping)

## 📄 License
MIT License

## 👤 Author
**Atamer Erkal**
- Portfolio: [GitHub](https://github.com/AtamerErkal)
- Certification: Azure AI Engineer Associate (AI-102) — In Progress


## 🎓 Learning Resources
- [AI-102 Study Guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ai-102)
- [Azure AI Services Docs](https://learn.microsoft.com/en-us/azure/ai-services/)
- [Microsoft Learn: Azure AI Language](https://learn.microsoft.com/en-us/azure/ai-services/language-service/)
