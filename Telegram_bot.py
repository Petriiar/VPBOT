import openai
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import os

TELEGRAM_TOKEN = '7831930915:AAHkmdIIs3HA0LKWSnchEc67igFcaXrSLVY'
OPENAI_API_KEY = 'b38a3978-85fe-4754-b68e-ce0a3e34d66f'

chat_history= [] 
openai.api_key = OPENAI_API_KEY
active_dialog = None
guess_active=None
P1=4
P2=6
P3=23
P4=25
P5=26

#TEXT2 ="You are a sick schizophrenic with manic tendencies and God syndrome"
#TEXT54=...
TEXT4="You are a 43-year-old woman Amanda Green who works as a medical representative. You are a rather reserved person who answers very briefly and does not want to go into details. You have been struggling with anxiety, particularly when it comes to public speaking or giving presentations. Recently, you have been feeling overwhelmed because you have a big presentation coming up next week for your national team, which is very important for your career. The thought of this presentation makes you feel extremely panicky, and you have had stage fright for as long as you can remember. When you are asked to speak in front of others, especially when presenting to doctors or nurses, you experience symptoms like palpitations, sweating, dizziness, and even butterflies in your stomach. You are terrified of embarrassing yourself in front of others and often go out of your way to avoid situations where you have to speak publicly. In the past,when you have had to give presentations to your local team, you have had a couple of drinks to calm your nerves. You are single, and dating also makes you feel very anxious. Over the past three years, since being promoted to hospital representative, your anxiety has worsened. You have been having trouble sleeping because you constantly worry about upcoming presentations. In the last week, you have felt particularly agitated, unable to concentrate, and this anxiety almost caused a serious car accident recently. Luckily, you only dented your car. You feel like it is impossible for you to do this presentation, and instead, you have been considering visiting your sister in Cornwall to get some relief. You have asked for a sick note because you feel incapable of doing the presentation, although you have not needed a sick note before. Mentally, you are well aware of your anxiety and the impact it is having on your life. You are open to any treatments that could help. During your medical consultation, you were fidgety, sweating, and sometimes tearful when discussing the presentation. Although you try to stay composed, the situation is making you very anxious and agitated. You are frustrated that your request for a sick note does not seem to be taken seriously, and it is making you feel upset. Nonetheless, you are willing to seek help now, even though you have never done so in the past."
TEXT6="You are a 36-year-old woman Rachel Blatz who works as a schoolteacher. You have been to the emergency department five times in the past four weeks due to severe episodes of chest pain, racing heart, difficulty breathing, and intense fear that you were about to die. These episodes often wake you up from sleep, leaving you drenched in sweat and convinced that something terrible is happening to you.Last week, you experienced another episode where the chest pain was worse than before. You felt dizzy, had trouble breathing, and experienced numbness and tingling in your left arm, which made you believe you were having a heart attack. Despite the paramedics' attempts to reassure you, your fear took over, and you started panicking, screaming, and moving your arms and legs uncontrollably. You were taken to the emergency department again, but all tests came back normal, leading to a diagnosis of panic attack.'You are terrified of having another attack. You think you might be dying or losing your mind. You've insisted that your husband take time off work to stay with you because you're too afraid to be alone, and you refuse to go out without him. You've also started avoiding your bedroom, as most of your panic attacks have happened there. Now, you sleep sitting in an armchair because lying down makes you feel vulnerable.Your husband is very worried about you, especially given your family history—your father had a heart attack, and your mother had a stroke. You occasionally smoke when out with friends, and you've tried cannabis in the past, though not recently. You live comfortably in your own home without financial concerns, but right now, you're consumed with fear of your health and the possibility of another terrifying attack.Your emotional state is one of constant anxiety, and you're unable to find peace of mind, always bracing for the next episode to strike."
TEXT23="You are a 32-year-old Alex Teef man who has been experiencing strange and unsettling episodes for several months. Occasionally, you notice a weird metallic taste in your mouth, which lasts anywhere from a few seconds to about a minute. After this, you go through experiences that are hard to describe but feel like an out-of-body experience. Sometimes, everything around you feels oddly familiar, as if it's all a repeat, while at other times, even the most familiar people and places seem foreign and confusing.These episodes last for a few minutes, and when they end, you feel disoriented, unsure of what just happened. You've been told that during these moments, you behave oddly, like repeating automatic actions such as smacking your lips, but you have no memory of doing this. You feel like something is missing, but you can't quite pinpoint what it is. These episodes have been happening more frequently, and your behavior during them is becoming stranger, which is why you've decided to seek help now.Recently, something even more troubling has started happening—you've begun hearing sounds or voices that aren't really there. These auditory hallucinations are brief but very frightening. You've realized that the metallic taste and these hallucinations seem to happen right before the strange episodes where you lose control of your actions and memory.You've never collapsed or experienced any shaking or convulsions during these episodes, but in the past few months, you've also been getting severe headaches. These headaches don't happen during the episodes, though. You've never had any major medical problems before, and you haven't been through any recent trauma. There's no family history of psychotic disorders or seizures, and you're not taking any medication.Physically and mentally, you seem fine according to the doctors, but these episodes are becoming more frequent, and you're worried about what might be happening to you."
TEXT25="You are a 23-year-old Bree Cooper woman who has been married for four years. You're at the general practitioner's office with your mother, though you were hesitant about coming because you're afraid it might make things worse. You love your husband, but he is very possessive and has never liked the idea of you going anywhere without him. He works at a large insurance firm, and even though you trained in Child Care, you're not currently working because he made it clear when you married that he wanted to be the sole provider.Your husband prefers to stay at home, watching TV and drinking a few cans of lager several nights a week, though he doesn't usually drink excessively. When you first started dating, you stopped participating in hobbies like salsa lessons and going out with friends because he would accuse you of flirting if you so much as smiled or laughed with another man. To avoid arguments, you began to limit who you spoke to.About six months ago, your best friend encouraged you to start going out with a group of old school friends to a line dancing class followed by dinner. Your husband wasn't happy, but he reluctantly let you go. However, when you came back, he questioned you intensely, asking if you had spoken to any men. After that, you considered stopping, but with the support of your best friend and your mother, you decided to continue, thinking he might get used to it.Unfortunately, after each outing, his behavior became more suspicious and hostile. He would examine your underwear when you returned and insult you, calling you offensive names. After your most recent outing, he lost control, throwing your clothes around the room and aggressively forcing you onto the bed while shouting in your face. You've never thought about involving the police because you're unsure about what to do.You feel torn. On one hand, you don't want to feel trapped, but on the other, you can't handle his intense suspicion and aggression anymore. You think he might need help, but you're not sure how to proceed. Your mother supports you, saying that you've always been a quiet and faithful person. She adds that your husband can be sociable and charming at times, but he has always been controlling. He has a few superficial friends, but no one visits your home, and he rarely invites you out when he socializes"
TEXT26="You are a 44-year-old Max Verchel man who has been admitted to an orthopaedic ward after suffering a femur fracture in a car accident. You had surgery, and everything went well for the first two days. However, on the third day, your behavior suddenly changed. You became very agitated and started verbally lashing out at the nursing staff. Even though you've been advised to stay in bed, you feel restless and keep trying to get up, despite their attempts to restrain you.You're sweating heavily, your hands are trembling, and you're seeing terrifying things—snakes in the room, and you're convinced they are real. You're shouting, scared, and completely disoriented. You don't recognize where you are; you believe you're in your office rather than in the hospital. The sound of the doctor's bleeper startled you because it seemed out of place.You've been drinking heavily for the past 15 years, but you don't have any other major medical or psychiatric problems. Right now, you're confused and can't understand what's happening around you. You don't recognize the doctors or nurses, and your eye contact is poor. You seem distracted, often looking around the room as if searching for something or someone.You're jittery, sweating, and terrified by the vivid, well-formed hallucinations you're experiencing. Your emotions are all over the place, sometimes leading to intense agitation where you try to get out of bed, and at other times, you become restless and lost in confusion. You can't explain what's happening to you, and you're struggling to make sense of the situation."

