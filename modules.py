from model_1 import ask, restart_sequence, start_sequence
from model_2 import S_model
from database import db_controller

#Sentimental model
S_model = S_model();
#Database controller
controller = db_controller.db_controller();

def get_response_with_sentiment(username ,message: str):
    print(S_model);
    #print(controller.get_sentiments(username));
    
    #get answer from model1
    response = ask(message, return_ChatLog(username));
    
    #get predicted sentiments from model2
    sentiment_array = (S_model.predict(message)).tolist();
    #get the sentiment
    print("Smodel:" , sentiment_array)
    sentiment = get_sentiment(sentiment_array, username);
    
    #The average of each sentiment used for personalization
    sentiments = get_sentiments_array(sentiment_array, username);
    
    append_ChatLog(message, response, username, sentiment, sentiment_array);
    
    response_and_sentiment = response + " (" + sentiment + ")";
    
    result = [response_and_sentiment, sentiments];
    
    return result;

#-------ChatLog Functions-------#

#function to append chatlog with new question and answer from model1 and sentiment from model2 and sentiment_array
def append_ChatLog(question, answer, username, sentiment, sentiment_array):
    anger= sentiment_array[0];
    sadness = sentiment_array[1];
    fear = sentiment_array[2];
    joy = sentiment_array[3];
    surprise = sentiment_array[4];
    love = sentiment_array[5];
    
    #format the new chatlog line
    new_ChatLog_Line = f'{restart_sequence} {question}{start_sequence}{answer}';
    
    controller.add_Chatlog(username, new_ChatLog_Line, sentiment, anger, sadness, fear, joy, surprise, love);
    
#function to return chatlog
def return_ChatLog(username):
    chatlog = controller.get_ChatLog(username);
    str1 = "";
    for i in range(0, len(chatlog)-1):
        str1 = str1.join(chatlog[i]+chatlog[i+1]);
    return str1
   
#-------Sentiment Functions-------#

def get_sentiment(current_sentiments_array, username):
    #get previous sentiments
    previous_sentiments_array = controller.get_sentiments_array(username);
    #get average of sentiments => new_sentiments_array
    prev_sent = controller.get_sentiment(username);
   
    #join the list of tuples into a list of strings
    previous_sentiments = [''.join(i) for i in prev_sent]

    print("Previous sentimentsss: ",previous_sentiments)
    if max(current_sentiments_array) > 0.65:
        current_sentiment = ['anger','sadness','fear','joy','surprise','love'][current_sentiments_array.index(max(current_sentiments_array))];
    else:
        current_sentiment = 'neutral';
    previous_sentiments.insert(0, current_sentiment);
    
    average_array = get_sentiments_weightedAverage(previous_sentiments_array, current_sentiments_array, previous_sentiments);
    if max(average_array) > 0.65:
        return ['anger','sadness','fear','joy','surprise','love'][average_array.index(max(average_array))];
    else:
        return 'neutral';
    
def get_sentiments_array(current_sentiments_array, username):
    #get previous sentiments
    previous_sentiments_array = controller.get_sentiments_array(username);
    #get average of sentiments => new_sentiments_array
    prev_sent = controller.get_sentiment(username);
   
    #join the list of tuples into a list of strings
    previous_sentiments = [''.join(i) for i in prev_sent]

    print("Previous sentimentsss: ",previous_sentiments)
    if max(current_sentiments_array) > 0.5:
        current_sentiment = ['anger','sadness','fear','joy','surprise','love'][current_sentiments_array.index(max(current_sentiments_array))];
    else:
        current_sentiment = 'neutral';
    previous_sentiments.insert(0, current_sentiment);
    
    average_array = get_sentiments_weightedAverage(previous_sentiments_array, current_sentiments_array, previous_sentiments);
    return average_array;
    

    
