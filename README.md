# getyoutubetranscript

[![License](https://img.shields.io/badge/License-MIT-4CAF50?style=for-the-badge)](./LICENSE)
[![Website](https://img.shields.io/badge/Website-getyoutubetranscript.com-FF3B00?style=for-the-badge)](https://getyoutubetranscript.com)

Python SDK for the [GetYouTubeTranscript](https://getyoutubetranscript.com) REST API - get YouTube transcripts, search videos and channels, resolve channel handles, browse a channel's full upload history, search inside a channel, and pull playlist contents, all with one typed client.

Not published to PyPI yet - install straight from this repo.

## Install

```bash
pip install git+https://github.com/tubeagentkit/python-sdk.git
```

Requires Python 3.9+.

## Quickstart

```python
from getyoutubetranscript import Client

client = Client(api_key="sk_live_...")

transcript = client.get_transcript("https://www.youtube.com/watch?v=jNQXAC9IVRw")
print(transcript["title"], transcript["word_count"])
print(transcript["transcript"])
```

## Getting an API key

Every request needs an API key. There are two ways to get one:

1. **Dashboard** - sign up at [getyoutubetranscript.com](https://getyoutubetranscript.com). Free tier: 100 credits, no card required.
2. **Self-serve, in code** - use the `signup`/`verify_signup` helpers below. No key required for either call.

```python
from getyoutubetranscript import signup, verify_signup

signup("you@example.com")          # sends a 6-digit code, valid 10 minutes
# ... read the code from your inbox ...
api_key = verify_signup("you@example.com", "123456")  # -> "sk_live_..."
```

The raw key is returned once by `verify_signup` and can't be retrieved again - store it yourself (env var, secret manager, etc).

## Usage

Every method costs 1 credit unless noted "free" below. Failed and rate-limited requests are never charged. All methods raise `GetYouTubeTranscriptError` on failure - see [Error handling](#error-handling).

### Transcripts

```python
client.get_transcript("jNQXAC9IVRw", language="en")
```

### Search

```python
client.search("lofi beats", type="video", limit=10)

# Pagination
page2 = client.search(page_token=first_page["pagination"]["next_page_token"])
```

### Channels

```python
client.resolve_channel("@mkbhd")            # free - handle/URL -> channel ID
client.get_channel_latest("@mkbhd")         # free - metadata + latest uploads
client.search_channel("@mkbhd", "iphone")   # search within a channel
client.list_channel_videos("@mkbhd")        # full paginated upload history

# Pagination (search_channel and list_channel_videos both work the same way)
page = client.list_channel_videos("@mkbhd")
while page["has_more"]:
    page = client.list_channel_videos(continuation=page["continuation_token"])
```

### Playlists

```python
page = client.get_playlist("PLillGF-RfqbYE6Ik_EuXA2iZFcE082B3s")
while page["has_more"]:
    page = client.get_playlist(continuation=page["continuation_token"])
```

## Error handling

Every non-2xx or `{"success": false}` response raises `GetYouTubeTranscriptError` with the API's parsed error shape:

```python
from getyoutubetranscript import Client, GetYouTubeTranscriptError

client = Client(api_key="sk_live_...")

try:
    client.get_transcript("no-captions-here")
except GetYouTubeTranscriptError as e:
    print(e.code)          # e.g. "NOT_FOUND"
    print(e.message)       # human-readable message from the API
    print(e.status_code)   # 400 / 401 / 402 / 404 / 429 / 503, or 0 for a local network failure
    print(e.response_body) # full parsed error body, e.g. {"creditsLeft": 0} on PAYMENT_REQUIRED
```

## Development

```bash
pip install -e ".[dev]"

# Unit tests - mocked HTTP, no network or API key needed, always safe to run
pytest tests -v --ignore=tests/live

# Live integration tests - hits the real API, spends credits, needs a key
GYT_API_KEY=sk_live_... pytest tests/live -v
```

## Links

- [Full API docs](https://getyoutubetranscript.com/docs)
- [OpenAPI spec](https://getyoutubetranscript.com/openapi.json)
- [MCP server](https://getyoutubetranscript.com/youtube-mcp-server) - if you want an AI agent to call this API directly instead of via Python

## License

MIT - see [LICENSE](./LICENSE).