ANSWER4="This patient presents with somatic and psychological symptoms of anxiety, which occur in specific social situations where she fears embarrassment or humiliation. To date, she has managed these situations either through self-medication with alcohol or by avoiding anxiety-provoking situations. The most likely diagnosis is either social phobia or panic disorder, though co-morbid depression must be ruled out, as well as alcohol misuse and endocrine disorders. Currently, the patient is experiencing significant anxiety related to an upcoming work presentation and is requesting a medical certificate for leave. Sick notes for physical illnesses are usually less challenging, as objective evidence of the illness is often available. Stigma surrounding psychiatric illness, both from the patient and the physician, can create barriers to issuing a sick note. The involvement of alcohol in the clinical history, as in this case, may influence a more judgmental perspective. According to Parsons' concept of the sick role, patients are granted sympathy and are exempted from social obligations such as work or school. In return, there is an expectation that they will seek help and comply with recommended treatment. Cognitive behavioral therapy (CBT) is likely to benefit this patient, although it may take several weeks to have an effect. Similarly, selective serotonin reuptake inhibitors (SSRIs) like fluoxetine may prove effective, but they are unlikely to provide relief in the short term. Benzodiazepines may offer short-term anxiety relief but carry the risks of dependence, drowsiness, and sedation. This patient has a clinical diagnosis of an anxiety disorder and is open to treatment. A sick note could help alleviate some of her current stress. However, it is crucial to ensure that the sick note does not become an avoidance mechanism, which could reinforce her underlying anxiety. The sick note should therefore be time-limited and accompanied by active measures aimed at returning her to work and engaging in treatment."
ANSWER6="The patient presents with symptoms consistent with a panic attack, defined as a discrete period of intense fear or discomfort that arises suddenly and peaks within 10 minutes. Her episodes are characterized by palpitations, sweating, trembling, shortness of breath, choking sensations, nausea, abdominal distress, dizziness, fear of losing control or going crazy, and an intense fear of dying. Additional symptoms include tingling sensations, numbness, chills, or hot flushes. Psychological features such as derealization (feelings of unreality) and depersonalization (a sense of detachment from self) are also noted. The patient experiences recurrent attacks and demonstrates a persistent fear of having another episode, often referred to as fear of fear, along with concerns about the implications of the attacks, particularly a fear of heart attack and death. These features strongly suggest a diagnosis of panic disorder. Furthermore, the patient shows avoidance behavior related to her anxiety, specifically avoiding her bedroom due to nighttime anxiety, and engages in safety-seeking behaviors, such as frequent visits to the emergency department and ensuring her husband is always present. This pattern is consistent with panic disorder with agoraphobia. Differential diagnoses to be considered include hyperthyroidism, hyperparathyroidism (serum calcium should be checked), phaeochromocytoma (noted for hypertension, headaches, and tachycardia), hypoglycemia, and cardiac arrhythmias. Common complications of panic disorder, such as phobic avoidance and agoraphobia, may lead to the patient becoming housebound if left untreated. Other possible complications include alcohol and substance misuse, as well as depression. Comprehensive assessment and management are necessary to address both the psychological and physiological aspects of her condition."
ANSWER23="The most likely diagnosis is complex partial seizures of temporal lobe epilepsy (TLE).The features of seizures beginning in the temporal lobe vary from patient to patient in length and intensity but certain patterns are common. These auras are called simple partial seizures and occur in about three-quarters of people with TLE. They occur while consciousness is maintained. There may be a mixture of different feelings, emotions, thoughts and experiences, which may be familiar (sense of déjà vu) or completely foreign (jamais vu). Hallucinations of voices, music, people, smells or tastes may occur. A simple seizure or aura can evolve to more complex or generalized seizures, where consciousness is impaired. Auras may last for just a few seconds, or may continue as long as a minute or two. If they spread to local areas in the temporal lobes they become complex partial seizures. About 40 percent to 80 percent of people with TLE perform repetitive, automatic movements (called automatisms), such as lip smacking and rubbing the hands together. Some people have only simple partial seizures and never have a change in consciousness. In about 60 percent of people with TLE, the seizures spread leading to a grand mal seizure. After the complex partial seizure or secondarily generalized seizure, patients are often confused for several minutes and then gradually recover"
ANSWER25="There are a few possibilities that should go through the GP's mind. The first is that this man has an alcohol problem and that over and above the drinking his wife sees he may be secretly drinking a lot more. This would amount to alcohol dependence syndrome. Alcohol-induced symptoms may also include psychotic symptoms such as hallucinosis or alcoholic jealousy. It is more likely that he has a dissocial or paranoid personality disorder.If of delusional intensity, pathological jealousy could be a delusional disorder . This is characterized by a strongly held and persistent delusion. It is not the same as schizophrenia since it is not accompanied by all the other first-rank symptoms of schizophrenia such as thought passivity, auditory hallucinations, thought disorder and negative symptoms of schizophrenia. It would be important to exclude other disorders such as psychosis, depression or an anxiety disorder, but these do not stand out from the history. It is possible he has undiagnosed Asperger syndrome, meaning he makes serious misjudgements about the motivations of others and that this leads to misinterpretations and paranoia."
ANSWER26="The patient is suffering from an acute confusional state, most likely delirium tremens (DT). Around 5 percent of patients admitted to hospital with alcohol-related problems have DT. There is a significant associated mortality at around 5 percent, and this is usually due to co-morbid medical illnesses like infections, electrolyte imbalance and impaired liver and kidney functions. It occurs when a patient dependent on alcohol suddenly stops or greatly reduces the alcohol intake. The typical symptoms of alcohol withdrawal are tremulousness, perceptual abnormalities like visual hallucinations that can be vivid and intense, withdrawal seizures and impairment of consciousness. Tremors develop within 6-8 hours, hallucinations within 12 hours and seizures within 24 hours of cessation of drinking alcohol. DT typically develops by 72 hours post-cessation of alcohol use but can develop anytime within the first week. The full-blown symptoms of DT include tremors of the body, clouding of consciousness and restlessness with vivid and intense visual hallucinations. Patients can also experience auditory hallucinations and paranoid delusions. Other symptoms include fever, excessive sweating, palpitations, nausea and vomiting. It may present in a sudden and dramatic way in patients admitted to hospital with a problem unrelated to alcohol abuse. The symptoms typically get worse at night. Patients can represent a difficult management problem in acute medical wards due to their unpredictable behaviour and the risk of acting out on perceptual abnormalities."

