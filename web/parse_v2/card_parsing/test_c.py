import requests
from common_info import read_common_info

def run():

    url = "https://zakupki.gov.ru/epz/contract/contractCard/common-info.html?reestrNumber=3352808136323000106"
    response = requests.get(url)

    response_text = read_common_info(response)
    print(response_text)

if __name__ == "__main__":
    run()
