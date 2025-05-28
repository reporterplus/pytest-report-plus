# import platform
# import shutil
# from datetime import datetime
# from pathlib import Path
#
# import pytest
#
# from pytest_json_reporter.generate_flakytest_report import generate_flaky_html
# from pytest_json_reporter.generate_html_report import JSONReporter
# from pytest_json_reporter.json_merge import merge_json_reports
# from pytest_json_reporter.send_email_report import send_email_from_env, load_email_env
#
# python_executable = shutil.which("python3") or shutil.which("python")
# test_screenshot_paths = {}
#
#
# import logging
#
# logger = logging.getLogger()  # root logger
# logger.setLevel(logging.INFO)
#
# if not logger.handlers:
#     handler = logging.StreamHandler()
#     formatter = logging.Formatter('%(levelname)s - %(message)s')
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)
#
#
# @pytest.hookimpl(tryfirst=True)
# def pytest_runtest_setup(item):
#     if "caplog" not in item.fixturenames:
#         item.fixturenames.append("caplog")
#
# import os
# _saved_config = None
#
# def pytest_collectreport(report):
#     if report.failed:
#         global _saved_config
#         reporter = getattr(_saved_config, "_json_reporter", None)
#         if reporter:
#             reporter.log_result(
#                 test_name="COLLECTION ERROR",
#                 nodeid=str(report.nodeid),
#                 status="failed",
#                 duration=getattr(report, "duration", 0.0),
#                 error=str(report.longrepr),
#                 markers=[],
#                 filepath=str(report.fspath),
#                 lineno=0,
#                 stdout="",
#                 stderr="",
#                 screenshot=None,
#                 logs=None,
#                 worker=os.getenv("PYTEST_XDIST_WORKER") or "main"
#             )
#
#
#
#
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()
#
#     if report.when == "call" or (report.when == "setup" and report.skipped):
#         is_error = report.failed and report.when != "call"
#         is_skipped = report.skipped
#         status = "skipped" if is_skipped else "failed" if is_error else report.outcome
#         config = item.config
#         capture_option = config.getoption("--capture-screenshots")
#         tool = config.getoption("--automation-tool")
#
#         caplog_text = None
#         if "caplog" in item.funcargs:
#             caplog = item.funcargs["caplog"]
#             caplog_text = "\n".join(caplog.messages) if caplog.messages else None
#
#         screenshot_path = None
#         should_capture_screenshot = (
#             capture_option == "all" or
#             (capture_option == "failed" and report.outcome == "failed")
#         )
#
#         if should_capture_screenshot:
#             driver = item.funcargs.get("page" if tool == "playwright" else "driver", None)
#             if driver:
#                 screenshot_path = take_screenshot_on_failure(item, driver)
#         reporter = config._json_reporter
#         worker_id = os.getenv("PYTEST_XDIST_WORKER") or "main"
#         reporter.log_result(
#             test_name=item.name,
#             nodeid=item.nodeid,
#             status=status,
#             duration=report.duration,
#             error=str(report.longrepr) if report.failed else None,
#             markers=[m.name for m in item.iter_markers()],
#             filepath=item.location[0],
#             lineno=item.location[1],
#             stdout=getattr(report, "capstdout", ""),
#             stderr=getattr(report, "capstderr", ""),
#             screenshot=screenshot_path,
#             logs=caplog_text,
#             worker=worker_id
#         )
#
# import subprocess
#
#
# def pytest_sessionfinish(session, exitstatus):
#     reporter = session.config._json_reporter
#     print("pytest_sessionfinish called")
#
#     json_path = session.config.getoption("--json-report") or "playwright_report.json"
#     html_output = session.config.getoption("--html-output") or "report_output"
#     screenshots = session.config.getoption("--screenshots") or "screenshots"
#
#     is_worker = os.getenv("PYTEST_XDIST_WORKER") is not None
#     is_xdist = hasattr(session.config, "workerinput") or is_worker
#     print(f"is_worker is {is_worker}")
#     if is_worker:
#         # Just write individual worker's report
#         reporter.write_report()
#         print(f"Worker {os.getenv('PYTEST_XDIST_WORKER')} finished – skipping merge.")
#         return
#
#     if is_xdist:
#         # Main process in xdist run — merge all worker reports
#         print("Merging reports in main process...")
#         merge_json_reports(directory=".pytest_worker_jsons", output_path=json_path)
#     # Main process: merge all and generate final report
#
#     # Now generate the HTML report
#     script_path = os.path.join(os.path.dirname(__file__), "generate_html_report.py")
#
#     if not os.path.exists(script_path):
#         print(f"Warning: Report generation script not found at {script_path}. Skipping HTML report generation.")
#         return
#
#     try:
#         subprocess.run([
#             sys.executable,
#             script_path,
#             "--report", json_path,
#             "--screenshots", screenshots,
#             "--output", html_output
#         ], check=True)
#         print(f"✅ HTML report generated at {html_output}/report.html")
#     except Exception as e:
#         print(f"❌ Exception during HTML report generation: {e}")
#
#     if session.config.getoption("--detect-flake"):
#         report_path = session.config.getoption("--json-report")
#         with open(report_path, "r") as f:
#             full_report = json.load(f)
#
#         timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
#
#         lib_root = Path(__file__).resolve().parent
#         internal_data_dir = lib_root / "flake_run_data" / "runs"
#         internal_data_dir.mkdir(parents=True, exist_ok=True)
#
#         output_path = internal_data_dir / f"{timestamp}.json"
#         with open(output_path, "w") as f:
#             json.dump(full_report, f, indent=2)
#
#         print(f"📦 Internal flake run data saved to {output_path}")
#
#         # Pass the path to internal_data_dir to detect_flakes so it knows where to read runs from
#         detect_flakes(runs_dir=internal_data_dir)
#     if session.config.getoption("--send-email"):
#         print("📬 --send-email enabled. Sending report...")
#         try:
#             config = load_email_env()
#             send_email_from_env(config)
#         except Exception as e:
#             print(f"❌ Failed to send email: {e}")
#
#
# def pytest_sessionstart(session):
#     configure_logging()
#     print("Plugin loaded: pytest_sessionstart called")
#
# def pytest_runtest_logreport(report):
#     print(f"pytest_runtest_logreport: {report.nodeid} - {report.outcome}")
#
# def pytest_load_initial_conftests(args):
#     if not any(arg.startswith("--capture") for arg in args):
#         args.append("--capture=tee-sys")
#
# def pytest_addoption(parser):
#     parser.addoption(
#         "--json-report",
#         action="store",
#         default="playwright_report.json",
#         help="Directory to save individual JSON test reports"
#     )
#     parser.addoption(
#         "--automation-tool",
#         action="store",
#         default="playwright",
#         choices=["selenium", "playwright"],
#         help="Specify automation tool: selenium (default) or playwright"
#     )
#     parser.addoption(
#         "--capture-screenshots",
#         action="store",
#         default="failed",
#         choices=["failed", "all", "none"],
#         help="Capture screenshots: failed (default), all, or none"
#     )
#     parser.addoption("--html-output", default="report_output")
#     parser.addoption("--screenshots", default="screenshots")
#     parser.addoption(
#         "--send-email",
#         action="store_true",
#         default=False,
#         help="Send HTML test report via email after test run"
#     )
#     parser.addoption(
#         "--detect-flake",
#         action="store",
#         default=False,
#         help="Helps capture flaky tests in the last n number of builds"
#     )
#
#
# def take_screenshot_on_failure(item, page):
#     print("✅ take_screenshot_on_failure was called")
#     screenshot_dir = os.path.join(os.getcwd(), "screenshots")
#     os.makedirs(screenshot_dir, exist_ok=True)
#     filename = f"{item.name}.png".replace("/", "_").replace("\\", "_")
#     path = os.path.join(screenshot_dir, filename)
#     # Assuming sync call here, adjust if async
#     page.screenshot(path=path)
#     return path
#
# def take_screenshot_selenium(item, driver):
#     screenshot_dir = os.path.join(os.getcwd(), "screenshots")
#     os.makedirs(screenshot_dir, exist_ok=True)
#     filename = f"{item.name}.png".replace("/", "_").replace("\\", "_")
#     path = os.path.join(screenshot_dir, filename)
#     driver.save_screenshot(path)
#     return path
#
# import logging
# import sys
#
# def configure_logging():
#     logger = logging.getLogger()
#     logger.setLevel(logging.INFO)
#
#     # Avoid adding multiple handlers if rerun in same session
#     if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
#         handler = logging.StreamHandler(sys.stdout)
#         handler.setLevel(logging.INFO)
#         formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#         handler.setFormatter(formatter)
#         logger.addHandler(handler)
#
# def pytest_configure(config):
#     global _saved_config
#     _saved_config = config
#
#     report_path = config.getoption("--json-report") or "playwright_report.json"
#     worker_id = os.getenv("PYTEST_XDIST_WORKER")
#
#     if worker_id:
#         INTERNAL_JSON_DIR = Path(".pytest_worker_jsons")
#         INTERNAL_JSON_DIR.mkdir(parents=True, exist_ok=True)
#         name, ext = os.path.splitext(report_path)
#         report_path = INTERNAL_JSON_DIR / f"{name}_{worker_id}{ext}"
#
#     config._json_reporter = JSONReporter(report_path=report_path)
#
#
# import os
# import json
# from collections import defaultdict
#
#
# def detect_flakes(runs_dir: Path):
#     # Read run files from the internal library folder
#     run_files = sorted(runs_dir.glob("*.json"))
#     print(run_files)
#
#     test_status_map = defaultdict(list)
#
#     for run_file in run_files:
#         with open(run_file) as f:
#             run_data = json.load(f)
#             for test in run_data:
#                 test_id = test["nodeid"]
#                 test_status_map[test_id].append({
#                     "status": test["status"],
#                     "timestamp": test["timestamp"]
#                 })
#
#     flaky_tests = {}
#
#     for test_id, history in test_status_map.items():
#         statuses = [entry["status"] for entry in history]
#         status_set = set(statuses)
#
#         if len(status_set) > 1 and 'passed' in status_set and 'failed' in status_set:
#             last_failed_entry = max(
#                 (entry for entry in history if entry["status"] == "failed"),
#                 key=lambda x: x["timestamp"]
#             )
#             flaky_tests[test_id] = {
#                 "statuses": statuses,
#                 "last_failed": last_failed_entry["timestamp"]
#             }
#
#     # Write output JSON and HTML report to the client's project folder `flake_data/`
#     client_output_dir = Path("report_output")  # relative to cwd (client's project)
#     client_output_dir.mkdir(parents=True, exist_ok=True)
#
#     flake_json_path = client_output_dir / "flake_report.json"
#     flake_html_path = client_output_dir / "flake_report.html"
#
#     with open(flake_json_path, "w") as f:
#         json.dump(flaky_tests, f, indent=2)
#     print(f"🌀 Flake summary JSON → {flake_json_path}")
#
#     generate_flaky_html(flake_summary=flaky_tests, output_html_path=flake_html_path)
#     print(f"🌐 Flake report HTML → {flake_html_path}")
#
#
import platform
import shutil
from datetime import datetime
from pathlib import Path