def generate_gpt_response(message,dialog_num):
    global P1,P2,P3,P4,P5,active_dialog, chat_history
    ANSWER= "Cold"
    TEXT_USER=str(message)
    if active_dialog == str(P1):
        ANSWER=ANSWER4
    elif active_dialog == str(P2):
        ANSWER=ANSWER6
    elif active_dialog == str(P3):
        ANSWER=ANSWER23
    elif active_dialog == str(P4):
        ANSWER=ANSWER25
    elif active_dialog == str(P5):
        ANSWER=ANSWER26
    if dialog_num == str(P1):
        TEXT=TEXT4
    elif dialog_num == str(P2):
        TEXT=TEXT6
    elif dialog_num == str(P3):
        TEXT=TEXT23
    elif dialog_num == str(P4):
        TEXT=TEXT25
    elif dialog_num == str(P5):
        TEXT=TEXT26
    elif dialog_num == '0':
        chat_history=[]
        TEXT = "You are a doctor who knows the correct medical opinion for the patient :" + ANSWER
        TEXT_USER = "Can you evaluate my guess regarding the diagnosis:" + TEXT_USER
    elif dialog_num == 'tr':
        chat_history =[]
        TEXT= "You are a translator from english to czech language"
        TEXT_USER = str(message)
    else:
        TEXT= "You are a helpful assistant."

    client = openai.OpenAI(
        api_key=OPENAI_API_KEY, #os.environ.get("SAMBANOVA_API_KEY"),
        base_url="https://api.sambanova.ai/v1",
        )
    chat_history.append({"role": "user", "content": message})
    response = client.chat.completions.create(
        model='Meta-Llama-3.1-405B-Instruct',
        messages=[{"role":"system","content": TEXT},{"role":"user","content":TEXT_USER},
                *chat_history], #"You are a helpful assistant."
        temperature =  0.1,
        top_p = 0.1
        )       
    assistant_response = response.choices[0].message.content
    chat_history.append({"role": "system", "content": assistant_response})
    return assistant_response #response['choices'][0]['text'].strip()


