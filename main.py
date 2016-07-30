import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import telebot
from telebot import types
import json
import os
import config
import random
import requests as req
import urllib
import urllib2
import re
import redis as r

bot = telebot.TeleBot(config.token)

f = "Bot Firstname: {}".format(bot.get_me().first_name)
u = "\nBot username: {}".format(bot.get_me().username)
i = "\nBot ID: {}".format(bot.get_me().id)
c = "\n\nThank you for using this source :)"
print(f + u + i + c)

@bot.message_handler(commands=['start'])
def welcome(m):
    cid = m.chat.id
    markup = types.InlineKeyboardMarkup()
    b = types.InlineKeyboardButton("MY OWner",callback_data='parsa')
    markup.add(b)
    nn = types.InlineKeyboardButton("Inline Mode", switch_inline_query='')
    markup.add(nn)
    redis = r.StrictRedis(host='localhost', port=6379, db=0)
    redis.sadd('start','{}'.format(m.from_user.id))
    ret_msg = bot.send_message(cid, "HI \n\n Welcome to UNF BOT \n\n PLease choose one :)", disable_notification=True, reply_markup=markup)
    assert ret_msg.message_id

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "parsa":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="MY owner is : @parsa alemi\nspecial tnx to my friends :D")

@bot.message_handler(commands=['help'])
def welcome(m):
    cid = m.chat.id
    markup = types.InlineKeyboardMarkup()
    ret_msg = bot.send_message(cid, "WE will add help soon", disable_notification=True, reply_markup=markup)
    assert ret_msg.message_id

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "music":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="@unfrobot music [music name]\n smart and advanced music searcher")

@bot.message_handler(commands=['id'])
def id(m):      # info menu
    cid = m.chat.id
    title = m.chat.title
    usr = m.chat.username
    f = m.chat.first_name
    l = m.chat.last_name
    t = m.chat.type
    d = m.date
    text = m.text
    p = m.pinned_message
    fromm = m.forward_from
    markup = types.InlineKeyboardMarkup()
#info text
    bot.send_chat_action(cid, "typing")
    bot.reply_to(m, "*ID from* : ```{}``` \n *Chat name* : ```{}``` \n *Your Username* : ```{}``` \n *Your First Name* : ```{}```\n *Your Last Name* : ```{}```\n *Type From* : ```{}``` \n *Msg data* : ```{}```\n *Your Msg* : ```{}```\n* pind msg * : ```{}```\n *from* : ```{}```".format(cid,title,usr,f,l,t,d,text,p,fromm), parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['rank'])
def rank(m):
    text = m.text
    rep = text.replace('/rank ', '')
    rank = os.popen('curl http://cruel-plus.ir/alexa/rank.php?url={}'.format(rep)).read()
    bot.send_message(m.chat.id,rank)

@bot.message_handler(commands=['contact'])
def c(m):
    uid = m.chat.id
    bot.send_chat_action(uid, 'typing')
    bot.send_contact(uid, phone_number="+989398391927", first_name="parsaalemi")

@bot.message_handler(commands=["ping"])
def on_ping(message):
    bot.reply_to(message, "*I am online*", parse_mode="Markdown")

@bot.message_handler(commands=['unf'])
def handler(m):
    cid = m.chat.id
    bot.send_message(cid, "I am UNF BOT :)))))\n dev by parsa alemi", parse_mode="Markdown")
    bot.send_chat_action(cid, "upload_photo")
    bot.send_photo(cid, open('slackbot-story1-582x436.jpg'), caption="UNF  \xF0\x9F\x98\x9C")

@bot.message_handler(commands=['stats'])
def stats(m):
    redis = r.StrictRedis(host='localhost', port=6379, db=0)
    msm = redis.scard('start')
    if str(m.from_user.id) == config.is_sudo:
        bot.send_message(m.chat.id, '<b>Users</b> : <code>{}</code>'.format(msm),parse_mode='HTML')

@bot.message_handler(commands=['idme'])
def test_handler(m):
    cid = m.from_user.id
    fl = m.from_user.first_name
    bot.send_message(cid, "*{}*  Your ID = ```{}```".format(fl,cid), parse_mode="Markdown")

