
import pytest
import sys

def run_tests():
    print("RUNNING UNIT TESTS")

    args = ["-v", "tests/", "--html=final_report.html", "--self-contained-html"]


    exit_code = pytest.main(args)

    if exit_code == pytest.ExitCode.OK:
        print("All tests passed successfully ✅")
    elif exit_code == pytest.ExitCode.TESTS_FAILED:
        print("Some tests failed ❌")
    else:
        print("There was an error while running the tests")


    sys.exit(exit_code)


if __name__ == "__main__":
    run_tests()



