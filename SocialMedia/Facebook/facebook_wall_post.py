import facebook


def main():
    cfg = {
        "page_id": "328045644353380",  # Step 1
        "access_token": "EAAZA1GWuwuqkBAIUZCINfcJayJuSEZB79mGHA4Fd0nId4BrEpkcxQgB0vgRFv2SCnqOiBcKDELecxCrk77OVDRrQFTDHLFj2kZA9YlrmckdFczmczb0OkavA9LJhZCAz8Q840w9tJZC6sIdKWROEvD3pZChdIzDDuYZD"
        # Step 3
    }
    api = get_api(cfg)
    msg = "Hello, wor213ld!"
    status = api.put_wall_post(msg)
    print(status)


def get_api(cfg):
    graph = facebook.GraphAPI(cfg['access_token'])
    resp = graph.get_object('me/accounts')
    page_access_token = None
    print(resp)
    for page in resp['data']:
        if page['id'] == cfg['page_id']:
            page_access_token = page['access_token']
    graph = facebook.GraphAPI(page_access_token)
    return graph


if __name__ == "__main__":
    main()
