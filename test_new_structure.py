#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to verify the new project structure with src/ and docs/ separation
"""
from pathlib import Path
from metagpt.software_company import generate_repo

def test_structure():
    """Test that the new structure creates src/ for code and docs/ for reports"""
    print("Testing new project structure...")
    
    # Generate a simple project
    project_path = generate_repo(
        idea="Create a simple calculator with add and subtract functions",
        investment=1.0,
        n_round=2,
        code_review=False,
        run_tests=False,
        implement=True,
        project_name="test_calculator",
    )
    
    if project_path:
        project_dir = Path(project_path)
        print(f"\nProject created at: {project_dir}")
        
        # Check if src/ and docs/ exist
        src_dir = project_dir / "src"
        docs_dir = project_dir / "docs"
        
        print(f"\nChecking directory structure:")
        print(f"  src/ exists: {src_dir.exists()}")
        print(f"  docs/ exists: {docs_dir.exists()}")
        
        if src_dir.exists():
            print(f"\n  Files in src/:")
            for file in src_dir.rglob("*"):
                if file.is_file():
                    print(f"    - {file.relative_to(project_dir)}")
        
        if docs_dir.exists():
            print(f"\n  Files in docs/:")
            for file in docs_dir.rglob("*"):
                if file.is_file():
                    print(f"    - {file.relative_to(project_dir)}")
        
        # Check root directory (should not have .py files except maybe main.py)
        print(f"\n  Files in root:")
        for file in project_dir.iterdir():
            if file.is_file():
                print(f"    - {file.name}")
        
        print("\n✅ Structure test complete!")
    else:
        print("❌ Failed to create project")

if __name__ == "__main__":
    test_structure()
