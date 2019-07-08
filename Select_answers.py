# Stack Apps API key
Auth_key = "rEi)4Xt7RnJf4tqP)pk5nQ(("
import requests
from pandas import DataFrame

def badge_reputation(dict_eta):
    """
    Simple function to calculate badge reputation of a user
    :param dict_eta: dictionary of badges the user have earned
    :return: a float value perfectly representing the badge reputation
    """
    if "badge_counts" in dict_eta:
        alpha = 0.3
        beta = 0.5
        gamma = 0.9
        badge_repu = 0
        dict_eta_2 = dict_eta['badge_counts']
        if 'bronze' in dict_eta_2:
            badge_repu+=alpha*dict_eta_2['bronze']
        if 'silver' in dict_eta_2:
            badge_repu+=beta*dict_eta_2['silver']
        if 'gold' in dict_eta_2:
            badge_repu+=gamma*dict_eta_2['gold']
        return badge_repu
    else:
        return 0


def top_answers_fun(q_id_eta):
    """
    Finds most appropriate answers based on user's reputation and answer's score and acceptance
    :param q_id_eta: ID of the question in stackoverflow database
    :return: returns top relevant answers of that question
    """
    # parameters
    delta = 0.5
    epsilon = 0.5
    zeta = 0.5
    url_eta = "https://api.stackexchange.com/2.2/questions/"+q_id_eta+"/answers?key="+Auth_key+"&order=desc&sort=votes&site=stackoverflow&filter=!)Q7ohwN5q2ex6NuB-d**q(*C"
    top_answers = requests.get(url_eta)
    top_answers = top_answers.json()
    df_ans = DataFrame(top_answers['items'])
#     print(df_ans)
    df_ans['badge_reputation'] = df_ans.apply(lambda row:badge_reputation(row.owner) , axis = 1)
    df_ans['repu'] = df_ans.apply(lambda row:row.owner['reputation'],axis=1)
    df_ans['final_function'] = df_ans.apply(lambda row:delta*row.badge_reputation+epsilon*row.repu+zeta*row.score,axis=1)
    df_ans = df_ans.sort_values(by = ["final_function"],ascending = False)
    eta = df_ans.iloc[0]['final_function']
    df_ans['final_function_2'] = df_ans.apply(lambda row:row.final_function+eta*int(row.is_accepted),axis=1)
    del df_ans['owner']
    type_a = list(df_ans['share_link'])
    return type_a
