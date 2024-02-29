from deep_translator import GoogleTranslator
def translate_text(text, target_language="ar"):
    max_chunk_length = 500
    words = text.split()

    translated_chunks = []
    current_chunk = ""

    for word in words:
        if len(current_chunk) + len(word) <= max_chunk_length:
            current_chunk += word + " "
        else:
            translated_chunk = GoogleTranslator(source='auto', target=target_language).translate(current_chunk.strip())
            translated_chunks.append(translated_chunk)
            current_chunk = word + " "

    # Translate the last chunk
    if current_chunk:
        translated_chunk = GoogleTranslator(source='auto', target=target_language).translate(current_chunk.strip())
        translated_chunks.append(translated_chunk)

    translated_text = " ".join(translated_chunks)
    return translated_text
