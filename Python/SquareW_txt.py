from PIL import Image, ImageOps, ImageDraw, ImageFont
import sys
import os
import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration

BORDER_RATIO = 0.055
FONT_RATIO = 0.021
TEXT_POSITION_RATIO = 0.975

print("モデルをロード開始")
model_path = r"C:\Users\mizug\.cache\huggingface\hub\models--Salesforce--blip2-opt-2.7b\snapshots\51572668da0eb669e01a189dc22abe6088589a24"
#def main():
processor = Blip2Processor.from_pretrained(model_path)
model = Blip2ForConditionalGeneration.from_pretrained(
    model_path,
    torch_dtype=torch.float16, 
    device_map="auto"
)

def add_square_white_border(input_image_path):
    try:
        # 画像を開く
        image = Image.open(input_image_path)

        # BLIP2モデルを使ってテキストを生成
        inputs = processor(images=image, return_tensors="pt").to("cuda", torch.float16)
        generated_ids = model.generate(**inputs)
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()

        # 枠幅を計算
        border_width = int(max(image.size) * BORDER_RATIO)

        # 正方形に余白を追加
        max_side = max(image.size)
        new_image = Image.new("RGB", (max_side, max_side), "white")
        new_image.paste(image, ((max_side - image.width) // 2, (max_side - image.height) // 2))
        image = ImageOps.expand(new_image, border=border_width, fill="white")

        # フォント設定
        font_size = int(image.size[1] * FONT_RATIO)
        font_path = "ZenKakuGothicNew-Bold.ttf"
        if not os.path.exists(font_path):
            raise FileNotFoundError("フォントファイルが見つかりません！")
        font = ImageFont.truetype(font_path, font_size)

        # テキスト位置計算
        draw = ImageDraw.Draw(image)
        text_bbox = draw.textbbox((0, 0), generated_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (image.size[0] - text_width) // 2
        text_y = int(image.size[1] * TEXT_POSITION_RATIO) - text_height
        text_position = (text_x, text_y)

        # テキスト描画
        draw.text(text_position, generated_text, fill="black", font=font)

        # 出力ファイル保存
        base, ext = os.path.splitext(input_image_path)
        generated_text2 = generated_text.replace(" ", "_")
        output_image_path = f"{base}_{generated_text2}{ext}"
        print(f"Saving image to {output_image_path}")
        image.save(output_image_path)
        print("Image saved successfully!")

        # 学習データ書き込み
        with open('caption.txt', 'a') as f:
            f.write(generated_text + "\n")

    except Exception as e:
        print(f"Error processing {input_image_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python add_square_white_border.py <image_path1> <image_path2> ...")
        sys.exit(1)

    image_paths = sys.argv[1:]
    for image_path in image_paths:
        add_square_white_border(image_path)