import pytest

from pytest_json_reporter.generate_flakytest_report import generate_flaky_html
from pytest_json_reporter.generate_html_report import JSONReporter
from pytest_json_reporter.json_merge import merge_json_reports
from pytest_json_reporter.send_email_report import send_email_from_env, load_email_env

python_executable = shutil.which("python3") or shutil.which("python")
test_screenshot_paths = {}


import logging

logger = logging.getLogger()  # root logger
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    if "caplog" not in item.fixturenames:
        item.fixturenames.append("caplog")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" or (report.when == "setup" and report.skipped):
        config = item.config
        capture_option = config.getoption("--capture-screenshots")
        tool = config.getoption("--automation-tool")

        caplog_text = None
        if "caplog" in item.funcargs:
            caplog = item.funcargs["caplog"]
            caplog_text = "\n".join(caplog.messages) if caplog.messages else None

        screenshot_path = None
        should_capture_screenshot = (
            capture_option == "all" or
            (capture_option == "failed" and report.outcome == "failed")
        )

        if should_capture_screenshot:
            driver = (
                    item.funcargs.get("page" if tool == "playwright" else "driver", None)
                    or getattr(item, "page_for_screenshot", None)
            )
            if driver:
                screenshot_path = take_screenshot_on_failure(item, driver)
        reporter = config._json_reporter
        worker_id = os.getenv("PYTEST_XDIST_WORKER") or "main"
        reporter.log_result(
            test_name=item.name,
            nodeid=item.nodeid,
            status=report.outcome,
            duration=report.duration,
            error=str(report.longrepr) if report.failed else None,
            markers=[m.name for m in item.iter_markers()],
            filepath=item.location[0],
            lineno=item.location[1],
            stdout=getattr(report, "capstdout", ""),
            stderr=getattr(report, "capstderr", ""),
            screenshot=screenshot_path,
            logs=caplog_text,
            worker=worker_id
        )

