import random
import string


def generate_inputs(input_types):
    result = []
    for typ in input_types:
        if typ.startswith("uint"):
            result.append(random.randint(0, 2**32))
        elif typ.startswith("int"):
            result.append(random.randint(-(2**31), 2**31 - 1))
        elif typ == "bool":
            result.append(random.choice([True, False]))
        elif typ.startswith("address"):
            result.append("0x" + "".join(random.choices("0123456789abcdef", k=40)))
        elif typ.startswith("string"):
            result.append(
                "".join(random.choices(string.ascii_letters + string.digits, k=8))
            )
        else:
            result.append(None)  # Unsupported type fallback
    return result
