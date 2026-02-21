import streamlit as st
import sys
import os
import base64

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.pii_redactor import PIIRedactor
from src.translator import MedicalTranslator
from src.speech_processor import SpeechProcessor
import json

st.set_page_config(
    page_title="Healthcare NLP Analyzer",
    page_icon="🏥",
    layout="wide"
)

# Load local icon
def get_icon_base64():
    """Load local icon and convert to base64"""
    icon_path = os.path.join(os.path.dirname(__file__), "..", "docs", "healthcare_icon.png")
    
    if not os.path.exists(icon_path):
        # Fallback to online icon
        return "https://img.icons8.com/fluency/96/medical-history.png"
    
    try:
        with open(icon_path, "rb") as f:
            icon_data = base64.b64encode(f.read()).decode()
            return f"data:image/png;base64,{icon_data}"
    except:
        return "https://img.icons8.com/fluency/96/medical-history.png"

# PROFESSIONAL CSS
st.markdown("""
<style>
    /* Sidebar dark theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #4CAF50 !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stSidebar"] .stAlert {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border-left: 4px solid #4CAF50 !important;
    }
    
    /* Main header */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4CAF50, #2196F3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: #B0B0B0;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Feature cards */
    .feature-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        border-left: 5px solid #4CAF50;
    }
    
    /* Entity boxes */
    .entity-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
        border-left: 4px solid #4CAF50;
        color: #ffffff;
        transition: transform 0.2s;
    }
    
    .entity-box:hover {
        transform: translateX(5px);
    }
    
    /* Translation result box */
    .translation-box {
        background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #2196F3;
        color: white;
    }
    
    /* Success box */
    .success-box {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
        padding: 1.2rem;
        border-radius: 8px;
        color: white;
        margin: 1rem 0;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 24px;
        background-color: #2d2d2d;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4CAF50 0%, #2196F3 100%);
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem !important;
        }
        .sub-header {
            font-size: 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# HEADER WITH LOCAL ICON
icon_src = get_icon_base64()
st.markdown(f"""
<div style='text-align: center; margin-bottom: 1rem;'>
    <img src='{icon_src}' width='80' style='vertical-align: middle; margin-right: 1rem;'>
    <span style='font-size: 3.5rem; font-weight: 800; background: linear-gradient(90deg, #4CAF50, #2196F3); -webkit-background-clip: text; -webkit-text-fill-color: transparent; vertical-align: middle;'>Healthcare NLP Analyzer</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="sub-header">Advanced Medical Text Processing Platform</div>', unsafe_allow_html=True)

# Feature badges
st.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <span style='background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.3rem; display: inline-block; color: white;'>
        🔍 PII Detection & Redaction
    </span>
    <span style='background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.3rem; display: inline-block; color: white;'>
        🌐 Medical Translation (7 Languages)
    </span>
    <span style='background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.3rem; display: inline-block; color: white;'>
        🎤 Voice-to-Text Transcription
    </span>
    <span style='background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.3rem; display: inline-block; color: white;'>
        🔐 Azure Key Vault Security
    </span>
</div>
""", unsafe_allow_html=True)

# Initialize services
if 'redactor' not in st.session_state:
    try:
        st.session_state.redactor = PIIRedactor()
        st.session_state.translator = MedicalTranslator()
        st.session_state.speech = SpeechProcessor()
        st.session_state.initialized = True
    except Exception as e:
        st.error(f"❌ Initialization failed: {e}")
        st.info("💡 Check your .env file and Azure credentials")
        st.stop()

# ENHANCED SIDEBAR
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/hospital.png", width=80)
    st.title("ℹ️ About")
    
    st.markdown("### 🎯 What Is This?")
    st.info("""
**Healthcare NLP Platform** — Complete medical text processing suite:

✅ **Extract** clinical information  
✅ **Protect** patient privacy (HIPAA-ready)  
✅ **Translate** to 7 languages  
✅ **Transcribe** doctor voice notes  
✅ **Preserve** medical data integrity
    """)
    
    st.markdown("---")
    st.markdown("### 🚀 Features")
    
    with st.expander("🔍 PII Detection & Redaction"):
        st.markdown("""
- Patient names → `[PERSON]`
- Contact info → `[EMAIL]`, `[PHONE]`
- Medical IDs → `[SSN]`
- Dates → `[DATE]`
- **Preserves:** Medications, vitals, diagnoses
        """)
    
    with st.expander("🌐 Medical Translation"):
        st.markdown("""
- **7 languages** supported (EN, TR, DE, FR, ES, AR, IT)
- Context-aware translation
- Medical terminology preserved
- Bidirectional translation
        """)
    
    with st.expander("🎤 Voice Transcription"):
        st.markdown("""
- Upload audio files (WAV, MP3)
- Real-time speech-to-text
- Doctor voice notes → Text
- Hands-free documentation
        """)
    
    st.markdown("---")
    st.markdown("### 💡 Use Cases")
    st.success("""
- **Clinical Research:** De-identify records
- **International Care:** Translate patient data
- **Voice Documentation:** Transcribe consultations
- **Data Sharing:** Remove PHI safely
- **ML Training:** Prepare medical datasets
    """)
    
    st.markdown("---")
    st.markdown("### 🛠️ Tech Stack")
    st.markdown("""
- 🧠 Azure AI Language (Healthcare Analytics)
- 🌐 Azure Translator (7 languages)
- 🎤 Azure Speech (STT/TTS)
- 🔐 Azure Key Vault (Secure credentials)
- 🐍 Python 3.10 + Streamlit
    """)
    
    st.markdown("---")
    st.markdown("### 🔗 Quick Links")
    st.markdown("""
- [📦 GitHub Repository](https://github.com/AtamerErkal/azure-healthcare-nlp-analyzer)
- [📚 Azure AI Docs](https://learn.microsoft.com/en-us/azure/ai-services/)
- [👨‍💻 Developer: Atamer Erkal](https://github.com/AtamerErkal)
    """)
    
    st.markdown("---")
    st.markdown(f"**Status:** {'🟢 All systems operational' if st.session_state.initialized else '🔴 Initialization failed'}")

# MAIN TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 Analyze Text",
    "🌐 Translate",
    "🎤 Voice Transcription",
    "📊 Batch Processing",
    "📖 Examples"
])

# ============================================================================
# TAB 1: ANALYZE TEXT (WITH COLOR HIGHLIGHTING!)
# ============================================================================
with tab1:
    st.subheader("🔍 Medical Text Analysis & PII Redaction")

    # Three columns: Original, Redacted with highlights, All Entities
    col_input, col_output, col_entities = st.columns([2, 2, 1.5])

    with col_input:
        st.markdown("**📄 Original Medical Text:**")
        text_input = st.text_area(
            "Paste clinical notes, patient records, or medical documentation:",
            height=400,
            placeholder="""Example:
Patient: Sarah Johnson, DOB: 03/15/1985
Chief Complaint: Type 2 Diabetes
Vitals: BP 142/88, HR 78, BMI 29.3
Labs: HbA1c 7.2%, LDL 156 mg/dL
Medications: Metformin 1000mg BID
Contact: sjohnson@email.com, +1-555-1234""",
            label_visibility="collapsed",
            key="analyze_input"
        )

    if st.button("🔍 Analyze & Redact", type="primary", use_container_width=True):
        if text_input.strip():
            with st.spinner("🔄 Processing with Azure AI Healthcare Analytics..."):
                result = st.session_state.redactor.process_document(text_input)

            # Color mapping
            healthcare_colors = {
                'MedicationName': '#4CAF50',
                'Dosage': '#66BB6A',
                'Diagnosis': '#81C784',
                'SymptomOrSign': '#A5D6A7',
                'TreatmentName': '#4DB6AC',
                'ExaminationName': '#4DD0E1',
                'BodyStructure': '#4FC3F7',
                'MedicationClass': '#64B5F6',
                'Frequency': '#7986CB',
                'RouteOrMode': '#9575CD'
            }
            
            medical_colors = {
                'Person': '#1976D2',
                'DateTime': '#1E88E5',
                'PersonType': '#2196F3'
            }
            
            pii_colors = {
                'Email': '#D32F2F',
                'PhoneNumber': '#C62828',
                'USSocialSecurityNumber': '#B71C1C',
                'IPAddress': '#E53935'
            }

            with col_output:
                st.markdown("**🔒 Redacted Text (PHI Removed):**")
                
                # Create highlighted redacted text
                redacted_highlighted = result["redacted_text"]
                
                # Highlight PII placeholders in redacted text
                pii_placeholders = {
                    '[PERSON]': '#1976D2',
                    '[EMAIL]': '#D32F2F',
                    '[PHONE]': '#D32F2F',
                    '[SSN]': '#D32F2F',
                    '[DATE]': '#1976D2'
                }
                
                for placeholder, color in pii_placeholders.items():
                    redacted_highlighted = redacted_highlighted.replace(
                        placeholder,
                        f'<span style="background-color: {color}; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold;">{placeholder}</span>'
                    )
                
                st.markdown(
                    f'<div style="background-color: #1a1a1a; padding: 1rem; border-radius: 8px; height: 400px; overflow-y: auto; line-height: 1.8;">{redacted_highlighted}</div>',
                    unsafe_allow_html=True
                )

            with col_entities:
                st.markdown("**🏷️ All Detected Entities:**")
                
                # Create highlighted version of ORIGINAL text with ALL entities colored
                highlighted_text = text_input
                
                # Collect all entities
                all_entities = []
                
                # Healthcare (green)
                for e in result["healthcare_entities"]:
                    all_entities.append({
                        'text': e['text'],
                        'color': healthcare_colors.get(e['category'], '#4CAF50'),
                        'category': e['category']
                    })
                
                # Medical (blue)
                for e in result["medical_entities"]:
                    all_entities.append({
                        'text': e['text'],
                        'color': medical_colors.get(e['category'], '#1976D2'),
                        'category': e['category']
                    })
                
                # PII (red)
                for e in result["pii_entities"]:
                    all_entities.append({
                        'text': e['text'],
                        'color': '#D32F2F',
                        'category': e['category']
                    })
                
                # Remove duplicates (keep first occurrence)
                seen = set()
                unique_entities = []
                for e in all_entities:
                    if e['text'] not in seen:
                        seen.add(e['text'])
                        unique_entities.append(e)
                
                # Apply highlighting to original text
                for entity in unique_entities:
                    entity_text = entity['text']
                    color = entity['color']
                    
                    replacement = f'<span style="background-color: {color}; color: white; padding: 3px 7px; border-radius: 4px; font-weight: 600; margin: 1px;">{entity_text}</span>'
                    
                    # Replace all occurrences
                    highlighted_text = highlighted_text.replace(entity_text, replacement)
                
                # Display
                st.markdown(
                    f'<div style="background-color: #1a1a1a; padding: 1.2rem; border-radius: 8px; height: 400px; overflow-y: auto; line-height: 2.2; font-size: 0.92rem;">'
                    f'{highlighted_text}'
                    f'</div>',
                    unsafe_allow_html=True
                )

            # Metrics row
            st.markdown("---")
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            with metric_col1:
                st.metric("📊 Total Entities", result["total_entities"])
            with metric_col2:
                st.metric("🏥 Healthcare Terms", len(result["healthcare_entities"]), delta="Preserved", delta_color="off")
            with metric_col3:
                st.metric("👤 Medical Entities", len(result["medical_entities"]), delta="Redacted", delta_color="inverse")
            with metric_col4:
                st.metric("🔒 PII Found", len(result["pii_entities"]), delta="Redacted", delta_color="inverse")

            # Entities breakdown
            st.markdown("---")
            st.subheader("🎯 Detected Entities Breakdown")

            ent_col1, ent_col2, ent_col3 = st.columns(3)

            with ent_col1:
                st.markdown("**🏥 Healthcare Terms (Preserved):**")
                if result["healthcare_entities"]:
                    for e in result["healthcare_entities"]:
                        color = healthcare_colors.get(e['category'], '#4CAF50')
                        st.markdown(
                            f'<div class="entity-box" style="background: linear-gradient(135deg, {color}22 0%, {color}44 100%); border-left: 4px solid {color};">'
                            f'<strong>{e["text"]}</strong><br>'
                            f'<span style="color: {color};">📋 {e["category"]}</span> • '
                            f'<span style="color: #BDBDBD;">Confidence: {e["confidence_score"]:.0%}</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.info("No healthcare terms detected")

            with ent_col2:
                st.markdown("**👤 Medical Entities (Redacted):**")
                if result["medical_entities"]:
                    for e in result["medical_entities"]:
                        color = medical_colors.get(e['category'], '#1976D2')
                        st.markdown(
                            f'<div class="entity-box" style="background: linear-gradient(135deg, {color}22 0%, {color}44 100%); border-left: 4px solid {color};">'
                            f'<strong>{e["text"]}</strong><br>'
                            f'<span style="color: {color};">📌 {e["category"]}</span> • '
                            f'<span style="color: #BDBDBD;">Confidence: {e["confidence_score"]:.0%}</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.info("No medical entities detected")

            with ent_col3:
                st.markdown("**🔒 PII (Contact - Redacted):**")
                if result["pii_entities"]:
                    for e in result["pii_entities"]:
                        st.markdown(
                            f'<div class="entity-box" style="background: linear-gradient(135deg, #D32F2F22 0%, #D32F2F44 100%); border-left: 4px solid #D32F2F;">'
                            f'<strong>{e["text"]}</strong><br>'
                            f'<span style="color: #EF5350;">🚫 {e["category"]}</span> • '
                            f'<span style="color: #BDBDBD;">Confidence: {e["confidence_score"]:.0%}</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.info("✅ No PII detected")

            # Download buttons
            st.markdown("---")
            dl_col1, dl_col2 = st.columns(2)

            with dl_col1:
                st.download_button(
                    label="📥 Download Redacted Text",
                    data=result["redacted_text"],
                    file_name="redacted_medical_note.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            with dl_col2:
                st.download_button(
                    label="📊 Download JSON Report",
                    data=json.dumps(result, indent=2),
                    file_name="analysis_report.json",
                    mime="application/json",
                    use_container_width=True
                )

        else:
            st.warning("⚠️ Please enter medical text to analyze")

# ============================================================================
# TAB 2: TRANSLATE (7 LANGUAGES!)
# ============================================================================
with tab2:
    st.subheader("🌐 Medical Text Translation")
    
    # Enhanced description
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem;'>
        <h4 style='color: white; margin: 0;'>🎯 Translation Features:</h4>
        <ul style='color: #E0E0E0; margin-top: 0.5rem;'>
            <li><strong>7 Languages Supported:</strong> English, Turkish, German, French, Spanish, Arabic, Italian</li>
            <li><strong>Medical Context-Aware:</strong> Preserves medical terminology accuracy</li>
            <li><strong>Instant Translation:</strong> Real-time Azure Translator API</li>
            <li><strong>Bidirectional:</strong> Translate from/to any supported language</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        default_translate_text = st.session_state.get('quick_translate_text', '')
        
        translate_input = st.text_area(
            "Enter medical text to translate:",
            height=200,
            value=default_translate_text,
            placeholder="Example: Patient diagnosed with Type 2 Diabetes Mellitus and essential hypertension. Prescribed Metformin 500mg BID."
        )
    
    with col2:
        st.markdown("**🔧 Translation Settings:**")
        
        languages = [
            ("🇬🇧 English", "en"),
            ("🇹🇷 Turkish", "tr"),
            ("🇩🇪 German", "de"),
            ("🇫🇷 French", "fr"),
            ("🇪🇸 Spanish", "es"),
            ("🇸🇦 Arabic", "ar"),
            ("🇮🇹 Italian", "it")
        ]
        
        from_lang = st.selectbox(
            "From Language:",
            options=languages,
            format_func=lambda x: x[0],
            index=0
        )
        
        to_lang = st.selectbox(
            "To Language:",
            options=languages,
            format_func=lambda x: x[0],
            index=1
        )
    
    if st.button("🌐 Translate", type="primary", use_container_width=True):
        if translate_input.strip():
            if from_lang[1] == to_lang[1]:
                st.warning("⚠️ Source and target languages are the same. Please select different languages.")
            else:
                with st.spinner("🔄 Translating with Azure Translator..."):
                    translated = st.session_state.translator.translate(
                        translate_input,
                        from_lang=from_lang[1],
                        to_lang=to_lang[1]
                    )
                
                st.markdown("---")
                st.markdown(
                    f'<div class="translation-box">'
                    f'<h3>{to_lang[0]} Translation:</h3>'
                    f'<p style="font-size: 1.2rem; margin-top: 1rem; line-height: 1.8;">{translated}</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                
                col_dl1, col_dl2 = st.columns(2)
                with col_dl1:
                    st.download_button(
                        label="📥 Download Translation",
                        data=translated,
                        file_name=f"translation_{from_lang[1]}_to_{to_lang[1]}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with col_dl2:
                    st.info("💡 Click text above to select and copy")
        else:
            st.warning("⚠️ Please enter text to translate")
    
    # EXPANDED Quick examples
    st.markdown("---")
    st.markdown("**⚡ Quick Translation Examples:**")
    
    quick_examples = {
        "💊 Prescription": "Patient prescribed Metformin 500mg twice daily for Type 2 Diabetes management, Lisinopril 10mg once daily for hypertension, and Atorvastatin 20mg at bedtime for hyperlipidemia. Monitor blood glucose levels and blood pressure weekly.",
        
        "🩺 Diagnosis": "Patient diagnosed with Type 2 Diabetes Mellitus with HbA1c of 8.2%, essential hypertension stage 2 with average BP 152/94 mmHg, and hyperlipidemia with LDL cholesterol 165 mg/dL. Family history positive for cardiovascular disease.",
        
        "📊 Vitals & Labs": "Vital signs: Blood pressure 140/90 mmHg, heart rate 82 bpm, respiratory rate 16/min, temperature 36.9°C, oxygen saturation 97% on room air. Laboratory results: Fasting glucose 156 mg/dL, HbA1c 7.8%, total cholesterol 245 mg/dL, triglycerides 198 mg/dL.",
        
        "🏥 Clinical Note": "64-year-old male with chief complaint of chest pain radiating to left arm, onset 2 hours ago. Patient reports associated shortness of breath and diaphoresis. Past medical history significant for hypertension and hyperlipidemia. Currently on aspirin 81mg daily and metoprolol 50mg BID.",
        
        "📋 Discharge Summary": "Patient admitted for acute exacerbation of congestive heart failure. Treated with IV furosemide 40mg BID and potassium supplementation. Condition improved with diuresis, dyspnea resolved. Discharged on oral furosemide 20mg daily, potassium chloride 20mEq daily, and metoprolol 25mg BID. Follow-up in cardiology clinic in 2 weeks.",
        
        "🔬 Lab Results": "Complete blood count shows white blood cells 8.5 K/uL, hemoglobin 13.2 g/dL, hematocrit 39%, platelets 245 K/uL. Comprehensive metabolic panel: sodium 138 mEq/L, potassium 4.2 mEq/L, chloride 102 mEq/L, bicarbonate 24 mEq/L, BUN 18 mg/dL, creatinine 1.1 mg/dL, glucose 142 mg/dL."
    }
    
    # 2 rows of 3 columns
    cols_row1 = st.columns(3)
    cols_row2 = st.columns(3)
    all_cols = cols_row1 + cols_row2
    
    for i, (title, text) in enumerate(quick_examples.items()):
        with all_cols[i]:
            if st.button(title, use_container_width=True, key=f"quick_translate_{i}"):
                st.session_state.quick_translate_text = text
                st.rerun()

# ============================================================================
# TAB 3: VOICE TRANSCRIPTION (WITH RECORDING!)
# ============================================================================
with tab3:
    st.subheader("🎤 Voice-to-Text Transcription")
    
    # Enhanced description
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem;'>
        <h4 style='color: white; margin: 0;'>🎯 Transcription Features:</h4>
        <ul style='color: #E0E0E0; margin-top: 0.5rem;'>
            <li><strong>Audio File Upload:</strong> WAV, MP3, M4A formats supported</li>
            <li><strong>Live Recording:</strong> Record directly from your microphone</li>
            <li><strong>Medical Accuracy:</strong> Optimized for medical terminology</li>
            <li><strong>Instant Analysis:</strong> Automatically detect PII in transcriptions</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Two modes: Upload or Record
    mode = st.radio(
        "Choose transcription mode:",
        options=["📤 Upload Audio File", "🎙️ Record Live"],
        horizontal=True
    )
    
    if mode == "📤 Upload Audio File":
        st.markdown("---")
        st.markdown("**🎵 Upload Audio File:**")
        audio_file = st.file_uploader(
            "Choose audio file (WAV, MP3, M4A)",
            type=["wav", "mp3", "m4a"],
            help="Upload doctor voice notes, patient consultations, or medical audio"
        )
        
        if audio_file:
            st.audio(audio_file, format="audio/wav")
            
            if st.button("🎤 Transcribe Audio", type="primary", use_container_width=True):
                with open("temp_audio.wav", "wb") as f:
                    f.write(audio_file.read())
                
                with st.spinner("🔄 Transcribing with Azure Speech..."):
                    result = st.session_state.speech.audio_to_text("temp_audio.wav")
                
                if os.path.exists("temp_audio.wav"):
                    os.remove("temp_audio.wav")
                
                if result["success"]:
                    st.markdown("---")
                    st.success("✅ Transcription Complete!")
                    
                    st.text_area(
                        "Transcribed Text:",
                        value=result["text"],
                        height=200,
                        key="transcribed_text"
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="📥 Download Transcription",
                            data=result["text"],
                            file_name="transcription.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    
                    with col2:
                        if st.button("🔍 Analyze for PII", use_container_width=True):
                            with st.spinner("Analyzing..."):
                                analysis = st.session_state.redactor.process_document(result["text"])
                            st.success(f"✅ Found {analysis['total_entities']} entities ({len(analysis['pii_entities'])} PII)")
                
                else:
                    st.error(f"❌ Transcription failed: {result['error']}")
        
        else:
            st.info("👆 Upload an audio file to start transcription")
    
    else:  # Live Recording
        st.markdown("---")
        st.markdown("**🎙️ Live Recording:**")
        
        st.info("""
        **How to use:**
        1. Click **Start Recording** button below
        2. Speak clearly into your microphone
        3. Azure Speech will transcribe in real-time
        4. Click **Stop** when finished
        """)
        
        if st.button("🔴 Start Recording", type="primary", use_container_width=True):
            with st.spinner("🎤 Listening... Speak now!"):
                result = st.session_state.speech.microphone_to_text()
            
            if result["success"]:
                st.markdown("---")
                st.success("✅ Recording Complete!")
                
                st.text_area(
                    "Transcribed Text:",
                    value=result["text"],
                    height=150,
                    key="live_transcribed_text"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 Download Transcription",
                        data=result["text"],
                        file_name="live_transcription.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col2:
                    if st.button("🔍 Analyze for PII", use_container_width=True, key="analyze_live"):
                        with st.spinner("Analyzing..."):
                            analysis = st.session_state.redactor.process_document(result["text"])
                        st.success(f"✅ Found {analysis['total_entities']} entities")
            
            else:
                st.error(f"❌ Recording failed: {result['error']}")
    
    st.markdown("---")
    st.markdown("**💡 Use Cases:**")
    st.markdown("""
    - **🏥 Clinical Documentation:** Transcribe doctor-patient consultations
    - **📝 Voice Notes:** Convert voice memos to structured text
    - **🔊 Dictation:** Hands-free medical record entry
    - **📞 Telemedicine:** Transcribe virtual appointments
    - **🎓 Medical Training:** Document clinical observations
    """)

# ============================================================================
# TAB 4: BATCH PROCESSING
# ============================================================================
with tab4:
    st.subheader("📊 Batch File Processing")
    st.markdown("Process multiple medical documents at once (TXT, PDF, DOCX)")
    
    uploaded_files = st.file_uploader(
        "Upload files:",
        type=["txt", "pdf", "docx"],
        accept_multiple_files=True,
        key="batch_uploader"
    )
    
    if uploaded_files:
        st.info(f"📁 {len(uploaded_files)} file(s) selected")
        
        if st.button("🔄 Process All Files", type="primary", use_container_width=True):
            batch_results = []
            progress = st.progress(0)
            
            for i, f in enumerate(uploaded_files):
                try:
                    if f.name.endswith('.txt'):
                        text = f.read().decode("utf-8")
                    
                    elif f.name.endswith('.pdf'):
                        try:
                            import PyPDF2
                            from io import BytesIO
                            pdf_reader = PyPDF2.PdfReader(BytesIO(f.read()))
                            text = ""
                            for page in pdf_reader.pages:
                                text += page.extract_text()
                        except ImportError:
                            st.error("⚠️ PyPDF2 not installed. Run: `pip install PyPDF2`")
                            continue
                    
                    elif f.name.endswith('.docx'):
                        try:
                            import docx
                            from io import BytesIO
                            doc = docx.Document(BytesIO(f.read()))
                            text = "\n".join([para.text for para in doc.paragraphs])
                        except ImportError:
                            st.error("⚠️ python-docx not installed. Run: `pip install python-docx`")
                            continue
                    
                    doc_result = st.session_state.redactor.process_document(text)
                    batch_results.append({
                        "filename": f.name,
                        "result": doc_result,
                    })
                
                except Exception as e:
                    st.error(f"❌ Error processing {f.name}: {e}")
                
                progress.progress((i + 1) / len(uploaded_files))
            
            progress.empty()
            
            st.success(f"✅ Processed {len(batch_results)} file(s) successfully!")
            
            total_entities = sum(r["result"]["total_entities"] for r in batch_results)
            total_healthcare = sum(len(r["result"]["healthcare_entities"]) for r in batch_results)
            total_pii = sum(len(r["result"]["pii_entities"]) for r in batch_results)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Entities", total_entities)
            col2.metric("Healthcare Terms", total_healthcare)
            col3.metric("PII Redacted", total_pii)
            
            st.markdown("---")
            for r in batch_results:
                with st.expander(f"📄 {r['filename']} — {r['result']['total_entities']} entities found"):
                    st.text_area(
                        "Redacted text:",
                        value=r["result"]["redacted_text"],
                        height=200,
                        key=f"batch_{r['filename']}"
                    )
                    
                    base_name = r['filename'].rsplit('.', 1)[0]
                    st.download_button(
                        label=f"📥 Download {base_name}_REDACTED.txt",
                        data=r["result"]["redacted_text"],
                        file_name=f"{base_name}_REDACTED.txt",
                        mime="text/plain",
                        key=f"dl_{r['filename']}"
                    )

# ============================================================================
# TAB 5: EXAMPLES (EXPANDED!)
# ============================================================================
with tab5:
    st.subheader("📖 Example Medical Texts")
    st.markdown("Click to load examples and test the analyzer:")

    examples = {
        "Annual Checkup": """Annual wellness visit for Linda Martinez, DOB: 05/22/1978, Age 45, BMI 28.5.
Chief complaint: Routine checkup, no specific concerns.
Vital signs: BP 128/82 mmHg, HR 76 bpm, Temperature 36.8°C, SpO2 98% on room air.
Laboratory results: HbA1c 6.2% (prediabetic range), fasting glucose 112 mg/dL, LDL cholesterol 145 mg/dL, HDL 52 mg/dL, triglycerides 178 mg/dL.
Assessment: Prediabetes, dyslipidemia, overweight (BMI 28.5).
Plan: Lifestyle modification with emphasis on diet and exercise, recheck labs in 6 months. Consider metformin if HbA1c continues to rise.
Contact: lmartinez@email.com, Phone: +1-555-4567.""",

        "Emergency Visit": """Emergency department visit: David Chen, DOB: 11/05/1990, MRN: 2847563.
Chief complaint: Laceration to right forearm sustained during carpentry work.
History of present illness: Patient reports acute injury 2 hours ago when saw slipped. Wound actively bleeding on arrival.
Examination: 4cm linear laceration to volar aspect of right forearm, no tendon involvement, neurovascular exam intact.
Procedure: Wound irrigation with 500mL normal saline, hemostasis achieved, closure with 8 interrupted 4-0 nylon sutures.
Vital signs: BP 118/76 mmHg, HR 82 bpm, Temperature 36.9°C.
Medications prescribed: Cephalexin 500mg PO TID x 7 days for infection prophylaxis, ibuprofen 400mg PO q6h PRN for pain.
Wound care instructions: Keep clean and dry, remove sutures in 10-12 days. Follow-up in 5 days for wound check.
Tetanus toxoid administered (last tetanus 2015).
Emergency contact: Phone +1-555-8901, Email: dchen@email.com""",

        "Hospital Admission": """Patient: John Robert Smith, Date of Birth: March 15, 1985, SSN: 123-45-6789, MRN: 9876543.
Admitted: January 20, 2024 at 14:30 to Memorial Hospital, 5th Floor Medical Unit, Room 512.
Attending physician: Dr. Sarah Williams, Internal Medicine.
Chief complaint: Uncontrolled Type 2 Diabetes Mellitus and hypertension.
History of present illness: 39-year-old male with 5-year history of Type 2 DM, poorly controlled despite oral medications. Recent home glucose readings 250-300 mg/dL. Also reports headaches and blurred vision.
Past medical history: Type 2 Diabetes Mellitus (2019), Essential Hypertension (2020), Hyperlipidemia (2021).
Vital signs on admission: BP 152/94 mmHg, HR 88 bpm, Temperature 37.1°C, BMI 31.2, SpO2 96% on room air.
Laboratory results: HbA1c 9.8%, fasting glucose 284 mg/dL, creatinine 1.4 mg/dL, eGFR 58 mL/min, urine microalbumin 180 mg/g creatinine.
Current medications: Metformin 1000mg BID, Lisinopril 10mg QD, Atorvastatin 20mg QHS.
Assessment: Uncontrolled Type 2 Diabetes with early diabetic nephropathy, stage 2 hypertension, dyslipidemia.
Plan: Initiate insulin therapy with glargine 20 units QHS and aspart sliding scale, increase lisinopril to 20mg QD, diabetes education, nephrology consult.
Contact information: Email john.smith@email.com, Mobile +1-555-0123, Emergency contact (wife): Mary Smith +1-555-0124.""",

        "Surgical Consultation": """Surgical consultation note for Patricia Anderson, DOB: 08/14/1962, Age 61, MRN: 5432109.
Referring physician: Dr. Michael Brown, Gastroenterology.
Chief complaint: Symptomatic cholelithiasis, recurrent biliary colic.
History of present illness: Patient reports multiple episodes of right upper quadrant pain over past 6 months, typically postprandial, lasting 2-4 hours. Most recent episode 3 days ago, severity 8/10, associated with nausea and vomiting.
Imaging: Abdominal ultrasound shows multiple gallstones, largest 1.2cm, gallbladder wall thickening 4mm, no ductal dilatation. HIDA scan demonstrates decreased gallbladder ejection fraction of 15% (normal >35%).
Past surgical history: Appendectomy 1985, cesarean section 1988, hysterectomy 2010.
Current medications: Amlodipine 5mg daily for hypertension, levothyroxine 75mcg daily for hypothyroidism.
Assessment: Symptomatic cholelithiasis with chronic cholecystitis, decreased gallbladder function.
Recommendation: Laparoscopic cholecystectomy. Discussed risks including bleeding, infection, bile duct injury (<1%), conversion to open (<5%). Patient agrees to proceed.
Preoperative clearance: Cardiology evaluation recommended given age and hypertension. Schedule EKG and basic metabolic panel.
Contact: panderson@email.com, Phone: +1-555-2468.""",

        "Psychiatric Evaluation": """Initial psychiatric evaluation: Michael Torres, DOB: 02/28/1995, Age 28, Patient ID: PSY-78921.
Chief complaint: "I've been feeling anxious and can't sleep."
History of present illness: Patient reports 6-month history of increasing anxiety, panic attacks 2-3 times per week, difficulty initiating and maintaining sleep. Denies suicidal ideation, homicidal ideation, or psychotic symptoms. No recent major life stressors identified.
Psychiatric history: No previous psychiatric hospitalizations or suicide attempts. Brief trial of sertraline 2 years ago, discontinued due to side effects.
Social history: Single, works as software engineer, denies alcohol or substance use, exercises regularly, good social support network.
Mental status exam: Alert and oriented x3, well-groomed, cooperative, normal speech, anxious mood, congruent affect, thought process goal-directed, no delusions or hallucinations, insight and judgment intact.
Assessment: Generalized anxiety disorder, moderate severity, with associated insomnia.
Plan: Initiate escitalopram 10mg daily, hydroxyzine 25mg PRN for acute anxiety, sleep hygiene education, refer to cognitive behavioral therapy. Follow-up in 2 weeks to assess response and side effects.
Contact: mtorres@email.com, Phone: +1-555-7890.""",

        "Pediatric Well-Child": """Well-child check: Emma Johnson, DOB: 06/15/2018, Age 5 years 8 months, Chart #: PED-45632.
Parent: Jennifer Johnson, Phone: +1-555-3698, Email: jjohnson@email.com
Chief complaint: Routine 6-year well-child visit, kindergarten physical.
Growth parameters: Height 112cm (50th percentile), Weight 19.2kg (45th percentile), BMI 15.3 (normal range). Head circumference 50.5cm.
Vital signs: BP 95/58 mmHg, HR 88 bpm, Respiratory rate 20/min, Temperature 36.7°C.
Developmental milestones: Age-appropriate. Speaks in complete sentences, recognizes colors and shapes, counts to 20, writes first name, follows multi-step instructions.
Physical examination: General appearance healthy, well-nourished. HEENT: normocephalic, atraumatic, TMs clear bilaterally, dentition good. Cardiovascular: regular rate and rhythm, no murmurs. Respiratory: clear to auscultation bilaterally. Abdomen: soft, non-tender. Musculoskeletal: normal gait, full range of motion. Neurological: age-appropriate reflexes and coordination.
Immunizations: Up to date per CDC schedule. Administered today: DTaP (5th dose), IPV (4th dose), MMR (2nd dose), Varicella (2nd dose).
Anticipatory guidance: Discussed nutrition, physical activity, screen time limits, stranger danger, bicycle helmet safety, booster seat usage.
Assessment: Healthy 5-year-old female, growth and development appropriate for age.
Plan: Continue routine diet and activities. Next well-child visit at age 7. Dental referral for 6-month cleaning. Vision and hearing screening normal, no referrals needed at this time."""
    }

    # 2 rows of 3 columns
    cols_row1 = st.columns(3)
    cols_row2 = st.columns(3)
    all_cols = cols_row1 + cols_row2
    
    for i, (title, text) in enumerate(examples.items()):
        with all_cols[i]:
            if st.button(f"📋 {title}", use_container_width=True, key=f"example_{i}"):
                st.session_state.example_loaded_text = text
                st.session_state.example_loaded_title = title
                st.rerun()
    
    if 'example_loaded_text' in st.session_state:
        st.markdown("---")
        st.success(f"✅ Loaded: **{st.session_state.example_loaded_title}**")
        st.code(st.session_state.example_loaded_text, language="text")
        st.info("👆 Copy this text and paste into the **Analyze Text** tab")

# FOOTER
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888; padding: 2rem;'>"
    "Built with ❤️ using Azure AI Services<br>"
    "<a href='https://github.com/AtamerErkal/azure-healthcare-nlp-analyzer' style='color: #4CAF50;'>🐙 GitHub Repository</a> • "
    "<a href='https://github.com/AtamerErkal' style='color: #4CAF50;'>👨‍💻 Atamer Erkal</a>"
    "</div>",
    unsafe_allow_html=True
)