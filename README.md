# PDF Processing & Search System

A comprehensive system for processing PDFs, generating embeddings, and creating intelligent search capabilities using Google Generative AI and Vespa search engine.

## 🎯 Overview

This system converts PDF documents into searchable content by:
- Extracting visual content (images) and text from PDFs
- Generating semantic embeddings using Google's Generative AI
- Indexing documents in Vespa for fast, intelligent search
- Providing both text-based and semantic similarity search

## 🏗️ Architecture

```
PDFs → PDF Processor → Model Handler → Vespa Handler → Search Interface
         ↓              ↓               ↓
    Images + Text   Embeddings    Search Index
```

### Components

- **PDF Processor**: Converts PDFs to images and extracts text
- **Model Handler**: Generates embeddings using Google Generative AI
- **Vespa Handler**: Manages search index and document storage
- **Main Script**: Orchestrates the entire processing pipeline

## 📋 Prerequisites

### System Requirements
- Python 3.8+
- Poppler (for PDF processing)
- Internet connection (for Google AI API)

### Dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- `google-generativeai`
- `pyvespa`
- `pdf2image`
- `Pillow`
- `requests`
- `numpy`

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd pdf-processing-system
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Poppler

#### Ubuntu/Debian
```bash
sudo apt-get install poppler-utils
```

#### macOS
```bash
brew install poppler
```

#### Windows
Download from: https://poppler.freedesktop.org/

### 4. Set up Google AI API
1. Get API key from Google AI Studio
2. Set environment variable:
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

## 📁 Project Structure

```
pdf-processing-system/
├── src/
│   ├── pdf_processor.py      # PDF processing logic
│   ├── model_handler.py      # AI model integration
│   ├── vespa_handler.py      # Vespa search engine
│   ├── config.py            # Configuration settings
│   └── utils.py             # Utility functions
├── main.py                  # Main execution script
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## ⚙️ Configuration

### config.py
```python
SAMPLE_PDFS = [
    {
        "id": "doc1",
        "title": "Sample Document 1",
        "url": "https://example.com/document1.pdf",
        "author": "Author Name"
    },
    # Add more PDFs here
]

# Vespa configuration
VESPA_APP_NAME = "pdf-search"
VESPA_TENANT = "default"

# Model configuration
EMBEDDING_MODEL = "models/embedding-001"
```

## 🚀 Usage

### Basic Usage
```bash
python main.py
```

### Step-by-Step Process

1. **Verify Setup**: System checks Poppler installation
2. **Initialize Components**: Creates processor, model, and search handlers
3. **Deploy Vespa**: Sets up search infrastructure
4. **Process PDFs**: For each PDF in configuration:
   - Downloads and converts to images
   - Extracts text content
   - Generates embeddings
5. **Index Documents**: Stores processed content in Vespa
6. **Test Search**: Runs sample search query

### Sample Output
```
INFO - Verifying Poppler setup...
INFO - Initializing handlers...
INFO - Deploying Vespa application...
INFO - Processing PDF: Sample Document 1
INFO - Extracted 15 pages
INFO - Generated embeddings for all pages
INFO - Indexing documents in Vespa...
INFO - Successfully indexed: Sample Document 1
INFO - Successfully processed and indexed all PDFs!
INFO - Performing sample search: Composition of the LoTTE benchmark
INFO - Search results: {...}
```

## 🔍 Search Capabilities

### Search Types

1. **Text Search**: Traditional keyword matching
2. **Semantic Search**: AI-powered similarity matching
3. **Visual Search**: Understanding charts, diagrams, and layouts

### Search Example
```python
# In your code
query = "machine learning algorithms"
query_embedding = model_handler.generate_embeddings([query])[0]
results = vespa_handler.search(query, query_embedding)
```

## 📊 Performance Considerations

### Processing Speed
- PDF conversion: ~1-2 seconds per page
- Embedding generation: ~0.5-1 second per page
- Indexing: ~0.1 seconds per document

### Memory Usage
- Images: ~1-5MB per page
- Embeddings: ~3KB per embedding
- Total: Plan for ~10MB per PDF page

### Scaling
- Batch processing: Process multiple PDFs concurrently
- Distributed processing: Use multiple Vespa nodes
- Caching: Store embeddings to avoid regeneration

## 🛠️ Troubleshooting

### Common Issues

#### Poppler Not Found
```
Error: Poppler setup verification failed
```
**Solution**: Install Poppler and ensure it's in PATH

#### Google AI API Issues
```
Error: API key not found
```
**Solution**: Set `GOOGLE_API_KEY` environment variable

#### Memory Issues
```
Error: Out of memory during processing
```
**Solution**: Process PDFs in smaller batches or increase system memory

#### Vespa Connection Issues
```
Error: Cannot connect to Vespa
```
**Solution**: Check Vespa deployment and network connectivity

### Debug Mode
Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔒 Security Considerations

- Store API keys securely (use environment variables)
- Validate PDF URLs before processing
- Implement rate limiting for API calls
- Consider data privacy for sensitive documents

## 📈 Monitoring & Logging

### Log Levels
- `INFO`: General processing information
- `WARNING`: Non-critical issues
- `ERROR`: Processing failures
- `DEBUG`: Detailed debugging information

### Metrics to Monitor
- Processing time per PDF
- API call success rates
- Search query performance
- System resource usage

## 🚀 Advanced Features

### Batch Processing
```python
# Process multiple PDFs concurrently
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(process_pdf, pdf) for pdf in pdfs]
```

### Custom Embeddings
```python
# Use different embedding models
model_handler = ModelHandler(model_name="custom-model")
```

### Search Filtering
```python
# Filter search results
results = vespa_handler.search(
    query, 
    query_embedding, 
    filters={"author": "specific_author"}
)
```

## 📝 API Reference

### PDFProcessor
```python
class PDFProcessor:
    def get_pdf_images(self, url: str) -> Tuple[List[Image], List[str]]
    def extract_text(self, pdf_path: str) -> List[str]
```

### ModelHandler
```python
class ModelHandler:
    def generate_embeddings(self, content: List[Any]) -> List[np.ndarray]
    def configure_model(self, model_name: str) -> None
```

### VespaHandler
```python
class VespaHandler:
    def deploy(self) -> None
    def prepare_document(self, pdf_data: Dict) -> Dict
    def index_documents(self, documents: List[Dict]) -> None
    def search(self, query: str, embedding: np.ndarray) -> List[Dict]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check the troubleshooting section
- Review logs for error details
- Open an issue on GitHub
- Contact the development team

## 📚 Additional Resources

- [Google AI Documentation](https://ai.google.dev/)
- [Vespa Documentation](https://docs.vespa.ai/)
- [Poppler Documentation](https://poppler.freedesktop.org/)
- [PDF Processing Best Practices](https://example.com/pdf-best-practices)

---

**Last Updated**: July 2025
**Version**: 1.0.0
