import soundfile as sf
from kokoro_onnx import Kokoro
from misaki import en, espeak

# Misaki G2P with espeak-ng fallback
fallback = espeak.EspeakFallback(british=False)
g2p = en.G2P(trf=False, british=False, fallback=fallback)

# Kokoro
kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")

# Phonemize
#text = """
#     [Misaki](/misˈɑki/) is a G2P engine designed for [Kokoro](/kˈOkəɹO/) models."""

#text = "A [FASTQ](/ˈfˈæstkju/) file"
#text = "fast"
#text = "Today, we'll break down what Phred quality scores are, how they're calculated, and how they're encoded in [FASTQ](/fæstˈkjuː/) files."
#text = "Today, we'll break down what Phred quality scores are, how they're calculated, and how they're encoded in [FASTQ](/ˈfˈæstkju/) files."
text = "Let us fectch the data"
    
phonemes, _ = g2p(text)
print(phonemes)
#print(dir(kokoro))
#print(kokoro.voices.files)

for voice in kokoro.voices.files:
    # Create
    samples, sample_rate = kokoro.create(phonemes, voice, is_phonemes=True)

    # Save
    sf.write(f"audio_{voice}.wav", samples, sample_rate)
    print(f"Created audio_{voice}.wav")