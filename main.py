from Get_Inf import PersonInf
from Get_Inf import GroupInf
from Get_Inf import GetData
import json
import linecache

group_id = {'Программирование': ['null_bytes', 'veb_programmirovanie', 'inf_dolb', '1c_prosto', 'codemika'],
            'Спорт': ['liveonly18', 'sportbst', 'sportmsu', 'miptsport', 'allvolley_ru'],
            'Политика': ['rp_ranepa', 'thepoliticstoday', 'keep_politics', 'peace.policy', 'rfpolitics'],
            'Бизнес': ['aliexpressforsellers', 'businessliteratura', 'mybiz63', 'fullcyclesite', 'boing.bizclub'],
            'Музыка': ['carmusic2022', 'muz2018muz', 'podborkahit', 'russian_music_official', 'club_music_2021'],
            'Вязание': ['evcrochet', 'crochet_work', 'anastasiya.priyma', 'margaritaterekhovaa', 'viazanie_igruhki'],
            'Философия': ['barinoffvictor', 'filosofia_toni', 'tailershelby', 'anti_tomas_shelby', 'marla_suka'],
            'Юмор': ['lookpics', 'polezumor', 'veseluxa_slv', 'cartime_vk', 'totsamiyumor'],
            'Цитаты': ['very_sad_and', 'citaatu', 'titatibobr', 'prepod_mipt', 'pacanskie_cutaty'],
            'Здоровье': ['zhenskoe_zdorovie', 'beauty_health_coach', 'zdorovye_03', 'beg.zdorove.krasota', 'zdorovieuglich']}

attributes = {'Программирование': '0',
            'Спорт': '1',
            'Политика': '2',
            'Бизнес': '3',
            'Музыка': '4',
            'Вязание': '5',
            'Философия': '6',
            'Юмор': '7',
            'Цитаты': '8',
            'Здоровье': '9'}

def create_attributes_json():

    keys = list(group_id.keys())

    massive = []
    for i in range(len(group_id)):
        for j in range(len(group_id[keys[i]])):

            with open(f'data/{keys[i]}/{group_id[keys[i]][j]}.txt', 'r') as file1:
                print(i, j)
                id_list = [x for x in next(file1).split()]
                for element in id_list:
                    massive.append(element)
            file1.close()

    massive = list(set(massive))
    data = {s: [] for s in massive}

    for i in range(len(group_id)):
        for j in range(len(group_id[keys[i]])):

            with open(f'data/{keys[i]}/{group_id[keys[i]][j]}.txt', 'r') as file1:
                id_list = [x for x in next(file1).split()]

                for pers_id in id_list:
                    if attributes[keys[i]] not in data[pers_id]:
                        data[pers_id].append(attributes[keys[i]])
            file1.close()

    with open('attributes.json', 'w') as outfile:
        json.dump(data, outfile)
    outfile.close()

def write_friends_txt():

    # чищу файл ошибок
    #open('errors.txt', 'w').close()

    with open('attributes.json', 'r') as json_file:
        data = json.load(json_file)
    json_file.close()
    keys = list(data.keys())

    with open('friends_2.txt', 'a') as file:

        cnt = 0
        for pers_id in keys:
            friends = PersonInf(pers_id).FriendsInf(pers_id).get_friends_id()
            if friends != -1:
                friends_str = str()
                for i in range(len(friends)):
                    friends_str += str(friends[i]) + ' '
                file.write(pers_id + ' ' + friends_str + '\n')
            cnt += 1
            print(cnt)
    file.close()

def create_adjacent_txt(): # создает файл смежности вершин

    mass = list() # список id пользователей (1-я колонка friends_joint.txt)
    with open('friends_joint.txt', 'r') as joint:
        mass_len = sum(1 for line in joint)
        for i in range(1, mass_len + 1):
            mass.append(linecache.getline('friends_joint.txt', i).split()[0])

    with open('adjacent_edges.txt', 'w') as file1:
        for i in range(1, mass_len + 1):
            user = linecache.getline('friends_joint.txt', i).split()[0]
            line = linecache.getline('friends_joint.txt', i).split()[1:]
            friends = list(set(mass) & set(line)) # друзья пользователя, которые находятся находятся также и в mass
            for each_id in friends:
                file1.write(user + ' ' + each_id + '\n')
            print(i)
    file1.close()


if __name__ == '__main__':
    pass
    #GetData(group_id)

    #create_attributes_json()

    #write_friends_txt()

    #create_adjacent_txt()






