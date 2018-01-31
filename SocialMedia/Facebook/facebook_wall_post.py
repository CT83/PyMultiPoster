import facebook


def main():
    cfg = {
        "page_id": "837037163169573",  # Step 1
        "access_token": "EAACTuZBakrZBEBAO2HapKkjpdWwk5goFeqk9OY7sA4n5ZBUX8u5FmQf06oLISOyd7YZAZCWMSRfk3VhUFOtSZCfMwqCLcIEDrKkJNUDGMjPZCzCwv2scjAaGYftLnIBVlhkB4Ggd91eviokaoxeNqh3y9tiPmUayBY3jowXqFUQfVRUKw8yZC1ZA9smpdJmt9jZBLKZATLGhQKitFAbz3stLJIUZCtc1kZBthLPQZD"
        # Step 3
    }
    api = get_api(cfg)
    msg = "Hello, wor213ld!"
    status = api.put_wall_post(msg)


def get_api(cfg):
    graph = facebook.GraphAPI(cfg['access_token'])
    resp = graph.get_object('me/accounts')
    page_access_token = None
    for page in resp['data']:
        if page['id'] == cfg['page_id']:
            page_access_token = page['access_token']
    graph = facebook.GraphAPI(page_access_token)
    return graph


if __name__ == "__main__":
    main()
