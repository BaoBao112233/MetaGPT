import typer

app = typer.Typer()

@app.command()
def startup(
    idea: str = typer.Argument(..., help="Your innovative idea, such as 'Create a 2048 game.'"),
    investment: float = typer.Option(default=3.0, help="Dollar amount to invest in the AI company."),
    n_round: int = typer.Option(default=5, help="Number of rounds for the simulation."),
    project_name: str = typer.Option(default="", help="Unique project name, such as 'game_2048'."),
    project_path: str = typer.Option(
        default="",
        help="Specify the directory path of the old version project to fulfill the incremental requirements.",
    ),
    reqa_file: str = typer.Option(
        default="", help="Specify the source file name for rewriting the quality assurance code."
    ),
    max_auto_summarize_code: int = typer.Option(
        default=0,
        help="The maximum number of times the 'SummarizeCode' action is automatically invoked, with -1 indicating "
        "unlimited. This parameter is used for debugging the workflow.",
    ),
):
    pass

if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        print(f"Caught error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
