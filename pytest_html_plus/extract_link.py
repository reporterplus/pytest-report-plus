def extract_links_from_item(item):
    links = []
    possible_link_markers = ["link", "testcase", "jira", "issue", "ticket"]

    for marker_name in possible_link_markers:
        for marker in item.iter_markers(name=marker_name):
            if marker.args:
                links.extend(str(arg) for arg in marker.args)

    return links
