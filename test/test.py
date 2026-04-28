import yfinance as yf

print("歡迎使用【台美股一週表現追蹤器】🚀")
stock_id = input("請輸入股票代號 (例如台積電輸入 2330.TW，蘋果輸入 AAPL): ")

stock = yf.Ticker(stock_id)
history = stock.history(period="5d")

if history.empty:
    print("\n❌ 找不到這檔股票的資料，請確認代號是否輸入正確喔！")
else:
    print("\n" + "="*40)
    print(f"📊 股票代號: {stock_id} (近 5 個交易日紀錄)")
    print("-" * 40)

    # --- 新增區塊：使用 for 迴圈印出每一天的漲跌幅 ---
    # len(history) 會算出總共有幾筆資料(5筆)
    # 我們從第 2 筆 (索引值 1) 開始跑，這樣才能跟前一天(索引值 i-1) 比較
    for i in range(1, len(history)):
        # 抓取日期，並格式化為 月-日 (例如 05-04)
        date = history.index[i].strftime("%m-%d") 
        
        yesterday_price = history['Close'].iloc[i-1]
        today_price = history['Close'].iloc[i]
        
        daily_diff = today_price - yesterday_price
        daily_percent = (daily_diff / yesterday_price) * 100
        
        # 決定顯示的圖示
        if daily_diff > 0:
            icon = "📈 漲"
        elif daily_diff < 0:
            icon = "📉 跌"
        else:
            icon = "➖ 平"
            
        # 印出每日紀錄 (使用 >5.2f 讓對齊更漂亮)
        print(f"📅 {date} | 收盤: {today_price:7.2f} | {icon} {daily_percent:>5.2f}%")

    # --- 原本區塊：一週總結 ---
    print("-" * 40)
    week_ago_price = history['Close'].iloc[0]
    today_price = history['Close'].iloc[-1]
    
    total_diff = today_price - week_ago_price
    total_percent = (total_diff / week_ago_price) * 100

    if total_diff > 0:
        print(f"💡 【本週總結】: 🚀 累積上漲 {total_diff:.2f} 元 (總漲幅 {total_percent:.2f}%)！")
    elif total_diff < 0:
        print(f"💡 【本週總結】: ⚠️ 累積下跌 {abs(total_diff):.2f} 元 (總跌幅 {abs(total_percent):.2f}%)。")
    else:
        print("💡 【本週總結】: ➖ 平盤 (沒有明顯漲跌)。")
    print("="*40 + "\n")