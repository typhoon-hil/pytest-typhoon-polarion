# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Options for attaching allure report hyperlink and to allow logining information on Polarion Tests Cases, including parametrized tests.
- Settings structure have more attributes for the new options.
- New exceptions added.

### Fixed
- Plugin check connection with Polarion before start to collect and run the tests.
- Exceptions on Polarion side are treated properly.

### Changed

### Removed

## [0.0.1]

### Added

- Implementation of syncing of test results with similar structure as `pytest-typhoon-xray` plugin to Polarion Server. The options implemented are:
    - `--secrets=<secrets_file>`: Passes the file with server and login information.
    - `--polarion-project-id=<project_id>`: Passes the project id configured in the Polarion server.
    - `--polarion-test-run=<test_run_id>`: Passes the test run id inside the project previously configured in the Polarion server.

- README.md and DEMO.md documentation files created.
