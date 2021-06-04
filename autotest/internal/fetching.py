import re
import requests
import bs4

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


class NowcoderPatFetch(Fetch):
    pattern = re.compile(r'^(?:https?://)?(?:www\.)?nowcoder\.com/pat/(?P<category_id>[^/\?#]*)/problem/(?P<problem_id>[^/\?#]*)')

    def __init__(self, source: str):
        super().__init__(source)
        match = re.match(NowcoderPatFetch.pattern, source)
        if not match:
            raise UnsupportedSourceError
        args = match.groupdict()
        self.category_id = args['category_id']
        self.problem_id = args['problem_id']

    def get(self) -> list[Case]:
        resp = requests.get('https://www.nowcoder.com/pat/{category_id}/problem/{problem_id}'.format(
            category_id=self.category_id,
            problem_id=self.problem_id
        ))
        resp.raise_for_status()
        soup = bs4.BeautifulSoup(resp.text, 'html.parser')
        main_content = soup.find('div', class_='subject-des')
        input = str(main_content.find('h3', string='输入例子:').find_next_sibling('pre').string)
        output = str(main_content.find('h3', string='输出例子:').find_next_sibling('pre').string)
        timeout_in_ms = int(re.match(r'^时间限制\s*(?P<timeout>\d+)', soup.find('div', class_='pat-detail-info').find('span').string).groupdict()['timeout'])
        return [Case(input, output, timeout_in_ms / 1000)]


handlers = [
    PintiaFetch,
    LuoguFetch,
    NowcoderPatFetch,
]
