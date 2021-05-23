# Autotest

A simple utility to run specified program and test its output against answers.

## Installation

```bash
pip install git+https://github.com/YangHanlin/autotest.git@main
```

## Usage

<!-- usage-replacement-start -->

```
$ autotest --help
usage: autotest [-h] action ...

positional arguments:
  action             action to take
    run (r)          run command and judge the results against cases
    generate (gen, g)
                     generate empty test case file or fetch from OJ

optional arguments:
  -h, --help         show this help message and exit

$ autotest run --help
usage: autotest run [-h] [-c CASE_PATH] [-z] command

positional arguments:
  command               command to run

optional arguments:
  -h, --help            show this help message and exit
  -c CASE_PATH, --case-path CASE_PATH
                        file to read cases from; defaults to
                        <command>.case.yml
  -z, --allow-nonzero   allow programs to exit with non-zero code; otherwise
                        it will be considered as a runtime error (RE)

$ autotest generate --help
usage: autotest generate [-h] [-s SOURCE] case_path

positional arguments:
  case_path             case file to generate; suffix '.case.yml' will be
                        appended if no extension is provided

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        source to fetch cases from, e.g.
                        https://www.luogu.com.cn/problem/UVA100
```

<!-- usage-replacement-end -->

## Case file format

Below is a case file for A+B problem to illustrate its format.

```yaml
cases:  # array
  - input: 1 2  # test input 
    output: 3  # expected output
  - input: 5 6
    output: 11
    timeout: 0.1  # time limit (in seconds, optional)
```
