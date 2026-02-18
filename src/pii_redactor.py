import json
import os
from datetime import datetime
from typing import Any, Dict, List

from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


class PIIRedactor:
    def __init__(self) -> None:
        load_dotenv()

        endpoint = os.getenv("LANGUAGE_ENDPOINT")
        key = os.getenv("LANGUAGE_KEY")

        if not endpoint or not key:
            raise ValueError("LANGUAGE_ENDPOINT and LANGUAGE_KEY must be set in the environment")

        self.client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    def detect_pii(self, text: str) -> List[Dict[str, Any]]:
        response = self.client.recognize_pii_entities([text])
        result = response[0]

        if getattr(result, "is_error", False):
            raise RuntimeError(f"Error from Text Analytics service: {result.error}")

        entities: List[Dict[str, Any]] = []
        for entity in result.entities:
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

    def redact_text(self, text: str, entities: List[Dict[str, Any]]) -> str:
        if not entities:
            return text

        sorted_entities = sorted(entities, key=lambda e: e["offset"])
        redacted_parts: List[str] = []
        current_index = 0

        for entity in sorted_entities:
            start = entity["offset"]
            length = entity["length"]

            if start < current_index:
                continue

            redacted_parts.append(text[current_index:start])
            redacted_parts.append(f"[{entity['category']}]")
            current_index = start + length

        redacted_parts.append(text[current_index:])
        return "".join(redacted_parts)

    def process_document(self, text: str) -> Dict[str, Any]:
        entities = self.detect_pii(text)
        redacted = self.redact_text(text, entities)
        categories = sorted({entity["category"] for entity in entities})

        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "original_text": text,
            "detected_entities": entities,
            "redacted_text": redacted,
            "entity_count": len(entities),
            "categories": categories,
        }

    def save_results(self, results: Dict[str, Any], filepath: str) -> None:
        directory = os.path.dirname(filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)


sample_text = """
Patient: John Smith, Date of Birth: March 15, 1985, SSN: 123-45-6789.
Admitted on January 20, 2024 at Memorial Hospital.
Chief Complaint: Type 2 Diabetes and Hypertension.
Medications: Metformin 500mg BID, Lisinopril 10mg QD.
Contact: john.smith@email.com, Phone: +1-555-0123.
"""


if __name__ == "__main__":
    try:
        redactor = PIIRedactor()
        result = redactor.process_document(sample_text)

        print("=" * 60)
        print("ORIGINAL TEXT:")
        print(result["original_text"])

        print("\n" + "=" * 60)
        print("DETECTED PII ENTITIES:")
        for entity in result["detected_entities"]:
            print(
                f"  - {entity['text']} ({entity['category']}) "
                f"[confidence: {entity['confidence_score']:.2f}]"
            )

        print("\n" + "=" * 60)
        print("REDACTED TEXT:")
        print(result["redacted_text"])

        print("\n" + "=" * 60)
        print(f"Total PII entities found: {result['entity_count']}")
        print(f"Categories: {', '.join(result['categories'])}")

        redactor.save_results(result, "data/pii_results.json")
        print("\nResults saved to data/pii_results.json")
    except Exception as exc:
        print(f"\nError while running PII redaction: {exc}")
