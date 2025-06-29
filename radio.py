

import pyaudio
import numpy as np
from rtlsdr import RtlSdr
from scipy import signal
import argparse
import asyncio
import string

# --- グローバル設定 ---
SDR_SAMPLE_RATE = 1.024e6
AUDIO_SAMPLE_RATE = 48000
NUM_SAMPLES = 16384

# --- FMモードの処理 ---
async def process_fm(sdr, audio_stream):
    print("FM受信を開始します...")
    decimation_rate = int(SDR_SAMPLE_RATE / AUDIO_SAMPLE_RATE)
    async for samples in sdr.stream(num_samples_or_bytes=NUM_SAMPLES):
        x = np.diff(np.unwrap(np.angle(samples)))
        norm = np.abs(samples[:-1])
        x /= np.where(norm == 0, 1e-6, norm)
        demodulated = signal.decimate(x, decimation_rate, ftype='fir')
        if np.max(np.abs(demodulated)) > 0:
            audio_signal = demodulated * 32767 / np.max(np.abs(demodulated))
            audio_signal = audio_signal.astype(np.int16)
            audio_stream.write(audio_signal.tobytes())

# --- AMモードの処理 ---
async def process_am(sdr, audio_stream):
    print("AM受信を開始します...")
    decimation_rate = int(SDR_SAMPLE_RATE / (AUDIO_SAMPLE_RATE / 2))
    async for samples in sdr.stream(num_samples_or_bytes=NUM_SAMPLES):
        demodulated = np.abs(samples)
        audio_signal = signal.decimate(demodulated, decimation_rate, ftype='fir')
        audio_signal -= np.mean(audio_signal)
        if np.max(np.abs(audio_signal)) > 0:
            output = audio_signal * 32767 / np.max(np.abs(audio_signal))
            output = output.astype(np.int16)
            audio_stream.write(output.tobytes())

# --- ACARSモードの処理 (簡易版) ---
async def process_acars(sdr):
    print("ACARS受信を開始します... メッセージが表示されるまで時間がかかることがあります。")
    decimation_rate = int(SDR_SAMPLE_RATE / 48000)
    async for samples in sdr.stream(num_samples_or_bytes=NUM_SAMPLES):
        demodulated = np.abs(samples)
        audio = signal.decimate(demodulated, decimation_rate, ftype='fir')
        if np.mean(audio**2) > 0.01:
            try:
                raw_bytes = (audio * 127).astype(np.int8).tobytes()
                text = raw_bytes.decode('ascii', errors='ignore')
                printable_text = ''.join(filter(lambda x: x in string.printable, text))
                if len(printable_text.strip()) > 10:
                    print(f"[ACARS Raw Data]: {printable_text.strip()}")
            except Exception:
                pass

def main():
    parser = argparse.ArgumentParser(description="RTL-SDR Receiver")
    parser.add_argument("-m", "--mode", dest="mode", required=True, choices=['fm', 'am', 'acars'], help="Operating mode")
    parser.add_argument("-f", "--freq", dest="freq", required=True, type=float, help="Center frequency in Hz")
    args = parser.parse_args()

    sdr = None
    p = None
    stream = None
    try:
        sdr = RtlSdr()
        sdr.sample_rate = SDR_SAMPLE_RATE
        sdr.center_freq = args.freq
        sdr.gain = 'auto'

        print(f"モード: {sdr.mode.upper()}")
        print(f"周波数: {sdr.center_freq/1e6:.3f} MHz")
        print(f"SDRサンプルレート: {sdr.sample_rate/1e6} MHz")

        loop = asyncio.get_event_loop()

        if args.mode != 'acars':
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=AUDIO_SAMPLE_RATE, output=True)
            if args.mode == 'fm':
                loop.run_until_complete(process_fm(sdr, stream))
            elif args.mode == 'am':
                loop.run_until_complete(process_am(sdr, stream))
        else:
            loop.run_until_complete(process_acars(sdr))

    except KeyboardInterrupt:
        print("\nプログラムを終了します。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        print("リソースを解放しています...")
        if stream is not None:
            stream.stop_stream()
            stream.close()
        if p is not None:
            p.terminate()
        if sdr is not None:
            sdr.close()
        print("終了しました。")

if __name__ == '__main__':
    main()

