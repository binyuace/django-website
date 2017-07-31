import webhoseio
from rango.models import Category
def run_query(query):
    webhoseio.config(token="2c57d5e2-1bfe-421a-9423-a98f8dc4d051")
    q = "\""+query+"\""+"site_category:tech site_type:blogs language:english"
    query_params = {
        "q": q,
        "ts": "1501170816664",
        "sort": "relevancy"
    }
    output = webhoseio.query("filterWebContent", query_params)
    result = []
    count = 0
    # print output['posts'][0]['text'] # Print the text of the first post
    # print output['posts'][0]['published'] # Print the text of the first post publication date
    for post in output['posts']:
        if count < 10:
            result.append({
                'title':post['title'],
                'link':post['url'],
                'summary':post['text'][0:300],
            })
        count = count+1
    return result
def get_category_list(max_length = 0, starts_with=''):
    cat_list = []
    if max_length and starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)
    if cat_list and cat_list.count() > max_length:
        return cat_list[:max_length]
    return cat_list
