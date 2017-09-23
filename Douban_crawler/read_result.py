import _pickle as pickle
'''
read crawler's result
'''
def get_result():
    with open("topic_list.db","rb") as file:
        topic_list =pickle.load(file)
    return topic_list
result = get_result()