"""
logger.py
"""

import os
import json
import argparse

class Logger:
    """
    人流のログを取得するクラス
    """

    def __init__(self, labels_dir, logs_dir, class_id):
        """
        クラスの初期化処理
        """
        self.labels_dir = labels_dir
        self.logs_dir = logs_dir
        self.class_id = int(class_id)
        self.txt_files = self.get_txt_files()

    def main(self):
        """
        これを実行
        """
        detect_log = self.create_detect_log()
        self.dump_json_file(os.path.join(self.logs_dir, 'detect_log.json'), detect_log)

    def get_txt_files(self):
        """
        txtファイルを取得する
        """
        txt_files = [file for file in os.listdir(self.labels_dir) if file.endswith(".txt")]
        return txt_files

    def get_bbox_log(self, lines):
        """
        bboxを取得する
        """
        bbox_log = []
        for line in lines:
            line = line.strip()
            bbox = {}
            if line.startswith(str(self.class_id)):
                objects = line.split()[1:]
                objects = [float(obj) for obj in objects]
                bbox['x'] = objects[0]
                bbox['y'] = objects[1]
                bbox['w'] = objects[2]
                bbox['h'] = objects[3]
                bbox_log.append(bbox)

        return bbox_log

    def create_detect_log(self):
        """
        detect_logを作成する
        """
        detect_log = []
        for txt_file in self.txt_files:
            file_path = os.path.join(self.labels_dir, txt_file)
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                lines = file.readlines()

            timestamp = txt_file.rstrip('.txt')
            bbox_log = self.get_bbox_log(lines)
            count = len(bbox_log)
            detect_log.append(
                {'timestamp': timestamp, "class_id": self.class_id, 'count': count, 'bbox': bbox_log}
            )

        return detect_log

    def dump_json_file(self,json_file_path,dict_data):
        """
        jsonファイルをdump
        """
        with open(json_file_path, 'w', encoding='utf-8-sig') as json_file:
            json.dump(dict_data, json_file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--labels_dir', default='./exports/labels', help='labels directory')
    parser.add_argument('--logs_dir', default='./logs', help='logs directory')
    parser.add_argument('--class_id', default=0, help='class id')
    args = parser.parse_args()

    func = Logger(args.labels_dir, args.logs_dir, args.class_id)
    func.main()
