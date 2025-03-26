from django.core.management.base import BaseCommand
from news.models import Post, Category, PostCategory

class Command(BaseCommand):
    help = 'Удаляет все новости из указанной категории после подтверждения'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str, help="Название категории, из которой нужно удалить все новости")

    def handle(self, *args, **options):
        category_name = options["category"].strip()

        try:
            category = Category.objects.get(name_category=category_name)
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка: категория "{category_name}" не найдена.'))
            return

        post_ids = PostCategory.objects.filter(category_through=category).values_list('post_through_id', flat=True)
        post_count = len(post_ids)

        if post_count == 0:
            self.stdout.write(self.style.WARNING(f'⚠️ Категория "{category_name}" не содержит новостей.'))
            return

        self.stdout.write(self.style.WARNING(
            f'Вы действительно хотите удалить {post_count} новостей из категории "{category_name}"? (yes/no)'
        ))
        answer = input().strip().lower()

        if answer == 'yes':
            Post.objects.filter(id__in=post_ids).delete()
            self.stdout.write(self.style.SUCCESS(
                f'✅ Успешно удалено {post_count} новостей из категории "{category_name}".'
            ))
        else:
            self.stdout.write(self.style.ERROR('❌ Операция отменена пользователем.'))
