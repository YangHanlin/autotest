from typing import Union

from .case import Case


class JudgeResult:
    def __init__(self, status: str, show_diff: bool):
        self.status = status
        self.show_diff = show_diff


class TrivialJudger:
    def __init__(self, options: Union[dict, None] = None):
        if options is None:
            options = {}
        self.allow_nonzero = bool(options.get('allow_nonzero'))
        labels = ['Total', 'AC', 'WA', 'TLE']
        if not self.allow_nonzero:
            labels.append('RE')
        self.stats = {}
        for label in labels:
            self.stats[label] = 0

    def judge(self, case: Case, output: str, time: float, exit_code: int) -> JudgeResult:
        self.stats['Total'] += 1
        status_fragments = []
        show_diff = False

        if case.output != output and case.output + '\n' != output and case.output != output + '\n':
            self.stats['WA'] += 1
            show_diff = True

        if not self.allow_nonzero and exit_code != 0:
            self.stats['RE'] += 1
            status_fragments.append('RE ({})'.format(exit_code))

        if case.timeout and time > case.timeout:
            self.stats['TLE'] += 1
            status_fragments.append('TLE (+{:.4f}s)'.format(time - case.timeout))

        if not status_fragments:
            self.stats['AC'] += 1
            status_fragments.append('AC')

        return JudgeResult(', '.join(status_fragments), show_diff)

    def get_stats(self) -> dict:
        return self.stats
