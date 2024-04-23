from google.cloud import translate_v3 as translate

project_id = "planar-night-421212"
key_file_path = "planar-night-421212-0b0f37e6ecb8.json"


def create_translate_cliente(project_id, key_file_path):
    from google.oauth2 import service_account

    credentials = service_account.Credentials.from_service_account_file(key_file_path)
    translate_client = translate.TranslationServiceClient(credentials=credentials)

    return translate_client

def translate_text(translate_client, text, input_language, target_language, project_id):
    parent = f"projects/{project_id}/locations/global"

    response = translate_client.translate_text(
        request = {
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": input_language,
            "target_language_code": target_language,
        }
        
    )

    return response.translations[0].translated_text

def print_supported_languages(translate_client, display_language_code: str):
    parent = f"projects/{project_id}/locations/global"

    response = translate_client.get_supported_languages(
        request = {
            "parent": parent,
            "display_language_code": display_language_code,
        }
    )

    languages = response.languages
    print(f" Languages: {len(languages)} ".center(60, "-"))
    for language in languages:
        language_code = language.language_code
        display_name = language.display_name
        print(f"{language_code:10}{display_name}")
    

def get_supported_languages(translate_client, display_language_code: str):
    parent = f"projects/{project_id}/locations/global"

    response = translate_client.get_supported_languages(
        request = {
            "parent": parent,
            "display_language_code": display_language_code,
        }
    )

    languages = response.languages
    language_codes = [language.language_code for language in languages]
    return language_codes

translate_client = create_translate_cliente(project_id, key_file_path)

input_language = "en"
target_language = "fr"
cont = True

print("Welcome to Python Translator!\n")
while cont==True:
    print(f"Choose an option:\n1. Translate (Current: {input_language} -> {target_language})\n2. See available languages\n3. Choose input language\n4. Choose output language\n5. Exit\n")
    option = int(input("Option: "))
    if option == 1:
        original_text = input(f"Text to translate ({input_language}): ")
        translated_text = translate_text(translate_client, original_text, input_language, target_language, project_id)
        print(f"Translated text ({target_language}): {translated_text}")
        input("\nPress Enter to continue...")
    elif option == 2:
        print_supported_languages(translate_client, "en")
        input("\nPress Enter to continue...")
    elif option == 3:
        new_input_language = input("Choose an input language: ")
        if new_input_language not in get_supported_languages(translate_client, "en"):
            print("Invalid language code, please use the option 2 to see all available languages codes.")
            input('Press Enter to continue...\n')
        else:
            input_language = new_input_language
        print('')
    elif option == 4:
        new_target_language = input("Choose an output language: ")
        if new_target_language not in get_supported_languages(translate_client, "en"):
            print("Invalid language code, please use the option 2 to see all available languages codes.")
            input('Press Enter to continue...\n')
        else:
            target_language = new_target_language
        print('')
    elif option == 5:
        cont = False
    else:
        print("Wrong Option!")
        input('Press Enter to continue...\n')
        
print("\nGoodbye!")