import os

from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def main() -> None:
    load_dotenv()

    endpoint = os.getenv("LANGUAGE_ENDPOINT")
    key = os.getenv("LANGUAGE_KEY")

    if not endpoint or not key:
        raise ValueError("LANGUAGE_ENDPOINT and LANGUAGE_KEY must be set in the environment")

    print(f"Endpoint: {endpoint}")
    print(f"Key (first 10 chars): {key[:10]}...")

    client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    documents = [
        "The patient has a history of diabetes mellitus type 2 and essential hypertension.",
        "Prescribed metformin 500mg twice daily and lisinopril 10mg once daily.",
    ]

    response = client.recognize_entities(documents)

    for idx, doc in enumerate(response, start=1):
        if getattr(doc, "is_error", False):
            print(f"\nDocument {idx} returned an error: {doc.error}")
            continue

        print(f"\nDocument {idx} entities:")
        for entity in doc.entities:
            print(f"- Text: {entity.text} | Category: {entity.category}")


if __name__ == "__main__":
    try:
        main()
        print("\nAzure Text Analytics entity recognition completed successfully.")
    except Exception as exc:
        print(f"\nError while testing Azure Text Analytics connection: {exc}")
