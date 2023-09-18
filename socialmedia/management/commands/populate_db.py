from django.core.management import BaseCommand, CommandError
from django.utils import timezone
from chat.models import ChatMessage, ChatRoom
from friends.models import Friend
from post.models import Comment, Like, Post
from userprofile.models import UserProfile
from django.contrib.auth.models import User
import csv
import time

import warnings

warnings.filterwarnings("ignore", message="DateTimeField .* received a naive datetime .*")


# I wrote this code
class Command(BaseCommand):
    help = "Earse previous protein data and populate new data"

    # File paths for data files
    auth_user_csv = "./data_files/auth_user.csv"
    chat_chatmessage_csv = "./data_files/chat_chatmessage.csv"
    chat_chatroom_csv = "./data_files/chat_chatroom.csv"
    chat_chatroom_online_csv = "./data_files/chat_chatroom_online.csv"
    friends_friend_csv = "./data_files/friends_friend.csv"
    post_comment_csv = "./data_files/post_comment.csv"
    post_like_csv = "./data_files/post_like.csv"
    post_post_csv = "./data_files/post_post.csv"
    userprofile_userprofile_csv = "./data_files/userprofile_userprofile.csv"

    start_time = timezone.now()
    inter_time = start_time

    def handle(self, *args, **options):
        self.stdout.write("Erasing previous data")
        self.erase_previous_data()
        test = timezone.now() - self.inter_time
        self.stdout.write(
            self.style.SUCCESS(
                "Time (sec): " + str((timezone.now() - self.inter_time).total_seconds())
            )
        )
        self.inter_time = timezone.now()
        self.stdout.write("Populating with new data")
        self.populate_with_new_data()

    # Erase previous data from database
    def erase_previous_data(self):
        ChatMessage.objects.all().delete()
        ChatRoom.objects.all().delete()
        Friend.objects.all().delete()
        Comment.objects.all().delete()
        Like.objects.all().delete()
        Post.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.all().delete()

    # Populate database with new data
    def populate_with_new_data(self):
        self.stdout.write("Populating Auth user data")
        self.populate_auth_user()
        self.stdout.write(
            self.style.SUCCESS(
                "Time (sec): " + str((timezone.now() - self.inter_time).total_seconds())
            )
        )
        self.inter_time = timezone.now()

        self.stdout.write("Populating User profile data")
        self.populate_userprofile()
        self.stdout.write(
            self.style.SUCCESS(
                "Time (sec): " + str((timezone.now() - self.inter_time).total_seconds())
            )
        )
        self.inter_time = timezone.now()

        self.stdout.write("Populating Post data")
        self.populate_post()
        self.stdout.write(
            self.style.SUCCESS(
                "Time (sec): " + str((timezone.now() - self.inter_time).total_seconds())
            )
        )
        self.inter_time = timezone.now()

        self.stdout.write("Populating Comment data")
        self.populate_comment()
        self.stdout.write(
            self.style.SUCCESS(
                "Time (sec): " + str((timezone.now() - self.inter_time).total_seconds())
            )
        )
        self.inter_time = timezone.now()

        self.stdout.write("Populating Like data")
        self.populate_like()
        self.stdout.write(
            self.style.SUCCESS(
                "Time (sec): " + str((timezone.now() - self.inter_time).total_seconds())
            )
        )
        self.inter_time = timezone.now()

        self.stdout.write("Populating Friend data")
        self.populate_friend()
        self.stdout.write(
            self.style.SUCCESS(
                "Time (sec): " + str((timezone.now() - self.inter_time).total_seconds())
            )
        )
        self.inter_time = timezone.now()

        self.stdout.write("Populating Chatroom data")
        self.populate_chatroom()
        self.stdout.write(
            self.style.SUCCESS(
                "Time (sec): " + str((timezone.now() - self.inter_time).total_seconds())
            )
        )
        self.inter_time = timezone.now()

        self.stdout.write("Populating Chat message data")
        self.populate_chatmessage()
        self.stdout.write(
            self.style.SUCCESS(
                "Time (sec): " + str((timezone.now() - self.inter_time).total_seconds())
            )
        )
        self.inter_time = timezone.now()

        self.stdout.write("Populating Chatroom online data")
        self.populate_chatroom_online()
        self.stdout.write(
            self.style.SUCCESS(
                "Time (sec): " + str((timezone.now() - self.inter_time).total_seconds())
            )
        )
        self.inter_time = timezone.now()

        self.stdout.write("Database populated successfully!")
        self.inter_time = timezone.now()
        self.stdout.write(
            self.style.SUCCESS(
                "Total time (sec): "
                + str((timezone.now() - self.start_time).total_seconds())
            )
        )

    # Populate auth_user data
    def populate_auth_user(self):
        with open(self.auth_user_csv, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user, created = User.objects.get_or_create(
                    id=row["id"],
                    password=row["password"],
                    last_login=row["last_login"],
                    is_superuser=row["is_superuser"],
                    username=row["username"],
                    last_name=row["last_name"],
                    email=row["email"],
                    is_staff=row["is_staff"],
                    is_active=row["is_active"],
                    date_joined=row["date_joined"],
                    first_name=row["first_name"]
                )
                if created:
                    user.save()

    # Populate user profile data
    def populate_userprofile(self):
        with open(self.userprofile_userprofile_csv, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Use update_or_create to update or create UserProfile instances
                userprofile = UserProfile.objects.get(user_id=row["user_id"])
                userprofile.date_of_birth = row["date_of_birth"]
                userprofile.profile_image = row["profile_image"]
                userprofile.status_message = row["status_message"]
                userprofile.status_updated_at = row["status_updated_at"]
                userprofile.save()

    # Populate post data
    def populate_post(self):
        with open(self.post_post_csv, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Handle None value for genus_species
                post, created = Post.objects.get_or_create(
                    id=row["id"],
                    title=row["title"],
                    content=row["content"],
                    image=row["image"],
                    created_at=row["created_at"],
                    user_id=row["user_id"]
                )
                if created:
                    post.save()

    # Populate comment data
    def populate_comment(self):
        with open(self.post_comment_csv, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Handle None value for genus_species
                comment, created = Comment.objects.get_or_create(
                    id=row["id"],
                    content=row["content"],
                    created_at=row["created_at"],
                    user_id=row["user_id"],
                    post_id=row["post_id"]
                )
                if created:
                    comment.save()

    # Populate like data
    def populate_like(self):
        with open(self.post_like_csv, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Handle None value for genus_species
                like = Like.objects.update_or_create(
                    id=row["id"],
                    created_at=row["created_at"],
                    user_id=row["user_id"],
                    post_id=row["post_id"]
                )

    # Populate friend data
    def populate_friend(self):
        with open(self.friends_friend_csv, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if (row["accepted_at"] == ""):
                    row["accepted_at"] = None
                # Handle None value for genus_species
                friend = Friend.objects.update_or_create(
                    id=row["id"],
                    created_at=row["created_at"],
                    accepted_at=row["accepted_at"],
                    accepted=row["accepted"],
                    user_id=row["user_id"],
                    friend_id=row["friend_id"]
                )

    # Populate chatroom data
    def populate_chatroom(self):
        with open(self.chat_chatroom_csv, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Handle None value for genus_species
                chatroom = ChatRoom.objects.update_or_create(
                    id=row["id"],
                    name=row["name"],
                    created_at=row["created_at"]
                )

    # Populate chat message data
    def populate_chatmessage(self):
        with open(self.chat_chatmessage_csv, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Handle None value for genus_species
                chatmessage = ChatMessage.objects.update_or_create(
                    id=row["id"],
                    message=row["message"],
                    created_at=row["created_at"],
                    user_id=row["user_id"],
                    room_name_id=row["room_name_id"]
                )

    # Populate chatroom online data
    def populate_chatroom_online(self):
        return
    #     with open(self.chat_chatroom_online_csv, "r", encoding="utf-8") as csvfile:
    #         reader = csv.DictReader(csvfile)
    #         for row in reader:
    #             # Now update or create the ChatRoomOnline instance
    #             chatroom_online = ChatRoom.online.through().objects.get(
    #                 id=row["id"],
    #             )
    #             chatroom_online.chatroom_id = row["chatroom_id"]
    #             chatroom_online.user_id = row["user_id"]
    #             chatroom_online.save()

# end of code I wrote
