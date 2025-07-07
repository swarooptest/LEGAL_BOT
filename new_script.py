from src.pdf_processor import PDFProcessor
from src.model_handler import ModelHandler
from src.vespa_handler import VespaHandler
from src.config import SAMPLE_PDFS
from src.utils import verify_poppler_setup
import google.generativeai as genai
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_single_pdf(pdf: Dict[str, Any], pdf_processor: PDFProcessor, model_handler: ModelHandler) -> Dict[str, Any]:
    """Process a single PDF and return the processed document."""
    try:
        logger.info(f"Processing PDF: {pdf['title']}")
        
        # Get images and texts
        images, texts = pdf_processor.get_pdf_images(pdf["url"])
        logger.info(f"Extracted {len(images)} pages")
        
        # Generate embeddings
        embeddings = model_handler.generate_embeddings(images)
        logger.info(f"Generated embeddings for all pages")
        
        # Prepare document
        processed_pdf = pdf.copy()
        processed_pdf.update({
            "images": images,
            "texts": texts,
            "embeddings": embeddings
        })
        
        return processed_pdf
        
    except Exception as e:
        logger.error(f"Error processing PDF {pdf.get('title', 'Unknown')}: {str(e)}")
        raise

def index_documents(processed_pdfs: List[Dict[str, Any]], vespa_handler: VespaHandler) -> None:
    """Index all processed documents in Vespa."""
    logger.info("Indexing documents in Vespa...")
    
    for pdf in processed_pdfs:
        try:
            vespa_doc = vespa_handler.prepare_document(pdf)
            vespa_handler.index_documents([vespa_doc])
            logger.info(f"Successfully indexed: {pdf.get('title', 'Unknown')}")
        except Exception as e:
            logger.error(f"Error indexing PDF {pdf.get('title', 'Unknown')}: {str(e)}")
            raise

def perform_sample_search(model_handler: ModelHandler, vespa_handler: VespaHandler) -> None:
    """Perform a sample search to test the system."""
    try:
        query = "Composition of the LoTTE benchmark"
        logger.info(f"Performing sample search: {query}")
        
        query_embedding = model_handler.generate_embeddings([query])[0]
        search_results = vespa_handler.search(query, query_embedding)
        
        logger.info(f"Search results: {search_results}")
        
    except Exception as e:
        logger.error(f"Error during sample search: {str(e)}")
        raise

def main():
    """Main function to orchestrate the PDF processing pipeline."""
    try:
        # Verify Poppler setup
        logger.info("Verifying Poppler setup...")
        if not verify_poppler_setup():
            logger.error("Poppler setup verification failed. Please check configuration.")
            exit(1)
        
        # Initialize handlers
        logger.info("Initializing handlers...")
        pdf_processor = PDFProcessor()
        model_handler = ModelHandler()
        vespa_handler = VespaHandler()
        
        # Deploy Vespa application
        logger.info("Deploying Vespa application...")
        vespa_handler.deploy()
        
        # Process PDFs
        processed_pdfs = []
        for pdf in SAMPLE_PDFS:
            try:
                processed_pdf = process_single_pdf(pdf, pdf_processor, model_handler)
                processed_pdfs.append(processed_pdf)
            except Exception as e:
                logger.error(f"Failed to process PDF {pdf.get('title', 'Unknown')}: {str(e)}")
                # Decide whether to continue or stop based on your requirements
                continue
        
        if not processed_pdfs:
            logger.error("No PDFs were successfully processed. Exiting.")
            exit(1)
        
        # Index documents in Vespa
        index_documents(processed_pdfs, vespa_handler)
        
        logger.info("Successfully processed and indexed all PDFs!")
        
        # Example search
        perform_sample_search(model_handler, vespa_handler)
        
    except Exception as e:
        logger.error(f"Critical error occurred: {str(e)}")
        raise
    finally:
        # Clean up resources if needed
        logger.info("Cleaning up resources...")
        # Add any cleanup code here if your handlers need it
        
if __name__ == "__main__":
    main()