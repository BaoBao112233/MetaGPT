#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MetaGPT Standard Workflow - creates proper src/ and docs/ structure
WITHOUT TeamLeader - uses classic PM->Architect->PM->Engineer workflow
"""
import sys
import asyncio
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: python metagpt_standard.py '<idea>' [options]")
        print("\nOptions:")
        print("  --project-name NAME")
        print("  --project-path PATH")
        print("  --investment AMOUNT (default: 3.0)")
        print("  --n-round N (default: 5)")
        print("  --code-review / --no-code-review")
        print("  --run-tests / --no-run-tests")
        print("\nExample:")
        print("  python metagpt_standard.py 'Create a calculator' --project-name calc --investment 2.0")
        sys.exit(1)
    
    # Parse arguments
    idea = sys.argv[1]
    args = sys.argv[2:]
    
    # Defaults
    project_name = ""
    project_path = ""
    investment = 3.0
    n_round = 5
    code_review = True
    run_tests = False
    
    i = 0
    while i < len(args):
        if args[i] == "--project-name" and i + 1 < len(args):
            project_name = args[i + 1]
            i += 2
        elif args[i] == "--project-path" and i + 1 < len(args):
            project_path = args[i + 1]
            i += 2
        elif args[i] == "--investment" and i + 1 < len(args):
            investment = float(args[i + 1])
            i += 2
        elif args[i] == "--n-round" and i + 1 < len(args):
            n_round = int(args[i + 1])
            i += 2
        elif args[i] == "--code-review":
            code_review = True
            i += 1
        elif args[i] == "--no-code-review":
            code_review = False
            i += 1
        elif args[i] == "--run-tests":
            run_tests = True
            i += 1
        elif args[i] == "--no-run-tests":
            run_tests = False
            i += 1
        else:
            i += 1
    
    # Call generate_repo with standard workflow
    asyncio.run(run_standard_workflow(
        idea=idea,
        investment=investment,
        n_round=n_round,
        code_review=code_review,
        run_tests=run_tests,
        project_name=project_name,
        project_path=project_path,
    ))

async def run_standard_workflow(
    idea: str,
    investment: float,
    n_round: int,
    code_review: bool,
    run_tests: bool,
    project_name: str,
    project_path: str,
):
    """Run standard workflow: PM -> Architect -> PM -> Engineer (NO TeamLeader)"""
    from metagpt.config2 import Config
    from metagpt.context import Context
    from metagpt.environment.base_env import Environment
    from metagpt.roles import ProductManager, Architect, ProjectManager, Engineer, QaEngineer
    from metagpt.team import Team
    from metagpt.logs import logger
    from metagpt.schema import Message
    
    # Setup config
    config = Config.default()
    if project_path:
        config.project_path = project_path
    if project_name:
        config.project_name = project_name
    
    config.inc = False
    config.reqa_file = ""
    config.max_auto_summarize_code = 0
    
    ctx = Context(config=config)
    if config.project_path:
        ctx.kwargs.set("project_path", config.project_path)
    
    # Create base environment (NOT MGXEnv - no TeamLeader needed)
    env = Environment(context=ctx)
    
    # Create roles
    pm = ProductManager()
    arch = Architect()
    pm2 = ProjectManager()
    eng = Engineer(n_borg=5, use_code_review=code_review)
    
    # Setup watchersโครงสร้าง rõ ràng
    pm.set_env(env)
    arch.set_env(env)
    pm2.set_env(env)
    eng.set_env(env)
    
    # PM watches user messages
    env.add_role(pm)
    
    # Architect watches PM's output (PRD)
    env.add_role(arch)
    
    # ProjectManager watches Architect's output (Design)
    env.add_role(pm2)
    
    # Engineer watches ProjectManager's output (Tasks)
    env.add_role(eng)
    
    if run_tests:
        qa = QaEngineer()
        qa.set_env(env)
        env.add_role(qa)
        if n_round < 8:
            n_round = 8
    
    logger.info(f"Starting standard workflow: {project_name or 'project'}")
    logger.info(f"  Investment: ${investment}")
    logger.info(f"  Rounds: {n_round}")
    logger.info(f"  Code Review: {code_review}")
    logger.info(f"  Run Tests: {run_tests}")
    
    # Publish user requirement
    env.publish_message(Message(content=idea, role="User"))
    
    # Run workflow
    n = 0
    while n < n_round and not env.is_idle:
        n += 1
        logger.info(f"\n{'='*60}")
        logger.info(f"Round {n}/{n_round}")
        logger.info(f"{'='*60}")
        
        await env.run()
        
        # Check if all done
        if env.is_idle:
            logger.info("All roles completed their work!")
            break
    
    # Show results
    project_dir = Path(config.project_path)
    if project_dir.exists():
        logger.info(f"\n{'='*60}")
        logger.info(f"✅ Project created at: {project_dir}")
        logger.info(f"{'='*60}")
        
        src_dir = project_dir / "src"
        docs_dir = project_dir / "docs"
        
        if src_dir.exists():
            logger.info(f"\n📁 Source code in src/:")
            py_files = list(src_dir.rglob("*.py"))
            if py_files:
                for file in sorted(py_files):
                    logger.info(f"   - {file.relative_to(project_dir)}")
            else:
                logger.warning("   No Python files found!")
        else:
            logger.warning(f"\n⚠️  src/ directory not found!")
        
        if docs_dir.exists():
            logger.info(f"\n📚 Documentation in docs/:")
            for pattern in ["*.md", "*.json"]:
                for file in sorted(docs_dir.rglob(pattern)):
                    logger.info(f"   - {file.relative_to(project_dir)}")
        else:
            logger.warning(f"\n⚠️  docs/ directory not found!")
        
        logger.info(f"\n{'='*60}")
        if src_dir.exists() and any(src_dir.rglob("*.py")):
            logger.info(f"✅ To run the code:")
            logger.info(f"  cd {project_dir}")
            logger.info(f"  python src/main.py")
        
        if docs_dir.exists():
            logger.info(f"\n✅ To review the development process:")
            logger.info(f"  # Requirements")
            logger.info(f"  cat docs/prd/*.md")
            logger.info(f"  # System Design")
            logger.info(f"  cat docs/system_design/*.json")
            logger.info(f"  # Task Breakdown")
            logger.info(f"  cat docs/task/*.json")
        logger.info(f"{'='*60}\n")

if __name__ == "__main__":
    main()
