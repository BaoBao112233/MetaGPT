import asyncio
from metagpt.config2 import config
from metagpt.context import Context
from metagpt.roles import ProductManager, Architect, Engineer2, TeamLeader, DataAnalyst
from metagpt.team import Team

async def main():
    requirement = """
    Develop a Python-based crawling service with MVC architecture that:
    1. Crawls Google Search, Facebook Search, and Facebook Group Members
    2. Extracts lead data: full_name, phone_number, email, company_name, province_or_city, source
    3. Exports to CSV (UTF-8 BOM, Excel-compatible)
    
    Technical Stack:
    - Python 3.10+
    - Playwright for crawling
    - BeautifulSoup/lxml for parsing
    - Rate limiting and retry logic
    - Centralized logging
    - Environment-based config
    
    Architecture: MVC with models, views, controllers, services, utils
    Output: google_results.csv, facebook_search_results.csv, facebook_group_members.csv
    
    Follow SOLID principles. Production-ready code only.
    """
    
    # Initialize context with config
    ctx = Context(config=config)
    
    # Create team (company)
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
    company.invest(investment=10.0)  # Budget in USD for API calls
    await company.run(n_round=30, idea=requirement)

if __name__ == "__main__":
    asyncio.run(main())