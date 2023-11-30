import requests
from bs4 import BeautifulSoup
import json
import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


def get_main_data():
    start_datetime = datetime.datetime.now()
    url = "https://roscarservis.ru/catalog/legkovye/?set_filter=Y&sort%5Bprice%5D=asc&PAGEN_1=0"
    req = requests.get(url, headers=HEADERS)
    src = req.text
    json_data = req.json()
    main_list = []

    # with open("1.html", 'w', encoding='utf-8') as file:
    #     file.write(src)
    # with open('1.json', 'w', encoding='utf-8') as file:
    #     json.dump(json_data, file, indent=4, ensure_ascii=False)
    page_count = json_data["pagesCount"]
    # page_count = 1
    for page_num in range(int(page_count)):
        url = f"https://roscarservis.ru/catalog/legkovye/?set_filter=Y&sort%5Bprice%5D=asc&PAGEN_1={
            page_num+1}"
        req = requests.get(url=url, headers=HEADERS)
        data = req.json()
        items = data['items']
        for item in items:
            item_id = item['id']
            items_props = item['props']
            items_prop_list = []
            for item_props in items_props:
                items_prop_list.append(
                    {
                        item_props['name']: item_props['value'].strip()
                    }
                )
            item_price = item['price']
            item_amount_t = item['amount']
            item_season = item['season']
            item_name = item['name']
            item_img = f"https://roscarservis.ru{item['imgSrc']}"
            item_url = f"https://roscarservis.ru{item['url']}"
            stores_list = ['discountStores', 'externalStores', 'commonStores']
            stores_data = []
            for stores in stores_list:
                store = item[stores]
                if store == None or len(store) == 0:
                    continue
                else:
                    for st in store:
                        stores_data.append({
                            "store_name": st['STORE_NAME'],
                            "store_price": st['PRICE'],
                            "store_amount": st['AMOUNT']

                        })

            main_list.append({
                'id': item_id,
                'name': item_name,
                'url': item_url,
                'img': item_img,
                'price': item_price,
                'amount_title': item_amount_t,
                'season': item_season,
                'items_props': items_prop_list,
                'stores_info': stores_data,

            })
        print(f"Обработано {page_num + 1}/{page_count}")
    # diff_time =
    print(datetime.datetime.now() - start_datetime)

    # print(main_list)
    with open('main.json', 'w', encoding='utf-8') as file:
        json.dump(main_list, file, indent=4, ensure_ascii=False)
        # print(data)

    # print(page_count)


if __name__ == '__main__':
    get_main_data()
