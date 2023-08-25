import gspread
from flask import Flask, render_template, request, Markup

app=Flask(__name__)
app.static_folder = 'static'

# 最終版
@app.route("/", methods=["GET", "POST"])
def display_data():
    # 讀取存在資料夾下的google sheets 金鑰檔案
    gc = gspread.service_account(filename='/Users/eason/Desktop/flask_project/exalted-kit-391608-bdaf37439175.json')
    # 打開 google sheets 中，名稱為 output 的試算表，
    sh = gc.open("output")
    # 選定試算表中 all的工作表
    worksheet_name = "all"
    # 把連線、指定試算表、選擇工作表整合方便後續操作
    worksheet = sh.worksheet(worksheet_name)
    # 使用get_all_values() 就可以把資料存成二維列表
    data = worksheet.get_all_values()
    # 拿取標頭行 [['平台', '名稱', '價格', '連結', '圖片']]
    header = data[0]  
    # 剩下資料行
    rows = data[1:]  
    #使用者選擇價錢排序的判斷式
    if request.method == "POST":
        # 取得使用者的選擇
        sort_option = request.form.get("sortOption") 
        if sort_option == "highToLow":
            rows = sorted(rows, reverse=True, key=lambda item: int(item[2].replace(',', '')))
        elif sort_option == "lowToHigh":
            rows = sorted(rows, reverse=False, key=lambda item: int(item[2].replace(',', '')))

    for i in range(len(rows)):
        # 這行讓讓網頁呈現價格時去除逗號
        # rows[i][2] = rows[i][2].replace(',', '')
        # 使資料中的連結文字，變成可以點選前往的網址  
        rows[i][3] = Markup(f'<a href="{rows[i][3]}">連結</a>')

    return render_template('index.html', header=header, rows=rows)

if __name__ == '__main__':
    app.run()