@bot.message_handler(commands=['imdb'])
def command_imdb(m):
    cid = m.chat.id
    token = m.text[6:]
    url = "http://www.omdbapi.com/?t=%s&y=&plot=short&r=json" % token
    link = urllib.urlopen(url)
    data = json.loads(link.read())
    if data['Response'] == 'False':
        bot.send_message(cid, 'you should write the movie name :D')

    image = urllib.URLopener()
    image.retrieve(data['Poster'], "imdb_tmp.jpg")
    bot.send_photo(cid, open( 'imdb_tmp.jpg', 'rb'))
    results = """*title*: """ + data['Title'] + "\n" """*Releas Date*: """ +data['Released']  + "\n" """*Time*: """ +data['Runtime']  + "\n" """*Rating*: """ +data['imdbRating'] + "\n" """*Year*: """ +data['Year'] + "\n" """*Group*: """ +data['Genre'] + "\n""""*Argumento*: """ + data['Plot'] + "\n" """*Director*: """ +data["Director"] + "\n" """*Actors*: """ +data["Actors"] + "\n" """*Language*: """ +data["Language"] + "\n" """*Country*: """ +data["Country"] + "\n" """*Awards*\xF0\x9F\x8E\x96: """ +data["Awards"]
    bot.send_message(cid, results, parse_mode="Markdown")

@bot.message_handler(commands=['send'])
def send(m):
    senderid = m.chat.id
    first = m.from_user.first_name
    usr = m.from_user.username
    str = m.text
    txt = str.replace('/send', '')
    bot.send_message(senderid, "*i have sent your pm to parsa :)*", parse_mode="Markdown")
    bot.send_message(config.is_sudo, "msg : {}\nid : {}\nname : {}\nUsername : @{}".format(txt,senderid,first,usr))

@bot.message_handler(commands=['aparat'])
def aparat(m):
    text = m.text.split(' ',1)[1]
    url = urllib.urlopen('http://www.aparat.com/etc/api/videoBySearch/text/'+text)
    data = url.read()
    js = json.loads(data)
    title1 = js['videobysearch'][0]['title']
    poster1 = js['videobysearch'][0]['big_poster']
    uid1 = js['videobysearch'][0]['uid']
    urllib.urlretrieve(poster1,'poster.png')
    bot.send_photo(m.chat.id, open('poster.png'), caption='Title : '+title1+'\nLink : http://www.aparat.com/v/'+uid1)
    os.remove('poster.png')

@bot.message_handler(commands=['map'])
def command_map(m):
    cid = m.chat.id
    token = m.text.split(" ", 1)[1]
    token = token.encode('utf-8')
    url = "https://maps.googleapis.com/maps/api/staticmap?center=%s&zoom=14&size=400x400&maptype=hybrid&key=AIzaSyBmZVQKUXYXYVpY7l0b2fNso4z82H5tMvE" % token
    urllib.urlretrieve(url, "map.png")
    bot.send_photo(cid, open( 'map.png', 'rb'))

@bot.message_handler(commands=['dev'])
def handle_message(msg):
	bot.reply_to(msg, text="dev by parsa alemi")

