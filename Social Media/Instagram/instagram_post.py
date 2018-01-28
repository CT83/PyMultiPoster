def post_to_instagram():
    from InstagramAPI import InstagramAPI
    InstagramAPI = InstagramAPI("pyreserver.pseudtech@gmail.com", "cybertech83")
    InstagramAPI.login()  # login

    photo_path = 'temp.jpg'
    caption = "Sample photo"
    InstagramAPI.uploadPhoto(photo_path, caption=caption)
