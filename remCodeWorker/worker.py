
from redis import from_url
import subprocess
import sys

import logging


def run(cmd, stdin=""):
    proc = subprocess.Popen(cmd,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True
                            )

    stdout, stderr = proc.communicate(input=stdin.encode())

    return proc.returncode, stdout, stderr


def execute_code(code_text, stdin, language, token):
    r = from_url("redis://redis:6379")
    if language == "python3":
        exit_code, out, err = run_py(code_text, stdin)
    else:
        exit_code, out, err = run_gcc(code_text, stdin)

    logging.info(out)
    logging.info(err)
    logging.info(exit_code)
    print("out: '{}'".format(out))
    print("err: '{}'".format(err))
    print("exit: {}".format(exit_code))
    if exit_code == 0:
        if out:
            r.set(token, out)
        else:
            r.set(token, "no output was produced by code")
    else:
        r.set(token, err)


def run_py(code_text, stdin):
    with open("tmp.py", "w") as file:
        file.write(code_text)

    exit_code, out, err = map(lambda x: x.decode() if type(x) == bytes else x,
                              run([f"{sys.executable} tmp.py"], stdin))
    run(["rm tmp.py"])

    return exit_code, out, err


def run_gcc(code_text, stdin):
    with open("tmp.c", "w") as file:
        file.write(code_text)

    exit_code, out, err = map(lambda x: x.decode() if type(x) == bytes else x,
                              run(["gcc tmp.c && ./a.out"], stdin))
    run(["rm tmp.c"])
    run(["rm a.out"])

    return exit_code, out, err


def main():
    while True:
        r = from_url("redis://redis:6379")
        token, lang_input_code = r.brpop("tasks")[1].decode().split("\n", 1)
        lang, input_code = lang_input_code.split("\n", 1)
        stdin, code = input_code.split(token, 1)
        execute_code(code, stdin, lang, token)


if __name__ == '__main__':
    main()

