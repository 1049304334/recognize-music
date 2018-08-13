import os
from src.recognize_tool import recognize_music


# 获取需要识别的文件的总数
def count_file_nums(path):
    total_count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.split('.')[-1].upper() == 'MP4' and file[0] != '.':
                total_count += 1
    return total_count


# 删除隐藏文件
def delete_hidden_file(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file[0] == '.':
                os.remove(root + '\\' + file)


# 标记推荐视频
def mark_recommend(dir_path):
    for root, dirs, files in os.walk(dir_path):
        if len(files) > 0 and root.split('\\')[-1].find('-') != -1:
            for file in files:
                if file.split('.')[-1] == 'MP4':
                    file.replace('recommend-', '')
                    os.rename(root + '\\' + file, root + '\\' + 'recommend-' + file)
                    break


# 去除歌名中特殊字符
def delete_dangerous_char(song_name):
    song_name = song_name.replace('"', '\'').replace('/', '').replace('\\', '')
    song_name = song_name.replace('?', '').replace('*', '').replace('<', '')
    song_name = song_name.replace('>', '').replace(':', '').replace(' ', '')
    return song_name


# 开始识别并重命名文件
def start_recognize(dir_path):

    need_recognize_count = count_file_nums(dir_path)  # 需要识别文件数
    curr_file_index = 0  # 当前操作文件序号
    recognized_file_count = 0  # 本次一共识别的文件数
    unknown_name_count = 0  # 本次识别无结果文件数量
    unknown_name_start_no = 207  # 用于命名系统音乐时的序号

    for root, dirs, files in os.walk(dir_path):
        for video in files:
            if video[0] == '.':  # 删除隐藏文件
                os.remove(root + '\\' + video)
                continue
            if video.split('.')[-1].upper() == 'MP4':
                video_path = root + '\\' + video
                music_name = delete_dangerous_char(recognize_music(video_path))
                recognized_file_count += 1
                curr_file_index += 1
                if music_name == 'UNKNOWN':
                    music_name = '系统音乐'+str(unknown_name_start_no)+'-未知歌手'
                    unknown_name_start_no += 1
                    unknown_name_count += 1

                print('['+str(curr_file_index)+' / '+str(need_recognize_count)+']  '+music_name, '    --->>>    ', root.split('\\')[-1] + '\\' + video)
                try:
                    os.rename(root + '\\' + video, root + '\\' + music_name + '.MP4')
                except FileExistsError:
                    continue
    print('共识别', recognized_file_count, '次，未知音乐', unknown_name_count, '首', ',序号已增加到', unknown_name_start_no)

    mark_recommend(dir_path)


if __name__ == '__main__':
    start_recognize('C:\\Users\\Amigo\\Desktop\\8.13')
