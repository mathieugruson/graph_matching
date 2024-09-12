import re

def format_word(word):
    if word:  # Check if the word is not empty
        return word[0] + word[1:].lower()
    return word 


# servait a cleaner la formation de l'etudiant, mtn on matche avec la totalite du nom de la formation
# donc c est inutile
# def extract_formation_name(input_string):
#     # Regular expression to find "Fusion" or "SketchUp"
#     match = re.search(r"\b(Fusion|SketchUp|Blender)\b", input_string)
#     if match:
#         # Return the matched string in lowercase
        
#         return format_word(match.group(1))
#     else:
#         # Return None if no match is found
#         return None

