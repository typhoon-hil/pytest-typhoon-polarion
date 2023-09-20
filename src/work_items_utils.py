
class AllureReportData:
    host = '192.168.1.92'
    port = 63650

    suite_uid = '88161aaa9646217cd0c3752f09c90267'

    test_cases_uid = {
        'Demo2/test_demo2.py::test_if_true': '1c10a9bbb0884ffc',
        'Demo2/test_demo2.py::test_if_false': 'dfbb10ec01e4e66d',
        'Demo2/test_demo2.py::test_with_parametrize[0]': '2cb1e146673ad37b',
    }


def get_test_case_url(test_node_id):
    a = AllureReportData()
    url_pattern = 'http://{host}:{port}/index.html#suites/{suite_uid}/{test_uid}/'

    host = a.host
    port = a.port

    suite_uid = a.suite_uid
    test_uid = a.test_cases_uid[test_node_id]

    return url_pattern.format(
        host=host,
        port=port,
        suite_uid=suite_uid,
        test_uid=test_uid
    )

    # def get_all_test_case_url(self):
    #     url_pattern = 'http://{host}:{port}/allure-html/#suites/{suite_uid}/{test_uid}/'

    #     host = self.host
    #     port = self.port

    #     suite_uid = self.suite_uid

    #     urls = {}

    #     for key in a.test_cases_uid:
    #         urls[key] = url_pattern.format(
    #             host=host,
    #             port=port,
    #             suite_uid=suite_uid,
    #             test_uid=self.test_cases_uid[key]
    #         )

    #     return urls


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