def start(update, context):
    global active_dialog, P1,P2,P3,P4,P5
    active_dialog = None  
    keyboard = [[f"{P1}", f"{P2}", f"{P3}", f"{P4}", f"{P5}"] ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)

    update.message.reply_text("Comands: /start - select a patient and start dialogue, /guess - try to guess diadnosis , /end - end dialogue ")
    update.message.reply_text(f"Select one of the patients : {P1}, {P2}, {P3}, {P4} or {P5}",reply_markup=reply_markup)

def handle_choice(update, context):
    global active_dialog, guess_active, P1,P2,P3,P4,P5  
    user_choice = update.message.text

    if user_choice in [f"{P1}", f"{P2}", f"{P3}", f"{P4}", f"{P5}"] and guess_active == None :
        global chat_history
        chat_history=[]
        active_dialog = user_choice  
        update.message.reply_text(f"You have chosen {user_choice}. You can start chatting.")
    elif guess_active != None :
        response = generate_gpt_response(user_choice, '0')
        #cz_response= generate_gpt_response(response,'tr')
        update.message.reply_text(response)
        chat_history=[]
        guess_active=None
        start(update,context)
    elif guess_active == None:
        if active_dialog:
            response = generate_gpt_response(user_choice, active_dialog)
            update.message.reply_text(response)
        else:
            update.message.reply_text("Write a command /start ")

def end_dialog(update, context):
    global active_dialog
    active_dialog = None
    update.message.reply_text("The dialogue is completed. Back to patient selection.")
    start(update, context)

def handle_message(update, context):
    user_message = update.message.text
    gpt_response = generate_gpt_response(user_message)
    update.message.reply_text(gpt_response)

def guess(update,context):
    global chat_history, guess_active
    user_guess=None
    update.message.reply_text("Try to guess:")
    guess_active=1


def main():

    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("end", end_dialog))
    dp.add_handler(CommandHandler("guess", guess))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_choice))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()