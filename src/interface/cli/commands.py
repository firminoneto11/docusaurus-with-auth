from typer import Typer

cli = Typer()


@cli.command("create-user")
def create_user(username: str, password: str): ...


@cli.command("remove-user")
def remove_user(username: str): ...
