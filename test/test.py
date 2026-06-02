import matplotlib.pyplot as plt
import yfinance as yf

# 設定 matplotlib 支援中文（解決圖表亂碼問題）
plt.rcParams["font.family"] = ["Microsoft JhengHei", "Arial"]  # 微軟正黑體
plt.rcParams["axes.unicode_minus"] = False  # 正常顯示負號

print("歡迎使用【台美股一週表現追蹤器】🚀")
stock_id = input(
    "請輸入股票代號 (例如台積電輸入 2330.TW，蘋果輸入 AAPL): "
)

stock = yf.Ticker(stock_id)
history = stock.history(period="5d")

if history.empty:
    print("\n❌ 找不到這檔股票的資料，請確認代號是否輸入正確喔！")
else:
    print("\n" + "=" * 40)
    print(f"📊 股票代號: {stock_id} (近 5 個交易日紀錄)")
    print("-" * 40)

    # --- 新增區塊：使用 for 迴圈印出每一天的漲跌幅 ---
    for i in range(1, len(history)):
        # 抓取日期，並格式化為 月-日 (例如 05-04)
        date = history.index[i].strftime("%m-%d")

        yesterday_price = history["Close"].iloc[i - 1]
        today_price = history["Close"].iloc[i]

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
        print(
            f"📅 {date} | 收盤: {today_price:7.2f} | {icon} {daily_percent:>5.2f}%"
        )

    # --- 原本區塊：一週總結 ---
    print("-" * 40)
    week_ago_price = history["Close"].iloc[0]
    today_price = history["Close"].iloc[-1]

    total_diff = today_price - week_ago_price
    total_percent = (total_diff / week_ago_price) * 100

    if total_diff > 0:
        print(
            f"💡 【本週總結】: 🚀 累積上漲 {total_diff:.2f} 元 (總漲幅 {total_percent:.2f}%)！"
        )
    elif total_diff < 0:
        print(
            f"💡 【本週總結】: ⚠️ 累積下跌 {abs(total_diff):.2f} 元 (總跌幅 {abs(total_percent):.2f}%)。"
        )
    else:
        print("💡 【本週總結】: ➖ 平盤 (沒有明顯漲跌)。")
    print("=" * 40 + "\n")

    # --- ✨ 新增區塊：使用 Matplotlib 繪製折線圖 ---
    print("正在產生走勢圖表...")

    # 1. 準備 X 軸（日期）與 Y 軸（收盤價）的資料
    # 將 index 轉換為 "月-日" 的字串格式
    x_dates = history.index.strftime("%m-%d")
    y_prices = history["Close"]

    # 2. 建立圖表
    plt.figure(figsize=(8, 4.5))  # 設定圖表寬高比

    # 3. 畫出折線（加上圓點標記、線條顏色、寬度）
    plt.plot(
        x_dates,
        y_prices,
        marker="o",
        color="#1f77b4",
        linewidth=2,
        markersize=6,
    )

    # 4. 在每個點上方加上具體的價格標籤
    for x, y in zip(x_dates, y_prices):
        plt.text(x, y + (y * 0.002), f"{y:.2f}", ha="center", va="bottom")

    # 5. 設定圖表標題與座標軸標籤
    plt.title(f"{stock_id} 近 5 個交易日收盤走勢", fontsize=14, fontweight="bold")
    plt.xlabel("日期", fontsize=12)
    plt.ylabel("收盤價", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.5)  # 加入淡淡的格線

    # 6. 自動調整佈局並顯示圖表
    plt.tight_layout()
    plt.show()
