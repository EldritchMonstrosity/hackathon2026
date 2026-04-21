import os
from django.core.management.base import BaseCommand
from django.conf import settings
from dashboard.models import Post
from django.core.files import File
from pathlib import Path

class Command(BaseCommand):
    help = "Import posts from post_data folder"

    def handle(self, *args, **kwargs):
        base_path = Path(settings.BASE_DIR).parent / "post_data"

        for folder_name in os.listdir(base_path):
            folder_path = os.path.join(base_path, folder_name)

            if not os.path.isdir(folder_path):
                continue

            caption_file = None
            image_file = None

            for file in os.listdir(folder_path):
                if file.endswith(".txt"):
                    caption_file = os.path.join(folder_path, file)
                elif file.lower().endswith((".png", ".jpg", ".jpeg")):
                    image_file = os.path.join(folder_path, file)

            if not caption_file or not image_file:
                self.stdout.write(self.style.WARNING(f"Skipping {folder_name} (missing files)"))
                continue

            # Read caption
            with open(caption_file, "r", encoding="utf-8") as f:
                full_read = f.read().strip()
                first_cut = full_read[:full_read.find("#")]
                second_cut = first_cut.strip()
                caption = second_cut

                #setting up eval dict
                eval_dict = {"politics": 0,
                      "art": 0,
                      "meme": 0,
                      "pop_culture": 0,
                      "science": 0,
                      "sports": 0,

                      "christian": 0,
                      "islam": 0,
                      "hinduism": 0,

                      }
                for keY in eval_dict:
                    if keY == "politics":
                        if "#rightwing" in full_read:
                            eval_dict["politics"]-=1
                        elif "#leftwing" in full_read:
                            eval_dict["politics"]+=1
                    else:
                        if "#"+keY in full_read:
                            eval_dict[keY]+=1


            # Save Post
            with open(image_file, "rb") as img:
                if Post.objects.filter(post_caption=caption).exists():
                    continue
                else:
                    post = Post(post_caption=caption, post_eval_dict = eval_dict)
                    post.post_image.save(os.path.basename(image_file), File(img), save=True)

            self.stdout.write(self.style.SUCCESS(f"Imported {folder_name}"))