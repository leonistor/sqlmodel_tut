from invoke import task


@task
def dummy(c, clean=False):
    """Dummy task with optional 'clean' argument."""
    if clean:
        print(f"cleaning")
    print(f"building")
    c.run("ls -la")


@task({"name": "Name of person to say hi to."})
def hi(c, name):
    """Say hi to someone."""
    print(f"hello: {name}")


@task
def clean(c):
    """Remove sqlite database."""
    c.run("rm data/db.sqlite")


@task(pre=[clean])
def run(c):
    """Run app."""
    c.run("clear")
    c.run("echo 'Not implemented yet.'")


@task
def dev(c):
    """Develop app."""
    c.run("uvicorn app:app --reload", pty=True)
