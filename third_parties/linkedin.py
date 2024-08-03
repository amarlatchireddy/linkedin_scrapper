import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()


class LinkedIn:

    def __init__(self):
        pass

    def Scrapper(self,name, linkedin_profile_url: str, mock: bool = False):
        """Scrapes the data from linkedin profile and stores the data"""
        with open("third_parties/"+"Amar Latchireddy"+".json", "r") as f:
            data = json.load(f)

        return data

    def data_cleaning(self,name):
        data = self.Scrapper(name,"2", "3")
        data = {
            k: v
            for k, v in data.items()
            if v not in ([], "", "", None)
            and k not in ["people_also_viewed", "certifications"]
        }
        if data.get("groups"):
            for group_dict in data.get("groups"):
                group_dict.pop("profile_pic_url")
                group_dict.pop("background_cover_image_url")

        return data


if __name__ == "__main__":
    res = LinkedIn().data_cleaning()
    print(res)
