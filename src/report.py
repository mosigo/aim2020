import os
import json


def write_value_td(f, min_val, max_val, val, color_on=True):
    blue = round((val - min_val) * 255 / (max_val - min_val), 0)
    text_color = 'black' if blue > 125 else 'white'
    value = str(val)
    if isinstance(val, int):
        value = "{:,d}".format(val).replace(',', ' ')
    color_styles = 'background-color: rgb(%s,%s,255); color:%s;' % (blue, blue, text_color) if color_on else ''
    f.write('<td style="%s">%s</td>' % (color_styles, value))


def make_value_for_each_task_block(f, data, color_on):
    min_val = min([min(a.values()) for a in data.values()])
    max_val = max([max(a.values()) for a in data.values()])

    max_variant = max([max([int(a) for a in variants.keys()]) for num, variants in data.items()])
    f.write('<table><tr><th>task</th>')
    for i in range(max_variant):
        f.write('<th>v' + str(i + 1) + '</th>')
    f.write('</tr>')
    for num, variants in data.items():
        f.write('<tr>')
        f.write('<th>%s</th>' % num)
        for i in range(max_variant):
            if variants.get(str(i + 1)) is None:
                f.write('<td style="background-color: lightgrey; text-align:center;">—</td>')
            else:
                val = variants[str(i + 1)]
                write_value_td(f, min_val, max_val, val, color_on)

        f.write('</tr>')
    f.write('</table>')


def make_value_for_each_task_number_block(f, data, color_on):
    f.write('<table><tr><th>task</th><th>value</th></tr>')
    min_val = min(data.values())
    max_val = max(data.values())
    for num, val in data.items():
        f.write('<tr>')
        f.write('<th>%s</th>' % num)
        write_value_td(f, min_val, max_val, val, color_on)
        f.write('</tr>')
    f.write('</table>')


def make_report(results_dir, out_path, report_title=''):
    f = open(out_path, 'wt', encoding='utf-8')
    f.write('<html><head><meta charset="utf-8">')
    f.write('<style>table, th, td {border: 1px solid lightgray; border-collapse: collapse; '
            'padding-left: 3px; padding-right: 3px;} </style>')
    f.write('<style>td {text-align:right; padding-left: 6px;} </style>')
    f.write('</head><body>')

    if report_title:
        f.write('<h1>%s</h1>' % report_title)

    for filename in os.listdir(results_dir):
        if filename.endswith(".json"):
            with open(results_dir + '/' + filename) as f_json:
                data = json.load(f_json)
                f.write('<h2>' + data.get('title', '') + '</h2>')

                color_on = data.get('render_type') == 'color-gradient-asc'
                if data.get('data_type') == 'value_for_each_task':
                    make_value_for_each_task_block(f, data['data'], color_on)
                elif data.get('data_type') == 'value_for_each_task_number':
                    make_value_for_each_task_number_block(f, data['data'], color_on)
    f.write('</body>')
    f.write('</html>')

    f.close()
