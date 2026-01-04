#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from pathlib import Path

import click

from metagpt.const import CONFIG_ROOT


def generate_repo(
    idea,
    investment=3.0,
    n_round=5,
    code_review=True,
    run_tests=False,
    implement=True,
    project_name="",
    inc=False,
    project_path="",
    reqa_file="",
    max_auto_summarize_code=0,
    recover_path=None,
):
    """Run the startup logic. Can be called from CLI or other Python scripts."""
    from metagpt.config2 import config
    from metagpt.context import Context
    from metagpt.roles import (
        Architect,
        DataAnalyst,
        Engineer2,
        ProductManager,
        TeamLeader,
        ProjectReporter,
    )
    from metagpt.team import Team

    config.update_via_cli(project_path, project_name, inc, reqa_file, max_auto_summarize_code)
    ctx = Context(config=config)
    
    # Ensure project_path is in context kwargs for roles to access
    if config.project_path:
        ctx.kwargs.set("project_path", config.project_path)

    if not recover_path:
        company = Team(context=ctx)
        company.hire(
            [
                TeamLeader(),
                ProductManager(),
                Architect(),
                Engineer2(),
                # ProjectManager(),
                DataAnalyst(),
                ProjectReporter(),
            ]
        )

        # if implement or code_review:
        #     company.hire([Engineer(n_borg=5, use_code_review=code_review)])
        #
        # if run_tests:
        #     company.hire([QaEngineer()])
        #     if n_round < 8:
        #         n_round = 8  # If `--run-tests` is enabled, at least 8 rounds are required to run all QA actions.
    else:
        stg_path = Path(recover_path)
        if not stg_path.exists() or not str(stg_path).endswith("team"):
            raise FileNotFoundError(f"{recover_path} not exists or not endswith `team`")

        company = Team.deserialize(stg_path=stg_path, context=ctx)
        idea = company.idea

    company.invest(investment)
    asyncio.run(company.run(n_round=n_round, idea=idea))

    return ctx.kwargs.get("project_path")


@click.command(help="Start a new project.")
@click.argument("idea", required=False)
@click.option("--investment", type=float, default=3.0, help="Dollar amount to invest in the AI company.")
@click.option("--n-round", type=int, default=5, help="Number of rounds for the simulation.")
@click.option("--code-review/--no-code-review", default=True, help="Whether to use code review.")
@click.option("--run-tests/--no-run-tests", default=False, help="Whether to enable QA for adding & running tests.")
@click.option("--implement/--no-implement", default=True, help="Enable or disable code implementation.")
@click.option("--project-name", default="", help="Unique project name, such as 'game_2048'.")
@click.option("--inc/--no-inc", default=False, help="Incremental mode. Use it to coop with existing repo.")
@click.option(
    "--project-path",
    default="",
    help="Specify the directory path of the old version project to fulfill the incremental requirements.",
)
@click.option("--reqa-file", default="", help="Specify the source file name for rewriting the quality assurance code.")
@click.option(
    "--max-auto-summarize-code",
    type=int,
    default=0,
    help="The maximum number of times the 'SummarizeCode' action is automatically invoked, with -1 indicating "
    "unlimited. This parameter is used for debugging the workflow.",
)
@click.option("--recover-path", default=None, help="recover the project from existing serialized storage")
@click.option("--init-config/--no-init-config", default=False, help="Initialize the configuration file for MetaGPT.")
def app(
    idea,
    investment,
    n_round,
    code_review,
    run_tests,
    implement,
    project_name,
    inc,
    project_path,
    reqa_file,
    max_auto_summarize_code,
    recover_path,
    init_config,
):
    """Run a startup. Be a boss."""
    if init_config:
        copy_config_to()
        return

    if idea is None:
        click.echo("Missing argument 'IDEA'. Run 'metagpt --help' for more information.")
        return

    return generate_repo(
        idea,
        investment,
        n_round,
        code_review,
        run_tests,
        implement,
        project_name,
        inc,
        project_path,
        reqa_file,
        max_auto_summarize_code,
        recover_path,
    )


DEFAULT_CONFIG = """# Full Example: https://github.com/geekan/MetaGPT/blob/main/config/config2.example.yaml
# Reflected Code: https://github.com/geekan/MetaGPT/blob/main/metagpt/config2.py
# Config Docs: https://docs.deepwisdom.ai/main/en/guide/get_started/configuration.html
llm:
  api_type: "openai"  # or azure / ollama / groq etc.
  model: "gpt-4-turbo"  # or gpt-3.5-turbo
  base_url: "https://api.openai.com/v1"  # or forward url / other llm url
  api_key: "YOUR_API_KEY"
"""


def copy_config_to():
    """Initialize the configuration file for MetaGPT."""
    target_path = CONFIG_ROOT / "config2.yaml"

    # 创建目标目录（如果不存在）
    target_path.parent.mkdir(parents=True, exist_ok=True)

    # 如果目标文件已经存在，则重命名为 .bak
    if target_path.exists():
        backup_path = target_path.with_suffix(".bak")
        target_path.rename(backup_path)
        print(f"Existing configuration file backed up at {backup_path}")

    # 复制文件
    target_path.write_text(DEFAULT_CONFIG, encoding="utf-8")
    print(f"Configuration file initialized at {target_path}")


if __name__ == "__main__":
    app()
