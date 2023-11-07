from rich._stack import Stack


def test_stack():
    stack = Stack()
    stack.push("foo")
    stack.push("bar")
    assert stack.top == "bar"
    assert stack.pop() == "bar"
    assert stack.top == "foo"
