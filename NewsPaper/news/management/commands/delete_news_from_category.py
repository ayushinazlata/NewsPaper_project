from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _ 
from news.models import Post, Category, PostCategory

class Command(BaseCommand):
    help = _('Removes all news from the specified category after confirmation')

    def add_arguments(self, parser):
        parser.add_argument('category', type=str, help=_("Name of the category from which all news should be removed"))

    def handle(self, *args, **options):
        category_name = options["category"].strip()

        try:
            category = Category.objects.get(name_category=category_name)
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(_('❌ Error: category "%s" not found.') % category_name))
            return

        post_ids = PostCategory.objects.filter(category_through=category).values_list('post_through_id', flat=True)
        post_count = len(post_ids)

        if post_count == 0:
            self.stdout.write(self.style.WARNING(_('⚠️ Category "%s" does not contain news.') % category_name))
            return

        self.stdout.write(self.style.WARNING(
            _('Do you really want to remove %d news items from the category? "%s"? (yes/no)') % (post_count, category_name)
        ))
        answer = input().strip().lower()

        if answer == 'yes':
            Post.objects.filter(id__in=post_ids).delete()
            self.stdout.write(self.style.SUCCESS(
                _('✅ Successfully removed %d news from category "%s".') % (post_count, category_name)
            ))
        else:
            self.stdout.write(self.style.ERROR(_('❌ Operation cancelled by user.')))
