# RTL-SDR Radio Receiver

This is a simple command-line tool written in Python to receive various radio signals using an RTL-SDR dongle.

## Features

*   **FM Radio Reception:** Listen to standard broadcast FM radio.
*   **AM Radio Reception:** Listen to AM broadcasts (e.g., aviation, amateur radio).
*   **ACARS Message Reception:** A basic decoder for Aircraft Communications Addressing and Reporting System messages.

## Prerequisites

*   Python 3.x
*   An RTL-SDR dongle with drivers properly installed.
*   The required Python libraries listed in `requirements.txt`.

## Installation

1.  Clone this repository or download the files.
2.  Install the necessary dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script from your command line, specifying the mode and frequency.

**Syntax:**
```bash
python radio.py -m <mode> -f <frequency>
```

**Arguments:**

*   `-m`, `--mode`: The operating mode. Choose from `fm`, `am`, or `acars`.
*   `-f`, `--freq`: The center frequency to tune to, specified in Hertz (Hz). You can use scientific notation (e.g., `80.0e6` for 80.0 MHz).

### Examples

*   **Listen to an FM radio station at 80.0 MHz:**
    ```bash
    python radio.py -m fm -f 80.0e6
    ```

*   **Listen to an AM broadcast at 594 kHz:**
    ```bash
    python radio.py -m am -f 594e3
    ```

*   **Decode ACARS messages on the Japan-wide frequency of 131.45 MHz:**
    ```bash
    python radio.py -m acars -f 131.45e6
    ```

## Notes

*   The ACARS decoder is very basic and may not correctly display all messages. It's intended as a simple proof-of-concept.
*   You will need a suitable antenna for the frequency you are trying to receive.
*   The SDR gain is set to 'auto' by default.
*   Press `Ctrl+C` to stop the program.

---
---

# RTL-SDR ラジオ受信機

これは、RTL-SDRドングルを使用して様々な無線信号を受信するための、Pythonで書かれたシンプルなコマンドラインツールです。

## 機能

*   **FMラジオ受信:** 一般的なFMラジオ放送を聴取します。
*   **AMラジオ受信:** AM放送（航空無線、アマチュア無線など）を聴取します。
*   **ACARSメッセージ受信:** ACARS (航空機通信アドレッシング・レポーティング・システム) メッセージの簡易的なデコーダーです。

## 必要なもの

*   Python 3.x
*   正しくドライバがインストールされたRTL-SDRドングル
*   `requirements.txt`に記載されているPythonライブラリ

## インストール

1.  このリポジトリをクローンするか、ファイルをダウンロードします。
2.  pipを使用して必要な依存関係をインストールします。
    ```bash
    pip install -r requirements.txt
    ```

## 使い方

コマンドラインからスクリプトを実行し、モードと周波数を指定します。

**書式:**
```bash
python radio.py -m <モード> -f <周波数>
```

**引数:**

*   `-m`, `--mode`: 動作モード。`fm`, `am`, `acars`の中から選択します。
*   `-f`, `--freq`: チューニングする中心周波数をヘルツ(Hz)で指定します。科学的記数法も使用できます (例: 80.0 MHzの場合は `80.0e6`)。

### 実行例

*   **周波数80.0 MHzのFMラジオ局を聴く:**
    ```bash
    python radio.py -m fm -f 80.0e6
    ```

*   **周波数594 kHzのAM放送を聴く:**
    ```bash
    python radio.py -m am -f 594e3
    ```

*   **日本国内共通周波数 131.45 MHz でACARSメッセージをデコードする:**
    ```bash
    python radio.py -m acars -f 131.45e6
    ```

## 注意事項

*   ACARSデコーダーは非常に簡易的なものであり、全てのメッセージを正しく表示できない場合があります。これは簡単な概念実証として意図されています。
*   受信しようとする周波数に適したアンテナが必要です。
*   SDRのゲインはデフォルトで 'auto' に設定されています。
*   プログラムを停止するには `Ctrl+C` を押してください。

このReadmeファイルはGoogle Geminiを使用して作成されました。
This file created by Google Gemini