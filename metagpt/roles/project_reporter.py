import json
import re
import datetime
from pathlib import Path
from metagpt.actions import Action
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger
from metagpt.utils.common import awrite
from metagpt.const import DEFAULT_WORKSPACE_ROOT

class WriteStepReport(Action):
    name: str = "WriteStepReport"

    async def run(self, step_name: str, content: str, project_path: Path, step_counter: int, source_codes: dict[str, str] = None):
        step_dir = project_path / "docs" / "steps" / f"step_{step_counter:03d}_{step_name}"
        step_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = step_dir / f"report_{timestamp}.md"
        
        report_content = f"# Step Report: {step_name}\n\n{content}\n"
        await awrite(report_path, report_content)
        
        if source_codes:
            for file_path, code in source_codes.items():
                # Ensure file_path is safe
                safe_path = Path(file_path).name
                code_path = step_dir / safe_path
                await awrite(code_path, code)
                logger.info(f"Source code saved to {code_path}")
        
        logger.info(f"Step report saved to {report_path}")
        return report_content

class WriteFinalReport(Action):
    name: str = "WriteFinalReport"

    async def run(self, all_steps_content: str, project_path: Path):
        report_path = project_path / "docs" / "final_report.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        report_content = f"# Final Project Report\n\n{all_steps_content}\n"
        await awrite(report_path, report_content)
        logger.info(f"Final report saved to {report_path}")
        return report_content

class ProjectReporter(Role):
    name: str = "Edwin"
    profile: str = "Project Reporter"
    goal: str = "Document each step of the project, including source code, and provide a final comprehensive report."
    step_counter: int = 0
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([WriteStepReport, WriteFinalReport])
        from metagpt.actions.di.run_command import RunCommand
        from metagpt.actions.add_requirement import UserRequirement
        from metagpt.actions import WritePRD, WriteDesign, WriteTasks, WriteCode
        self._watch([RunCommand, UserRequirement, WritePRD, WriteDesign, WriteTasks, WriteCode])
        self.observe_all_msg_from_buffer = True

    async def _think(self) -> bool:
        """Always act if there is news."""
        if self.rc.news:
            self._set_state(0)
            return True
        return False

    def _extract_source_codes(self, content: str) -> dict[str, str]:
        source_codes = {}
        # Try to parse as JSON first (for RoleZero commands)
        try:
            # Find JSON block
            json_match = re.search(r"```json\s*(\[.*\])\s*```", content, re.DOTALL)
            if json_match:
                commands = json.loads(json_match.group(1))
                for cmd in commands:
                    if cmd.get("command_name") in ["Editor.create_file", "Editor.edit_file_by_replace", "Editor.append_file"]:
                        args = cmd.get("args", {})
                        file_path = args.get("file_path") or args.get("path")
                        file_content = args.get("file_content") or args.get("content") or args.get("new_content")
                        if file_path and file_content:
                            source_codes[file_path] = file_content
        except Exception:
            pass
            
        # Also look for markdown code blocks
        code_blocks = re.findall(r"```(?:\w+)?\s*\n(.*?)\n```", content, re.DOTALL)
        for i, block in enumerate(code_blocks):
            if f"block_{i}" not in source_codes:
                source_codes[f"block_{i}.txt"] = block
                
        return source_codes

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to write report")
        
        news = self.rc.news
        if not news:
            return Message(content="No progress to report yet.", role=self.profile)
            
        project_path = self.context.kwargs.get("project_path")
        if not project_path:
            project_name = self.config.project_name or "project"
            project_path = DEFAULT_WORKSPACE_ROOT / project_name
        else:
            project_path = Path(project_path)

        last_content = ""
        for msg in news:
            if msg.role == self.profile:
                continue

            self.step_counter += 1
            cause_by = msg.cause_by
            if isinstance(cause_by, type):
                step_name = cause_by.__name__
            elif isinstance(cause_by, str):
                step_name = cause_by.split(".")[-1]
            else:
                step_name = "UnknownStep"
            
            source_codes = self._extract_source_codes(str(msg.content))
            content = await self._think_report_content(msg)
            await WriteStepReport().run(step_name, content, project_path, self.step_counter, source_codes)
            last_content = content
            
            # Check if we should write final report
            content_str = str(msg.content).lower()
            if '"command_name": "end"' in content_str or "'command_name': 'end'" in content_str or "hoàn tất" in content_str or "finished" in content_str:
                logger.info(f"{self._setting}: detected end of project, writing final report")
                
                # Gather all step reports
                steps_dir = project_path / "docs" / "steps"
                all_reports = ""
                if steps_dir.exists():
                    # Find all report_*.md files recursively
                    for f in sorted(steps_dir.glob("**/report_*.md")):
                        all_reports += f"\n---\n## Step {f.parent.name}\n{f.read_text()}\n"
                
                final_content = await self._think_final_report(all_reports)
                await WriteFinalReport().run(final_content, project_path)

        return Message(content=last_content or "Reported.", role=self.profile, cause_by=WriteStepReport)

    async def _think_report_content(self, last_msg: Message) -> str:
        prompt = f"""Bạn là một Project Reporter. Hãy tóm tắt công việc mà {last_msg.role} vừa thực hiện trong bước này. 
Tài liệu này sẽ giúp người dùng kiểm soát quy trình từng bước một. 

Nếu có mã nguồn được tạo hoặc chỉnh sửa, hãy đề cập đến tên tệp và mục đích của nó.

Hãy viết bằng tiếng Việt.

Nội dung công việc:
{last_msg.content}"""
        return await self.llm.aask(prompt)

    async def _think_final_report(self, all_reports: str) -> str:
        prompt = f"Dựa trên các báo cáo từng bước sau đây, hãy viết một báo cáo tổng thể về toàn bộ dự án từ khâu lên ý tưởng đến sản phẩm cuối cùng. Hãy viết bằng tiếng Việt.\n\nCác báo cáo thành phần:\n{all_reports}"
        return await self.llm.aask(prompt)
