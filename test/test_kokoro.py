import soundfile as sf
from kokoro_onnx import Kokoro
from misaki import en, espeak

# Misaki G2P with espeak-ng fallback
fallback = espeak.EspeakFallback(british=False)
g2p = en.G2P(trf=False, british=False, fallback=fallback)

# Kokoro
kokoro = Kokoro("kokoro-v0_19.onnx", "voices.bin")

# Phonemize
text = """
     [Misaki](/misˈɑki/) is a G2P engine designed for [Kokoro](/kˈOkəɹO/) models."""
phonemes, _ = g2p(text)
print(dir(kokoro))
print(kokoro.voices.files)

for voice in kokoro.voices.files:
    # Create
    samples, sample_rate = kokoro.create(phonemes, voice, is_phonemes=True)

    # Save
    sf.write(f"audio_{voice}.wav", samples, sample_rate)
    print(f"Created audio_{voice}.wav")