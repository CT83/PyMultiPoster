import facebook


def main():
    graph = facebook.GraphAPI(
        access_token='EAABcDA1kKO8BAPv5QHb3F3erAjZCZB8PjTQ1uDyjo0fTFELyhpzjTTv4Acczoyh7YdBJr1HFcqecAkK9pfUAy6lCFhWZAJibhoUUdIZCnCBOOKWxlt4KRoA7va8RiJ0m25qsmCKnyy9lMYmgU1FjCuMAL8USRpzH2Y8uXnxjc8ZBEhM90EyZBIZBKxACpLKzrsAKjmJZCksQjwZDZD')
    # if version 2.8 show error use 2.6
    attachment = {
        'name': 'Link name',
        'link': 'https://www.example.com/',
        'caption': 'Check out this example',
        'description': 'This is a longer description of the attachment',
        # 'picture': 'https://www.example.com/thumbnail.jpg'
    }

    graph.put_wall_post(message='Check this out...', profile_id='326213351200598')
    # graph.put_wall_post(message='Check this out...', attachment=attachment, profile_id='your_page_id')


if __name__ == "__main__":
    main()
