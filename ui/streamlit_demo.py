import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.pii_redactor import PIIRedactor
import json

st.set_page_config(
    page_title="Healthcare NLP Analyzer",
    page_icon="🏥",
    layout="wide"
)

# IMPROVED CSS - Dark mode sidebar + better contrast
st.markdown("""
<style>
    /* Force dark background for sidebar */
    [data-testid="stSidebar"] {
        background-color: #1e1e1e !important;
    }
    
    /* Sidebar text styling */
    [data-testid="stSidebar"] .element-container {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #4CAF50 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    /* Info/Success boxes in sidebar */
    [data-testid="stSidebar"] .stAlert {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border: 1px solid #4CAF50 !important;
    }
    
    /* Main content styling */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #888;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Entity boxes */
    .entity-box {
        padding: 0.8rem;
        border-radius: 5px;
        margin: 0.4rem 0;
        background-color: #2d2d2d;
        border-left: 4px solid #4CAF50;
        color: #ffffff;
    }
    
    .medical-entity {
        background-color: #1a237e;
        border-left: 4px solid #1976d2;
    }
    
    .pii-entity {
        background-color: #4a1515;
        border-left: 4px solid #d32f2f;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🏥 Healthcare NLP Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Real-time PII detection with medical data preservation</div>', unsafe_allow_html=True)

if 'redactor' not in st.session_state:
    try:
        st.session_state.redactor = PIIRedactor()
        st.session_state.initialized = True
    except Exception as e:
        st.error(f"Failed to initialize: {e}")
        st.stop()

# IMPROVED SIDEBAR
with st.sidebar:
    st.title("ℹ️ About")
    
    st.markdown("### 🎯 What Is This?")
    st.info("""
**Healthcare NLP Analyzer** automatically processes medical text to:

✅ **Extract** clinical information (medications, diagnoses, vitals)  
✅ **Protect** patient privacy (redact names, contact info)  
✅ **Preserve** medical data (lab values, measurements)
    """)
    
    st.markdown("---")
    st.markdown("### 📋 How To Use")
    st.success("""
1. **Upload or paste** medical text (clinical notes, discharge summaries)
2. **Click "Analyze"** — AI processes in real-time
3. **Review results** — see detected entities and redacted text
4. **Download** redacted version for safe sharing
    """)
    
    st.markdown("---")
    st.markdown("### 🔍 What AI Detects")
    
    st.markdown("**🏥 Healthcare Terms (Preserved):**")
    st.markdown("""
- 💊 Medications & dosages
- 🩺 Diagnoses & symptoms
- 📊 Vital signs & lab values
- 🦴 Body parts & anatomy
- 💉 Treatments & procedures
    """)
    
    st.markdown("**🔒 PII (Redacted):**")
    st.markdown("""
- 👤 Patient names → `[PERSON]`
- 📧 Email addresses → `[EMAIL]`
- 📞 Phone numbers → `[PHONE]`
- 🆔 SSN/IDs → `[SSN]`
- 📅 Specific dates → `[DATE]`
    """)
    
    st.markdown("---")
    st.markdown("### 💡 Use Cases")
    st.markdown("""
- **Clinical Research:** De-identify patient records
- **Data Sharing:** Remove PHI for collaboration
- **Quality Assurance:** Review clinical documentation
- **Training Data:** Prepare datasets for ML models
- **Compliance:** HIPAA-ready redaction
    """)
    
    st.markdown("---")
    st.markdown("### 🛠️ Tech Stack")
    st.markdown("""
- **Azure AI Language** (Healthcare Text Analytics)
- **Python 3.10**
- **Streamlit** (Web UI)
    """)
    
    st.markdown("---")
    st.markdown("### 🔗 Links")
    st.markdown("""
- [GitHub Repository](https://github.com/AtamerErkal/azure-healthcare-nlp-analyzer)
- [Azure AI Docs](https://learn.microsoft.com/en-us/azure/ai-services/language-service/)
    """)

tab1, tab2, tab3 = st.tabs(["📝 Analyze Text", "📊 Batch Upload", "📖 Examples"])

with tab1:
    st.subheader("Enter Medical Text")

    col_input, col_output = st.columns(2)

    with col_input:
        st.markdown("**🔓 Original Text:**")
        text_input = st.text_area(
            "Paste medical notes, patient records, or clinical documentation:",
            height=300,
            placeholder="""Example:
Patient: Sarah Johnson, DOB: 03/15/1985
Chief Complaint: Type 2 Diabetes
Vitals: BP 142/88, HR 78, BMI 29.3
Labs: HbA1c 7.2%, LDL 156 mg/dL
Medications: Metformin 1000mg BID
Contact: sjohnson@email.com, +1-555-1234""",
            label_visibility="collapsed"
        )

    if st.button("🔍 Analyze & Redact", type="primary", use_container_width=True):
        if text_input.strip():
            with st.spinner("🔄 Processing with Azure AI..."):
                result = st.session_state.redactor.process_document(text_input)

            with col_output:
                st.markdown("**🔒 Redacted Text:**")
                st.text_area(
                    "",
                    value=result["redacted_text"],
                    height=300,
                    label_visibility="collapsed"
                )

            # Metrics row - include healthcare
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            with metric_col1:
                st.metric("Total Entities", result["total_entities"])
            with metric_col2:
                st.metric("Healthcare Terms", len(result["healthcare_entities"]))
            with metric_col3:
                st.metric("Medical Entities", len(result["medical_entities"]))
            with metric_col4:
                st.metric("PII Found", len(result["pii_entities"]))

            # Entities display - 3 columns
            st.markdown("---")
            st.subheader("🎯 Detected Entities")

            ent_col1, ent_col2, ent_col3 = st.columns(3)

            with ent_col1:
                st.markdown("**Healthcare Terms (Preserved):**")
                if result["healthcare_entities"]:
                    for e in result["healthcare_entities"]:
                        st.markdown(
                            f'<div class="entity-box medical-entity">'
                            f'<strong>{e["text"]}</strong> '
                            f'<span style="color: #64B5F6;">({e["category"]})</span> '
                            f'<span style="color: #BDBDBD;">Confidence: {e["confidence_score"]:.0%}</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.info("No healthcare terms detected")

            with ent_col2:
                st.markdown("**Medical Entities (Redacted):**")
                if result["medical_entities"]:
                    for e in result["medical_entities"]:
                        st.markdown(
                            f'<div class="entity-box medical-entity">'
                            f'<strong>{e["text"]}</strong> '
                            f'<span style="color: #64B5F6;">({e["category"]})</span> '
                            f'<span style="color: #BDBDBD;">Confidence: {e["confidence_score"]:.0%}</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.info("No medical entities detected")

            with ent_col3:
                st.markdown("**PII (Contact - Redacted):**")
                if result["pii_entities"]:
                    for e in result["pii_entities"]:
                        st.markdown(
                            f'<div class="entity-box pii-entity">'
                            f'<strong>{e["text"]}</strong> '
                            f'<span style="color: #EF5350;">({e["category"]})</span> '
                            f'<span style="color: #BDBDBD;">Confidence: {e["confidence_score"]:.0%}</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.info("No PII detected")

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
            st.warning("⚠️ Please enter some text to analyze.")

# IMPROVED BATCH TAB - PDF + DOCX support
with tab2:
    st.subheader("📊 Batch Processing")
    st.markdown("Upload multiple files (`.txt`, `.pdf`, `.docx`) to process in batch. Each file is analyzed and you can download redacted versions.")
    
    uploaded_files = st.file_uploader(
        "Choose files",
        type=["txt", "pdf", "docx"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        if st.button("🔄 Process All Files", type="primary", use_container_width=True):
            batch_results = []
            progress = st.progress(0)
            
            for i, f in enumerate(uploaded_files):
                try:
                    # Read based on file type
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
                            st.error("PyPDF2 not installed. Run: `pip install PyPDF2`")
                            continue
                    
                    elif f.name.endswith('.docx'):
                        try:
                            import docx
                            from io import BytesIO
                            doc = docx.Document(BytesIO(f.read()))
                            text = "\n".join([para.text for para in doc.paragraphs])
                        except ImportError:
                            st.error("python-docx not installed. Run: `pip install python-docx`")
                            continue
                    
                    else:
                        st.warning(f"Unsupported file type: {f.name}")
                        continue
                    
                    doc_result = st.session_state.redactor.process_document(text)
                    batch_results.append({
                        "filename": f.name,
                        "result": doc_result,
                    })
                
                except Exception as e:
                    st.error(f"Error processing {f.name}: {e}")
                
                progress.progress((i + 1) / len(uploaded_files))
            
            progress.empty()

            st.success(f"Processed {len(batch_results)} file(s).")
            total_entities = sum(r["result"]["total_entities"] for r in batch_results)
            st.metric("Total entities detected (all files)", total_entities)

            for r in batch_results:
                with st.expander(f"📄 {r['filename']} — {r['result']['total_entities']} entities"):
                    st.text_area("Redacted text", value=r["result"]["redacted_text"], height=200, label_visibility="collapsed")
                    
                    # Separate filename and extension
                    name_parts = r['filename'].rsplit('.', 1)
                    base_name = name_parts[0]
                    
                    st.download_button(
                        label=f"📥 Download {base_name}_REDACTED.txt",
                        data=r["result"]["redacted_text"],
                        file_name=f"{base_name}_REDACTED.txt",
                        mime="text/plain",
                        key=f"dl_{r['filename']}"
                    )

with tab3:
    st.subheader("📖 Example Medical Texts")
    st.markdown("Click to load example and test the analyzer:")

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

    for title, text in examples.items():
        if st.button(f"📋 {title}", use_container_width=True, key=f"ex_{title}"):
            st.session_state.example_text = text
            st.rerun()

    if 'example_text' in st.session_state:
        st.markdown("**Loaded Example:**")
        st.code(st.session_state.example_text, language="text")
        st.info("👆 Copy this text and paste it in the 'Analyze Text' tab")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Built with ❤️ using Azure AI Services | "
    "<a href='https://github.com/AtamerErkal/azure-healthcare-nlp-analyzer'>GitHub</a>"
    "</div>",
    unsafe_allow_html=True
)