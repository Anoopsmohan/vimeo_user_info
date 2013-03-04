from django.core.management.base import NoArgsCommand

from user_info.views import get_info


class Command(NoArgsCommand):
    help_text = ''' Fetch vimeo user info by using API's and store it in to database '''

    def handle_noargs(self, **options):
        get_info(5)