import subprocess


def pytest_sessionfinish(session, exitstatus):
    reporter = session.config._json_reporter

    json_path = session.config.getoption("--json-report") or "playwright_report.json"
    html_output = session.config.getoption("--html-output") or "report_output"
    screenshots = session.config.getoption("--screenshots") or "screenshots"

    is_worker = os.getenv("PYTEST_XDIST_WORKER") is not None
    is_xdist =  session.config.getoption("-n")

    if is_worker:
        reporter.write_report()
        print(f"Worker {os.getenv('PYTEST_XDIST_WORKER')} finished – skipping merge.")
        return

    if is_xdist:
        print("Merging reports in main process...")
        merge_json_reports(directory=".pytest_worker_jsons", output_path=json_path)
        print(f"✅ Merged report written to {json_path}")
    else:
        reporter.write_report()
        print(f"✅ Standalone JSON report written to {json_path}")

    # Now generate the HTML report
    script_path = os.path.join(os.path.dirname(__file__), "generate_html_report.py")

    if not os.path.exists(script_path):
        print(f"Warning: Report generation script not found at {script_path}. Skipping HTML report generation.")
        return

    try:
        subprocess.run([
            sys.executable,
            script_path,
            "--report", json_path,
            "--screenshots", screenshots,
            "--output", html_output
        ], check=True)
        print(f"✅ HTML report generated at {html_output}/report.html")
    except Exception as e:
        print(f"❌ Exception during HTML report generation: {e}")

    if session.config.getoption("--detect-flake"):
        report_path = session.config.getoption("--json-report")
        with open(report_path, "r") as f:
            full_report = json.load(f)

        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")

        lib_root = Path(__file__).resolve().parent
        internal_data_dir = lib_root / "flake_run_data" / "runs"
        internal_data_dir.mkdir(parents=True, exist_ok=True)

        output_path = internal_data_dir / f"{timestamp}.json"
        with open(output_path, "w") as f:
            json.dump(full_report, f, indent=2)

        print(f"📦 Internal flake run data saved to {output_path}")

        # Pass the path to internal_data_dir to detect_flakes so it knows where to read runs from
        detect_flakes(runs_dir=internal_data_dir)
    if session.config.getoption("--send-email"):
        print("📬 --send-email enabled. Sending report...")
        try:
            config = load_email_env()
            send_email_from_env(config)
        except Exception as e:
            print(f"❌ Failed to send email: {e}")


