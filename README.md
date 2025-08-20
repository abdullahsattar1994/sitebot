# 🚀 SiteBot - AI Engineering Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6B35?style=flat)](https://www.trychroma.com/)

> **Revolutionary AI-powered document assistant designed for engineering professionals working in the field**
 | **Portfolio:** [Abdullah Sattar](https://linkedin.com/in/abdullahsattar)

---

## 🏗️ **The Problem: Engineering on Site**

Picture this: You're a **civil engineer on a construction site** at 6 AM. The contractor has questions about foundation specifications from a 200-page structural report. Your options?

❌ **Traditional approach:** Flip through hundreds of pages in muddy conditions  
❌ **Cloud AI tools:** Upload sensitive blueprints to external servers (security nightmare)  
❌ **Generic ChatPDF:** Misses technical context and engineering terminology  

✅ **SiteBot approach:** Ask "What's the minimum concrete strength for the foundation?" and get instant, accurate answers from your documents - **completely offline and secure**.

### **Why This Matters**
- **Field accessibility:** Works on tablets and mobile devices without internet
- **Data sovereignty:** Your blueprints never leave your device
- **Engineering-specific:** Understands technical specifications, measurements, and standards
- **Real-time decisions:** Instant answers prevent costly delays and mistakes

---

## 🧠 **Architecture & Technical Decisions**

### **Why ChromaDB Over Alternatives?**

| Feature | ChromaDB | Pinecone | Weaviate | FAISS |
|---------|----------|----------|----------|-------|
| **Local Processing** | ✅ | ❌ Cloud-only | ⚠️ Self-hosted | ✅ |
| **Data Privacy** | ✅ Complete | ❌ External servers | ⚠️ Complex setup | ✅ |
| **Ease of Setup** | ✅ Plug & play | ⚠️ API keys | ❌ Complex | ⚠️ Manual |
| **Metadata Filtering** | ✅ Rich queries | ✅ | ✅ | ❌ Limited |
| **Production Ready** | ✅ | ✅ | ✅ | ⚠️ Research-focused |

**Why ChromaDB wins for SiteBot:**
- **🔒 Zero external dependencies:** Perfect for sensitive engineering documents
- **⚡ Simple setup:** `pip install chromadb` and you're ready
- **📊 Rich metadata:** Filter by document type, page number, section  
- **🐳 Docker-friendly:** Easy containerization for field deployments

### **Why Qwen 2.5 Over Alternatives?**

| Model | Size | Speed | Engineering Knowledge | Local Deployment |
|-------|------|-------|---------------------|------------------|
| **Qwen 2.5:3b** | ✅ 3B | ⚡ Ultra-fast | ✅ Technical focus | ✅ Easy |
| GPT-4 | ❌ Cloud | ❌ API calls | ✅ Excellent | ❌ Impossible |
| Llama 2 | ⚠️ 7B+ | ⚠️ Slower | ⚠️ General purpose | ✅ Possible |
| Mistral | ⚠️ 7B+ | ⚠️ Slower | ⚠️ General purpose | ✅ Possible |

**Qwen 2.5 advantages:**
- **⚡ Efficient performance:** Runs well on consumer hardware
- **🌐 Multilingual:** Supports multiple languages
- **🔧 Instruction-following:** Good at understanding specific requests

---

## 🔄 **RAG Pipeline Architecture**

### **What is RAG (Retrieval-Augmented Generation)?**

RAG combines the best of both worlds:
1. **Retrieval:** Find relevant document chunks using semantic search
2. **Generation:** Use AI to synthesize information and answer questions

```
Document → Chunks → Embeddings → Vector Store → Similarity Search → Context + Query → AI Response
```

### **My RAG Implementation**

```python
class DocumentRAG:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("engineering_docs")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    def add_document(self, text: str, filename: str):
        # Smart chunking with overlap
        chunks = self.create_chunks(text, size=500, overlap=50)
        
        for chunk in chunks:
            embedding = self.embedder.encode([chunk])
            self.collection.add(
                embeddings=embedding.tolist(),
                documents=[chunk],
                metadatas=[{"filename": filename, "type": "text"}]
            )
    
    def search_documents(self, query: str, n_results: int = 3):
        query_embedding = self.embedder.encode([query])
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=n_results
        )
        return results['documents'][0]
```

**Key RAG Benefits:**
- **📚 Accurate context:** Always grounds responses in your actual documents
- **🎯 Relevant retrieval:** Finds the most pertinent information first
- **🔍 Explainable AI:** Can show which document sections informed the answer
- **📈 Scalable:** Performance stays consistent as document library grows

---

## ✂️ **Chunking Strategy**

### **Current Implementation: Simple Fixed-Size Chunking**

```python
def create_chunks(text: str, size: int = 500, overlap: int = 50):
    chunks = []
    for i in range(0, len(text), size - overlap):
        chunk = text[i:i + size]
        chunks.append(chunk)
    return chunks
```

**Why 500 characters with 50-character overlap?**
- **🧩 Preserves context:** Overlap prevents important phrases from being split
- **⚡ Fast processing:** Optimal size for embedding model performance
- **💾 Memory efficient:** Balances accuracy with resource usage

### **🚀 Future: Intelligent Semantic Chunking**

Planning to implement:
- **📄 Page-aware chunking:** Respect document structure and page boundaries
- **📋 Section-based splitting:** Use headings and document hierarchy
- **🔗 Sentence boundary preservation:** Never split mid-sentence
- **📊 Table extraction:** Special handling for technical specifications tables

```python
# Future implementation preview
def smart_chunk(document):
    sections = extract_sections(document)  # H1, H2, H3 hierarchy
    tables = extract_tables(document)      # Specification tables
    images = extract_images(document)      # Technical diagrams
    
    return {
        'text_chunks': section_aware_chunks(sections),
        'table_chunks': structured_table_data(tables),
        'image_descriptions': analyze_technical_diagrams(images)
    }
```

---

## 👁️ **Multimodal AI: The Future is Visual**

### **Current Status: Text-Only Processing**
SiteBot currently excels at text-based documents but the future is **multimodal**.

### **🎯 Planned Implementation: Qwen-VL + LLaVA Integration**

**Why multimodal matters for engineering:**
- **📐 Blueprint analysis:** "What's the beam spacing in this structural drawing?"
- **📊 Chart interpretation:** Extract data from performance graphs and charts
- **🔍 Photo documentation:** Analyze field photos against specification drawings
- **✍️ Handwritten notes:** Process field sketches and annotations

**Technical approach:**
```python
def analyze_multimodal_document(pdf_path):
    # Extract text (current)
    text = extract_pdf_text(pdf_path)
    
    # Extract images (future)
    images = extract_pdf_images(pdf_path)
    
    # Process with Qwen-VL (future)
    for image in images:
        description = qwen_vl.analyze(
            image=image,
            context=text,
            prompt="Analyze this engineering diagram and extract all technical specifications"
        )
        add_to_rag(description, metadata={'type': 'image', 'source': pdf_path})
```

**Timeline:** Multimodal capabilities coming in **Q1 2025**

---

## 🏗️ **Architecture Evolution: Monolith → Microservices**

### **Current: Monolithic Architecture**
```
FastAPI App
├── Document Processing
├── RAG System  
├── AI Chat
└── File Upload
```

**Benefits:** Simple deployment, easy development, minimal overhead

### **🚀 Future: Microservices Architecture**

```
API Gateway
├── Document Service (Python + PyMuPDF)
├── AI Service (Qwen + LLaVA)
├── Search Service (ChromaDB + embeddings)
├── Chat Service (FastAPI + WebSockets)
└── File Service (MinIO + metadata)
```

**Why microservices for SiteBot:**
- **📈 Independent scaling:** Scale AI processing separately from file uploads
- **🔧 Technology flexibility:** Use best tool for each service
- **🛡️ Fault isolation:** One service failure doesn't crash entire system
- **👥 Team development:** Multiple developers can work on different services

**Migration strategy:**
1. **Phase 1:** Extract document processing service
2. **Phase 2:** Separate AI inference service  
3. **Phase 3:** Split search and chat services
4. **Phase 4:** Add API gateway and service mesh

---

## 🧪 **Custom Testing Framework Development**

### **Why Build Our Own Testing Framework?**

**Current testing pain points:**
- Generic frameworks don't understand AI model outputs
- No built-in support for RAG pipeline testing
- Limited multimodal testing capabilities
- Engineering document validation needs custom logic

### **🎯 SiteBot Testing Framework Features**

```python
class SiteBotTestFramework:
    def test_rag_accuracy(self, test_cases):
        """Test RAG retrieval accuracy with engineering documents"""
        
    def test_ai_response_quality(self, query, expected_topics):
        """Validate AI responses contain required technical information"""
        
    def test_multimodal_processing(self, image_path, expected_elements):
        """Test image analysis accuracy for technical diagrams"""
        
    def benchmark_performance(self, concurrent_users, target_latency):
        """Load testing for field deployment scenarios"""
```

**Timeline:** Custom testing framework **Q2 2025**

---

## ⚡ **Scaling & Concurrency Challenges**

### **Current Limitations**
- **🔄 Single-threaded processing:** One document at a time
- **💾 Memory constraints:** Large PDFs may require more RAM
- **⏱️ Response latency:** Complex queries can take several seconds  
- **👥 User isolation:** Currently single-user focused

### **🚀 Planned Solutions**

**1. Async Processing Pipeline**
```python
async def process_document_async(file_path):
    async with aiofiles.open(file_path, 'rb') as f:
        content = await f.read()
    
    # Parallel processing
    text_task = asyncio.create_task(extract_text_async(content))
    image_task = asyncio.create_task(extract_images_async(content))
    
    text, images = await asyncio.gather(text_task, image_task)
    return combine_results(text, images)
```

**2. Intelligent Caching**
```python
@redis_cache(ttl=3600)
def search_documents(query: str):
    # Cache frequent queries for faster responses
    pass
```

**3. Horizontal Scaling Architecture**
```
Load Balancer
├── SiteBot Instance 1 (ChromaDB Replica 1)
├── SiteBot Instance 2 (ChromaDB Replica 2)  
└── SiteBot Instance N (ChromaDB Replica N)
```

**Timeline:** Scaling improvements **Q3 2025**

---

## 🚀 **Quick Start Guide**

### **Prerequisites**
- Python 3.11+
- Docker (optional)
- 8GB RAM minimum
- Ollama (for local AI models)

### **Option 1: Docker Setup (Recommended)**

```bash
# Clone the repository
git clone https://github.com/abdullahsattar1994/sitebot.git
cd sitebot

# Build and run with Docker
docker-compose up --build

# Access SiteBot
open http://localhost:8000
```

### **Option 2: Local Development Setup**

```bash
# Clone and setup
git clone https://github.com/abdullahsattar1994/sitebot.git
cd sitebot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install and start Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve

# Download Qwen model
ollama pull qwen2.5:3b

# Start SiteBot
python app/main1.py

# Open browser
open http://localhost:8000
```

### **Option 3: OpenAI Integration**

```bash
# Set OpenAI API key for enhanced vision capabilities
export OPENAI_API_KEY="your-api-key-here"

# Run with OpenAI integration
python app/main1.py
```

### **Testing Your Setup**

1. **Upload a test PDF:** Try with a technical document or engineering report
2. **Ask technical questions:** "What are the concrete specifications?" or "What's the load capacity?"
3. **Verify responses:** SiteBot should provide specific answers based on your document content

### **Troubleshooting**

**Common issues:**
- **Ollama not running:** Make sure `ollama serve` is active
- **Model not found:** Run `ollama pull qwen2.5:3b`
- **Port conflicts:** Change port in `main1.py` if 8000 is occupied
- **Memory issues:** Close other applications or upgrade to larger instance

---

## 🛣️ **Roadmap**

### **Q2 2025: Foundation** ✅
- [x] Basic RAG implementation
- [x] ChromaDB integration  
- [x] Qwen 2.5 integration
- [x] Web interface
- [x] Docker containerization

### **Q3 2025: Multimodal** 🚧
- [ ] Qwen-VL integration for image analysis
- [ ] LLaVA model integration
- [ ] Technical diagram understanding
- [ ] Blueprint specification extraction

### **Q4 2025: Enterprise** 📋
- [ ] Custom testing framework
- [ ] Smart chunking implementation
- [ ] Multi-tenant architecture
- [ ] Advanced security features

### **Q1 2026: Scale** 📈
- [ ] Microservices migration
- [ ] Horizontal scaling
- [ ] Performance optimization
- [ ] Enterprise deployment tools

### **Q2 2026: Innovation** 🚀
- [ ] Real-time collaboration
- [ ] Mobile app development
- [ ] Advanced AI agents
- [ ] Industry-specific models

---

## 🤝 **Contributing**

SiteBot is built for the engineering community. Contributions welcome!

### **Areas needing help:**
- **🧪 Testing:** Help build comprehensive test suites
- **📱 Mobile:** React Native app development
- **🔧 DevOps:** Kubernetes deployment configurations
- **📚 Documentation:** Technical writing and tutorials
- **🎨 UI/UX:** Interface improvements for field use

### **Getting started:**
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open pull request

---

## 📄 **License**

MIT License - see [LICENSE](LICENSE) for details.

---

## 👨‍💻 **About the Developer**

**Muhammad Abdullah Sattar** - Senior Software Engineer with 5+ years at Morgan Stanley, specializing in AI engineering and enterprise software development.

- **🔗 LinkedIn:** [abdullahsattar](https://linkedin.com/in/abdullahsattar)
- **💼 Experience:** Enterprise Java development, AI/ML systems, financial technology
- **🎯 Mission:** Making AI accessible and secure for engineering professionals


---

## ⭐ **Star History**

If SiteBot helps your engineering workflow, please ⭐ this repository!

**Share your success stories:** Email abdullahsattar73@gmail.com or connect on LinkedIn

---

*Built with ❤️ for engineers who refuse to compromise on data security and need AI that actually understands their work.*
