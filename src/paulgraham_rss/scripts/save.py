import json
import sys

# Read all input first
input_data = sys.stdin.read()

try:
    # Try to parse as JSON
    data = json.loads(input_data)

    # Check if it has the nested "content" structure
    if (
        isinstance(data, dict)
        and "content" in data
        and isinstance(data["content"], str)
    ):
        content = data["content"]
    elif (
        isinstance(data, dict)
        and "content" in data
        and isinstance(data["content"], dict)
        and "content" in data["content"]
    ):
        content = data["content"]["content"]
    else:
        content = input_data

    # Get title if available
    if (
        isinstance(data, dict)
        and "content" in data
        and isinstance(data["content"], dict)
        and "title" in data["content"]
    ):
        title = data["content"]["title"]
    else:
        title = "Saved Content"

except (json.JSONDecodeError, KeyError, TypeError):
    # If not JSON or wrong structure, use the entire input as content
    content = input_data
    title = "Saved Content"

print(
    f"<!DOCTYPE html>"
    f"<html>"
    f"<head><meta charset=\"UTF-8\"><title>{title}</title></head>"
    f"<body>{content}</body>"
    f"</html>"
)
