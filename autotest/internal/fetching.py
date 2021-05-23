import re
import requests

from .case import Case


class UnsupportedSourceError(RuntimeError):
    def __init__(self, *args, **kwargs):
        super(UnsupportedSourceError, self).__init__(*args, **kwargs)


class Fetch:
    def __init__(self, source: str):
        pass

    def get(self) -> list[Case]:
        raise NotImplementedError


class PintiaFetch(Fetch):
    pattern = re.compile(r'^(?:https?://)?pintia\.cn/problem-sets/(?P<problem_set_id>[^/\?#]*)/problems/(?P<problem_id>[^/\?#]*)')

    def __init__(self, source: str):
        super().__init__(source)
        match = re.search(PintiaFetch.pattern, source)
        if match is None:
            raise UnsupportedSourceError
        groups = match.groupdict()
        self.problem_set_id = groups['problem_set_id']
        self.problem_id = groups['problem_id']

    def get(self) -> list[Case]:
        resp = requests.get('https://pintia.cn/api/problem-sets/{problem_set_id}/problems/{problem_id}'.format(
            problem_set_id=self.problem_set_id,
            problem_id=self.problem_id
        ), headers={
            'Accept': 'application/json;charset=utf-8'
        })
        resp.raise_for_status()
        data = resp.json()
        timeout = data['problemSetProblem']['problemConfig']['programmingProblemConfig']['timeLimit'] / 1000
        raw_cases = data['problemSetProblem']['problemConfig']['programmingProblemConfig']['exampleTestDatas']
        cases = []
        for raw_case in raw_cases:
            cases.append(Case(raw_case['input'], raw_case['output'], timeout))
        return cases


class LuoguFetch(Fetch):
    pattern = re.compile(r'^(?:https?://)(?:www\.)luogu\.com\.cn/problem/(?P<problem_id>[^/\?#]+)')

    def __init__(self, source: str):
        super().__init__(source)
        match = re.search(LuoguFetch.pattern, source)
        if match is None:
            raise UnsupportedSourceError
        self.problem_id = match.groupdict()['problem_id']

    def get(self) -> list[Case]:
        resp = requests.get('https://www.luogu.com.cn/problem/{problem_id}'.format(
            problem_id=self.problem_id
        ), headers={
            'X-Luogu-Type': 'content-only',
            'User-Agent': 'Autotest/0'
        })
        resp.raise_for_status()
        data = resp.json()
        timeout = data['currentData']['problem']['limits']['time'][0] / 1000
        cases = []
        for sample in data['currentData']['problem']['samples']:
            cases.append(Case(sample[0], sample[1], timeout))
        return cases


handlers = [
    PintiaFetch,
    LuoguFetch,
]