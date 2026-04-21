from django.db.models import *

class Post(Model):
    post_caption = CharField(max_length = 255)
    post_image = ImageField(upload_to = "posts/")
    post_creation_time = DateTimeField(auto_now_add = True)
    post_eval_dict = JSONField(default=dict)

    def __str__(self):
        return self.post_caption
# Create your models here.
