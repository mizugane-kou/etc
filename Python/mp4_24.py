import ffmpeg
import sys
import os

def process_video(input_file):
    try:
        # 出力ファイルのパスを決定
        output_file = input_file.rsplit('.', 1)
        output_file = f"{output_file[0]}_24fps.{output_file[1]}"

        # FFmpegを使用して24fpsに変換（解像度を保持）
        ffmpeg.input(input_file).output(output_file, r=24, vf="fps=24,scale=-1:-1").run()

        print(f"変換完了: {output_file}")
    
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    # 引数として渡されたファイルパスを処理
    for input_file in sys.argv[1:]:
        process_video(input_file)
