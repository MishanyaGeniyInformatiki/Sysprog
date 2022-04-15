import requests
from vk_config import VK_CONFIG

domain = VK_CONFIG["domain"]
access_token = VK_CONFIG["access_token"]
custom_access_token = VK_CONFIG["custom_access_token"]
v = VK_CONFIG["version"]
fields = 'sex'


class GetData:

    def __init__(self, group_id):

        group_id = group_id
        keys = list(group_id.keys())

        for i in range(len(group_id)):
            for j in range(len(group_id[keys[i]])):

                with open(f'data/{keys[i]}/{group_id[keys[i]][j]}.txt', 'w') as file1:
                    id_list = GroupInf(group_id[keys[i]][j]).get_members_id()
                    if id_list == -1:
                        pass
                    else:
                        for element in id_list:
                            file1.write(str(element))
                            file1.write(' ')
                        print(f'{group_id[keys[i]][j]}.txt is write')
                    file1.close()


class GroupInf:

    def __init__(self, group_id):
        self.group_id = group_id

    def get_response(self):
        query = f"{domain}/groups.getMembers?access_token={access_token}&group_id={self.group_id}&v={v}"
        response = requests.get(query)
        return response.json()

    def get_count_members(self):
        response = self.get_response()
        if list(response.keys())[0] == 'error':
            print('Error:', 'error_code =', str(response['error']['error_code']) + ';',
                  str(response['error']['error_msg']))
            return -1
        else:
            return response['response']['count']

    def get_members_id(self):
        resp = self.get_response()
        if list(resp.keys())[0] == 'error':
            with open('errors.txt', 'a') as file1:
                file1.write('Error: ' + 'error_code = ' + str(resp['error']['error_code']) + '; ' +
                            str(resp['error']['error_msg']) + '; ' + 'id = ' + str(self.group_id) + '\n')
            file1.close()
            return -1
        else:
            offset = 0
            array = []
            while True:
                query = f"{domain}/groups.getMembers?access_token={access_token}&group_id={self.group_id}&offset={offset}&v={v}"
                response = requests.get(query)
                array += response.json()['response']['items']
                offset += 1000
                if offset > response.json()['response']['count']:
                    break
            return array

    def get_group_name(self):
        query = f"{domain}/groups.getById?access_token={access_token}&group_id={self.group_id}&v={v}"
        response = requests.get(query)
        return response.json()['response'][0]['name']


class PersonInf:

    def __init__(self, user_id):
        self.user_id = user_id

    class AllGroupsInf:

        def __init__(self, user_id):
            self.user_id = user_id

        def get_response(self, user_id):
            query = f"{domain}/groups.get?access_token={custom_access_token}&user_id={user_id}&v={v}"
            response = requests.get(query)
            return response.json()

        def get_groups(self):
            response = self.get_response(self.user_id)
            if list(response.keys())[0] == 'error':
                if response['error']['error_code'] == 6: # Too many requests per second
                    return -2
                else: # другие ошибки записываю в файл 'errors.txt'
                    with open('errors.txt', 'a') as file1:
                        file1.write('Error: ' + 'error_code = ' + str(response['error']['error_code']) + '; ' + str(response['error']['error_msg']) + '; ' + 'id = ' + str(self.user_id) + '\n')
                    file1.close()
                    #print('Error:', 'error_code =', str(response['error']['error_code']) + ';', str(response['error']['error_msg']))
                    return -1
            else: # без ошибок
                return response['response']['items']

        def get_count_groups(self):
            response = self.get_response(self.user_id)
            if list(response.keys())[0] == 'error':
                print('Error:', 'error_code =', str(response['error']['error_code']) + ';', str(response['error']['error_msg']))
                return -1
            else:
                return response['response']['count']

    class FriendsInf:

        def __init__(self, user_id):
            self.user_id = user_id

        def get_response(self):
            query = f"{domain}/friends.get?access_token={access_token}&user_id={self.user_id}&fields={fields}&v={v}"
            response = requests.get(query)
            return response.json()

        def get_count_friends(self):
            response = self.get_response()
            if list(response.keys())[0] == 'error':
                print('Error:', 'error_code =', str(response['error']['error_code']) + ';', str(response['error']['error_msg']))
                return -1
            else:
                return response['response']['count']

        def get_friends_id(self):
            response = self.get_response()
            if list(response.keys())[0] == 'error':
                with open('errors_2.txt', 'a') as file1:
                    file1.write('Error: ' + 'error_code = ' + str(response['error']['error_code']) + '; ' + str(
                        response['error']['error_msg']) + '; ' + 'id = ' + str(self.user_id) + '\n')
                file1.close()
                return -1
            else:
                dict = response['response']['items']
                len = self.get_count_friends()
                list_id = [dict[i]['id'] for i in range(len)]
                return list_id