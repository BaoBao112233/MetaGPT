#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to create a properly structured project with src/ and docs/
Uses the standard workflow (not TeamLeader/Engineer2)
"""
import asyncio
from pathlib import Path
from metagpt.config2 import Config
from metagpt.context import Context
from metagpt.roles import ProductManager, Architect, ProjectManager, Engineer
from metagpt.team import Team
from metagpt.logs import logger

async def create_structured_project(
    idea: str,
    project_name: str,
    project_path: str = None,
    n_round: int = 5,
):
    """Create a project with proper src/ and docs/ structure"""
    
    # Setup config
    config = Config.default()
    if project_path:
        config.project_path = project_path
    if project_name:
        config.project_name = project_name
    
    ctx = Context(config=config)
    if config.project_path:
        ctx.kwargs.set("project_path", config.project_path)
    
    # Create team with standard workflow
    company = Team(context=ctx)
    company.hire([
        ProductManager(),
        Architect(),
        ProjectManager(),
        Engineer(n_borg=1, use_code_review=False),
    ])
    
    company.invest(investment=3.0)
    
    logger.info(f"Starting project: {project_name}")
    await company.run(n_round=n_round, idea=idea)
    
    # Show results
    project_dir = Path(config.project_path)
    if project_dir.exists():
        logger.info(f"\n{'='*60}")
        logger.info(f"Project created at: {project_dir}")
        logger.info(f"{'='*60}")
        
        src_dir = project_dir / "src"
        docs_dir = project_dir / "docs"
        
        if src_dir.exists():
            logger.info(f"\n✅ Source code in src/:")
            for file in sorted(src_dir.rglob("*.py")):
                logger.info(f"   - {file.relative_to(project_dir)}")
        
        if docs_dir.exists():
            logger.info(f"\n✅ Documentation in docs/:")
            for file in sorted(docs_dir.rglob("*.md")):
                logger.info(f"   - {file.relative_to(project_dir)}")
            for file in sorted(docs_dir.rglob("*.json")):
                logger.info(f"   - {file.relative_to(project_dir)}")
        
        logger.info(f"\n{'='*60}")
        logger.info(f"To run the code:")
        logger.info(f"  cd {project_dir}")
        logger.info(f"  python src/main.py")
        logger.info(f"\nTo review the process:")
        logger.info(f"  cat docs/prd/*.md")
        logger.info(f"  cat docs/system_design/*.json")
        logger.info(f"  cat docs/task/*.json")
        logger.info(f"{'='*60}\n")
    
    return config.project_path

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python create_structured_project.py '<idea>' [project_name] [project_path]")
        print("\nExample:")
        print("  python create_structured_project.py 'Create a calculator' my_calc ./workspace/my_calc")
        sys.exit(1)
    
    idea = sys.argv[1]
    project_name = sys.argv[2] if len(sys.argv) > 2 else "my_project"
    project_path = sys.argv[3] if len(sys.argv) > 3 else f"./workspace/{project_name}"
    
    asyncio.run(create_structured_project(
        idea=idea,
        project_name=project_name,
        project_path=project_path,
        n_round=5,
    ))
