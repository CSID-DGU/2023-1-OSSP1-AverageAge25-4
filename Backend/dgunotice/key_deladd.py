import requests

keywordlist = []

def fetch_keywords():
    try:
        response = requests.get('http://127.0.0.1:8000/mainPage/notices/')
        response.raise_for_status()
        keywordlist.extend(response.json())
        print(keywordlist)
    except requests.exceptions.RequestException as error:
        print(error)

fetch_keywords()

def delete_keyword(keyword):
    try:
        response = requests.delete(f"http://127.0.0.1:8000/keywords/{keyword}")
        response.raise_for_status()
        print(f'키워드 "{keyword}" 삭제됨')
        # Perform any necessary post-deletion actions
    except requests.exceptions.RequestException as error:
        print(error)

delete_keyword('취업')  # Replace '취업' with the actual keyword you want to delete

def add_keyword(keyword, cid):
    try:
        data = {
            'key': keyword,
            'Cid': cid
        }
        response = requests.post("http://127.0.0.1:8000/keywords/", json=data)
        response.raise_for_status()
        print('키워드 추가 요청 성공')
        # Perform any necessary post-addition actions
    except requests.exceptions.RequestException as error:
        print(error)