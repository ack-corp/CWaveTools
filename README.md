# C~ Tools

## JSON To Class

`jsonToClass.py` is a small Python script that reads a JSON object and generates simple C~ class definitions.

It supports:
- `string`
- `int`
- `double`
- typed arrays such as `string[]`, `int[]`, and `double[]`
- nested JSON objects converted into sub-classes

Example usage:

```bash
python3 jsonToClass.py --file test.json --class-name MyObject
```

The root object is generated as a class inheriting from `Json`, and nested objects are emitted as additional classes.
