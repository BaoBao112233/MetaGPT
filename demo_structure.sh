#!/bin/bash
# Demo script để test cấu trúc mới của MetaGPT

echo "==================================="
echo "MetaGPT Project Structure Demo"
echo "==================================="
echo ""

# Activate conda environment
echo "Activating conda environment..."
eval "$(conda shell.bash hook)"
conda activate metagpt

# Test 1: Simple Python Project
echo ""
echo "Test 1: Creating a simple calculator project..."
echo "---------------------------------------"
metagpt "Create a simple calculator with add, subtract, multiply, divide functions. Include a main.py to demo usage." \
  --project-name "demo_calculator" \
  --project-path "./workspace/demo_calculator" \
  --investment 1.0 \
  --n-round 3 \
  --no-code-review \
  --no-run-tests

# Check structure
if [ -d "./workspace/demo_calculator" ]; then
    echo ""
    echo "✅ Project created successfully!"
    echo ""
    echo "Directory structure:"
    tree -L 2 ./workspace/demo_calculator/
    echo ""
    echo "Source files in src/:"
    ls -la ./workspace/demo_calculator/src/
    echo ""
    echo "Documentation in docs/:"
    find ./workspace/demo_calculator/docs/ -type f -name "*.md" -o -name "*.json"
else
    echo "❌ Project creation failed!"
fi

echo ""
echo "==================================="
echo "Demo Complete!"
echo "==================================="
echo ""
echo "To run the calculator:"
echo "  cd workspace/demo_calculator"
echo "  python src/main.py"
echo ""
echo "To review the development process:"
echo "  cat docs/prd/*.md              # Requirements"
echo "  cat docs/system_design/*.json  # Design"
echo "  cat docs/task/*.json           # Tasks"
