# Hướng dẫn sử dụng MetaGPT để tạo Crawling Service

## 🎯 Tổng quan

MetaGPT là một framework multi-agent AI có thể tự động tạo code theo yêu cầu. Có 3 cách chính để sử dụng MetaGPT:

---

## ✅ **Cách 1: Sử dụng CLI (ĐƠN GIẢN NHẤT - KHUYẾN NGHỊ)**

### Bước 1: Kích hoạt môi trường conda
```bash
conda activate metagpt
```

### Bước 2: Chạy lệnh MetaGPT
```bash
metagpt "Develop a Python-based crawling service with MVC architecture that crawls Google Search, Facebook Search, and Facebook Group Members to extract lead data (name, phone, email, company, location) and exports to CSV. Use Playwright for crawling, implement rate limiting, retry logic, and centralized logging. Follow SOLID principles and create production-ready code." \
  --project-name "lead_crawler" \
  --investment 5.0 \
  --n-round 10
```

### Hoặc sử dụng script có sẵn:
```bash
./run_crawler_generation.sh
```

### Các tham số quan trọng:
- `--project-name`: Tên project (tạo thư mục workspace/lead_crawler)
- `--investment`: Ngân sách cho API calls (USD)
- `--n-round`: Số vòng chạy (mỗi role sẽ thực hiện action)
- `--code-review`: Bật/tắt code review (mặc định: bật)
- `--run-tests`: Bật/tắt QA testing (mặc định: tắt)

---

## 📝 **Cách 2: Sử dụng file requirement**

### Bước 1: Tạo file PRD (Product Requirement Document)
File `crawling_service_prd.txt` đã được tạo sẵn với nội dung chi tiết.

### Bước 2: Chạy MetaGPT với file requirement
```bash
conda activate metagpt
metagpt "$(cat crawling_service_prd.txt)" \
  --project-name "lead_crawler" \
  --investment 5.0 \
  --n-round 10
```

---

## 🐍 **Cách 3: Sử dụng Python API (NÂNG CAO)**

### File: `test_folders/run_metagpt.py` (đã sửa lỗi)

```python
import asyncio
from metagpt.config2 import config
from metagpt.context import Context
from metagpt.roles import ProductManager, Architect, Engineer2, TeamLeader, DataAnalyst
from metagpt.team import Team

async def main():
    requirement = """
    Develop a Python-based crawling service with MVC architecture...
    """
    
    # Initialize context
    ctx = Context(config=config)
    
    # Create team
    company = Team(context=ctx)
    
    # Hire roles
    company.hire([
        TeamLeader(),
        ProductManager(),
        Architect(),
        Engineer2(),
        DataAnalyst(),
    ])
    
    # Set investment and run
    company.invest(investment=5.0)
    await company.run(n_round=10, idea=requirement)

if __name__ == "__main__":
    asyncio.run(main())
```

### Chạy script Python:
```bash
conda activate metagpt
python test_folders/run_metagpt.py
```

---

## ⚙️ **Cấu hình API Key**

MetaGPT cần API key để hoạt động. Kiểm tra file config:

```bash
cat ~/.metagpt/config2.yaml
```

Nếu chưa có, khởi tạo config:

```bash
metagpt --init-config
```

Sau đó chỉnh sửa file `~/.metagpt/config2.yaml`:

```yaml
llm:
  api_type: "openai"  # hoặc azure / ollama / groq
  model: "gpt-4-turbo"  # hoặc gpt-3.5-turbo
  base_url: "https://api.openai.com/v1"
  api_key: "YOUR_API_KEY"  # Thay bằng API key thực
```

---

## 📂 **Kết quả đầu ra**

MetaGPT sẽ tạo project trong thư mục:
```
workspace/lead_crawler/
├── docs/               # Tài liệu (PRD, Design, API docs)
├── resources/          # Resources
├── lead_crawler/       # Source code
│   ├── app/
│   │   ├── models/
│   │   ├── views/
│   │   ├── controllers/
│   │   ├── services/
│   │   └── utils/
│   ├── config/
│   ├── main.py
│   └── requirements.txt
└── tests/              # Test files
```

---

## 🔍 **Các Roles trong MetaGPT**

1. **TeamLeader**: Điều phối team, phân công công việc
2. **ProductManager**: Viết PRD (Product Requirement Document)
3. **Architect**: Thiết kế kiến trúc hệ thống
4. **Engineer2**: Viết code implementation
5. **DataAnalyst**: Phân tích dữ liệu (nếu cần)
6. **QaEngineer**: Viết test cases (nếu bật --run-tests)

---

## 🚀 **Lệnh khuyến nghị để chạy ngay**

```bash
# Kích hoạt môi trường
conda activate metagpt

# Chạy MetaGPT với cấu hình tối ưu
metagpt "Develop a Python-based crawling service with MVC architecture that crawls Google Search, Facebook Search, and Facebook Group Members to extract lead data (full_name, phone_number, email, company_name, province_or_city, source) and exports to CSV. Use Playwright for browser automation, BeautifulSoup for parsing. Implement rate limiting with exponential backoff, centralized logging, and environment-based configuration. Follow SOLID principles. Create production-ready code with no TODOs." \
  --project-name "lead_crawler" \
  --investment 5.0 \
  --n-round 10 \
  --code-review \
  --run-tests
```

---

## 📌 **Lưu ý quan trọng**

1. **API Cost**: Mỗi lần chạy sẽ tốn API calls. Với `--investment 5.0`, MetaGPT sẽ dừng khi đạt $5.

2. **Thời gian chạy**: Quá trình có thể mất 10-30 phút tùy thuộc vào độ phức tạp.

3. **Kết quả**: Code được tạo ra sẽ ở dạng production-ready, nhưng vẫn cần review và test thủ công.

4. **Incremental mode**: Nếu muốn cải tiến project có sẵn, dùng `--inc` flag.

5. **Recovery**: Nếu bị gián đoạn, có thể recover bằng `--recover-path workspace/lead_crawler/team`.

---

## 🎯 **So sánh các phương pháp**

| Phương pháp | Độ khó | Linh hoạt | Khuyến nghị |
|-------------|--------|-----------|-------------|
| CLI | ⭐ Dễ | ⭐⭐ Trung bình | ✅ Dùng cho hầu hết trường hợp |
| File PRD | ⭐⭐ Trung bình | ⭐⭐⭐ Cao | ✅ Dùng cho requirement phức tạp |
| Python API | ⭐⭐⭐ Khó | ⭐⭐⭐⭐ Rất cao | Dùng khi cần custom workflow |

---

## ✨ **Bắt đầu ngay**

Chạy lệnh sau để bắt đầu:

```bash
conda activate metagpt && ./run_crawler_generation.sh
```

Hoặc nếu muốn control nhiều hơn:

```bash
conda activate metagpt
metagpt --help  # Xem tất cả options
```
