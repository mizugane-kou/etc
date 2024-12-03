from PIL import Image, ImageOps 
import sys 
import os 
 
# 白枠の幅の割合を指定 
BORDER_RATIO = 0.055
 
def add_square_white_border(input_image_path): 
    # 画像を開く 
    image = Image.open(input_image_path) 
    
    # 枠幅を計算 (画像の長辺に基づく割合) 
    border_width = int(max(image.size) * BORDER_RATIO) 
    
    # 正方形になるように長辺を基準に余白を追加
    max_side = max(image.size)
    new_image = Image.new("RGB", (max_side, max_side), "white")
    new_image.paste(image, ((max_side - image.width) // 2, (max_side - image.height) // 2))
    
    # 出力ファイル名を生成 
    base, ext = os.path.splitext(input_image_path) 
    output_image_path = f"{base}_bordered_square{ext}" 
    
    # 白枠を追加 
    bordered_image = ImageOps.expand(new_image, border=border_width, fill="white") 
    
    # 画像を保存 
    bordered_image.save(output_image_path) 
    print(f"Saved bordered image as {output_image_path}") 
 
if __name__ == "__main__": 
    # コマンドライン引数でファイルパスのみを取得 
    if len(sys.argv) < 2: 
        print("Usage: python add_square_white_border.py <image_path>") 
        sys.exit(1) 
     
    image_path = sys.argv[1] 
    add_square_white_border(image_path)
