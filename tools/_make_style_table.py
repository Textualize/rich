"""Generate a ANSI style table."""


def make_table():
    table = []
    for attributes in range(0, 512):
        ansi_codes = []
        for bit_no in range(0, 9):
            bit = 1 << bit_no
            if attributes & bit:
                ansi_codes.append(str(1 + bit_no))
        table.append(";".join(ansi_codes))
    return table


table = make_table()
print(repr(table))

