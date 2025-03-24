from enum import Enum


def gen_enum_doc(e: Enum):
    items = [f"{i.name}: {i.value}" for i in list(e)]
    doc = "\n".join(items)
    return f"```\n{doc}\n```"
