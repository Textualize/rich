from rich.repr import rich_repr


@rich_repr
class Bird:
    def __init__(self, name, eats=None, fly=True, extinct=False):
        self.name = name
        self.eats = list(eats) if eats else []
        self.fly = fly
        self.extinct = extinct

    def __rich_repr__(self):
        yield self.name
        yield "eats", self.eats
        yield "fly", self.fly, True
        yield "extinct", self.extinct, False

    __rich_repr__.angular = True


from rich import print

BIRDS = {
    "gull": Bird("gull", eats=["fish", "chips", "ice cream", "sausage rolls"]),
    "penguin": Bird("penguin", eats=["fish"], fly=False),
    "dodo": Bird("dodo", eats=["fruit"], fly=False, extinct=True),
}
print(BIRDS)
