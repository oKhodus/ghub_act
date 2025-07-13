import requests
from sys import argv


def main(username):
    try:
        events = fetch_events(username)
        parsed = parse_events(events)
        messages = format_messages(parsed, username)
        for message in messages:
            print(message)
    except Exception as e:
        print(f"Error: {e}")


def fetch_events(username):
    """Fetch events JSON data from GitHub API for a username"""
    url = f"https://api.github.com/users/{username}/events"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"GitHub API returned status {response.status_code}")
    return response.json()


def parse_events(events):
    """Parse raw events JSON into a list of dicts with event details."""
    parsed = []
    for event in events:
        event_type = event.get("type")
        payload = event.get("payload", {})
        repo = event.get("repo", {}).get("name", "unknown repo")

        parsed.append(
            {
                "type": event_type,
                "repo": repo,
                "issue": payload.get("issue", {}).get("number"),
                "pr": payload.get("pull_request", {}).get("number"),
                "ref_type": payload.get("ref_type"),
                "ref": payload.get("ref"),
            }
        )
    return parsed


def format_messages(events_info, username):
    """Format parsed events into readable messages."""
    messages = []
    templates = {
        "IssueCommentEvent": "- {username} commented on issue #{issue}",
        "PushEvent": "- {username} pushed commit to {repo}",
        "IssuesEvent": "- {username} created issue #{issue}",
        "WatchEvent": "- {username} starred {repo}",
        "PullRequestEvent": "- {username} created pull request #{pr}",
        "PullRequestReviewEvent": "- {username} reviewed pull request #{pr}",
        "PullRequestReviewCommentEvent": "- {username} commented on pull request #{pr}",
        "CreateEvent": "- {username} created {ref_type} {ref}",
        "ForkEvent": "- {username} forked {repo}",
    }
    for event in events_info:
        msg = templates.get(event["type"], f"- ??? {event['type']} (event not handled)")
        messages.append(
            msg.format(
                username=username,
                repo=event["repo"],
                issue=event["issue"] or "unknown",
                pr=event["pr"] or "unknown",
                ref_type=event["ref_type"] or "unknown",
                ref=event["ref"] or "unknown",
            )
        )
    return messages


if __name__ == "__main__":

    (
        main(argv[1])
        if len(argv) > 1
        else print("Usage: python3 (or just <python>) fetch.py <username>")
    )
