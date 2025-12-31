import typer
from typing import Optional

app = typer.Typer()

@app.command()
def startup(
    investment: float = typer.Option(3.0, help="Dollar amount to invest in the AI company."),
    n_round: int = typer.Option(5, help="Number of rounds for the simulation."),
    code_review: bool = typer.Option(True, help="Whether to use code review."),
    run_tests: bool = typer.Option(False, help="Whether to enable QA for adding & running tests."),
    implement: bool = typer.Option(True, help="Enable or disable code implementation."),
    project_name: str = typer.Option("", help="Unique project name, such as 'game_2048'."),
    inc: bool = typer.Option(False, help="Incremental mode. Use it to coop with existing repo."),
    project_path: str = typer.Option(
        "",
        help="Specify the directory path of the old version project to fulfill the incremental requirements.",
    ),
    reqa_file: str = typer.Option(
        "", help="Specify the source file name for rewriting the quality assurance code."
    ),
    max_auto_summarize_code: int = typer.Option(
        0,
        help="The maximum number of times the 'SummarizeCode' action is automatically invoked, with -1 indicating "
        "unlimited. This parameter is used for debugging the workflow.",
    ),
    recover_path: str = typer.Option("", help="recover the project from existing serialized storage"),
    init_config: bool = typer.Option(False, help="Initialize the configuration file for MetaGPT."),
):
    pass

if __name__ == "__main__":
    app()