def get_sentiments_weightedAverage(previous_sentiments_array, current_sentiments_array, sentiments):
    standard_weight = 1;
    '''Rules:
    1- if a sentiment is counted 3 times, it's weight is increased 35%
    2- if a sentiment is counted 2 times, it's weight is increased 20%
    3- if a sentiment is counted 0 time, it's weight is decreased 10%
    4- if 'neutral' is counted 4 times, it's weight is increased 30%
    5- if 'neutral' is counted 3 times, it's weight is increased 20%
    6- if 'neutral' is counted 2 times, it's weight is increased 10%
    7- if the last sentiment is the same as the current sentiment, it's weight is increased 20%
    8- if it's the biggest sentiment, it's weight is increased 10%
    9- weights gets decreased each time by 10%
    '''
    
    print("Current:", current_sentiments_array);
    
    def filter_emotion_array(emotion_num):
        emotion_array = [current_sentiments_array[emotion_num]];
        for i in range(0, len(previous_sentiments_array)):
                emotion_array.append(previous_sentiments_array[i][emotion_num]);
        print("emotion_array:", emotion_array);
        return emotion_array;
    
    def caculate(sentiment_array, sentiment_count, neutral_count, previous_sentiment, current_sentiment):
        x1 = sentiment_array[0];
        x2 = sentiment_array[1];
        x3 = sentiment_array[2];
        x4 = sentiment_array[3];
        x5 = sentiment_array[4];
        
        w1 = standard_weight;
        
        #rules 1,2,3
        if sentiment_count == 3:
            w1 *= 1.1;
        elif sentiment_count == 2:
            w1 *= 1.05;
        elif sentiment_count == 0 :
            w1 *= 0.9;
        
        #rule 4,5,6
        print("neutral:",neutral_count)
        if neutral_count >= 4:
            w1 *= 1.4;
        elif neutral_count == 3:
            w1 *= 1.25;
        elif neutral_count == 2:
            w1 *= 1.1;
        
        #rule 7
        if previous_sentiment:
            w1 *= 1.2;
        
        #rule 8
        if current_sentiment:
            w1 *= 1.1;
            
        #rule 9
        w2 = w1*0.9;
        w3 = w2*0.9;
        w4 = w3*0.9;
        w5 = w4*0.9;
        
        average = (x1*w1 + x2*w2 + x3*w3 + x4*w4 + x5*w5)/(5);
        print("Average:", average);
        return average;
    
    #filter emotions each in an array
    anger_array = filter_emotion_array(0);
    sadness_array = filter_emotion_array(1);
    fear_array = filter_emotion_array(2);
    joy_array = filter_emotion_array(3);
    surprise_array = filter_emotion_array(4);
    love_array = filter_emotion_array(5);
    
    #count the amount of each emotion
    anger_count = sentiments.count('anger');
    sadness_count = sentiments.count('sadness');
    fear_count = sentiments.count('fear');
    joy_count = sentiments.count('joy');
    surprise_count = sentiments.count('surprise');
    love_count = sentiments.count('love');
    
    neutral_count = sentiments.count('neutral');
    print("joy:", joy_count)
    
    #get the average of each emotion
    anger_average = caculate(anger_array, anger_count, neutral_count, sentiments[0] == 'anger' and sentiments[1] == 'anger',  sentiments[0] == 'anger');
    sadness_average = caculate(sadness_array, sadness_count, neutral_count, sentiments[0] == 'sadness' and sentiments[1] == 'sadness',  sentiments[0] == 'sadness');
    fear_average = caculate(fear_array, fear_count, neutral_count, sentiments[0] == 'fear' and sentiments[1] == 'fear',  sentiments[0] == 'fear');
    joy_average = caculate(joy_array, joy_count, neutral_count, sentiments[0] == 'joy' and sentiments[1] == 'joy',  sentiments[0] == 'joy');
    surprise_average = caculate(surprise_array, surprise_count, neutral_count, sentiments[0] == 'surprise' and sentiments[1] == 'surprise',  sentiments[0] == 'surprise');
    love_average = caculate(love_array, love_count, neutral_count, sentiments[0] == 'love' and sentiments[1] == 'love',  sentiments[0] == 'love');
    
    #assemble the average array
    average_array = [anger_average, sadness_average, fear_average, joy_average, surprise_average, love_average];
    
    return average_array;
