import requests
import time


def main():
    api_url = "https://zenquotes.io/api/quotes"

    for i in range(5):
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            if data:
                first_item = data[0]
                print(first_item['q'])
            else:
                print("No items in the response.")
        else:
            print("API request failed with status code:", response.status_code)

        time.sleep(7)


if __name__ == "__main__":
    main()
