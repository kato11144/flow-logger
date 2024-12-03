#!/bin/bash

for folder in ./assets/*; do
    if [[ -d "$folder" ]]; then
        unit_id=$(basename "$folder")

        mkdir -p ./exports/${unit_id}/
        mkdir -p ./exports/${unit_id}/labels/
        mkdir -p ./logs/${unit_id}/

        for jpg_file in "$folder"/*.jpg; do
            if [[ -f "$jpg_file" ]]; then
                txt_filename=$(basename "$jpg_file" .jpg).txt
                touch "./exports/${unit_id}/labels/$txt_filename"
            fi
        done

        yolo task=detect mode=predict model=yolov8x.pt source="./assets/${unit_id}/" project="./exports/" name="${unit_id}" save_txt=True exist_ok=True
        python3 ./src/logger.py --labels_dir ./exports/${unit_id}/labels/ --logs_dir ./logs/${unit_id}/ --class_id 0
    fi
    echo
done

mkdir -p ./out/
python3 ./src/analysis.py --out_dir ./out/
