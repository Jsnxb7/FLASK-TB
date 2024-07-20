from nltk.translate.bleu_score import sentence_bleu

translations = [
    {
        "serial_number": 1,
        "original_text": "hello",
        "translated_text": "こんにちは",
        "translation_check": "こんにちは"
    },
    {
        "serial_number": 2,
        "original_text": "hello",
        "translated_text": "こんにちは",
        "translation_check": "こんにちは"
    },
    {
        "serial_number": 3,
        "original_text": "hello",
        "translated_text": "こんにちは",
        "translation_check": "こんにちは"
    },
    {
        "serial_number": 4,
        "original_text": "this a is text to show the translations",
        "translated_text": "この a は,翻訳文を表示するテキストです.",
        "translation_check": "これは翻訳を表示するテキストです"
    },
    {
        "serial_number": 5,
        "original_text": "this is an apple, exiled from its country",
        "translated_text": "これは,その国から追放されたリンゴです.",
        "translation_check": "これはその国から追放されたリンゴです"
    },
    {
        "serial_number": 6,
        "original_text": "hello",
        "translated_text": "こんにちは",
        "translation_check": "こんにちは"
    },
    {
        "serial_number": 7,
        "original_text": "exile",
        "translated_text": "流刑",
        "translation_check": "流刑"
    },
    {
        "serial_number": 8,
        "original_text": "exiled",
        "translated_text": "送信",
        "translation_check": "エグザイル/絆"
    },
    {
        "serial_number": 9,
        "original_text": "apple in a country",
        "translated_text": "ある 国 の りんご",
        "translation_check": "国にあるリンゴ"
    }
]

# Extract reference translations
references = [translation["translation_check"].split() for translation in translations]

bleu_scores = []
for translation in translations:
    candidate = translation["translated_text"].split()
    reference = references[translation["serial_number"] - 1]  # Reference corresponding to the candidate
    bleu = sentence_bleu([reference], candidate, weights=(0.5, 0.5))  # Include unigrams, bigrams, trigrams, and 4-grams
    bleu_scores.append(bleu)

# Display BLEU scores
for i, bleu_score in enumerate(bleu_scores):
    print(f"Pair {i+1}: BLEU Score = {bleu_score}")
