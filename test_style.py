from re import match
from subprocess import Popen, PIPE


def test_flake8():
    proc = Popen("flake8 owo --exclude=__init__.py".split(),
                 stdout=PIPE)

    out = proc.stdout.read().decode()

    lines = [l for l in out.split("\n")if l]

    print(out)

    assert not bool(lines)


def test_pylint():
    proc = Popen(("pylint --disable=missing-docstring,too-many-branches,fixme,"
                  "invalid-name,redefined-builtin,too-many-statements,"
                  "no-name-in-module,protected-access,too-many-arguments,"
                  "attribute-defined-outside-init,arguments-differ,no-member,"
                  "too-many-instance-attributes,import-error,too-many-locals,"
                  "parse-error,too-few-public-methods,exec-used,"
                  "cell-var-from-loop,wildcard-import,duplicate-code,"
                  "function-redefined"
                  " owo").split(),
                 stdout=PIPE)

    proc.wait()

    out = proc.stdout.read().decode()

    last_line = [l for l in out.split("\n")if l][-1]

    print(out)

    m = match("Your code has been rated at 10\.00\/10", last_line)

    assert m is not None


if __name__ == "__main__":
    test_flake8()
    print("Flake8 success!")

    test_pylint()
    print("Pylint success!")
