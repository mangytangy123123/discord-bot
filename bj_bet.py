import json

json_dir = 'bj_bets.json'

def read_json():
    with open(json_dir,'r') as read_file:
        return json.load(read_file)
    
def write_json(data):
    with open(json_dir,'w') as write_file:
        json.dump(data,write_file)

def check_lowest(data,id):
    lowest_idx = 0
    for i,v in enumerate(list(data.keys())):
        print(v)
        if data[id][0] < data[v][0]:
            lowest_idx = i
    
    if list(data.keys())[lowest_idx] == id:
        return ' (lowest in the server lmao)'
    
    return ''
    
async def get_bet(author,channel,client):
    #return json file as a dictionary
    data = read_json()
    author_id = str(author.id)

    # { user_id : [money, restarts] } is the format im using
    try:
        data[author_id][0]
    except KeyError:
        print('key error')
        data[author_id] = [1000,0]

    if data[author_id][0] == 0:
        await channel.send(f"youve been rebirthed and gracefully given 100 by me.\na restart tally has been added to your account.\nreach 10 and youll be banned from this server. ahahaha")
        data[author_id][0] = 100
        data[author_id][1] += 1
        write_json(data)
        return
    
    def check_message(msg):
        return msg.content.isdigit() and msg.channel == channel

    await channel.send(f"you have: {data[author_id][0]}{check_lowest(data,author_id)}. how much you wanna bet")
    bet_amnt = int((await client.wait_for('message',timeout = 15, check=check_message)).content)
    print(bet_amnt)
    if (data[author_id][0] - bet_amnt) < 0:
        await channel.send(f"you dont have enough for that...")
        return
    
    
    data[author_id][0] -= bet_amnt
    print(data)
    
    write_json(data)

    return bet_amnt

async def add_money(dollars,author,channel):
    data = read_json()
    author_id = str(author.id)

    data[author_id][0] += dollars
    await channel.send(f"you now have: {data[author_id][0]} dollars, with {data[author_id][1]} rebirths")
    write_json(data)


