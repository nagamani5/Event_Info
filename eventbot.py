from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from watson_developer_cloud import ConversationV1
import json
import sqlite3

context = None
print("Context1:",context)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    print('Received /start command')
    update.message.reply_text('Hi!')


def help(bot, update):
    print('Received /help command')
    update.message.reply_text('Help!')


def message(bot, update):
    print('Received an update')
    global context

    conversation = ConversationV1(username='4509b52a-a56b-4862-88f0-dbad17991077',  # TODO
                                  password='3ybDKqyCdglf',  # TODO
                                  version='2018-02-16')

    # get response from watson
    response = conversation.message(
        workspace_id='dc71d785-d2df-41a5-b448-5ffa8122deec',  # TODO
        input={'text': update.message.text},
        context=context)
    print(json.dumps(response, indent=2))
    context = response['context']
    print("Context2:",context)

#Register

    if (("Teamname" in context.keys()) and ("person" in context.keys()) and ("person_2" in context.keys()) and ("evenreg" in context.keys())):
        conn=sqlite3.connect("event.db")
        cur=conn.cursor()
        var1=context['person']
        var2=context['person_2']
        var3=context['evenreg']
        var4=context['Teamname']
        print(var1,var2,var3,var4)
        cur.execute("INSERT INTO register VALUES(?,?,?,?)",(var1,var2,var3,var4))
        conn.commit()
        print(var1,var2,var3,var4)
        conn.close()
        del context['person']
        del context['person_2']
        del context['evenreg']
        del context['Teamname']

#Deregister

    if (("First_name" in context.keys()) and ("Last_name" in context.keys()) and ("event_reg" in context.keys())):
        conn=sqlite3.connect("event.db")
        cur=conn.cursor()
        var1=context['First_name']
        var2=context['Last_name']
        var3=context['event_reg']
        #var4=context['Teamname']
        print(var1,var2,var3)
        cur.execute("DELETE FROM register WHERE fname=? and lname=? and event=?",(var1,var2,var3))
        update.message.reply_text("Done...")
        conn.commit()
        #print(var1,var2,var3,var4)
        conn.close()
        del context['First_name']
        del context['Last_name']
        del context['event_reg']
        
        #num=cur.rowcount()
        #print("ROWS",num)

#Check1

    if (("Firs_name" in context.keys()) and ("Las_name" in context.keys())):
        conn=sqlite3.connect("event.db")
        cur=conn.cursor()
        var1=context['Firs_name']
        var2=context['Las_name']
        #str1=""
        count=0
        list1=list()
        print(var1,var2)
        cur.execute("SELECT event FROM register WHERE fname=? and lname=?",(var1,var2))
        rows=cur.fetchall()
        for row in rows:
            #print(row)
            count+=1
            list2=list(row)
            list1.extend(list2)
            #print(list1)
        print(list1)
        if (count>0):
            msg="You have registered in "
            str1=",".join(list1)
            res=msg+str1
            print(res)
            update.message.reply_text(res)
        else:
            res="You have not registered for any event...!!!"
            update.message.reply_text(res)
            #response=response+" "+res
        #print(response)
        #update.message.reply_text(res)
            #res.join(row)
            #response+=res
        #update.message.reply_text(response)
        conn.commit()
        conn.close()
        del context['Firs_name']
        del context['Las_name']

#check2

    if (("F_name" in context.keys()) and ("L_name" in context.keys()) and ("evenregi" in context.keys())):
        conn=sqlite3.connect("event.db")
        cur=conn.cursor()
        var1=context['F_name']
        var2=context['L_name']
        var3=context['evenregi']
        count=0
        cur.execute("SELECT event FROM register WHERE fname=? and lname=? and event=?",(var1,var2,var3))
        rows=cur.fetchall()
        for row in rows:
            count+=1
        if (count>0):
            res="Yes...you have registered"
            update.message.reply_text(res)
        else:
            res="You have not registered...!!!"
            update.message.reply_text(res)
        conn.commit()
        conn.close()
        del context['F_name']
        del context['L_name']
        del context['evenregi']
	    

    # build response
    resp = ''
    for text in response['output']['text']:
        resp += text
   
    update.message.reply_text(resp)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater('516216265:AAG4iAArOrNDXj8PAfy1rqXduTuBHC5zPYY')  # TODO

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, message))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
