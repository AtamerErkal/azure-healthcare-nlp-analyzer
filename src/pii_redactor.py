import os
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import json
from datetime import datetime
import glob


class PIIRedactor:
    def __init__(self) -> None:
        load_dotenv()

        endpoint = os.getenv("LANGUAGE_ENDPOINT")
        key = os.getenv("LANGUAGE_KEY")

        if not endpoint or not key:
            raise ValueError("LANGUAGE_ENDPOINT and LANGUAGE_KEY must be set in the environment")

        self.client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    def detect_healthcare_entities(self, text: str) -> list:
        """
        Detect healthcare-specific entities using Text Analytics for Health.
        Categories: MedicationName, Dosage, Diagnosis, BodyStructure, etc.
        """
        try:
            poller = self.client.begin_analyze_healthcare_entities(documents=[text])
            result = poller.result()

            entities: list = []
            for doc in result:
                if getattr(doc, "is_error", False):
                    continue
                for entity in doc.entities:
                    if entity.category in [
                        "MedicationName",
                        "Dosage",
                        "Diagnosis",
                        "SymptomOrSign",
                        "TreatmentName",
                        "ExaminationName",
                        "BodyStructure",
                        "MedicationClass",
                        "Frequency",
                        "RouteOrMode",
                        "ConditionQualifier",
                    ]:
                        entities.append({
                            "text": entity.text,
                            "category": entity.category,
                            "confidence_score": float(getattr(entity, "confidence_score", 1.0)),
                            "offset": int(entity.offset),
                            "length": int(entity.length),
                        })
            return entities
        except Exception as e:
            print(f"Healthcare entity detection error: {e}")
            return []

    def detect_medical_entities(self, text: str) -> list:
        """
        Detect person names and dates using general NER (for PII redaction).
        """
        try:
            response = self.client.recognize_entities(documents=[text], language="en")
            entities: list = []
            for doc in response:
                if getattr(doc, "is_error", False):
                    continue
                for entity in doc.entities:
                    if entity.category == "Person":
                        entities.append({
                            "text": entity.text,
                            "category": entity.category,
                            "confidence_score": float(entity.confidence_score),
                            "offset": int(entity.offset),
                            "length": int(entity.length),
                        })
                    elif entity.category == "DateTime":
                        # Only keep specific dates (with numbers), not durations or words like "Annual"
                        text_lower = entity.text.lower()
                        duration_patterns = [
                            "day", "days", "week", "weeks", "month", "months",
                            "year", "years", "hour", "hours", "minute", "minutes",
                        ]
                        is_duration = any(pattern in text_lower for pattern in duration_patterns)
                        if (
                            entity.confidence_score > 0.95
                            and any(char.isdigit() for char in entity.text)
                            and not is_duration
                        ):
                            entities.append({
                                "text": entity.text,
                                "category": entity.category,
                                "confidence_score": float(entity.confidence_score),
                                "offset": int(entity.offset),
                                "length": int(entity.length),
                            })
            return entities
        except Exception as exc:
            print(f"Error in medical entity detection: {exc}")
            return []

    def detect_contact_pii(self, text: str) -> list:
        """
        Detect contact PII ONLY (email, phone, SSN, IP, URL).
        """
        try:
            response = self.client.recognize_pii_entities(documents=[text], language="en")
            entities: list = []

            for doc in response:
                if getattr(doc, "is_error", False):
                    continue

                for entity in doc.entities:
                    if entity.category in [
                        "Email",
                        "PhoneNumber",
                        "USSocialSecurityNumber",
                        "IPAddress",
                        "URL",
                    ]:
                        entities.append(
                            {
                                "text": entity.text,
                                "category": entity.category,
                                "confidence_score": float(entity.confidence_score),
                                "offset": int(entity.offset),
                                "length": int(entity.length),
                            }
                        )

            return entities
        except Exception as exc:
            print(f"Error in PII detection: {exc}")
            return []

    def redact_text(self, text: str, medical_entities: list, pii_entities: list) -> str:
        """
        Redact text based on BOTH medical and PII entities.
        """
        redacted = text
        all_entities = medical_entities + pii_entities

        all_entities.sort(key=lambda x: x["offset"], reverse=True)

        for entity in all_entities:
            start = entity["offset"]
            end = start + entity["length"]

            category = entity["category"]
            if category == "Person":
                tag = "[PERSON]"
            elif category == "Location":
                tag = "[LOCATION]"
            elif category == "Organization":
                tag = "[ORGANIZATION]"
            elif category == "DateTime":
                tag = "[DATE]"
            elif category == "Email":
                tag = "[EMAIL]"
            elif category == "PhoneNumber":
                tag = "[PHONE]"
            elif category == "USSocialSecurityNumber":
                tag = "[SSN]"
            elif category == "IPAddress":
                tag = "[IP]"
            elif category == "URL":
                tag = "[URL]"
            else:
                continue

            redacted = redacted[:start] + tag + redacted[end:]

        return redacted

    def process_document(self, text: str) -> dict:
        healthcare_entities = self.detect_healthcare_entities(text)
        medical_entities = self.detect_medical_entities(text)
        pii_entities = self.detect_contact_pii(text)
        redacted_text = self.redact_text(text, medical_entities, pii_entities)

        return {
            "timestamp": datetime.now().isoformat(),
            "original_text": text,
            "healthcare_entities": healthcare_entities,
            "medical_entities": medical_entities,
            "pii_entities": pii_entities,
            "total_entities": len(healthcare_entities) + len(medical_entities) + len(pii_entities),
            "redacted_text": redacted_text,
        }

    def save_results(self, results: dict, filepath: str) -> None:
        os.makedirs("data", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

    def process_batch(self, input_dir: str, output_dir: str) -> dict:
        """Process multiple text files"""
        files = glob.glob(os.path.join(input_dir, "*.txt"))

        results = {
            "timestamp": datetime.now().isoformat(),
            "total_files": len(files),
            "total_entities": 0,
            "files_processed": [],
            "category_breakdown": {}
        }

        os.makedirs(output_dir, exist_ok=True)

        for filepath in files:
            filename = os.path.basename(filepath)
            print(f"\n📄 Processing: {filename}")

            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()

            doc_result = self.process_document(text)

            # Save redacted file
            output_path = os.path.join(output_dir, f"redacted_{filename}")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(doc_result["redacted_text"])

            # Update statistics
            entity_count = doc_result["total_entities"]
            results["total_entities"] += entity_count

            all_entities = (
                doc_result["healthcare_entities"]
                + doc_result["medical_entities"]
                + doc_result["pii_entities"]
            )

            file_result = {
                "filename": filename,
                "entity_count": entity_count,
                "categories": [e["category"] for e in all_entities]
            }
            results["files_processed"].append(file_result)

            # Count categories
            for entity in all_entities:
                cat = entity["category"]
                results["category_breakdown"][cat] = results["category_breakdown"].get(cat, 0) + 1

            print(f"  ✅ Found {entity_count} entities")

        return results


if __name__ == "__main__":
    import sys

    redactor = PIIRedactor()

    if len(sys.argv) > 1 and sys.argv[1] == "--batch":
        # Batch mode
        print("=" * 70)
        print("BATCH PROCESSING MODE")
        print("=" * 70)

        results = redactor.process_batch(
            input_dir="data/sample_texts",
            output_dir="data/redacted_texts"
        )

        print("\n" + "=" * 70)
        print("BATCH PROCESSING SUMMARY")
        print("=" * 70)
        print(f"Total files processed: {results['total_files']}")
        print(f"Total entities found: {results['total_entities']}")
        print(f"\nCategory Breakdown:")
        for category, count in sorted(results['category_breakdown'].items()):
            print(f"  - {category}: {count}")

        redactor.save_results(results, "data/batch_summary.json")
        print(f"\n✅ Summary saved to data/batch_summary.json")
        print(f"✅ Redacted files saved to data/redacted_texts/")

    else:
        # Single document mode (keep existing code)
        sample_text = """Annual checkup: Linda Martinez, Age 45, BMI 28.5.
Labs: HbA1c 6.2% (prediabetic range), LDL 145 mg/dL.
Recommendations: Lifestyle modification, recheck in 6 months.
Email: lmartinez@email.com, Phone: +1-555-4567."""

        result = redactor.process_document(sample_text)

        print("=" * 70)
        print("ORIGINAL TEXT:")
        print(result["original_text"])
        print("\n" + "=" * 70)
        print("DETECTED HEALTHCARE ENTITIES:")
        for entity in result["healthcare_entities"]:
            print(f"  - {entity['text']} ({entity['category']}) [confidence: {entity['confidence_score']:.2f}]")
        print("\n" + "=" * 70)
        print("DETECTED MEDICAL ENTITIES (For Redaction):")
        for entity in result["medical_entities"]:
            print(f"  - {entity['text']} ({entity['category']}) [confidence: {entity['confidence_score']:.2f}]")
        print("\n" + "=" * 70)
        print("DETECTED PII (Contact Info):")
        for entity in result["pii_entities"]:
            print(f"  - {entity['text']} ({entity['category']}) [confidence: {entity['confidence_score']:.2f}]")
        print("\n" + "=" * 70)
        print("REDACTED TEXT:")
        print(result["redacted_text"])
        print("\n" + "=" * 70)
        print(f"Total entities: {result['total_entities']}")
        redactor.save_results(result, "data/pii_results.json")
        print("\n✅ Results saved to data/pii_results.json")
