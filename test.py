from translate import Translator
translator = Translator(to_lang="ja")
translation = translator.translate("this is a pen")
print(translation)