def pytest_sessionstart(session):
    configure_logging()
    print("Plugin loaded: pytest_sessionstart called")

def pytest_runtest_logreport(report):
    print(f"pytest_runtest_logreport: {report.nodeid} - {report.outcome}")

def pytest_load_initial_conftests(args):
    if not any(arg.startswith("--capture") for arg in args):
        args.append("--capture=tee-sys")

def pytest_addoption(parser):
    parser.addoption(
        "--json-report",
        action="store",
        default="playwright_report.json",
        help="Directory to save individual JSON test reports"
    )
    parser.addoption(
        "--automation-tool",
        action="store",
        default="playwright",
        choices=["selenium", "playwright"],
        help="Specify automation tool: selenium (default) or playwright"
    )
    parser.addoption(
        "--capture-screenshots",
        action="store",
        default="failed",
        choices=["failed", "all", "none"],
        help="Capture screenshots: failed (default), all, or none"
    )
    parser.addoption("--html-output", default="report_output")
    parser.addoption("--screenshots", default="screenshots")
    parser.addoption(
        "--send-email",
        action="store_true",
        default=False,
        help="Send HTML test report via email after test run"
    )
    parser.addoption(
        "--detect-flake",
        action="store",
        default=False,
        help="Helps capture flaky tests in the last n number of builds"
    )


