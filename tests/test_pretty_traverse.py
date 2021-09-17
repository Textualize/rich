from rich.pretty import traverse


def test_class():
    """Test if can traverse a class."""

    class Plop:
        pass

    traverse(Plop)


def test_instance():
    """Test if can traverse a class's instance."""

    class Plop:
        pass

    traverse(Plop())


def test_class_getattr():
    """Test if can traverse a class with special __getattr__'s casting."""

    class NotCallable:
        pass

    class Meta(type):
        def __getattr__(self, name):
            return NotCallable()

    class Plop(metaclass=Meta):
        pass

    traverse(Plop)


def test_instance_getattr():
    """Test if can traverse a class's instance with special __getattr__'s casting."""

    class NotCallable:
        pass

    class Plop:
        def __getattr__(self, name):
            return NotCallable()

    traverse(Plop())


def test_method():
    """Test if can traverse a method."""

    def plop():
        pass

    traverse(plop)


def test_integer():
    """Test if can traverse an integer."""
    plop = 44
    traverse(plop)


def test_float():
    """Test if can traverse a float."""
    plop = 1.618
    traverse(plop)


def test_string():
    """Test if can traverse a string."""
    plop = "plop"
    traverse(plop)


def test_list():
    """Test if can traverse a list."""
    plop = ["plop", "test"]
    traverse(plop)


def test_tuple():
    """Test if can traverse a tuple."""
    plop = ("plop", "test")
    traverse(plop)


def test_set():
    """Test if can traverse a set."""
    plop = {"plop", "test"}
    traverse(plop)


def test_dictionary():
    """Test if can traverse a dictionary."""
    plop = {"plop": "PLOP", "test": 5}
    traverse(plop)


def test_iterator():
    """Test if can traverse an iterator."""
    plop = ["plop", "test"]
    traverse(iter(plop))


def test_generator():
    """Test if can traverse a generator."""
    plop = ["plop", "test"]
    traverse(item for item in plop)


def test_builtin_method():
    """Test if can traverse a built-in method."""
    plop = bool
    traverse(plop)


def test_module():
    """Test if can traverse a module."""
    import rich as plop

    traverse(plop)
