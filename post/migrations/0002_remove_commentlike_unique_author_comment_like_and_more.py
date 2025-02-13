# Generated by Django 5.1.5 on 2025-02-13 17:32

import django.core.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='commentlike',
            name='unique_author_comment_like',
        ),
        migrations.RemoveConstraint(
            model_name='postlike',
            name='unique_author_post_like',
        ),
        migrations.AlterField(
            model_name='post',
            name='caption',
            field=models.TextField(default=1, validators=[django.core.validators.MaxLengthValidator(2000)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='post_images', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])]),
        ),
        migrations.AddConstraint(
            model_name='commentlike',
            constraint=models.UniqueConstraint(fields=('author', 'comment'), name='CommentLikeUnique'),
        ),
        migrations.AddConstraint(
            model_name='postlike',
            constraint=models.UniqueConstraint(fields=('author', 'post'), name='postLikeUnique'),
        ),
        migrations.AlterModelTable(
            name='commentlike',
            table=None,
        ),
        migrations.AlterModelTable(
            name='postcomment',
            table=None,
        ),
        migrations.AlterModelTable(
            name='postlike',
            table=None,
        ),
    ]
