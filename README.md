# Kucoin PumpDump Crypto Alerts Telegram Bot

![Kucoin PumpDump Crypto Alerts Telegram Bot](./assets/screenshot.png?raw=true)

## Description

The Kucoin PumpDump Crypto Alerts Telegram Bot is an automated system designed to monitor and analyse cryptocurrency pairs on the KuCoin exchange. It uses technical indicators to identify buying or selling opportunities based on price fluctuations and market trends. Alerts are sent through Telegram, allowing users to respond quickly to market changes.

## Features

-   **Real-Time Monitoring:** The bot monitors a configurable list of cryptocurrency pairs and analyses their prices in real time.
-   **Technical Analysis:** Utilises indicators such as RSI (Relative Strength Index) and MACD (Moving Average Convergence Divergence) to assess market conditions.
-   **Telegram Alerts:** Sends custom alerts via Telegram when it detects favourable market conditions for buying or selling.

## Prerequisites

Before starting the bot, ensure you have installed:

-   Python 3.10 or higher
-   pip (Python package manager)
-   A KuCoin API account
-   A configured Telegram bot with a token

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Takk8IS/kucoin-pumpdump-crypto-alerts-telegram-bot.git
cd kucoin-pumpdump-crypto-alerts-telegram-bot
```

### 2. Install dependencies

```bash
pip install --upgrade --force-reinstall -r requirements.txt
```

### 3. Configure your environment variables

Create a `.env` file in the project root and add the following variables:

```plaintext
TELEGRAM_BOT_TOKEN=your_token_here
CHANNEL_ID=@your_channel_here
API_KEY=your_api_key_here
API_SECRET=your_api_secret_here
API_PASSPHRASE=your_passphrase_here
```

## Usage

### Selected USDT pars version

To start the bot, run:

```bash
python3 kucoin-pumpdump-crypto-alerts-telegram-bot-selected-usdt-pars.py
```

### All USDT pars version

To start, run:

```bash
python3 kucoin-pumpdump-crypto-alerts-telegram-bot-all-usdt-pars.py
```

## Contributing

Contributions are always welcome! If you would like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your modifications (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a Pull Request.

## Licence

This project is licensed under the Attribution 4.0 International License.

## Support

If you need help with the bot, please contact via email at say@takk.ag or through Telegram.

## Donations

If this script has been helpful for you, consider making a donation to support our work:

-   $USDT (TRC-20): TGpiWetnYK2VQpxNGPR27D9vfM6Mei5vNA

Your donations help us continue developing useful and innovative tools.

## Takk™ Innovate Studio

Leading the Digital Revolution as the Pioneering 100% Artificial Intelligence Team.

-   Copyright (c)
-   Licence: Attribution 4.0 International (CC BY 4.0)
-   Author: David C Cavalcante
-   LinkedIn: https://www.linkedin.com/in/hellodav/
-   Medium: https://medium.com/@davcavalcante/
-   Positive results, rapid innovation
-   URL: https://takk.ag/
-   X: https://twitter.com/takk8is/
-   Medium: https://takk8is.medium.com/
