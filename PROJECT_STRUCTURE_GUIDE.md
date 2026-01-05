# Hướng Dẫn Cấu Trúc Project Mới

## Tổng Quan

MetaGPT đã được cập nhật để tổ chức output theo cấu trúc rõ ràng hơn, tách biệt giữa source code và tài liệu báo cáo.

## Cấu Trúc Mới

Sau khi chạy lệnh `metagpt`, project sẽ có cấu trúc như sau:

```
<project_name>/
├── src/                          # Source code thực thi
│   ├── main.py
│   ├── module1.py
│   ├── module2.py
│   └── ...
├── docs/                         # Tài liệu và báo cáo quá trình
│   ├── prd/                      # Product Requirements Documents
│   │   └── <project_name>.md
│   ├── system_design/            # System Design Documents
│   │   └── <project_name>.json
│   ├── task/                     # Project Schedule/Tasks
│   │   └── <project_name>.json
│   ├── code_summary/             # Code Summary Documents
│   ├── code_plan_and_change/     # Code Planning Documents
│   └── steps/                    # Step-by-step reports (if ProjectReporter is used)
│       └── step_001_xxx/
├── tests/                        # Test files (nếu có --run-tests)
├── resources/                    # Resource files (diagrams, etc.)
└── requirements.txt              # Python dependencies
```

## Lợi Ích

### 1. **Tách Biệt Rõ Ràng**
- **`src/`**: Chứa toàn bộ code có thể chạy được (Python, JS, HTML, CSS, ...)
- **`docs/`**: Chứa tài liệu quy trình từ ý tưởng đến sản phẩm

### 2. **Dễ Dàng Review Quy Trình**
Trong thư mục `docs/` bạn có thể xem:
- PRD (Product Requirements Document): Yêu cầu ban đầu
- System Design: Thiết kế hệ thống
- Tasks/Schedule: Lịch trình và task được chia nhỏ
- Code Summary: Tóm tắt code
- Step Reports: Báo cáo từng bước (nếu có)

### 3. **Quản Lý Code Tốt Hơn**
- Code được tổ chức trong `src/` theo cấu trúc module rõ ràng
- Dễ dàng import và sử dụng
- Phù hợp với best practices của Python và web development

## Cách Sử Dụng

### Chạy Project Mới

```bash
metagpt "Tạo một landing page cho nền tảng SaaS quản lý công việc" \
  --project-name "oxii-landing-page" \
  --project-path "./workspace/oxii-landing-page" \
  --code-review \
  --n-round 20
```

### Kiểm Tra Cấu Trúc

Sau khi chạy xong, bạn sẽ thấy:

```bash
workspace/oxii-landing-page/
├── src/          # ← Code ở đây
└── docs/         # ← Báo cáo ở đây
```

### Chạy Code

```bash
cd workspace/oxii-landing-page
python src/main.py

# Hoặc cho web project
cd workspace/oxii-landing-page/src
npm install
npm run dev
```

### Xem Quy Trình Phát Triển

```bash
# Xem requirements
cat docs/prd/*.md

# Xem system design
cat docs/system_design/*.json

# Xem task breakdown
cat docs/task/*.json

# Xem step-by-step reports (nếu có)
ls docs/steps/
```

## So Sánh Với Cấu Trúc Cũ

### Trước đây:
```
<project_name>/
├── <project_name>/      # Code lẫn với tên project
│   ├── main.py
│   └── ...
├── docs/                # Docs
│   └── ...
└── requirements.txt
```

### Bây giờ:
```
<project_name>/
├── src/                 # Code rõ ràng
│   ├── main.py
│   └── ...
├── docs/                # Docs rõ ràng
│   └── ...
└── requirements.txt
```

## Thay Đổi Kỹ Thuật

### File Đã Sửa

1. **`metagpt/utils/common.py`**
   - Hàm `get_project_srcs_path()` giờ luôn trả về `src/` thay vì tên project

2. **`metagpt/utils/project_repo.py`**
   - `ProjectRepo.srcs` tự động trỏ đến thư mục `src/`

3. **Các Actions và Roles**
   - `Engineer`: Tự động lưu code vào `self.repo.srcs` → `src/`
   - `ProductManager`, `Architect`, `ProjectManager`: Tự động lưu docs vào `self.repo.docs` → `docs/`

## Lưu Ý

- Cấu trúc này tương thích ngược với projects cũ
- Incremental mode (`--inc`) vẫn hoạt động bình thường
- Web projects (React/Vue) vẫn được tổ chức trong `src/`

## Test

Có script test để verify cấu trúc:

```bash
python test_new_structure.py
```

Script này sẽ:
1. Tạo một project test
2. Kiểm tra xem `src/` và `docs/` có được tạo đúng không
3. Liệt kê các files trong mỗi thư mục
