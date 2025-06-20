import re

INPUT_FILE = "temperatureWifi_ex.ino"
OUTPUT_FILE = "../obfusque_minify/obfusque_minify.ino"

# Décalage César simple
def caesar_shift(text, shift=3):
    result = []
    for c in text:
        if 32 <= ord(c) <= 126:
            result.append(chr((ord(c) - 32 + shift) % 95 + 32))
        else:
            result.append(c)
    return ''.join(result)

def obfuscate_arduino_strings(code):
    pattern = re.compile(r'"(.*?)"')

    obfuscated_map = {}
    var_count = 0
    new_lines = []
    
    # Fonction pour créer des variables uniques
    def new_var():
        nonlocal var_count
        var = f'_obf_{var_count}'
        var_count += 1
        return var

    # Remplacement dans le code
    def replacer(match):
        original = match.group(1)
        obfuscated = caesar_shift(original)
        var_name = obfuscated_map.get(original)
        if not var_name:
            var_name = new_var()
            obfuscated_map[original] = var_name
            new_lines.append(f'String {var_name} = oeird32("{obfuscated}");')
        return var_name  # Remplacer la chaîne par le nom de variable

    code_body = pattern.sub(replacer, code)

    # Ajouter la fonction decodeCaesar + variables obfusquées
    decoder_function = """
String oeird32(String obf, int shift = 3) {
  String res = "";
  for (int i = 0; i < obf.length(); i++) {
    char c = obf.charAt(i);
    if (c >= 32 && c <= 126) {
      c = (c - 32 - shift + 95) % 95 + 32;
    }
    res += c;
  }
  return res;
}
"""

    # Ajouter les définitions de variables au début du fichier
    obfuscated_definitions = "\n".join(new_lines)
    final_code = decoder_function.strip() + "\n\n" + obfuscated_definitions + "\n\n" + code_body

    return final_code

def main():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        code = f.read()

    obfuscated_code = obfuscate_arduino_strings(code)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(obfuscated_code)

    print(f"Fichier obfusqué généré : {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
