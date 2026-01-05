# MetaGPT Project Structure Update

## Tóm Tắt Thay Đổi

Repo MetaGPT đã được cập nhật để tổ chức output project một cách rõ ràng hơn:

### 🎯 Mục Đích
- **Tách biệt source code và tài liệu báo cáo**
- **Dễ dàng review quy trình phát triển từ ý tưởng đến sản phẩm**
- **Cấu trúc project chuẩn và chuyên nghiệp hơn**

### 📁 Cấu Trúc Mới

```
<project_name>/
├── src/              # ← CODE CHỈ Ở ĐÂY (Python, JS, HTML, CSS, ...)
│   ├── main.py
│   └── ...
├── docs/             # ← TÀI LIỆU CHỈ Ở ĐÂY
│   ├── prd/          # Requirements
│   ├── system_design/  # Design documents
│   ├── task/         # Task breakdown
│   └── steps/        # Step-by-step reports
├── tests/            # Test files
├── resources/        # Resources (diagrams, etc.)
└── requirements.txt
```

## 🚀 Cách Sử Dụng

### Chạy metagpt như bình thường:

```bash
metagpt "Create a landing page for SaaS platform" \
  --project-name "my-landing-page" \
  --project-path "./workspace/my-landing-page" \
  --code-review \
  --n-round 10
```

### Kết quả:

```
workspace/my-landing-page/
├── src/          ✅ Tất cả code ở đây - có thể chạy ngay
└── docs/         ✅ Tất cả báo cáo ở đây - review được quy trình
```

## 📖 Xem Quy Trình Phát Triển

```bash
# 1. Xem requirements ban đầu
cat workspace/my-landing-page/docs/prd/*.md

# 2. Xem thiết kế hệ thống
cat workspace/my-landing-page/docs/system_design/*.json

# 3. Xem task được chia nhỏ như thế nào
cat workspace/my-landing-page/docs/task/*.json

# 4. Xem step-by-step reports (nếu có)
ls workspace/my-landing-page/docs/steps/
```

## 🏃 Chạy Code

```bash
# Python project
cd workspace/my-landing-page
python src/main.py

# Web project (React/Vue)
cd workspace/my-landing-page/src
npm install && npm run dev
```

## 🔧 Files Đã Thay Đổi

1. **`metagpt/utils/common.py`**
   - `get_project_srcs_path()` → luôn return `src/`

2. Các role tự động lưu:
   - Engineer → code vào `src/`
   - PM/Architect/PM → docs vào `docs/`

## 📚 Tài Liệu Chi Tiết

Xem [PROJECT_STRUCTURE_GUIDE.md](PROJECT_STRUCTURE_GUIDE.md) để biết thêm chi tiết.

## 🧪 Test

```bash
# Chạy demo script
./demo_structure.sh

# Hoặc test thủ công
python test_new_structure.py
```

## ✨ Lợi Ích

1. ✅ **Code và docs tách biệt rõ ràng**
2. ✅ **Dễ review quy trình multi-agent**
3. ✅ **Cấu trúc project chuẩn**
4. ✅ **Phù hợp với workflow thực tế**
5. ✅ **Tương thích ngược với projects cũ**

---

**Updated:** January 2026
