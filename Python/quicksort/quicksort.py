def quicksort(arr, low, high, output_file, comparison_count, move_count):
    if low < high:
        pi, comparison_count, move_count = partition(arr, low, high, output_file, comparison_count, move_count)
        comparison_count, move_count = quicksort(arr, low, pi - 1, output_file, comparison_count, move_count)
        comparison_count, move_count = quicksort(arr, pi + 1, high, output_file, comparison_count, move_count)
    return comparison_count, move_count

def partition(arr, low, high, output_file, comparison_count, move_count):
    pivot = len(arr[high].strip())  # 改行を取り除いて長さを計算
    i = low - 1
    for j in range(low, high):
        comparison_count += 1  # 比較回数を増加
        if len(arr[j].strip()) < pivot:  # 改行を取り除いて長さを計算
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            move_count += 1  # 移動回数を増加
            write_step(arr, output_file, j, i)  # 移動前後の行をハイライト
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    move_count += 1  # 移動回数を増加
    write_step(arr, output_file, high, i + 1)  # 移動前後の行をハイライト
    return i + 1, comparison_count, move_count

def write_step(arr, output_file, moved_index_1, moved_index_2):
    with open(output_file, 'a', encoding='utf-8') as file:
        # 現在の並べ替え結果をテキストとしてファイルに書き出す
        file.write("\n")
        for idx, line in enumerate(arr):
            # 移動前の行に矢印を追加
            if idx == moved_index_1:
                file.write(f"{line.strip()}←\n")
            # 移動先の行に矢印を追加
            elif idx == moved_index_2:
                file.write(f"{line.strip()}←\n")
            else:
                file.write(f"{line.strip()}\n")
        file.write("\n")

def sort_lines_by_length(input_file, output_file):
    # テキストファイルを読み込む
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 出力ファイルを初期化して書き出す
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("Quicksort:\n")
    
    comparison_count = 0
    move_count = 0
    comparison_count, move_count = quicksort(lines, 0, len(lines) - 1, output_file, comparison_count, move_count)

    # 最終的な比較回数と移動回数をファイルに書き出す
    with open(output_file, 'a', encoding='utf-8') as file:
        file.write(f"\nTotal comparisons: {comparison_count}\n")
        file.write(f"Total moves: {move_count}\n")

# 使用例
input_file = 'Input.txt'  # ここに入力ファイルのパスを指定
output_file = 'Output.txt'

sort_lines_by_length(input_file, output_file)
