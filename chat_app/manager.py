import asyncio
import json
from pathlib import Path
from metagpt.logs import set_llm_stream_logfunc
from metagpt.roles.role import Role
from metagpt.team import Team
from metagpt.actions import Action
from metagpt.schema import Message
from metagpt.utils.stream_pipe import StreamPipe
from contextvars import ContextVar

stream_pipe_var: ContextVar[StreamPipe] = ContextVar("stream_pipe")

def stream_pipe_log(content):
    stream_pipe = stream_pipe_var.get(None)
    if stream_pipe:
        stream_pipe.set_message(content)

class MetaGPTManager:
    def __init__(self, workspace_path: Path):
        self.workspace_path = workspace_path
        self.workspace_path.mkdir(parents=True, exist_ok=True)
        set_llm_stream_logfunc(stream_pipe_log)

    async def run_project(self, idea: str):
        stream_pipe = StreamPipe()
        stream_pipe_var.set(stream_pipe)
        
        # We use a queue to bridge the callback-based StreamPipe to our async generator
        queue = asyncio.Queue()

        # Run MetaGPT in a separate task
        async def run_metagpt_and_get_result(sp: StreamPipe):
            # Set context var inside this task's context
            stream_pipe_var.set(sp)
            try:
                # Import correct Role classes
                from metagpt.roles import Engineer, ProductManager, Architect, ProjectManager
                
                team = Team()
                team.hire([
                    ProductManager(),
                    Architect(),
                    ProjectManager(),
                    Engineer(),
                ])
                
                team.invest(budget=3.0)
                team.run_project(idea)
                history = await team.run(n_round=5)
                
                # Extract final result from history
                if history:
                    final_msg = history[-1]
                    await queue.put({"type": "content", "content": final_msg.content})
                
                await queue.put({"type": "status", "content": "completed"})
            except Exception as e:
                import traceback
                error_msg = f"{str(e)}\n{traceback.format_exc()}"
                print(f"Error in MetaGPT: {error_msg}")
                await queue.put({"type": "error", "content": error_msg})
            finally:
                await queue.put(None) # End marker

        asyncio.create_task(run_metagpt_and_get_result(stream_pipe))

        # Poll stream_pipe and put into queue
        async def poll_stream(sp: StreamPipe):
            while True:
                msg = sp.get_message()
                if msg:
                    await queue.put({"type": "reasoning", "content": msg})
                await asyncio.sleep(0.1)

        poll_task = asyncio.create_task(poll_stream(stream_pipe))

        try:
            while True:
                item = await queue.get()
                if item is None:
                    break
                yield item
        finally:
            poll_task.cancel()

    def get_generated_files(self):
        files = []
        for path in self.workspace_path.rglob("*"):
            if path.is_file():
                files.append({
                    "name": path.name,
                    "path": str(path.relative_to(self.workspace_path)),
                    "size": path.stat().st_size
                })
        return files
