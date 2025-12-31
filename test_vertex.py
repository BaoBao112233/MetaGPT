import asyncio
import json
from metagpt.configs.llm_config import LLMConfig, LLMType
from metagpt.provider.vertex_ai_api import VertexAILLM

async def test_vertex():
    config = LLMConfig(
        api_type=LLMType.VERTEX_AI,
        model="gemini-1.5-flash-001",
        service_account_path="/home/baobao/Projects/MetaGPT/config/service-account.json",
        project_id="kfactory-prod",
        location="asia-southeast1"
    )
    
    # Try to get project_id from json if not provided
    with open(config.service_account_path, 'r') as f:
        sa_data = json.load(f)
        config.project_id = sa_data.get('project_id')
        print(f"Project ID: {config.project_id}")

    llm = VertexAILLM(config)
    resp = await llm.aask("Hello, are you working?")
    print(f"Response: {resp}")

if __name__ == "__main__":
    asyncio.run(test_vertex())
