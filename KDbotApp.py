import random

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.clock import Clock
from pyswip import Prolog


class KDbotApp(App):
    global positivePrefix, positiveSuffix,negativePrefix,negativeSuffix
    positivePrefix = ['That\'s great!', 'Splendid!', 'Fantastic!', 'Sounds wonderful!']
    positiveSuffix = ['as well?', 'too?', 'also?']
    negativePrefix = ['ouh!', 'Its ok!', 'Hmm,', 'Aww, ']
    negativeSuffix = ['perferably?', 'perhaps?', 'hopefully?']

    def build(self):
        # Load the prolog module
        global prolog, item, stop, follow
        prolog = Prolog()
        prolog.consult("talkingtokid.pl")
        item = 'basketball'
        stop = False
        follow =False
        self.query(item, 'Hi Sweetie', '?')
    #generate the popout with the custom questions
    def callpopup(self, question):
        dlg = MessageBox(titleheader="Kids Day Chatbot", message=question, options={"yes": "printyes()", "no": "printno()"})
    #the routine runs when the yes button is selected when answering questions
    def printyes(self):
        global item, first, stop, follow
        if follow:
            prolog.asserta('like({})'.format(item)) # By adding the item into the knowledge base as it was liked  and asserting this to the prolog script
            follow = False
        else:
            followup = list(prolog.query('followup({}, Y)'.format(item)))

            # Retrieve a random followup question related to the item (Since some items can have multiple followups)
            followup_item = random.choice(followup)['Y']
            follow = True
            return self.askFollow(followup_item)
        # Adding the item to the prolog history of items
        prolog.assertz('history({})'.format(item))

        # Next, getting the next item that should be ask
        queryResult = list(prolog.query('ask(X, {})'.format(item)))
        if len(queryResult) != 0:
            # Get the first item in the query result.
            item = queryResult[0]['X']
        else:
            # If there are no result means there is no more possible items to ask
            stop = True  # to break the loop

        if stop==False:
            return self.query(item, random.choice(positivePrefix), random.choice(positiveSuffix)) #proceed to ask a related topic question if there is any left
        else:
            self.endbox()
    #the routine run when the no button is pressed when answering questions
    def printno(self):
        global item, first, stop, follow
        follow=False
        # Assume immediately the kid dislike the item if they didn't do it
        prolog.assertz('dislike({})'.format(item))
        # Adding the item to the prolog history of items
        prolog.assertz('history({})'.format(item))

        # Next, getting the next item that should be ask
        queryResult = list(prolog.query('ask(X, {})'.format(item)))
        if len(queryResult) != 0:
            # Get the first item in the query result.
            item = queryResult[0]['X']
        else:
            # If there are no result means there is no more possible items to ask
            stop = True  # to break the loop

        if stop == False:
            return self.query(item, random.choice(negativePrefix), random.choice(negativeSuffix)) #proceed to ask a random question
        else:
            self.endbox() #exit the application with a popup box with a message to close the convo and and exit button to acknowledge

    def query(self, item, begin, end):
        # generate popup GUI with the question with the apporiate prefix, item and sufix
        return self.callpopup(question='{} was there {} today {}'.format(begin, item, end))

    def askFollow(self, item):
        # generate followup popup GUI with the question with the adjective
        return self.callpopup(question='Did you {}?'.format(item.replace("_"," ")))
    def callexit(self):
        App.get_running_app().stop()
    def endbox(self):
        return Endbox(titleheader="Kids Day Chatbot",message="Gald to hear about your day at school!", options={"exit": "callexit()"})

# class of the structure of the GUI popup box for questions, with 2 button yes and no for answering the questions
class MessageBox(KDbotApp):
    def __init__(self, titleheader="Title", message="Message", options={"OK": "self.ok()", "NO": "self.no()"}):

        def popup_callback(instance):
            "callback for button press"
            # print('Popup returns:', instance.text)
            self.retvalue = instance.text
            self.popup.dismiss()

        self.retvalue = None
        self.options = options
        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text=message, font_size=20))
        b_list =  []
        buttonbox = BoxLayout(orientation='horizontal')
        for b in options:
            b_list.append(Button(text=b, size_hint=(1,.35), font_size=20))
            b_list[-1].bind(on_press=popup_callback)
            buttonbox.add_widget(b_list[-1])
        box.add_widget(buttonbox)
        self.popup = Popup(title=titleheader, content=box, size_hint=(None, None), size=(800, 400), auto_dismiss=False)
        self.popup.open()
        self.popup.bind(on_dismiss=self.OnClose)

    def OnClose(self, event):
        self.popup.unbind(on_dismiss=self.OnClose)
        self.popup.dismiss()
        if self.retvalue != None:
            command = "super(MessageBox, self)."+self.options[self.retvalue]
            # print "command", command
            exec (command)
# class of the structure of the GUI popup box for closing the convo, with a button to acknowledge the end of convo
class Endbox(KDbotApp):
    def __init__(self, titleheader="Title", message="Message", options={"OK": "self.ok()"}):

        def popup_callback(instance):
            "callback for button press"
            # print('Popup returns:', instance.text)
            self.retvalue = instance.text
            self.popup.dismiss()

        self.retvalue = None
        self.options = options
        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text=message, font_size=20))
        b_list =  []
        buttonbox = BoxLayout(orientation='horizontal')
        for b in options:
            b_list.append(Button(text=b, size_hint=(1,.35), font_size=20))
            b_list[-1].bind(on_press=popup_callback)
            buttonbox.add_widget(b_list[-1])
        box.add_widget(buttonbox)
        self.popup = Popup(title=titleheader, content=box, size_hint=(None, None), size=(800, 400), auto_dismiss=False)
        self.popup.open()
        self.popup.bind(on_dismiss=self.OnClose)

    def OnClose(self, event):
        self.popup.unbind(on_dismiss=self.OnClose)
        self.popup.dismiss()
        if self.retvalue != None:
            command = "super(MessageBox, self)."+self.options[self.retvalue]
            # print "command", command
            App.get_running_app().stop()
if __name__ == '__main__':
    KDbotApp().run()
