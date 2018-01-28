import facebook


def main():
    graph = facebook.GraphAPI(access_token='your_user_access_token')
    # if version 2.8 show error use 2.6
    attachment = {
        'name': 'Link name',
        'link': 'https://www.example.com/',
        'caption': 'Check out this example',
        'description': 'This is a longer description of the attachment',
        'picture': 'https://www.example.com/thumbnail.jpg'
    }

    graph.put_wall_post(message='Check this out...', attachment=attachment, profile_id='your_page_id')


if __name__ == "__main__":
    main()
