# MetaGPT Chat Application

Ứng dụng chat web sử dụng FastAPI và MetaGPT với Gemini 2.5 Flash qua Vertex AI.

## Tính năng

- 💬 Giao diện chat thời gian thực với streaming responses
- 📝 Hỗ trợ hiển thị Markdown đầy đủ
- 🎨 Syntax highlighting cho code blocks
- 📋 Nút copy cho tất cả code blocks
- 🐳 Docker support để deploy dễ dàng
- 🚀 FastAPI backend hiệu năng cao

## Cấu trúc thư mục

```
chat_app/
├── main.py                 # FastAPI backend
├── static/
│   ├── index.html         # Frontend HTML
│   ├── style.css          # CSS styling
│   └── script.js          # JavaScript logic
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose config
├── requirements-api.txt   # Python dependencies
└── README.md             # This file
```

## Cài đặt và Chạy

### Phương án 1: Chạy trực tiếp với Python

1. Cài đặt dependencies:
```bash
cd chat_app
pip install -r requirements-api.txt
```

2. Đảm bảo MetaGPT đã được cấu hình đúng (config/config2.yaml)

3. Chạy ứng dụng:
```bash
python main.py
```

Hoặc sử dụng uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

4. Mở trình duyệt và truy cập: http://localhost:8000

### Phương án 2: Chạy với Docker

1. Build Docker image:
```bash
cd /home/baobao/Projects/MetaGPT
docker build -f chat_app/Dockerfile -t metagpt-chat .
```

2. Chạy container:
```bash
docker run -p 8000:8000 -v $(pwd)/config:/app/config:ro metagpt-chat
```

### Phương án 3: Chạy với Docker Compose (Khuyến nghị)

1. Chạy ứng dụng:
```bash
cd chat_app
docker-compose up -d
```

2. Xem logs:
```bash
docker-compose logs -f
```

3. Dừng ứng dụng:
```bash
docker-compose down
```

4. Mở trình duyệt và truy cập: http://localhost:8000

## API Endpoints

- `GET /` - Trang chủ với UI chat
- `POST /chat/stream` - Streaming chat endpoint
- `POST /chat` - Non-streaming chat endpoint
- `GET /health` - Health check endpoint

## Cấu hình

Ứng dụng sử dụng cấu hình MetaGPT từ `config/config2.yaml`. Đảm bảo file này đã được cấu hình đúng với:

- API type: `vertex_ai`
- Model: `gemini-2.5-flash`
- Service account path
- Max tokens

## Yêu cầu hệ thống

- Python 3.12+
- Docker (nếu sử dụng containerization)
- Service account JSON cho Vertex AI

## Troubleshooting

### Lỗi kết nối đến Vertex AI
- Kiểm tra file `config/service-account.json` có tồn tại
- Đảm bảo service account có quyền truy cập Vertex AI

### Port 8000 đã được sử dụng
- Thay đổi port trong docker-compose.yml hoặc khi chạy uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

### UI không hiển thị đúng
- Kiểm tra console trong trình duyệt (F12)
- Đảm bảo các file trong thư mục `static/` có quyền đọc

## License

Theo license của MetaGPT project.
