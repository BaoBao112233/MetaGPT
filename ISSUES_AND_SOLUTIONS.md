# ⚠️ QUAN TRỌNG: Vấn Đề Cấu Trúc Project và Giải Pháp

## 🔴 Vấn Đề Hiện Tại

Khi chạy `metagpt`, bạn thấy output chỉ có:
- ❌ File `.txt`, `.md` trong workspace
- ❌ Không có code thực thi
- ❌ Không có cấu trúc `src/` và `docs/` rõ ràng

### Nguyên Nhân

MetaGPT hiện tại mặc định sử dụng **TeamLeader + Engineer2** workflow:
1. **TeamLeader** cố gắng giải quyết trực tiếp requirement
2. **Engineer2** được thiết kế cho web projects (React/Vue)
3. Workflow này **bypass** quy trình chuẩn: PM → Architect → PM → Engineer
4. Engineer2 có nhiều tool errors → không tạo code được

## ✅ Giải Pháp Đã Thực Hiện

### 1. **Sửa Core Function**

File đã sửa: [`metagpt/utils/common.py`](metagpt/utils/common.py)

```python
def get_project_srcs_path(workdir: str | Path) -> Path:
    """
    Get the source code directory path for a project.
    Now always returns 'src/' subdirectory to organize code separately from docs.
    """
    return Path(workdir) / "src"  # ← Luôn return src/
```

**Kết quả**: Code giờ sẽ được lưu vào `src/` thay vì folder với tên project.

### 2. **Sửa Software Company Workflow**

File đã sửa: [`metagpt/software_company.py`](metagpt/software_company.py)

Giờ khi `--implement` flag được set (default), nó sẽ dùng:
- ✅ **ProductManager** → tạo PRD
- ✅ **Architect** → tạo System Design  
- ✅ **ProjectManager** → tạo Tasks
- ✅ **Engineer** → viết code vào `src/`

**NHƯNG** vẫn cần TeamLeader (do MGXEnv requirement) và workflow này có issues.

### 3. **Tạo Script Mới (RECOMMENDED)**

File mới: [`metagpt_standard.py`](metagpt_standard.py)

Script này:
- ❌ Không dùng TeamLeader
- ✅ Dùng workflow chuẩn PM → Architect → PM → Engineer
- ✅ Code vào `src/`
- ✅ Docs vào `docs/`

**NHƯNG** có vấn đề với Environment setup → roles không react.

## 🎯 Cấu Trúc Mục Tiêu

```
<project_name>/
├── src/                # ← CODE CHỈ Ở ĐÂY
│   ├── main.py
│   ├── calculator.py
│   └── ...
├── docs/               # ← TÀI LIỆU CHỈ Ở ĐÂY
│   ├── prd/
│   │   └── <project>.md
│   ├── system_design/
│   │   └── <project>.json
│   ├── task/
│   │   └── <project>.json
│   └── code_summary/
├── tests/
└── requirements.txt
```

## 🔧 Cách Giải Quyết Tạm Thời

### Option A: Dùng generate_repo trực tiếp (Python API)

```python
from metagpt.software_company import generate_repo

# Workflow này sẽ dùng Engineer standard (không phải Engineer2)
project_path = generate_repo(
    idea="Create a calculator with add and subtract",
    project_name="my_calc",
    project_path="./workspace/my_calc",
    investment=2.0,
    n_round=5,
    code_review=False,
    run_tests=False,
    implement=True,  # ← QUAN TRỌNG: must be True
)
```

### Option B: Sửa lại Environment cho standard workflow

Cần sửa thêm để base Environment hoạt động đúng với role observations.

### Option C: Keep TeamLeader nhưng cấu hình đúng

Cần research thêm cách config TeamLeader để nó không bypass workflow.

## 📝 Files Đã Tạo/Sửa

1. ✅ `metagpt/utils/common.py` - Sửa `get_project_srcs_path()`
2. ✅ `metagpt/software_company.py` - Sửa workflow selection
3. ✅ `PROJECT_STRUCTURE_GUIDE.md` - Hướng dẫn chi tiết
4. ✅ `STRUCTURE_UPDATE_README.md` - Tóm tắt
5. ✅ `metagpt_standard.py` - Script workflow chuẩn (có issues)
6. ✅ `test_new_structure.py` - Test script
7. ✅ `demo_structure.sh` - Demo script

## 🚧 Vấn Đề Còn Tồn Tại

1. **Default `metagpt` command** vẫn dùng TeamLeader workflow
2. **TeamLeader workflow** không tạo code như mong đợi
3. **Base Environment** không hoạt động với standard roles
4. **Engineer2 tools** có nhiều lỗi

## 💡 Giải Pháp Dài Hạn Cần Làm

1. **Sửa MGXEnv** để không bắt buộc TeamLeader
2. **Hoặc** sửa TeamLeader để delegate đúng cho team
3. **Hoặc** fix base Environment để work với standard roles
4. **Hoặc** tạo custom Environment cho standard workflow

## 📞 Tóm Lại

**Đã làm được:**
- ✅ Code sẽ vào `src/` (khi workflow hoạt động)
- ✅ Docs vào `docs/` (đã hoạt động)
- ✅ Hiểu rõ vấn đề workflow

**Chưa làm được:**
- ❌ Workflow chuẩn chưa chạy được end-to-end
- ❌ Default `metagpt` command vẫn có issues

**Cần làm tiếp:**
- 🔧 Fix Environment hoặc workflow để code được tạo ra
- 🔧 Test với project thực tế

---

**Created**: January 5, 2026  
**Status**: In Progress - Core changes done, workflow integration pending
