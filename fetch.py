import requests, sys

def parse(username):
    """
    parse() - function of parsing total activities of user
    username - argument from sys.argv (terminal input), 
                actual username of user's profile in github, who will be parsed
    url - actual api link of github
        if status code is 200 (connection is ok) then will be made function imple()
    """

    url = f"https://api.github.com/users/{username}/events"

    response = requests.get(url)

    try:
        if response.status_code == 200:
            imple(response.json(), username)
        else:
            raise e

    except Exception as e:
        print(
            f"Something goes wrong... :(\nResponse is: {response.status_code} \
\nPlease check internet or your entered username"
        )


def imple(response, username):
    """
    imple() - implementation function of parsing user's profile
    args:
        response - total data in json format
        username - argument from parse(username), 
                actual username of user's profile in github, who will be parsed
    
    messages - dict of templates, which wull be used for formatting of otput and checking condition, 
    if event in messages then will be used suitable template

    """
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
    
        print(messages.get(event_type, f"\n- ??? {event_type}\n\
that event hasn't added to the dict, wait please for new update\n"))

# example_username = "torvalds"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        """
        checking if username (sys.argv[1]) was inputted 
        else will be printed - template how to input properly
        """
        parse(sys.argv[1])
        # parse(example_username)
    else:
        print("Usage: python3 fetch.py <username>\nexample_username = \'torvalds\'")

"""
link of API

https://api.github.com/users/<username>/events

"""


