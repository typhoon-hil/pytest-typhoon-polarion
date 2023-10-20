import os
import json


def process_report(report_path):
    suites_path = None
    for root, dirs, files in os.walk(report_path):
        if root.endswith("data"):
            data_path = root
            if "suites.json" in files:
                suites_path = os.path.join(root, "suites.json")
    if suites_path is not None:
        with open(suites_path, encoding="utf-8") as json_file:
            suites = json.load(json_file)
    return suites


def _get_uid_values_rec(children, uid_test_name_mapping=dict(), child_full_name=list()):
    for child in children:
        if 'children' in child.keys():
            child_full_name.append(child['name'])
            return _get_uid_values_rec(child['children'], uid_test_name_mapping, child_full_name)
        else:
            key = '/'.join(child_full_name) + '.py::' + child['name']
            uid = child['uid']

            uid_test_name_mapping[key] = uid

    parent_uid = child['parentUid']
    return uid_test_name_mapping, parent_uid


def get_uid_values(report_path):
    json_file = process_report(report_path)
    json_file_children = json_file['children']
    return _get_uid_values_rec(json_file_children)


def get_test_case_url(web_url, parent_uid, uid_test_mapping, test_node_id):
    url_pattern = '{web_url}#suites/{parent_uid}/{test_uid}/'

    return url_pattern.format(
        web_url=web_url,
        parent_uid=parent_uid,
        test_uid=uid_test_mapping[test_node_id],
    )
