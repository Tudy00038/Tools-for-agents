from argostranslate import package, translate


def translate_text(text, source_lang, target_lang):
    installed_languages = translate.get_installed_languages()

    source = next(
        (lang for lang in installed_languages if lang.code == source_lang), None
    )
    target = next(
        (lang for lang in installed_languages if lang.code == target_lang), None
    )

    if not source or not target:
        return "Language pair not available. Please download the model."

    translation = source.get_translation(target)
    return translation.translate(text)


if __name__ == "__main__":
    translated_text = translate_text("Hello, how are you?", "en", "es")
    print(translated_text)
    # Output: "Hola, ¿cómo estás?"
