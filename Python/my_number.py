def find_string_positions(text, search_string, context_length=10):

    results = []
    start = 0

    while True:
        # 指定文字列の位置を探す
        start = text.find(search_string, start)
        if start == -1:  # 見つからなければ終了
            break

        # 前後の文脈を取得
        start_context = max(0, start - context_length)
        end_context = min(len(text), start + len(search_string) + context_length)
        context = text[start_context:start] + f'"{search_string}"' + text[start + len(search_string):end_context]

        # 結果を記録
        results.append({
            "position": start,
            "context": context,
        })

        # 次の検索開始位置を設定
        start += len(search_string)

    return results


# テスト用
if __name__ == "__main__":
    # test.txt を読み込む
    try:
        with open("pi-10oku.txt", "r", encoding="utf-8") as file:
            text_data = file.read()

        # 探したい文字列を入力
        search_term = input("マイナンバーを入力してください: ").strip()

        # 検索結果を取得
        result = find_string_positions(text_data, search_term)

        # 結果を表示
        if result:
            for entry in result:
                print(f"{entry['position']}文字目 ,  {entry['context']}")
            print(f"\n合計: {len(result)} 個見つかりました。")
        else:
            print(f"マイナンバー '{search_term}' は見つかりませんでした。")

    except FileNotFoundError:
        print("エラー: テキストファイルが見つかりませんでした。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
