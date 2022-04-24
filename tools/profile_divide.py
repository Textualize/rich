from rich.segment import Segment

text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""


segments = [Segment(text[n : n + 7]) for n in range(0, len(text), 7)]


from time import perf_counter

start = perf_counter()
for _ in range(10000):
    list(Segment.divide(segments, [0, 1, 20, 24, 65, len(text)]))
print(perf_counter() - start)
