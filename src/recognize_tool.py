#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from acrcloud.recognizer import ACRCloudRecognizer
from acrcloud.recognizer import ACRCloudRecognizeType

config = {
        'host': 'cn-north-1.api.acrcloud.com',
        'access_key': 'b669d499dcf1d8ab7b801950a3ab5f94',
        'access_secret': 'uS0ejrzxR84RnlOrwmFnaSn6IDwWsVRl1WV6d8QS',
        # 可选值 ：ACR_OPT_REC_AUDIO,ACR_OPT_REC_HUMMING,ACR_OPT_REC_BOTH
        'recognize_type': ACRCloudRecognizeType.ACR_OPT_REC_BOTH,
        'debug': False,
        'timeout': 10  # 单位: 秒
    }


def recognize_music(full_path):
    re = ACRCloudRecognizer(config)
    result = json.loads(re.recognize_by_file(full_path, 0))
    if result['status']['code'] != 0:
        buf = open(full_path, 'rb').read()
        result = json.loads(re.recognize_by_filebuffer(buf, 0))
        if result['status']['code'] != 0:
            return 'UNKNOWN'
    data = result['metadata']['music'][0]
    return data['title'] + '-' + data['artists'][0]['name']
