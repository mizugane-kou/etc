import sys

# 標準的なサイズ(mm)の辞書
BOOK_SIZES = {
    1: ("A4", 210, 297),
    2: ("A5", 148, 210),
    3: ("B5", 182, 257),
    4: ("B6", 128, 182),
    5: ("文庫", 105, 148),
    6: ("新書", 103, 182)
}

def calculate_guides(size, bleed, thickness=0, spread=False):
    width, height = size
    
    # 塗り足し幅を含めたサイズ
    total_width_with_bleed = width + (2 * bleed)
    total_height_with_bleed = height + (2 * bleed)
    
    if spread:  # 見開きの場合
        total_width = 2 * width + thickness + (2 * bleed)
        horizontal_guides = [
            0, bleed, 
            bleed + width, 
            bleed + width + thickness, 
            total_width - bleed, 
            total_width
        ]
        vertical_guides = [0, bleed, total_height_with_bleed - bleed, total_height_with_bleed]
        return horizontal_guides, vertical_guides, total_width, total_height_with_bleed
    
    # 単ページの場合
    horizontal_guides = [0, bleed, total_width_with_bleed - bleed, total_width_with_bleed]
    vertical_guides = [0, bleed, total_height_with_bleed - bleed, total_height_with_bleed]
    return horizontal_guides, vertical_guides, total_width_with_bleed, total_height_with_bleed

def main():
    # 見開き選択
    while True:
        is_spread = input("見開きデータですか？ (y/n): ").strip().lower()
        if is_spread in ("y", "yes"):
            spread = True
            break
        elif is_spread in ("n", "no"):
            spread = False
            break
        else:
            print("無効な入力です。'y' または 'n' を入力してください。")

    # 本のサイズ入力
    print("\n利用可能なサイズ:")
    for key, (name, width, height) in BOOK_SIZES.items():
        print(f"  {key}: {name} ({width}x{height} mm)")
    print("  0: カスタムサイズ")

    try:
        choice = int(input("本のサイズを選んでください (番号): ").strip())
        if choice == 0:  # カスタムサイズ
            book_size = input("幅x高さ[mm]を入力してください: ").strip()
            try:
                width, height = map(float, book_size.split("x"))
                size = (width, height)
            except ValueError:
                print("無効なサイズ形式です。例: 148x210")
                sys.exit(1)
        elif choice in BOOK_SIZES:
            _, width, height = BOOK_SIZES[choice]
            size = (width, height)
        else:
            print("無効な選択です。")
            sys.exit(1)
    except ValueError:
        print("番号で入力してください。")
        sys.exit(1)

    # 塗り足し幅入力
    try:
        bleed = float(input("塗り足し幅(mm)を入力してください: ").strip())
        if bleed < 0:
            print("塗り足し幅は0以上にしてください。")
            sys.exit(1)
    except ValueError:
        print("数値として有効な塗り足し幅を入力してください。")
        sys.exit(1)

    # 厚み入力（見開きの場合のみ）
    thickness = 0
    if spread:
        try:
            thickness = float(input("厚み(mm)を入力してください（本文は0を入力）: ").strip())
            if thickness < 0:
                print("厚みは0以上にしてください。")
                sys.exit(1)
        except ValueError:
            print("数値として有効な厚みを入力してください。")
            sys.exit(1)

    # ガイド線の計算
    horizontal_guides, vertical_guides, total_width, total_height = calculate_guides(size, bleed, thickness, spread)

    # 結果の表示
    if spread:
        print(f"\n見開きサイズ (塗り足し込み): {total_width}x{total_height} mm, 塗り足し幅: {bleed} mm, 厚み: {thickness} mm")
    else:
        print(f"\nサイズ (塗り足し込み): {total_width}x{total_height} mm, 塗り足し幅: {bleed} mm")

    print("水平方向のガイド線位置 (mm):", horizontal_guides)
    print("垂直方向のガイド線位置 (mm):", vertical_guides)

if __name__ == "__main__":
    main()
