from SocialMedia.SocialMedia import SocialMedia
from blueprints.login.Login import get_current_user, load_user
from models.comon_queue.InstagramQueuer import InstagramQueuer


class Instagram(SocialMedia):

    def publish_update_image(self, message, image, db_session=None, user_email=None):
        add_post_to_queue_instagram(message, image,
                                    session=db_session,
                                    user_email=user_email)
        print("Added Post to Instagram Queue: Message:", message, " Image:", image)


def add_post_to_queue_instagram(content, image_url=None, session=None, user_email=None):
    if not session:
        raise NameError
    if user_email is None:
        user_email = load_user(get_current_user())

    import datetime
    time_indian = datetime.datetime.utcnow()
    time_indian = time_indian + datetime.timedelta(hours=5, minutes=30)
    queuer = InstagramQueuer(content=content, image_url=image_url,
                             date_queued=time_indian,
                             user_email=user_email)
    session.add(queuer)
    session.commit()
