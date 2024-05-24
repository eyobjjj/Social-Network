
# file = ('c:/Users/Administrator/Desktop/@@@@@@/my_web/category/')
# lists = []
# def find_phone_number(file_path):
#     with open(file_path, 'r') as f:
#         for line in f:
#             lists.append(line)
#     print(lists)

# file_path = file+'@/20.txt'
# find_phone_number(file_path)



category = [
 'News & Politics',
 'Movies',
 'Entertainment',
 'Sports',
 'Food & Cooking',
 'Travel',
 'Fitness & Wellness',
 'Fashion & Beauty',
 'Technology',
 'Music',
 'Education',
 'Business & Finance',
 'Parenting',
 'Pets & Animals',
 'DIY & Crafts',
 'Humor & Comedy',
 'Science & Nature',
 'Health & Medicine',
 'Gaming',
 'Lifestyle',
 'Art & Photography']


import requests
#ACCESS_TOKEN = ""
#headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
endpoint = "http://127.0.0.1:8000/api/catagory/" 
for i in category:
    data = {
        "name": i
    }
    get_response = requests.post(endpoint, json=data) 
    print(get_response.json())

