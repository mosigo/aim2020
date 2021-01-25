import json
import csv


def make_answers_count_block(src_dir, out_file_path):
    task_id_to_cnt = {}
    with open(src_dir + '/results.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            if row['verdict'] == 'none':
                continue
            task_id = int(row['task_id'])
            cnt = task_id_to_cnt.get(task_id, 0)
            task_id_to_cnt[task_id] = cnt + 1

    task_id_to_num = {}
    with open(src_dir + '/task_ids.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            task_id = int(row['id'])
            task_id_to_num[task_id] = row['task_no']

    data = {}
    for task_id, cnt in task_id_to_cnt.items():
        [num, variant] = task_id_to_num[task_id].split('-')
        variants = data.get(num, {})
        if variants == {}:
            data[num] = variants
        variants[variant] = cnt

    json_result = {
        'title': 'Non-empty answers count',
        'data_type': 'value_for_each_task',
        'render_type': 'color-gradient-asc',
        'data': data
    }
    with open(out_file_path, 'w', encoding='utf-8') as f:
        json.dump(json_result, f, ensure_ascii=False, indent=4)


def make_fraction_block(src_dir, out_file_path):
    task_id_to_cnt = {}
    task_id_to_cnt_ok = {}
    with open(src_dir + '/results.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            if row['verdict'] == 'none':
                continue
            task_id = int(row['task_id'])
            cnt = task_id_to_cnt.get(task_id, 0)
            task_id_to_cnt[task_id] = cnt + 1

            if row['verdict'] == 'ok':
                cnt_ok = task_id_to_cnt_ok.get(task_id, 0)
                task_id_to_cnt_ok[task_id] = cnt_ok + 1

    task_id_to_num = {}
    with open(src_dir + '/task_ids.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            task_id = int(row['id'])
            task_id_to_num[task_id] = row['task_no']

    data = {}
    for task_id, cnt in task_id_to_cnt.items():
        [num, variant] = task_id_to_num[task_id].split('-')
        variants = data.get(num, {})
        if variants == {}:
            data[num] = variants
        variants[variant] = round(task_id_to_cnt_ok.get(task_id, 0) / cnt, 2) if cnt > 0 else 0

    json_result = {
        'title': 'Fraction of correct answers',
        'data_type': 'value_for_each_task',
        'render_type': 'color-gradient-asc',
        'data': data
    }
    with open(out_file_path, 'w', encoding='utf-8') as f:
        json.dump(json_result, f, ensure_ascii=False, indent=4)


def make_fraction_for_task_num_block(src_dir, out_file_path):
    task_id_to_cnt = {}
    task_id_to_ok_cnt = {}
    with open(src_dir + '/results.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            if row['verdict'] == 'none':
                continue
            task_id = int(row['task_id'])

            cnt = task_id_to_cnt.get(task_id, 0)
            task_id_to_cnt[task_id] = cnt + 1

            if row['verdict'] == 'ok':
                cnt_ok = task_id_to_ok_cnt.get(task_id, 0)
                task_id_to_ok_cnt[task_id] = cnt_ok + 1

    task_id_to_num = {}
    with open(src_dir + '/task_ids.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            task_id = int(row['id'])
            task_id_to_num[task_id] = row['task_no']

    result_by_task_num = {}
    for task_id, cnt in task_id_to_cnt.items():
        cnt_ok = task_id_to_ok_cnt.get(task_id, 0)

        [num, _] = task_id_to_num[task_id].split('-')
        (cur_cnt, cur_cnt_ok) = result_by_task_num.get(num, (0, 0))
        result_by_task_num[num] = (cur_cnt + cnt, cur_cnt_ok + cnt_ok)

    data = {}
    for task_num, (cnt, cnt_ok) in result_by_task_num.items():
        fraction = cnt_ok / cnt if cnt != 0 else 0
        data[task_num] = round(fraction, 2)

    json_result = {
        'title': 'Fraction of correct answers by task number',
        'data_type': 'value_for_each_task_number',
        'render_type': 'color-gradient-asc',
        'data': data
    }
    with open(out_file_path, 'w', encoding='utf-8') as f:
        json.dump(json_result, f, ensure_ascii=False, indent=4)


def make_scores_for_task_num_block(src_dir, out_file_path):
    task_id_to_max_score = {}
    with open(src_dir + '/results.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            task_id = int(row['task_id'])
            max_score = float(row['max_score'])

            task_id_to_max_score[task_id] = max_score

    task_id_to_num = {}
    with open(src_dir + '/task_ids.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            task_id = int(row['id'])
            task_id_to_num[task_id] = row['task_no']

    result_by_task_num = {}
    for task_id, max_score in task_id_to_max_score.items():
        [num, _] = task_id_to_num[task_id].split('-')
        cur_max_score = result_by_task_num.get(num, 0)
        result_by_task_num[num] = max(cur_max_score, max_score)

    data = {'max_scores': {}, 'scaled_max_scores': {}}
    for task_num, max_score in result_by_task_num.items():
        data['max_scores'][task_num] = max_score
        data['scaled_max_scores'][task_num] = max_score * 2

    data['max_scores']['total'] = sum(data['max_scores'].values())
    data['scaled_max_scores']['total'] = sum(data['scaled_max_scores'].values())

    json_result = {
        'title': 'Max scores by task number',
        'data_type': 'scores_for_each_task_number',
        'render_type': 'none',
        'data': data
    }
    with open(out_file_path, 'w', encoding='utf-8') as f:
        json.dump(json_result, f, ensure_ascii=False, indent=4)