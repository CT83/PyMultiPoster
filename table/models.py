from flask_table import Table, Col


class PostTable(Table):
    def sort_url(self, col_id, reverse=False):
        pass

    classes = ['table', 'table-bordered', 'table-hover', 'table-striped']

    # id = Col('ID')
    date_posted = Col('Date')
    title = Col('Title')
    content = Col('Content')
    image = Col('Image')
    social_network = Col('Social Network')
