#!/usr/bin/env python3

import argparse
import json
import re
import sys
from collections import OrderedDict


def to_pascal_case(value: str) -> str:
    parts = re.split(r"[^a-zA-Z0-9]+", value)
    cleaned = [part for part in parts if part]
    if not cleaned:
        return "GeneratedClass"
    return "".join(part[:1].upper() + part[1:] for part in cleaned)


def sanitize_identifier(value: str) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9_]", "_", value)
    if not sanitized:
        sanitized = "field"
    if sanitized[0].isdigit():
        sanitized = f"_{sanitized}"
    return sanitized


def nested_class_name_from_key(key: str) -> str:
    pascal_name = to_pascal_case(key)
    if pascal_name.lower().startswith("sub"):
        return pascal_name
    return f"Sub{pascal_name}"


class ClassCollector:
    def __init__(self) -> None:
        self.classes: "OrderedDict[str, list[tuple[str, str]]]" = OrderedDict()
        self.used_names: set[str] = set()

    def unique_class_name(self, base_name: str) -> str:
        name = to_pascal_case(base_name)
        if name not in self.used_names:
            self.used_names.add(name)
            return name

        index = 1
        while f"{name}{index}" in self.used_names:
            index += 1
        unique_name = f"{name}{index}"
        self.used_names.add(unique_name)
        return unique_name

    def resolve_type(self, key: str, value):
        if isinstance(value, bool):
            return "int"
        if isinstance(value, int):
            return "int"
        if isinstance(value, float):
            return "double"
        if isinstance(value, str):
            return "string"
        if isinstance(value, list):
            return self.resolve_array_type(key, value)
        if value is None:
            return "string"
        if isinstance(value, dict):
            class_name = self.build_class(nested_class_name_from_key(key), value)
            return class_name
        return "string"

    def resolve_array_type(self, key: str, values: list) -> str:
        if not values:
            return "string[]"

        element_types = {self.resolve_array_element_type(key, value) for value in values}
        if len(element_types) == 1:
            return f"{element_types.pop()}[]"

        if element_types.issubset({"int", "double"}):
            return "double[]"

        return "string[]"

    def resolve_array_element_type(self, key: str, value) -> str:
        if isinstance(value, bool):
            return "int"
        if isinstance(value, int):
            return "int"
        if isinstance(value, float):
            return "double"
        if isinstance(value, str):
            return "string"
        if isinstance(value, dict):
            return self.build_class(nested_class_name_from_key(key), value)
        if isinstance(value, list):
            return "string"
        if value is None:
            return "string"
        return "string"

    def build_class(self, class_name: str, data: dict) -> str:
        unique_name = self.unique_class_name(class_name)
        fields = []
        for key, value in data.items():
            field_name = sanitize_identifier(key)
            field_type = self.resolve_type(key, value)
            fields.append((field_type, field_name))
        self.classes[unique_name] = fields
        return unique_name


def render_classes(classes: "OrderedDict[str, list[tuple[str, str]]]", root_class_name: str) -> str:
    output = []
    class_items = list(classes.items())

    for class_name, fields in class_items:
        header = f"class {class_name} : public Json" if class_name == root_class_name else f"class {class_name}"
        output.append(header)
        output.append("{")
        for field_type, field_name in fields:
            output.append(f"    {field_type} {field_name};")
        output.append("};")
        output.append("")

    return "\n".join(output).rstrip() + "\n"


def load_json(args) -> dict:
    if args.json_text:
        return json.loads(args.json_text)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as handle:
            return json.load(handle)
    return json.load(sys.stdin)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate simple C++-style classes from a JSON object."
    )
    parser.add_argument(
        "--class-name",
        default="MyObject",
        help="Name of the root class. Default: MyObject",
    )
    parser.add_argument(
        "--file",
        help="Path to a JSON file. If omitted, stdin is used unless --json is provided.",
    )
    parser.add_argument(
        "--json",
        dest="json_text",
        help="JSON text passed directly on the command line.",
    )

    args = parser.parse_args()

    try:
        data = load_json(args)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Failed to read input: {exc}", file=sys.stderr)
        return 1

    if not isinstance(data, dict):
        print("Root JSON value must be an object.", file=sys.stderr)
        return 1

    collector = ClassCollector()
    root_class_name = collector.build_class(args.class_name, data)
    output = render_classes(collector.classes, root_class_name)
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
