from flask_table import Table, Col, LinkCol


class PostTable(Table):
    def sort_url(self, col_id, reverse=False):
        pass

    no = Col('#')
    classes = ['table', 'table-hover', 'table-striped']
    date_posted = Col('Date')
    title = Col('Title')
    content = Col('Content')
    image = Col('Image')
    link = LinkCol('View', 'Posters.view_post', url_kwargs=dict(url='link'))
    social_network = Col('Social Network')


class UsersTable(Table):
    def sort_url(self, col_id, reverse=False):
        pass

    classes = ['table', 'table-hover', 'table-striped']
    no = Col('#')
    email = Col('Email')
    name = Col('Name')
    no_of_posts = Col('Posts')
    role = Col('Role')
    link = LinkCol('Link', 'Administrator.admin_user_posts',
                   url_kwargs=dict(username='link'), attr='name')


class CredentialsTable(Table):
    def sort_url(self, col_id, reverse=False):
        pass

    classes = ['table', 'table-hover', 'table-striped']
    no = Col('#')

    facebook_access_token = Col("Facebook Token")
    twitter_access_token = Col("Twitter Token")
    twitter_access_secret = Col("Twitter Secret")
    instagram_email = Col("Instagram Email")
    instagram_password = Col("Instagram Password")
    linkedin_access_token = Col("LinkedIn Token")
    tumblr_access_token = Col("Tumblr Token")
    tumblr_access_secret = Col("Tumblr Secret")
