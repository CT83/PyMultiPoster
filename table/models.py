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
