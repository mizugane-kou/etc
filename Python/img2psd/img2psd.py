

# pip install opencv-python pytoshop numpy Pillow pykakasi six

import os
import cv2
import pytoshop
from pytoshop import layers
import numpy as np
from PIL import Image
from datetime import datetime
import pykakasi

def get_max_image_size(folder_path):
    heights = []
    widths = []

    # フォルダ内の全画像を読み込み、サイズをリストに追加
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img_path = os.path.join(folder_path, filename)
            with Image.open(img_path) as img:
                width, height = img.size
                widths.append(width)
                heights.append(height)

    # 最大値を取得
    W = max(widths) if widths else None
    H = max(heights) if heights else None

    return W, H

def convert_to_romaji(text):
    kakasi = pykakasi.kakasi()
    kakasi.setMode("H", "a")  # ひらがなをローマ字に変換
    kakasi.setMode("K", "a")  # カタカナをローマ字に変換
    kakasi.setMode("J", "a")  # 漢字をローマ字に変換
    kakasi.setMode("r", "Hepburn")  # ヘボン式ローマ字を使用
    converter = kakasi.getConverter()
    return converter.do(text)

def main(folder_path):
    # 親フォルダのパスを取得
    parent_folder = os.path.dirname(folder_path)

    # PSDファイル用の白紙の画像サイズを決定
    W, H = get_max_image_size(folder_path)
    if not W or not H:
        print("画像ファイルが見つかりません。")
        return

    # PSDオブジェクトを作成
    psd = pytoshop.core.PsdFile(num_channels=4, height=H, width=W)  # 4チャンネルに変更（アルファを含む）

    # フォルダ内の画像ファイルを取得
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

    # 画像を1枚ずつ読み込み、新しいレイヤーとして追加
    for idx, image_file in enumerate(image_files):
        img_path = os.path.join(folder_path, image_file)

        # 日本語ファイル名を読み込むために np.fromfile を利用
        try:
            img_array = np.fromfile(img_path, np.uint8)
            test_img = cv2.imdecode(img_array, cv2.IMREAD_UNCHANGED)  # 透明度（アルファチャンネル）を含む
        except Exception as e:
            print(f"画像の読み込み中にエラーが発生しました: {image_file}\n詳細: {e}")
            continue

        if test_img is None:
            print(f"画像の読み込みに失敗しました: {image_file}")
            continue

        # 画像にアルファチャンネルがあれば、それを適切に処理
        if test_img.shape[2] == 4:  # 画像にアルファチャンネルがある場合
            rgba = test_img
            rgb = rgba[:, :, :3]
            alpha = rgba[:, :, 3]
        else:  # アルファチャンネルがない場合
            rgb = test_img
            alpha = np.full(test_img.shape[:2], 255, dtype=np.uint8)  # アルファチャンネルを255で埋める

        # 透明度用レイヤーを作成
        layer_1 = layers.ChannelImageData(image=alpha, compression=1)  # 透明度
        layer0 = layers.ChannelImageData(image=rgb[:, :, 2], compression=1)  # R
        layer1 = layers.ChannelImageData(image=rgb[:, :, 1], compression=1)  # G
        layer2 = layers.ChannelImageData(image=rgb[:, :, 0], compression=1)  # B

        # ファイル名をローマ字に変換
        layer_name = os.path.splitext(image_file)[0]
        layer_name_romaji = convert_to_romaji(layer_name)

        # レイヤーを作成
        new_layer = layers.LayerRecord(
            channels={-1: layer_1, 0: layer0, 1: layer1, 2: layer2},
            top=0, bottom=test_img.shape[0], left=0, right=test_img.shape[1],  # 画像の位置
            name=layer_name_romaji,  # レイヤー名をローマ字に変換した名前に設定
            opacity=255,  # 不透明度
        )

        # レイヤーをPSDに追加
        psd.layer_and_mask_info.layer_info.layer_records.append(new_layer)

    # 現在の日時を取得し、指定のフォーマットで文字列に変換
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # 出力ファイル名を生成（親フォルダに出力）
    output_filename = os.path.join(parent_folder, f"{folder_path}_{timestamp}.psd")

    # 書き出し
    with open(output_filename, 'wb') as fd2:
        psd.write(fd2)

if __name__ == '__main__':
    import sys
    folder_path = sys.argv[1]  # バッチから渡されたフォルダパスを取得
    main(folder_path)
