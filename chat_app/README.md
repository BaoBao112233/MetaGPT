# MetaGPT Chat Application với DockerỨng dụng chat web sử dụng MetaGPT với Gemini 2.5 Flash thông qua Vertex AI.## Tính năng- ✅ Giao diện chat hiện đại với gradient design- ✅ Hỗ trợ markdown rendering (bold, italic, lists, etc.)- ✅ Syntax highlighting cho code blocks- ✅ Nút copy cho tất cả code blocks- ✅ Streaming responses (thời gian thực)- ✅ Docker containerization- ✅ FastAPI backend với OpenAPI docs## Chạy với Docker### Quick Start```bash# Build imagedocker build -f chat_app/Dockerfile -t metagpt-chat:latest .# Run containerdocker run -d \  --name metagpt-chat \  -p 8001:8001 \  -v $(pwd)/config:/app/config:ro \  --restart unless-stopped \  metagpt-chat:latest# Check healthcurl http://localhost:8001/health# Access UI# Open browser: http://localhost:8001```### Với Docker Compose```bashcd chat_appdocker-compose up -ddocker-compose logs -f```## API Endpoints- **GET /** - Chat UI- **POST /chat/stream** - Streaming responses (SSE)- **POST /chat** - Non-streaming responses- **GET /health** - Health check- **GET /docs** - OpenAPI documentation## Docker Commands```bash# Logsdocker logs metagpt-chat -f# Restartdocker restart metagpt-chat# Stopdocker stop metagpt-chat# Removedocker rm -f metagpt-chat# Rebuilddocker build -f chat_app/Dockerfile -t metagpt-chat:latest . --no-cache```## Troubleshooting### Permission denied (Google Cloud)Nếu thấy lỗi `403 CONSUMER_INVALID`, cần enable Vertex AI API:```bashgcloud services enable aiplatform.googleapis.com --project=metagpt-446414gcloud projects add-iam-policy-binding metagpt-446414 \  --member="serviceAccount:YOUR_SA@metagpt-446414.iam.gserviceaccount.com" \  --role="roles/aiplatform.user"```### Port conflict```bash# Change portdocker run -d -p 8002:8001 metagpt-chat:latest```### Debug```bash# Exec into containerdocker exec -it metagpt-chat bash# Check configdocker exec metagpt-chat cat /app/config/config2.yaml# Check logsdocker logs metagpt-chat --tail 50```## ConfigurationConfig được mount từ `config/` directory. Container tự động sử dụng `/app/config/config2.yaml`.**Host config** (`config/config2.yaml`):```yamlllm:  service_account_path: "/home/baobao/Projects/MetaGPT/config/service-account.json"```**Docker-specific** (`config/config2-docker.yaml`):```yamlllm:  service_account_path: "/app/config/service-account.json"```Dockerfile tự động copy `config2-docker.yaml` → `config2.yaml` nếu file tồn tại.## Development### Local (no Docker)

```bash
conda activate metagpt
cd chat_app
pip install -r requirements-api.txt
uvicorn main:app --reload --port 8001
```

### Hot reload với Docker

Uncomment volume mounts trong `docker-compose.yml`:
```yaml
volumes:
  - ./static:/app/chat_app/static
  - ./main.py:/app/chat_app/main.py
```
