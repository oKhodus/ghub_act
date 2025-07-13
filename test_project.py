import project


def test_parse_events():
    raw = [
        {"type": "PushEvent", "payload": {}, "repo": {"name": "repo1"}},
        {
            "type": "IssuesEvent",
            "payload": {"issue": {"number": 5}},
            "repo": {"name": "repo2"},
        },
    ]
    parsed = project.parse_events(raw)
    assert parsed[0]["type"] == "PushEvent"
    assert parsed[0]["repo"] == "repo1"
    assert parsed[1]["issue"] == 5
    assert parsed[1]["repo"] == "repo2"


def test_format_messages():
    events_info = [
        {
            "type": "PushEvent",
            "repo": "repo1",
            "issue": None,
            "pr": None,
            "ref_type": None,
            "ref": None,
        },
        {
            "type": "IssuesEvent",
            "repo": "repo2",
            "issue": 10,
            "pr": None,
            "ref_type": None,
            "ref": None,
        },
        {
            "type": "UnknownEvent",
            "repo": "repo3",
            "issue": None,
            "pr": None,
            "ref_type": None,
            "ref": None,
        },
    ]
    messages = project.format_messages(events_info, "testuser")
    assert messages[0] == "- testuser pushed commit to repo1"
    assert messages[1] == "- testuser created issue #10"
    assert messages[2].startswith("- ??? UnknownEvent")


def test_format_messages_handles_none():
    events_info = [
        {
            "type": "CreateEvent",
            "repo": "repoX",
            "issue": None,
            "pr": None,
            "ref_type": None,
            "ref": None,
        }
    ]
    messages = project.format_messages(events_info, "alex")
    assert "- alex created unknown unknown" in messages[0]
