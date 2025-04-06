from langchain.tools import BaseTool
import argostranslate.package
import argostranslate.translate
from typing import ClassVar


class ArgosTranslateTool(BaseTool):
    name: str = "argos_translate"
    description: str = (
        "Translates text from one language to another. "
        "Input must be formatted as 'text|from_language|to_language', "
        "where languages can be either ISO codes (en, es, fr, etc.) or full names (English, Spanish, etc.)."
    )

    LANGUAGE_CODES: ClassVar[dict] = {
        "english": "en",
        "spanish": "es",
        "french": "fr",
        "german": "de",
        "italian": "it",
        "romanian": "ro",
        # Add more languages as needed
    }

    def __init__(self):
        super().__init__()
        argostranslate.package.update_package_index()

    def _run(self, input_text: str):
        # Parse the input
        try:
            text, from_lang, to_lang = input_text.strip().split("|")
        except ValueError:
            return "Invalid input format. Please use 'text|from_language|to_language'."

        # Convert language names to ISO codes if needed
        from_lang_code = self.LANGUAGE_CODES.get(from_lang.lower(), from_lang.lower())
        to_lang_code = self.LANGUAGE_CODES.get(to_lang.lower(), to_lang.lower())

        # Check installed languages
        installed_languages = argostranslate.translate.get_installed_languages()
        from_lang_obj = next(
            (lang for lang in installed_languages if lang.code == from_lang_code), None
        )
        to_lang_obj = next(
            (lang for lang in installed_languages if lang.code == to_lang_code), None
        )

        # Handle missing language models
        if not from_lang_obj or not to_lang_obj:
            try:
                available_packages = argostranslate.package.get_available_packages()
                available_package = next(
                    (
                        pkg
                        for pkg in available_packages
                        if pkg.from_code == from_lang_code
                        and pkg.to_code == to_lang_code
                    ),
                    None,
                )
                if available_package:
                    download_path = available_package.download()
                    argostranslate.package.install_from_path(download_path)
                    # Refresh installed languages after installation
                    installed_languages = (
                        argostranslate.translate.get_installed_languages()
                    )
                    from_lang_obj = next(
                        (
                            lang
                            for lang in installed_languages
                            if lang.code == from_lang_code
                        ),
                        None,
                    )
                    to_lang_obj = next(
                        (
                            lang
                            for lang in installed_languages
                            if lang.code == to_lang_code
                        ),
                        None,
                    )
                    if not from_lang_obj or not to_lang_obj:
                        return f"Failed to install language models for {from_lang_code} to {to_lang_code}."
                else:
                    return f"No translation package available for {from_lang_code} to {to_lang_code}."
            except Exception as e:
                return f"Error installing translation package: {str(e)}"

        # Perform translation
        translation = from_lang_obj.get_translation(to_lang_obj)
        translated_text = translation.translate(text)
        return translated_text

    async def _arun(self, input_text: str):
        raise NotImplementedError("Async operation not implemented.")