@bot.inline_handler(lambda query: query.query == 'pic')
def query_photo(inline_query):
    try:
        r2 = types.InlineQueryResultPhoto('1',
                                          'http://apod.nasa.gov/apod/image/1601/aurora_vetter_2000.jpg',
                                          'http://apod.nasa.gov/apod/image/1601/aurora_vetter_2000.jpg')
        r3 = types.InlineQueryResultPhoto('2',
                                          'http://www.menucool.com/slider/prod/image-slider-5.jpg',
                                          'http://www.menucool.com/slider/prod/image-slider-5.jpg')
        r4 = types.InlineQueryResultPhoto('3',
                                          'http://www.w3schools.com/css/img_fjords.jpg',
                                          'http://www.w3schools.com/css/img_fjords.jpg')
        r5 = types.InlineQueryResultPhoto('4',
                                          'https://www.nasa.gov/sites/default/files/styles/image_card_4x3_ratio/public/thumbnails/image/idcs1426.jpg?itok=Gc_-Q58L',
                                          'https://www.nasa.gov/sites/default/files/styles/image_card_4x3_ratio/public/thumbnails/image/idcs1426.jpg?itok=Gc_-Q58L')
        r6 = types.InlineQueryResultPhoto('5',
                                          'http://static1.squarespace.com/static/553a8716e4b0bada3c80ca6b/553a9655e4b03939abece18a/5731fc75f85082142b12b095/1462893710445/mayfourblocknature.jpg',
                                          'http://static1.squarespace.com/static/553a8716e4b0bada3c80ca6b/553a9655e4b03939abece18a/5731fc75f85082142b12b095/1462893710445/mayfourblocknature.jpg')
        r7 = types.InlineQueryResultPhoto('6',
                                          'https://i.kinja-img.com/gawker-media/image/upload/s--BVBooEGz--/c_scale,fl_progressive,q_80,w_800/vjamorotezzukhdvpccc.jpg',
                                          'https://i.kinja-img.com/gawker-media/image/upload/s--BVBooEGz--/c_scale,fl_progressive,q_80,w_800/vjamorotezzukhdvpccc.jpg')
        r8 = types.InlineQueryResultPhoto('7',
                                          'http://www.planwallpaper.com/static/images/beautiful-sunset-images-196063.jpg',
                                          'http://www.planwallpaper.com/static/images/beautiful-sunset-images-196063.jpg')
        r9 = types.InlineQueryResultPhoto('8',
                                          'https://upload.wikimedia.org/wikipedia/commons/0/00/Center_of_the_Milky_Way_Galaxy_IV_%E2%80%93_Composite.jpg',
                                          'https://upload.wikimedia.org/wikipedia/commons/0/00/Center_of_the_Milky_Way_Galaxy_IV_%E2%80%93_Composite.jpg')
        r10 = types.InlineQueryResultPhoto('9',
                                          'http://s3.freefoto.com/images/9912/01/9912_01_4132_web.jpg',
                                          'http://s3.freefoto.com/images/9912/01/9912_01_4132_web.jpg')
        r11 = types.InlineQueryResultPhoto('10',
                                          'http://www.spyderonlines.com/images/wallpapers/nature-image/nature-image-1.jpg',
                                          'http://www.spyderonlines.com/images/wallpapers/nature-image/nature-image-1.jpg')
        r12 = types.InlineQueryResultPhoto('11',
                                          'https://cdn.eso.org/images/large/eso1209a.jpg',
                                          'https://cdn.eso.org/images/large/eso1209a.jpg')
        r13 = types.InlineQueryResultPhoto('12',
                                          'https://upload.wikimedia.org/wikipedia/commons/9/98/UNF_Ospreys_logo.png',
                                          'https://upload.wikimedia.org/wikipedia/commons/9/98/UNF_Ospreys_logo.png')

        bot.answer_inline_query(inline_query.id, [r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13], cache_time=1)
    except Exception as e:
        print(e)

@bot.inline_handler(lambda q: q.query)
def inline(query):
    if query.query.split()[0] == 'music':
          oo = query.query
          input = oo.replace("music ","")
          t5 = input.replace(" ","%20")
          eeqq = urllib.quote(input)
          req = urllib2.Request("http://api.gpmod.ir/music.search/?v=2&q={}&count=30".format(eeqq))
          opener = urllib2.build_opener()
          f = opener.open(req)
          parsed_json = json.loads(f.read())
          yy = random.randrange(10)
          yy1 = random.randrange(10)
          yy2 = random.randrange(10)
          yy3 = random.randrange(10)
          yy4 = random.randrange(10)
          rrrr = parsed_json['response'][yy]['link']
          rrrr1 = parsed_json['response'][yy1]['link']
          rrrr2 = parsed_json['response'][yy2]['link']
          rrrr4 = parsed_json['response'][yy3]['link']
          rrrr5 = parsed_json['response'][yy4]['link']
          rrrr01 = parsed_json['response'][yy]['title']
          rrrr11 = parsed_json['response'][yy1]['title']
          rrrr21 = parsed_json['response'][yy2]['title']
          rrrr41 = parsed_json['response'][yy3]['title']
          rrrr51 = parsed_json['response'][yy4]['title']
          pic = types.InlineQueryResultAudio('1', rrrr ,'Music of {}  \n{}'.format(input,rrrr01))
          pic1 = types.InlineQueryResultAudio('2', rrrr1 ,'Music of {}  \n{}'.format(input,rrrr11))
          pic2 = types.InlineQueryResultAudio('3', rrrr2 ,'Music of {}  \n{}'.format(input,rrrr21))
          pic3 = types.InlineQueryResultAudio('4', rrrr4 ,'Music of {}  \n{}'.format(input,rrrr41))
          pic4 = types.InlineQueryResultAudio('5', rrrr5 ,'Music of {}  \n{}'.format(input,rrrr51))
          bot.answer_inline_query(query.id, [pic,pic1,pic2,pic3,pic4], cache_time="15")
