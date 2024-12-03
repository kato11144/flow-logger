"""
analysis.py
"""

import os
import json
import argparse
from pathlib import Path
import pandas as pd

class Analysis:
    """
    人流のログを解析するクラス
    """

    def __init__(self, out_dir):
        """
        クラスの初期化処理
        """
        self.out_dir = out_dir
        self.folder_names = self.get_folder_names()

    def main(self):
        """
        これを実行
        """
        self.analysis_detect_log()

    def get_folder_names(self):
        """
        ディレクトリ内のフォルダ名を取得する
        """
        folder_names = [item.name for item in Path('./logs/').iterdir() if item.is_dir()]
        return folder_names

    def get_json_files(self, log_dir):
        """
        jsonファイルを取得する
        """
        json_files = [file for file in os.listdir(log_dir) if file.endswith('.json')][0]
        return json_files

    def load_json_file(self, json_file_path):
        """
        jsonファイルをload
        """
        dict_data = json.load(open(json_file_path, 'r' , encoding='utf-8-sig'))
        return dict_data

    def analysis_detect_log(self):
        """
        logを解析する
        """
        df_analysis = pd.DataFrame(columns=[])
        for folder_name in self.folder_names:
            json_files = self.get_json_files(f'./logs/{folder_name}/')
            dict_data = self.load_json_file(f'./logs/{folder_name}/{json_files}')
            for data in dict_data:
                unit_id = folder_name
                timestamp = data['timestamp']
                count = data['count']

                if unit_id not in df_analysis.columns:
                    df_analysis[unit_id] = None
                df_analysis.loc[timestamp, unit_id] = count

        df_analysis.to_excel(f'{self.out_dir}/analysis.xlsx', index=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out_dir', type=str, default='./out/')
    args = parser.parse_args()

    func = Analysis(args.out_dir)
    func.main()
