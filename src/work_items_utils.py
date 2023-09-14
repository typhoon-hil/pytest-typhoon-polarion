
# URL is: localhost:port/index.html#suites/SUITE_UID/TEST_UID/

def __find_element_in_dict_list(data, prop, value):
    return next((item for i, item in enumerate(data) if item[prop] == value), None)


def store_results(report, behaviors, suites,  path):
    executed_tests = []
    for test in behaviors['children']:
        test_path = os.path.join(path, 'test-cases', test['uid'] + '.json')
        try:
            with open(test_path, encoding="utf-8") as json_file:
                test_data = json.load(json_file)
                parent_suite = __find_element_in_dict_list(test_data['labels'], 'name', 'parentSuite')
                test_suite = __find_element_in_dict_list(test_data['labels'], 'name', 'suite')
                suite_parts = []
                test_uid = test_data['uid']
                suite_uid = ''
                if parent_suite is not None:
                    suite_parts.append(parent_suite['value'].replace(".", "/"))
                    parent_suite_data = __find_element_in_dict_list(suites['children'], 'name', parent_suite['value'])
                    if parent_suite_data is not None and test_suite is not None:
                        suite_data = __find_element_in_dict_list(parent_suite_data['children'], 'name',
                                                                 test_suite['value'])
                        if parent_suite_data is not None:
                            suite_uid = suite_data['uid']
                if test_suite is not None:
                    suite_parts.append(test_suite['value'] + ".py")
                suite = "/".join(suite_parts)
                name = test_data['name'] if "[" not in test_data['name'] else test_data['name'].replace("-", ",")

                status = TestStatus.parse(test_data['status'].upper()).value
                executed_tests.append(ExecutedTest(name=name, suite=suite, status=status, report=report,
                                                   test_uid=test_uid, suite_uid=suite_uid,
                                                   created_at=datetime.now(timezone.utc)))
        except Exception as e:
            log.fatal(e)
            continue


def store_test_results(report, allure_report_path):
    behaviors, suites, environment, path = utils.process_report(allure_report_path)
    if behaviors is not None and suites is not None:
        store_results(report, behaviors, suites, path)


def process_report(report_path):
    behaviors_path, suites_path, environment_path, data_path, environment = None, None, None, None, []
    for root, dirs, files in os.walk(report_path):
        if root.endswith("data"):
            data_path = root
            if "behaviors.json" in files:
                behaviors_path = os.path.join(root, "behaviors.json")
            if "suites.json" in files:
                suites_path = os.path.join(root, "suites.json")
        elif root.endswith("widgets"):
            if "environment.json" in files:
                environment_path = os.path.join(root, "environment.json")
    if behaviors_path is not None and suites_path is not None:
        with open(behaviors_path, encoding="utf-8") as json_file:
            behaviors = json.load(json_file)
        with open(suites_path, encoding="utf-8") as json_file:
            suites = json.load(json_file)
    if environment_path is not None:
        with open(environment_path, encoding="utf-8") as json_file:
            environment = json.load(json_file)
    return behaviors, suites, environment, data_path
