import asyncio
from metagpt.roles import Architect, Engineer, ProductManager, ProjectManager, QaEngineer
from metagpt.team import Team
from metagpt.context import Context
from metagpt.config2 import config
from pathlib import Path

async def main():
    prompt = Path("prompt.txt").read_text()
    
    # Configure project
    # config.project_name = "oxii-landing-page"
    # config.project_path = "./oxii/landingPage"
    
    # MetaGPT config is often global or via context
    from metagpt.const import METAGPT_ROOT
    
    ctx = Context() # It will load from default config
    company = Team(context=ctx, use_mgx=False)
    
    # Hire classic roles
    company.hire([
        ProductManager(),
        Architect(),
        ProjectManager(),
        Engineer(use_code_review=True),
        QaEngineer()
    ])
    
    company.invest(3.0)
    # idea is passed to run
    await company.run(n_round=5, idea=prompt) # Reduced rounds for test

if __name__ == "__main__":
    asyncio.run(main())
