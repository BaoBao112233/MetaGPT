import asyncio
import argparse
from metagpt.config2 import config
from metagpt.context import Context
from metagpt.roles import ProductManager, Architect, Engineer2, TeamLeader, DataAnalyst
from metagpt.team import Team

async def run_task(idea: str, investment: float = 10.0, n_round: int = 15):
    ctx = Context(config=config)
    company = Team(context=ctx)
    
    company.hire([
        TeamLeader(),
        ProductManager(),
        Architect(),
        Engineer2(),
        DataAnalyst(),
    ])
    
    company.invest(investment=investment)
    print(f"Starting MetaGPT with idea: {idea}")
    await company.run(n_round=n_round, idea=idea)
    print("MetaGPT run completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run MetaGPT with a custom requirement.")
    parser.add_argument("requirement", type=str, help="The requirement/idea for the project")
    parser.add_argument("--budget", type=float, default=10.0, help="Investment budget (USD)")
    parser.add_argument("--rounds", type=int, default=20, help="Max rounds of interaction")
    
    args = parser.parse_args()
    
    asyncio.run(run_task(args.requirement, args.budget, args.rounds))
