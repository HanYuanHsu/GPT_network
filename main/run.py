import langchain
import openai
import os
import argparse

# just do experiments

api_key = os.getenv("OPENAI_API_KEY", "")
if api_key != "":
    openai.api_key = api_key
else:
    print("Warning: OPENAI_API_KEY is not set")

class Person:
    def __init__(self, personality:str, name:str=""):
        '''
        personality: a one-word adjective describing the personality of this person.
        name: the name of this person
        '''
        self.personality = personality
        self.name = name
        self.fondness = dict()

    def get_response(self, input:str):
        msg = [
          {"role": "system", "content": f"You are a {self.personality} person. Given an input from another person, provide a thoughtful response to it based on how you feel. Keep the response within 30 words."},
          {"role": "user", "content": input}
        ]
    
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=msg,
            temperature=0
        )
        return response.choices[0]['message']['content']
    
    def fondness_score(self, sentence:str) -> int:
        msg = [
          {"role": "system", "content": f"Recall that your personality is {self.personality}. Given the input sentence, give a score to that describes how much you like this sentence based on your personality. The score can be -1 (dislike), 0 (neutral), and 1 (like). Output the score as an integer ONLY."},
          {"role": "user", "content": sentence}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=msg,
            temperature=0
        )
        score_string = response.choices[0]['message']['content']
        if score_string not in {'-1', '0', '1'}:
            # modify this later
            raise RuntimeError()

        return int(score_string)

def test_fondness():
    person = Person(personality="optimistic")
    suicide_sentence = "I wanna kill myself."
    happy_sentence = "What a sunny day! Makes me feel happy."
    print(f"Fondness score of '{suicide_sentence}': {person.fondness_score(suicide_sentence)}")
    print(f"Fondness score of '{happy_sentence}': {person.fondness_score(happy_sentence)}")

def simulate_two_person_dialogue():
    '''
    For example, run
    python run.py --input "Nice weather today"
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='input your first question to person 1')
    args = parser.parse_args()
    person1 = Person()
    person2 = Person()
    response2 = args.input
    for i in range(10):
        response1 = person1.get_response(response2)
        print(f'Person 1: {response1}')
        response2 = person2.get_response(response1)
        print(f'Person 2: {response2}')


if __name__ == "__main__":
    test_fondness()


