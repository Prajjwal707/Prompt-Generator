# PromptGenius Backend 🚀

A production-ready backend API for prompt enhancement powered by LLaMA-2 and fine-tuned on custom datasets.

## 🎯 Features

- **Prompt Enhancement**: AI-powered prompt improvement for various task types
- **Task-Specific Templates**: Specialized templates for website development, image editing, PPT generation, and general tasks
- **Fine-Tuning Pipeline**: Complete LoRA/QLoRA fine-tuning system with evaluation metrics
- **Production API**: RESTful API with authentication, rate limiting, and monitoring
- **Docker Support**: Containerized deployment with Docker Compose
- **Comprehensive Monitoring**: Request logging, performance metrics, and health checks
- **Security**: API key authentication, input validation, and security headers

## 📋 Requirements

- Python 3.8+
- CUDA-compatible GPU (optional, for faster inference)
- 8GB+ RAM (16GB+ recommended for fine-tuning)
- 20GB+ disk space for models and datasets

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd promptgenius-backend
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download Model

Download a LLaMA-2 model (GGUF format) and place it in the `models/` directory:

```bash
# Example: Download LLaMA-2 7B Chat GGUF
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf -O models/llama-2-7b-chat.Q4_K_M.gguf
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Prepare Dataset (Optional)

```bash
python data.py  # Downloads and prepares Alpaca dataset
```

### 6. Run the Application

```bash
python main.py
```

The API will be available at `http://localhost:5000`

## 📚 API Documentation

### Authentication

All protected endpoints require an API key in the `x-api-key` header:

```bash
curl -X POST http://localhost:5000/api/enhance \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_api_key_here" \
  -d '{"prompt": "create a website", "task_type": "website"}'
```

### Endpoints

#### Prompt Enhancement

```http
POST /api/enhance
Content-Type: application/json
x-api-key: your_api_key

{
  "prompt": "create a portfolio website",
  "task_type": "website"
}
```

#### Batch Enhancement

```http
POST /api/enhance/batch
Content-Type: application/json
x-api-key: your_api_key

{
  "prompts": ["prompt1", "prompt2"],
  "task_type": "general"
}
```

#### Validation

```http
POST /api/validate
Content-Type: application/json

{
  "prompt": "test prompt"
}
```

#### Health Check

```http
GET /api/health
```

#### Model Information

```http
GET /api/model-info
x-api-key: your_api_key
```

#### Monitoring

```http
GET /api/metrics
x-api-key: your_api_key
```

## 🔧 Fine-Tuning

### 1. Prepare Dataset

```bash
python finetune/prepare_dataset.py --input promptgenius_training_data.json
```

### 2. Tokenize Dataset

```bash
python finetune/tokenize_dataset.py
```

### 3. Start Training

```bash
python finetune/train.py --config finetune/config.yaml
```

### 4. Evaluate Model

```bash
python finetune/evaluate.py --model finetune/checkpoints/best_model
```

## 🐳 Docker Deployment

### Using Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Docker Build

```bash
# Build image
docker build -t promptgenius-backend .

# Run container
docker run -p 5000:5000 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/logs:/app/logs \
  promptgenius-backend
```

## 📊 Monitoring

The application includes comprehensive monitoring:

- **Request Logging**: All API requests logged with timing and metadata
- **Performance Metrics**: Response times, error rates, and system usage
- **Health Checks**: System health and application status
- **Error Tracking**: Detailed error logging and analysis

Access monitoring endpoints:
- `/api/health` - Basic health check
- `/api/metrics` - Comprehensive metrics (requires API key)
- `/api/system/info` - System information (requires API key)

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test categories
pytest -m unit
pytest -m api
pytest -m finetune
```

## 📁 Project Structure

```
promptgenius-backend/
├── app/                    # Flask application
│   ├── routes/            # API routes
│   └── __init__.py        # App factory
├── config/                # Configuration files
│   ├── model_config.py    # Model configuration
│   └── settings.py        # Application settings
├── services/              # Business logic
│   ├── prompt_templates.py
│   └── prompt_enhancer.py
├── utils/                 # Utilities
│   ├── auth.py           # Authentication
│   ├── model_loader.py   # Model loading
│   └── validators.py     # Input validation
├── finetune/             # Fine-tuning pipeline
│   ├── config.yaml
│   ├── prepare_dataset.py
│   ├── tokenize_dataset.py
│   ├── train.py
│   └── evaluate.py
├── scripts/              # Data processing
│   ├── data_validation.py
│   └── data_cleaning.py
├── logging/              # Monitoring utilities
│   └── monitor.py
├── tests/                # Test suite
├── logs/                 # Application logs
├── models/               # Model files
└── docker-compose.yml    # Docker configuration
```

## 🔒 Security

- **API Key Authentication**: Secure API access with configurable keys
- **Rate Limiting**: Prevent abuse with per-key rate limits
- **Input Validation**: Comprehensive input sanitization and validation
- **Security Headers**: OWASP-recommended security headers
- **CORS Protection**: Configurable CORS policies

## 📈 Performance

- **Lazy Loading**: Models loaded on-demand
- **GPU Acceleration**: Automatic GPU detection and utilization
- **Caching**: Response caching for repeated requests
- **Batch Processing**: Efficient batch enhancement support
- **Connection Pooling**: Optimized database connections

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review the example configurations

## 🔄 Version History

- **v1.0.0** - Initial release with complete fine-tuning pipeline and production API

---

**Built with ❤️ for the PromptGenius project**
