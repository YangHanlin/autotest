# Autotest

A simple utility to run specified program and test its output against answers.

## Installation

```bash
pip install git+https://github.com/YangHanlin/autotest.git@main
```

## Usage

<!-- usage-replacement-start -->

```bash
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
usage: autotest run [-h] [-c CASE] [-r] command

positional arguments:
  command               command to run

optional arguments:
  -h, --help            show this help message and exit
  -c CASE, --case CASE  file to read cases from; defaults to <command>.case.yml
  -r, --allow-runtime-error
                        allow runtime errors (in which command exits with non-zero code)

$ autotest generate --help
usage: autotest generate [-h] [-s SOURCE] case

positional arguments:
  case                  case file to generate; suffix '.case.yml' will be appended if no extension is provided

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        source to fetch cases from, e.g. luogu/p1001
```

<!-- usage-replacement-end -->
