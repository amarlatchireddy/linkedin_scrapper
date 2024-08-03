from typing import Tuple

from dotenv import load_dotenv
import os
from langchain.prompts.prompt import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from third_parties.linkedin import *
from agents.linkedin_lookup_agents import lookup
from third_parties.linkedin import *
from output_parser import summary_parser, Summary
print("hello")
print(os.environ["OPENAI_API_KEY"])
print("hi")
# information = """Konidala Pawan Kalyan[3] (born Konidala Kalyan Babu; 2 September 1971[2]) is an Indian politician, actor, action choreographer, martial artist and philanthropist who has been serving as the 10th deputy chief minister of Andhra Pradesh since June 2024. He is also the Minister of Panchayat Raj, Rural Development & Rural Water Supply; Environment, Forests, Science & Technology in the Government of Andhra Pradesh and an MLA representing Pitapuram constituency. He is the founder and president of the Jana Sena Party.
#
# As an actor, Kalyan works in Telugu cinema and is known for his unique style and mannerisms. He boasts a vast fanbase in the Telugu states, often described as "unfathomable," "fiercely loyal," and a "cult following."[7] He is among the highest-paid actors in Indian cinema[8] and has been featured in Forbes India's Celebrity 100 list multiple times since 2012.[13] He is the recipient of a Filmfare Award and a SIIMA Award among other accolades.
#
# Kalyan made his acting debut in the 1996 film Akkada Ammayi Ikkada Abbayi, a moderate success. Then, he had a streak of six consecutive hits, among which Tholi Prema (1998), Thammudu (1999), Badri (2000), and Kushi (2001) became back-to-back blockbusters. These films established Kalyan as a youth icon with a massive following distinct from his elder brother Chiranjeevi's fanbase.[4][6] In 2001, he became the first ever South Indian brand ambassador for Pepsi.[17] Kalyan later faced a slump, yet his popularity kept soaring despite the flops.[19] He made a comeback with Jalsa (2008), the highest-grossing Telugu film of that year, and continued with hits like Gabbar Singh (2012), Attarintiki Daredi (2013), Gopala Gopala (2015), and Bheemla Nayak (2022). He received the Filmfare Award for Best Actor for Gabbar Singh. Kushi and Attarintiki Daredi held the record of being the highest-grossing Telugu film of all time.
#
# Kalyan holds a black belt in Karate.[20] In 1997, he was awarded the title "Pawan" by the Isshin-ryū Karate Association after a public martial arts demonstration.[21] He trains in various martial arts which he depicts in his films regularly both as a performer and as an action choreographer. Kalyan is referred to as Power Star by his fans and in the media."""


class Scrapper:


    def __init__(self):
        pass
    def linkedin_scrape(self,name:str) -> Tuple[Summary,str]:

        linkedin_user_name = lookup(name)

        api_key = "KK5oiKHin6XzILl-ggcBig"
        headers = {"Authorization": "Bearer " + api_key}
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        params = {
            "url": linkedin_user_name
        }
        response = requests.get(api_endpoint, params=params, headers=headers)
        import json

        with open("third_parties/"+name+".json", "w") as f:
            json.dump(response.json(), f)
        # print(response.text)
        linkedin_data = LinkedIn().data_cleaning(name)
        # linkedin_data = LinkedIn().data_cleaning()
        summary_template = """ From the linkedin profile {information} json data information I want you to create:
          1. short summary
          2. two interesting facts about them
          
          \n {format_instructions}
          """
        prompt = PromptTemplate(input_variables=["information"], template=summary_template,
                                partial_variables={"format_instructions": summary_parser.get_format_instructions()})

        # llm = ChatOpenAI(temperature=0)
        llm = ChatOllama(model="llama3.1")
        # chain = prompt | llm | StrOutputParser()
        chain = prompt|llm|summary_parser
        res: Summary = chain.invoke(input={"information": linkedin_data})
        print(res)

        return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    res = Scrapper().linkedin_scrape("Amar Latchireddy")
    print(res)