def take_screenshot_on_failure(item, page):
    print("✅ take_screenshot_on_failure was called")
    screenshot_dir = os.path.join(os.getcwd(), "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)
    filename = f"{item.name}.png".replace("/", "_").replace("\\", "_")
    path = os.path.join(screenshot_dir, filename)
    # Assuming sync call here, adjust if async
    page.screenshot(path=path)
    return path

def take_screenshot_selenium(item, driver):
    screenshot_dir = os.path.join(os.getcwd(), "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)
    filename = f"{item.name}.png".replace("/", "_").replace("\\", "_")
    path = os.path.join(screenshot_dir, filename)
    driver.save_screenshot(path)
    return path

import logging
import sys

def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Avoid adding multiple handlers if rerun in same session
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

def pytest_configure(config):
    global _saved_config
    _saved_config = config  # store it for use in collectreport

    INTERNAL_JSON_DIR = Path(".pytest_worker_jsons")
    report_path = config.getoption("--json-report") or "playwright_report.json"
    worker_id = os.getenv("PYTEST_XDIST_WORKER")

    if worker_id:
        INTERNAL_JSON_DIR.mkdir(parents=True, exist_ok=True)
        name, ext = os.path.splitext(report_path)
        report_path = INTERNAL_JSON_DIR / f"{name}_{worker_id}{ext}"

    config._json_reporter = JSONReporter(report_path=report_path)


def pytest_collectreport(report):
    if report.failed:
        global _saved_config
        reporter = getattr(_saved_config, "_json_reporter", None)
        if reporter:
            reporter.log_result(
                test_name="COLLECTION ERROR",
                nodeid=str(report.nodeid),
                status="error",
                duration=getattr(report, "duration", 0.0),
                error=str(report.longrepr),
                markers=[],
                filepath=str(report.fspath),
                lineno=0,
                stdout="",
                stderr="",
                screenshot=None,
                logs=None,
                worker=os.getenv("PYTEST_XDIST_WORKER") or "main"
            )


import os
import json
from collections import defaultdict


def detect_flakes(runs_dir: Path):
    # Read run files from the internal library folder
    run_files = sorted(runs_dir.glob("*.json"))

    test_status_map = defaultdict(list)

    for run_file in run_files:
        with open(run_file) as f:
            run_data = json.load(f)
            for test in run_data:
                test_id = test["nodeid"]
                test_status_map[test_id].append({
                    "status": test["status"],
                    "timestamp": test["timestamp"]
                })

    flaky_tests = {}

    for test_id, history in test_status_map.items():
        statuses = [entry["status"] for entry in history]
        status_set = set(statuses)

        if len(status_set) > 1 and 'passed' in status_set and 'failed' in status_set:
            last_failed_entry = max(
                (entry for entry in history if entry["status"] == "failed"),
                key=lambda x: x["timestamp"]
            )
            flaky_tests[test_id] = {
                "statuses": statuses,
                "last_failed": last_failed_entry["timestamp"]
            }

    # Write output JSON and HTML report to the client's project folder `flake_data/`
    client_output_dir = Path("report_output")  # relative to cwd (client's project)
    client_output_dir.mkdir(parents=True, exist_ok=True)

    flake_json_path = client_output_dir / "flake_report.json"
    flake_html_path = client_output_dir / "flake_report.html"

    with open(flake_json_path, "w") as f:
        json.dump(flaky_tests, f, indent=2)
    print(f"🌀 Flake summary JSON → {flake_json_path}")

    generate_flaky_html(flake_summary=flaky_tests, output_html_path=flake_html_path)
    print(f"🌐 Flake report HTML → {flake_html_path}")

