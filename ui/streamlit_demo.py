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

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .entity-box {
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.3rem 0;
    }
    .medical-entity {
        background-color: #e3f2fd;
        border-left: 4px solid #1976d2;
    }
    .pii-entity {
        background-color: #ffebee;
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

with st.sidebar:
    st.title("ℹ️ About")
    st.info("""
**Healthcare NLP Analyzer** uses Azure AI Language to intelligently process medical text.

**What Gets Preserved:**
✅ Vital signs (BP, HR, Temp, SpO2)
✅ Lab values (HbA1c, LDL, WBC, CRP)
✅ Medications and dosages
✅ Clinical measurements (BMI, weight)
✅ Medical terminology

**What Gets Redacted:**
🔒 Patient names
🔒 Email addresses
🔒 Phone numbers
🔒 Social Security Numbers
🔒 Specific dates (preserved as [DATE])
    """)

    st.markdown("---")
    st.markdown("**Tech Stack:**")
    st.markdown("- Azure AI Language")
    st.markdown("- Python 3.10")
    st.markdown("- Streamlit")
    st.markdown("---")
    st.markdown("**GitHub:** [View Project](https://github.com/AtamerErkal/azure-healthcare-nlp-analyzer)")

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
                st.markdown("**Healthcare Terms:**")
                if result["healthcare_entities"]:
                    for e in result["healthcare_entities"]:
                        st.markdown(
                            f'<div class="entity-box medical-entity">'
                            f'<strong>{e["text"]}</strong> '
                            f'<span style="color: #1976d2;">({e["category"]})</span> '
                            f'<span style="color: #666;">Confidence: {e["confidence_score"]:.0%}</span>'
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
                            f'<span style="color: #1976d2;">({e["category"]})</span> '
                            f'<span style="color: #666;">Confidence: {e["confidence_score"]:.0%}</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.info("No medical entities detected")

            with ent_col3:
                st.markdown("**PII (Contact Info - Redacted):**")
                if result["pii_entities"]:
                    for e in result["pii_entities"]:
                        st.markdown(
                            f'<div class="entity-box pii-entity">'
                            f'<strong>{e["text"]}</strong> '
                            f'<span style="color: #d32f2f;">({e["category"]})</span> '
                            f'<span style="color: #666;">Confidence: {e["confidence_score"]:.0%}</span>'
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

with tab2:
    st.subheader("📊 Batch Upload")
    st.markdown("Upload one or more `.txt` files to redact in batch. Each file is processed and you can download the redacted versions.")
    uploaded_files = st.file_uploader(
        "Choose .txt files",
        type=["txt"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    if uploaded_files:
        if st.button("🔄 Process All Files", type="primary", use_container_width=True):
            batch_results = []
            progress = st.progress(0)
            for i, f in enumerate(uploaded_files):
                text = f.read().decode("utf-8")
                doc_result = st.session_state.redactor.process_document(text)
                batch_results.append({
                    "filename": f.name,
                    "result": doc_result,
                })
                progress.progress((i + 1) / len(uploaded_files))
            progress.empty()

            st.success(f"Processed {len(batch_results)} file(s).")
            total_entities = sum(r["result"]["total_entities"] for r in batch_results)
            st.metric("Total entities redacted (all files)", total_entities)

            for r in batch_results:
                with st.expander(f"📄 {r['filename']} — {r['result']['total_entities']} entities"):
                    st.text_area("Redacted text", value=r["result"]["redacted_text"], height=200, label_visibility="collapsed")
                    st.download_button(
                        label=f"📥 Download redacted_{r['filename']}",
                        data=r["result"]["redacted_text"],
                        file_name=f"redacted_{r['filename']}",
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
