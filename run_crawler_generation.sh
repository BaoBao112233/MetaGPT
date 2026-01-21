#!/bin/bash

# Script to run MetaGPT with the crawling service requirement

# Method 1: Using MetaGPT CLI (Recommended - Simplest)
echo "=== Method 1: Using MetaGPT CLI ==="
echo "Running: metagpt 'Develop a Python-based crawling service...'"
echo ""

metagpt "Develop a Python-based crawling service with MVC architecture that crawls Google Search, Facebook Search, and Facebook Group Members to extract lead data (name, phone, email, company, location) and exports to CSV. Use Playwright for crawling, implement rate limiting, retry logic, and centralized logging. Follow SOLID principles and create production-ready code." \
  --project-name "lead_crawler" \
  --investment 5.0 \
  --n-round 10

# Method 2: Using requirement file
# echo "=== Method 2: Using requirement file ==="
# metagpt --project-name "lead_crawler" --investment 5.0 --n-round 10 "$(cat crawling_service_prd.txt)"

# Method 3: Using Python API (if you want more control)
# python test_folders/run_metagpt.py
