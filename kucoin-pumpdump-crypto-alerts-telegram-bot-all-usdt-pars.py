import os
from dotenv import load_dotenv
import requests
import time
from datetime import datetime, timedelta
import base64
import hashlib
import asyncio
import hmac
import telegram.error
from telegram import Bot
from telegram.error import RetryAfter
import pandas as pd
import pandas_ta as ta

# Settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
API_PASSPHRASE = os.getenv("API_PASSPHRASE")
API_IP = os.getenv("API_IP")

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def get_headers(method, request_path, body=""):
    timestamp = str(int(time.time() * 1000))
    str_to_sign = timestamp + method + request_path + (body if body else "")
    signature = base64.b64encode(
        hmac.new(
            API_SECRET.encode("utf-8"), str_to_sign.encode("utf-8"), hashlib.sha256
        ).digest()
    ).decode("utf-8")
    passphrase = base64.b64encode(
        hmac.new(
            API_SECRET.encode("utf-8"), API_PASSPHRASE.encode("utf-8"), hashlib.sha256
        ).digest()
    ).decode("utf-8")
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": timestamp,
        "KC-API-KEY": API_KEY,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
    }
    return headers

def fetch_market_data():
    url = "https://api.kucoin.com/api/v1/market/allTickers"
    try:
        response = requests.get(
            url, headers=get_headers("GET", "/api/v1/market/allTickers")
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        bot.send_message(chat_id=CHANNEL_ID, text=f"Error fetching data: {e}")
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        bot.send_message(chat_id=CHANNEL_ID, text=f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")
        return None

def calculate_indicators(prices_history, minutes_to_evaluate=5, hours_for_trend=4):
    """
    Calculates technical indicators for each pair of cryptocurrencies.
    Returns a dictionary with the calculated indicators.
    """
    current_time = datetime.now()
    indicators = {}

    evaluation_period = minutes_to_evaluate
    # Convert hours to minutes
    trend_period = hours_for_trend * 60

    for pair, prices in prices_history.items():
        prices_df = pd.DataFrame(prices, columns=["price", "time"])
        prices_df = prices_df.set_index("time")

        # Filter prices for trial and trend periods
        prices_evaluation = prices_df.loc[
            current_time - timedelta(minutes=evaluation_period): current_time, "price"
        ]
        prices_trend = prices_df.loc[
            current_time - timedelta(minutes=evaluation_period + trend_period): current_time, "price"
        ]

        if len(prices_evaluation) >= 1 and len(prices_trend) >= 1:
            # Calculate technical indicators
            rsi_evaluation = calculate_rsi(prices_evaluation)
            rsi_trend = calculate_rsi(prices_trend)

            macd_evaluation, signal_evaluation, hist_evaluation = calculate_macd(
                prices_evaluation
            )
            macd_trend, signal_trend, hist_trend = calculate_macd(prices_trend)

            indicators[pair] = {
                "rsi_evaluation": rsi_evaluation,
                "rsi_trend": rsi_trend,
                "macd_evaluation": macd_evaluation,
                "macd_trend": macd_trend,
                "signal_evaluation": signal_evaluation,
                "signal_trend": signal_trend,
                "hist_evaluation": hist_evaluation,
                "hist_trend": hist_trend,
            }
        else:
            print(f"Error calculating indicators for {pair}")

    return indicators

def calculate_rsi(prices):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).mean()
    loss = (-delta.where(delta < 0, 0)).mean()
    if loss == 0:
        return 100
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_ema(prices, window):
    weights = pd.Series(1.0, index=prices.index)
    weights /= weights.sum()
    ema = prices.ewm(span=window, min_periods=window).mean()
    return ema

def calculate_macd(prices):
    ema12 = calculate_ema(prices, 12)
    ema26 = calculate_ema(prices, 26)
    macd_line = ema12 - ema26
    signal_line = calculate_ema(macd_line, 9)
    histogram = macd_line - signal_line
    return macd_line.iloc[-1], signal_line.iloc[-1], histogram.iloc[-1]

async def send_telegram_message(chat_id, message):
    try:
        await bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")
    except telegram.error.RetryAfter as e:
        print(f"Flood control exceeded. Retrying in {e.retry_after} seconds.")
        await asyncio.sleep(e.retry_after)
        await send_telegram_message(chat_id, message)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
    else:
        await asyncio.sleep(1)

# 60 minutes and 15 seconds
async def send_donation_message(interval=60 * 60 + 15):
    while True:
        message = f"💚 Help us push the boundaries of AI-driven analysis! Your contributions fuel our relentless pursuit of innovative trading strategies:\n\n🤲 <b>Every donation propels us forward.</b>\n\n<b>$USDT (TRC-20):</b>\nTGpiWetnYK2VQpxNGPR27D9vfM6Mei5vNA\n\n🫶 <b>Designed to help you.</b>\n🫶 <b>From AIs to human-beans.</b>\n\n🔸 <i>Version 2.0.1 (2024/06/29)</i>⠀"
        print(message)
        await send_telegram_message(CHANNEL_ID, message)
        await asyncio.sleep(interval)

def calculate_variation_and_trend(prices_history, minutes_to_evaluate=5, hours_for_trend=4):
    current_time = datetime.now()
    variations = {}

    evaluation_period = minutes_to_evaluate
    # Convert hours to minutes
    trend_period = hours_for_trend * 60

    for pair, prices in prices_history.items():
        prices_in_evaluation_period = [(price, time) for price, time in prices if current_time - time <= timedelta(minutes=evaluation_period)]
        trend_start_time = current_time - timedelta(minutes=(evaluation_period + trend_period))
        prices_in_trend_period = [(price, time) for price, time in prices if trend_start_time <= time <= trend_start_time + timedelta(minutes=trend_period)]

        if len(prices_in_evaluation_period) >= 1 and len(prices_in_trend_period) >= 1:
            initial_price_evaluation = prices_in_evaluation_period[0][0]
            final_price_evaluation = prices_in_evaluation_period[-1][0]
            initial_price_trend = prices_in_trend_period[0][0]
            final_price_trend = prices_in_trend_period[-1][0]

            variation_evaluation = ((final_price_evaluation - initial_price_evaluation) / initial_price_evaluation) * 100
            variation_trend = ((final_price_trend - initial_price_trend) / initial_price_trend) * 100

            if variation_evaluation > 0 and variation_trend > 0:
                variations[pair] = variation_evaluation

    return variations

async def monitor_prices():
    prices_history = {}
    last_indicators = {}
    sold_pairs = {}
    monitoring_message_sent = False

    while True:
        data = fetch_market_data()
        if data:
            tickers = data["data"]["ticker"]
            for ticker in tickers:
                symbol = ticker["symbol"]
                # Checks if the pair is desired, not containing "UP-", "DOWN-", "3L-", "3S-", "2L-", " 2S-"
                if "USDT" in symbol and not any(x in symbol for x in ["UP-", "DOWN-", "3L-", "3S-", "2L-", "2S-"]):
                    last_price = ticker.get("last")
                    if last_price:
                        price = float(last_price)
                        if symbol not in prices_history:
                            prices_history[symbol] = []
                        prices_history[symbol].append((price, datetime.now()))

            # Clear old data
            for pair in list(prices_history.keys()):
                if len(prices_history[pair]) > 1000:
                    prices_history[pair] = prices_history[pair][-1000:]

            indicators = calculate_indicators(
                prices_history, minutes_to_evaluate=5, hours_for_trend=4
            )

            variations = calculate_variation_and_trend(prices_history, minutes_to_evaluate=5, hours_for_trend=4)

            any_signal = False

            for pair, pair_indicators in indicators.items():
                rsi_evaluation = pair_indicators["rsi_evaluation"]
                rsi_trend = pair_indicators["rsi_trend"]
                macd_evaluation = pair_indicators["macd_evaluation"]
                macd_trend = pair_indicators["macd_trend"]
                signal_evaluation = pair_indicators["signal_evaluation"]
                signal_trend = pair_indicators["signal_trend"]
                hist_evaluation = pair_indicators["hist_evaluation"]
                hist_trend = pair_indicators["hist_trend"]

                current_price = prices_history[pair][-1][0]
                variation = ((current_price - prices_history[pair][0][0]) / prices_history[pair][0][0]) * 100

                # Conditions for buy signal
                if (
                    rsi_evaluation > 45
                    and macd_evaluation > signal_evaluation
                    and hist_evaluation > 0
                    and rsi_trend > 45
                    and macd_trend > signal_trend
                    and hist_trend > 0
                    and pair not in sold_pairs
                    and pair in variations
                    and variations[pair] > 2
                ):
                    message = f"🟢️ <b>STRONG PUMP DETECTED</b> 🟢️\n\n🧧 <b>${pair}</b>\n\n🐋 <b>Price:</b> {current_price:.8f} $USDT\n\n📈 <b>Variation:</b> {variation:.2f}%\n\n🏄‍♂️ RSI, MACD, and Histogram indicate strong upward momentum\n\n💠 This is an excellent buying opportunity!⠀"
                    print(message)
                    await send_telegram_message(CHANNEL_ID, message)
                    sold_pairs[pair] = True
                    any_signal = True
                    # os.system("afplay /System/Library/Sounds/Ping.aiff")

                # Conditions for sale sign
                elif pair in sold_pairs and (
                    # -4% drop after buy signal
                    (rsi_evaluation > 90 and variation < -3)
                    # RSI high and MACD indicating fall
                    or (rsi_evaluation > 90 and macd_evaluation < signal_evaluation and macd_trend < signal_trend)
                ):
                    message = f"🔴 <b>MOMENTUM DUMPING BELOW</b> 🔴\n\n🧧 <b>${pair}</b>\n\n🦈 <b>Price:</b> {current_price:.8f} $USDT\n\n📉 <b>Variation:</b> {variation:.2f}%\n\n🏄‍♀️ RSI, MACD, and Histogram indicate weakening upward momentum\n\n💠 Consider selling to mitigate risk!⠀"
                    print(message)
                    await send_telegram_message(CHANNEL_ID, message)
                    del sold_pairs[pair]
                    any_signal = True
                    # os.system("afplay /System/Library/Sounds/Glass.aiff")

            if not any_signal and not monitoring_message_sent:
                message = "📊 <b>MONITORING FOR PUMP ENTRIES</b> 📊\n\n🏄 Once an optimal wave pattern emerges\n\n🔔 You'll be instantly notified to ride the momentum...⠀"
                print(message)
                await send_telegram_message(CHANNEL_ID, message)
                monitoring_message_sent = True

        else:
            print("Error fetching market data.")

        await asyncio.sleep(1)

async def main():
    donation_task = asyncio.create_task(send_donation_message())
    monitor_task = asyncio.create_task(monitor_prices())
    await asyncio.gather(donation_task, monitor_task)

if __name__ == "__main__":
    asyncio.run(main())
