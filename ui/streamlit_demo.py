import streamlit as st
import sys
import os

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

# PROFESSIONAL CSS - Dark mode + Modern design
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
    
    .medical-entity {
        background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
        border-left: 4px solid #1976d2;
    }
    
    .pii-entity {
        background: linear-gradient(135deg, #4a1515 0%, #6d1f1f 100%);
        border-left: 4px solid #d32f2f;
    }
    
    .healthcare-entity {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
        border-left: 4px solid #4CAF50;
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
    
    /* Success/Info boxes */
    .success-box {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
        padding: 1.2rem;
        border-radius: 8px;
        color: white;
        margin: 1rem 0;
    }
    
    /* Language flag icons */
    .flag-icon {
        font-size: 2rem;
        margin-right: 0.5rem;
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

st.markdown('<div class="main-header">🏥 Healthcare NLP Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Advanced Medical Text Processing Platform</div>', unsafe_allow_html=True)

# Add feature badges
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
✅ **Translate** to 100+ languages  
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
- 100+ languages supported
- Context-aware translation
- Medical terminology preserved
- EN ↔ TR, DE, FR, ES, etc.
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
- 🌐 Azure Translator (100+ languages)
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
# TAB 1: ANALYZE TEXT (Existing - Enhanced)
# ============================================================================
with tab1:
    st.subheader("🔍 Medical Text Analysis & PII Redaction")

    col_input, col_output = st.columns(2)

    with col_input:
        st.markdown("**📄 Original Medical Text:**")
        text_input = st.text_area(
            "Paste clinical notes, patient records, or medical documentation:",
            height=350,
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

            with col_output:
                st.markdown("**🔒 Redacted Text (PHI Removed):**")
                st.text_area(
                    "",
                    value=result["redacted_text"],
                    height=350,
                    label_visibility="collapsed",
                    key="redacted_output"
                )

            # Metrics
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

            # Entities display
            st.markdown("---")
            st.subheader("🎯 Detected Entities Breakdown")

            ent_col1, ent_col2, ent_col3 = st.columns(3)

            with ent_col1:
                st.markdown("**🏥 Healthcare Terms (Preserved):**")
                if result["healthcare_entities"]:
                    for e in result["healthcare_entities"]:
                        st.markdown(
                            f'<div class="entity-box healthcare-entity">'
                            f'<strong>{e["text"]}</strong><br>'
                            f'<span style="color: #81C784;">📋 {e["category"]}</span> • '
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
                        st.markdown(
                            f'<div class="entity-box medical-entity">'
                            f'<strong>{e["text"]}</strong><br>'
                            f'<span style="color: #64B5F6;">📌 {e["category"]}</span> • '
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
                            f'<div class="entity-box pii-entity">'
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
# TAB 2: TRANSLATE (ENHANCED WITH 7 LANGUAGES!)
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
            index=1  # Default to Turkish
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
                    # Copy to clipboard hint
                    st.info("💡 Click text above to select and copy")
        else:
            st.warning("⚠️ Please enter text to translate")
    
    # Quick examples
    st.markdown("---")
    st.markdown("**⚡ Quick Translation Examples:**")
    
    quick_examples = {
        "💊 Medication": "Patient prescribed Metformin 500mg twice daily and Lisinopril 10mg once daily.",
        "🩺 Diagnosis": "Patient diagnosed with Type 2 Diabetes Mellitus and essential hypertension.",
        "📊 Vitals": "Blood pressure: 140/90 mmHg. Heart rate: 82 bpm. Temperature: 36.9°C."
    }
    
    cols = st.columns(3)
    for i, (title, text) in enumerate(quick_examples.items()):
        with cols[i]:
            if st.button(title, use_container_width=True, key=f"quick_translate_{i}"):
                st.session_state.quick_translate_text = text
                st.rerun()


# ============================================================================
# TAB 3: VOICE TRANSCRIPTION (ENHANCED WITH RECORDING!)
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
                # Save temporarily
                with open("temp_audio.wav", "wb") as f:
                    f.write(audio_file.read())
                
                with st.spinner("🔄 Transcribing with Azure Speech..."):
                    result = st.session_state.speech.audio_to_text("temp_audio.wav")
                
                # Clean up
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
    
    else:  # Live Recording Mode
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
# TAB 4: BATCH PROCESSING (FIXED - was in tab2 by mistake!)
# ============================================================================
with tab4:  # Changed from tab2 to tab4
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
                    # Read file based on type
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
            
            # Summary
            st.success(f"✅ Processed {len(batch_results)} file(s) successfully!")
            
            total_entities = sum(r["result"]["total_entities"] for r in batch_results)
            total_healthcare = sum(len(r["result"]["healthcare_entities"]) for r in batch_results)
            total_pii = sum(len(r["result"]["pii_entities"]) for r in batch_results)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Entities", total_entities)
            col2.metric("Healthcare Terms", total_healthcare)
            col3.metric("PII Redacted", total_pii)
            
            # Individual results
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
# TAB 5: EXAMPLES (FIXED!)
# ============================================================================
with tab5:
    st.subheader("📖 Example Medical Texts")
    st.markdown("Click to load examples and test the analyzer:")

    examples = {
        "Annual Checkup": """Annual checkup: Linda Martinez, Age 45, BMI 28.5.
Labs: HbA1c 6.2% (prediabetic range), LDL 145 mg/dL.
Recommendations: Lifestyle modification, recheck in 6 months.
Email: lmartinez@email.com, Phone: +1-555-4567.""",

        "Emergency Visit": """Emergency visit: David Chen, DOB 11/05/1990.
Presenting: Laceration to right forearm, 4cm length.
Procedure: Wound irrigation, closure with 8 sutures.
Vitals: BP 118/76, HR 82, Temp 36.9°C.
Discharge: Cephalexin 500mg TID x 7 days.
Follow-up in 5 days.""",

        "Hospital Admission": """Patient: John Smith, Date of Birth: March 15, 1985, SSN: 123-45-6789.
Admitted on January 20, 2024 at Memorial Hospital.
Chief Complaint: Type 2 Diabetes and Hypertension.
Vitals: BP 152/94, HR 88, BMI 31.2, SpO2 96%
Medications: Metformin 500mg BID, Lisinopril 10mg QD.
Contact: john.smith@email.com, Phone: +1-555-0123."""
    }

    cols = st.columns(3)
    for i, (title, text) in enumerate(examples.items()):
        with cols[i]:
            if st.button(f"📋 {title}", use_container_width=True, key=f"example_{i}"):
                # Use a different session state key
                st.session_state.example_loaded_text = text
                st.session_state.example_loaded_title = title
                st.rerun()
    
    # Show loaded example
    if 'example_loaded_text' in st.session_state:
        st.success(f"✅ Loaded: {st.session_state.example_loaded_title}")
        st.code(st.session_state.example_loaded_text, language="text")
        st.info("👆 Copy this text and paste into the **Analyze Text** tab")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888; padding: 2rem;'>"
    "Built with ❤️ using Azure AI Services<br>"
    "<a href='https://github.com/AtamerErkal/azure-healthcare-nlp-analyzer' style='color: #4CAF50;'>🐙 GitHub Repository</a> • "
    "<a href='https://github.com/AtamerErkal' style='color: #4CAF50;'>👨‍💻 Atamer Erkal</a>"
    "</div>",
    unsafe_allow_html=True
)