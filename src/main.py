import os

from eval.all_functions import get_all_evaluation_functions
from report import make_report


def make_report_for_olympiad(dir_name):
    src_dir = '../data/' + dir_name
    out_dir = '../out/' + dir_name

    results_dir = out_dir + '/results'
    os.makedirs(results_dir, exist_ok=True)

    funcs = get_all_evaluation_functions()
    for i in range(len(funcs)):
        out_file_path = results_dir + '/out_%s.json' % i
        funcs[i](src_dir, out_file_path)

    file_report_name = out_dir + '/' + dir_name + '.html'
    make_report(results_dir, file_report_name, report_title='Olympiad from "%s"' % dir_name)


if __name__ == '__main__':
    make_report_for_olympiad('math')
    # make_report_for_olympiad('bio')

    # make_report_for_olympiad('1211')
    # make_report_for_olympiad('1259')
