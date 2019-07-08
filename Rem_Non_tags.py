import json

# All the 55000 stack overflow tags stored in value_list  to be used by remove_nonsotag function
with open('SO_tags.txt', 'r') as f:
    value_list = json.load(f)
f.close()


def remove_nonsotag(words_list_eta):
    """
    To remove unnecssary tag from the previous generated tags.
    :param words_list_eta: Take a list of words.
    :return: Returns a list of words with non stackoverflow tags removed
    """
    for i in words_list_eta:
        if i not in value_list:
            words_list_eta.remove(i)
    local_list_eta = set(words_list_eta)
    return local_list_eta
