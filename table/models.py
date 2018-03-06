from flask_table import Table, Col, LinkCol


class PostTable(Table):
    def sort_url(self, col_id, reverse=False):
        pass

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
    email = Col('Email')
    name = Col('Name')
    role = Col('Role')
    link = LinkCol('Link', 'admin_user_posts',
                   url_kwargs=dict(username='link'), attr='name')