@bot.message_handler(commands=['test'])
def command_test(m):
    cid = m.chat.id
    domain = m.text[6:]
    resp = urllib.urlopen("http://www.isup.me/%s" % domain).read()
    if re.search("It's just you.", resp, re.DOTALL):
        bot.send_message(cid, "*i have chek it the site is online*", parse_mode="Markdown")
    else:
        bot.send_message(cid, "i have chek it the site is offline", parse_mode="Markdown")

@bot.message_handler(func=lambda m: True, content_types=['new_chat_participant'])
def on_user_joins(m):
	cid = m.chat.id
	inviter = m.from_user.first_name
	if m.content_type == 'new_chat_participant':
		if m.new_chat_participant.id == bot.get_me().id:
			chatid = m.chat.id
			if str(cid) not in user:
				user.append(str(cid))
				with open('user.txt', 'a') as f:
					f.write(str(cid)+"\n")
			bot.send_message(cid, "HI ALl\n" + str(inviter) + " has invited me into this group!")
			print "New group received."
			userwhogotadded = m.new_chat_participant.first_name
			username = m.new_chat_participant.username
			groupname = m.chat.title
			groupid = m.chat.id

@bot.message_handler(func=lambda message: True)
def m(m):
    if m.text == 'Sticker' or m.text == '/sticker':
        urllib.urlretrieve("https://source.unsplash.com/random", "img.jpg")
        bot.send_chat_action(m.chat.id, 'upload_photo')
        bot.send_sticker(m.chat.id, open('img.jpg'))
        print 'command Sticker'
        print '{}'.format(m.from_user.first_name)
        print '{}'.format(m.from_user.username)

@bot.message_handler(commands=['date'])
def command_date(m):
    cid = m.chat.id
    x = datetime.datetime.now()
    switcher = {
        1: "enero ",
        2: "febrero ",
        3: " March",
        4: "april ",
        5: "may ",
        6: "june ",
        7: "july",
        8: "agost ",
        9: " September",
        10: " October",
        11: " November",
        12: "December "
    }
    mes = switcher[x.month]
    date = "We are at %s de %s" % (x.day, mes)
    bot.send_message(cid, date)

