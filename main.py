from src.pdf_processor import PDFProcessor
from src.model_handler import ModelHandler
from src.vespa_handler import VespaHandler
from src.config import SAMPLE_PDFS
from src.utils import verify_poppler_setup
import google.generativeai as genai


def main():
    try:
        # Verify Poppler setup
        if not verify_poppler_setup():
            print("Poppler setup verification failed. Please check configuration.")
            exit(1)

        # Initialize handlers
        pdf_processor = PDFProcessor()
        model_handler = ModelHandler()
        vespa_handler = VespaHandler()

        # Deploy Vespa application
        print("Deploying Vespa application...")
        vespa_handler.deploy()

        # Process PDFs
        processed_pdfs = []
        for pdf in SAMPLE_PDFS:
            print(f"Processing PDF: {pdf['title']}")

            # Get images and texts
            images, texts = pdf_processor.get_pdf_images(pdf["url"])
            print(f"Extracted {len(images)} pages")

            # Generate embeddings
            embeddings = model_handler.generate_embeddings(images)
            print(f"Generated embeddings for all pages")

            # Prepare document for Vespa
            processed_pdf = pdf.copy()
            processed_pdf.update({
                "images": images,
                "texts": texts,
                "embeddings": embeddings
            })
            processed_pdfs.append(processed_pdf)

        # Index documents in Vespa
        print("Indexing documents in Vespa...")
        for pdf in processed_pdfs:
            vespa_doc = vespa_handler.prepare_document(pdf)
            vespa_handler.index_documents([vespa_doc])

        print("Successfully processed and indexed all PDFs!")

        # Example search
        query = "Composition of the LoTTE benchmark"
        query_embedding = model_handler.generate_embeddings([query])[0]
        search_results = vespa_handler.search(query, query_embedding)
        print(f"Search results: {search_results}")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    main()