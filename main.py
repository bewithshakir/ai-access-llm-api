import json
import os
import urllib.error
import urllib.request

TOKEN = os.environ.get("GITHUB_TOKEN")
ENDPOINT = "https://models.github.ai/inference"
MODEL = os.environ.get("GITHUB_MODEL", "openai/gpt-4o-mini")


def main() -> None:
    if not TOKEN:
        raise RuntimeError("GITHUB_TOKEN environment variable is not set")

    payload = {
        "messages": [
            {"role": "system", "content": ""},
            {"role": "user", "content": "How to learn OpenAI API?"},
        ],
        "model": MODEL,
    }

    request = urllib.request.Request(
        f"{ENDPOINT}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as response:
            body = json.load(response)
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8")
        raise RuntimeError(f"API request failed: {exc.code} {error_body}") from exc

    print(body["choices"][0]["message"]["content"])


if __name__ == "__main__":
    main()

