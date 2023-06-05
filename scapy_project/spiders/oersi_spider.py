import json
import os

import scrapy


class OersiSpider(scrapy.Spider):
    def __init__(self, num_search_results_per_request=10):
        self.name = 'oersi_spider'
        self.start_urls = ['https://oersi.org/resources/api/search/oer_data/_pit?keep_alive=1m&pretty']
        # The pit_id is used by oersi for session tracking
        self.pit_id = None
        self.size = num_search_results_per_request
        # To keep track of how many oersi Items have been processed
        self.num_results_processed = 0
        super().__init__()

    def start_requests(self):
        # Currently, the for loop only ever iterates over one URL
        for url in self.start_urls:
            # Maybe at this point self.num_results_processed should be reset, if there will ever be more than one
            # URLs (?)
            yield scrapy.Request(url=url, method="POST", headers={"accept": "application/json"},
                                 callback=self.save_pit)

    def save_pit(self, response):
        # The initial request without body returns a pit id
        # Also the following 3 lines are only for debugging, since we didnt know, if this method was hit
        # path = "E:\Projects"
        # with open(os.path.join(path, "test.txt"), "w") as f:
        #     f.write(response.text)
        self.pit_id = json.loads(response.text)["id"]

        yield response.follow(url=self.start_urls[0], body=self.construct_next_body(),
                              callback=self.parse_search_results)

    def parse_search_results(self, response):
        data = json.loads(response.text)
        self.num_results_processed += self.size

        # Iterate over individual items and process each one
        for item in data:
            # The two methods below need to be fully implemented, once the spider works properly
            self.save_as_json(item)
            self.store_in_entity_graph(item)

        # Points to this method, unless the processed number of Items exceeds the total number provided by oersi
        if self.num_results_processed < data["hits"]["total"]["value"]:
            yield response.follow(self.start_urls[0], body=self.construct_next_body(data["hits"]["hits"][-1]["sort"]),
                                  callback=self.parse_search_results)

    def construct_next_body(self, search_after=None):
        # Only changes to body during one use are from and search_after
        body = {
            "size": self.size,
            "from": self.num_results_processed,
            "pit": {
                "id": self.pit_id,
                "keep_alive": "1m"
            },
            "sort": [
                {
                    "id": "asc"
                }
            ],
            "track_total_hits": True
        }
        if search_after is not None:
            body["search_after"] = search_after

        return body

    def save_as_json(self, item):
        # Save as JSON locally
        json_filename = f"{item['id']}.json"
        with open(json_filename, 'w') as json_file:
            json.dump(item, json_file)

    def store_in_entity_graph(self, item):
        # Replace this method with your actual storage logic
        # Store the item in the entity graph
        print(f"Storing item with id: {item['id']} in entity graph")


# Only for debugging
if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess()
    process.crawl(OersiSpider)

    # spider = OersiSpider()
    # spider.save_pit(next(spider.start_requests()))
    #
    # print(spider.pit_id)

    # import requests
    # req = requests.post(url="https://oersi.org/resources/api/search/oer_data/_pit?keep_alive=1m&pretty",
    #               headers={"accept": "application/json"})
    # print(req.json())
