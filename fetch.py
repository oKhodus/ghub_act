import requests, sys

def parse(username):

    url = f"https://api.github.com/users/{username}/events"

    response = requests.get(url)

    if response.status_code == 200:
        imple(response.json(), username)
    else:
        print(
            f"Something goes wrong... :(\nResponse is: {response.status_code} \
\nPlease check internet or your entered username"
        )


def imple(response, username):
    
    for event in response:
        event_type = event.get('type')
        payload = event.get('payload', {})
        repo = event.get('repo', {}).get('name', 'unknown repo')

        issue = payload.get('issue', {}).get('number', 'unknown')
        pr = payload.get('pull_request', {}).get('number', 'unknown')
        ref_type = payload.get('ref_type', 'unknown')
        ref = payload.get('ref', 'unknown')

        messages = {
            'IssueCommentEvent': f"- {username} commented on issue #{issue}",
            'PushEvent': f"- {username} pushed commit to {repo}",
            'IssuesEvent': f"- {username} created issue #{issue}",
            'WatchEvent': f"- {username} starred {repo}",
            'PullRequestEvent': f"- {username} created pull request #{pr}",
            'PullRequestReviewEvent': f"- {username} reviewed pull request #{pr}",
            'PullRequestReviewCommentEvent': f"- {username} commented on pull request #{pr}",
            'CreateEvent': f"- {username} created {ref_type} {ref}",
            'ForkEvent': f"- {username} forked {repo}",
        }
    
        print(messages.get(event_type, f"- ??? {event_type}"))

# example_username = "torvalds"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        parse(sys.argv[1])
    else:
        print("Usage: python3 github_events.py <username>")
    # parse(example_username)


# https://api.github.com/users/<username>/events