@bot.inline_handler(lambda query: len(query.query) is 0)
def query_text(query):
    user = query.from_user.username
    name = query.from_user.first_name
    lname = query.from_user.last_name
    uid = query.from_user.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('{}'.format(name), url="https://telegram.me/{}".format(user)))
    thumb_url = 'http://www.hopsten.de/assets/images/iNFO_LOGO.jpg'
    info = types.InlineQueryResultArticle('1','Your Info ',types.InputTextMessageContent('*Username : @{}\nYour First Name : {}\nYour Last Name : {}\nYour ID :  {}*'.format(user,name,lname,uid), parse_mode="Markdown"),reply_markup=markup,thumb_url=thumb_url)
    #pic = types.InlineQueryResultPhoto('2',
                                       #'http://vip.opload.ir/vipdl/95/3/negative23/photo-2016-06-09-01-09-41.jpg',
                                       #'http://vip.opload.ir/vipdl/95/3/negative23/photo-2016-06-09-01-09-41.jpg',
                                       #input_message_content=types.InputTextMessageContent('@Taylor_Team')
    #gif = types.InlineQueryResultGif('2',
                                    # 'http://andrewtrimmer.com/wp-content/uploads/2014/09/Coming-Soon_Light-Bulbs_Cropped-Animation-Set_03c.gif',
                                     #'http://andrewtrimmer.com/wp-content/uploads/2014/09/Coming-Soon_Light-Bulbs_Cropped-Animation-Set_03c.gif',
                                     #gif_width=70,
                                     #gif_height=40,
                                     #title="Soon Update",
                                    # input_message_content=types.InputTextMessageContent('New Update #Soon'))

    tumsss = 'http://images.clipartpanda.com/contact-clipart-contact-phone-md.png'
    random_text = random.randint(1, 100)
    tmpp = 'http://static.nautil.us/3006_5f268dfb0fbef44de0f668a022707b86.jpg'
    randowm = types.InlineQueryResultArticle('2', 'random number',types.InputTextMessageContent('random NUmber : {}'.format(random_text)), thumb_url=tmpp)

    req = urllib2.Request("http://unf.xzn.ir/data/joke.db")
    opener = urllib2.build_opener()
    f = opener.open(req)
    text = f.read()
    text1 = text.split(",")
    last = random.choice(text1)
    joke = types.InlineQueryResultArticle('3', 'Joke', types.InputTextMessageContent('{}'.format(last)),thumb_url='http://up.persianscript.ir/uploadsmedia/5b63-download-2-.png')
    reqa = urllib2.Request('http://api.gpmod.ir/time/')
    openera = urllib2.build_opener()
    fa = openera.open(reqa)
    parsed_jsona = json.loads(fa.read())
    EN = parsed_jsona['ENtime']
    FA = parsed_jsona['ENdate']
    time_tmp = 'http://a4.mzstatic.com/us/r30/Purple49/v4/c4/bf/0b/c4bf0bbe-f71c-12be-6017-818ab2594c98/icon128-2x.png'
    timesend = types.InlineQueryResultArticle('4', 'Time\Date', types.InputTextMessageContent('`Tehran` : *{}*\n`date` :*{}*'.format(EN,FA), parse_mode='Markdown'), thumb_url=time_tmp)

    req = urllib2.Request("http://umbrella.shayan-soft.ir/txt/danestani.db")
    opener = urllib2.build_opener()
    f = opener.open(req)
    text = f.read()
    text1 = text.split(",")
    last = random.choice(text1)
    logo = 'https://d2vvqscadf4c1f.cloudfront.net/R1H3Ms7QSQOwRpTbUImd_science.jpg'
    since = types.InlineQueryResultArticle('5', 'science', types.InputTextMessageContent(last.replace('@UmbrellaTeam',"\nUNF ROBOT")),thumb_url=logo)

    hi_tmp = 'https://d85wutc1n854v.cloudfront.net/live/products/600x375/WB0PGGM81.png?v=1.0'
    hi = types.InlineQueryResultArticle('6', 'Music', types.InputTextMessageContent('*@UNFrobot music [Music name]*', parse_mode='Markdown'), thumb_url=hi_tmp)

    bot.answer_inline_query(query.id, [info, randowm, joke, since, timesend, hi], cache_time=5, switch_pm_text='Welcome to UNF inline')

@bot.message_handler(commands=['uptime'])
def ss(m):
    cc = os.popen("uptime").read()
    bot.send_message(m.chat.id, '{}'.format(cc))

@bot.message_handler(commands=['leave'])
def leavehandler(m):
    if m.from_user.id == config.is_sudo:
        bot.leave_chat(m.chat.id)

@bot.message_handler(commands=['whois'])
def whois(m):
    text = m.text
    repll = text.replace('/whois', '')
    whois = os.popen('whois {}'.format(repll)).read()
    bot.send_message(m.chat.id, '{}'.format(whois))

bot.polling(True)
#end
#
# _   _   _   _   _____
#| | | | | \ | | |  ___|
#| | | | |  \| | | |_
#| |_| | | |\  | |  _|
 #\___/  |_| \_| |_|
#Copy right  2016 PArsaALemi
#MIT license
#UNF-ROBOT BY PARSA ALEMI
