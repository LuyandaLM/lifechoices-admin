from django.db import models
from django.conf import settings


class PublicChatRoom(models.Model):
    """
    the chatrooms that can be joined by the users
    """
    title = models.CharField(max_length=255, unique=True, blank=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, help_text="users who are connected to the chatroom")

    def __str__(self):
        return self.title

    def connect_user(self, user):
        """
        add the user to the list of users in the chat room
        :param user: the user trying to join the chatroom
        :return: if the user has been added to the chatroom or not
        """
        is_user_added = False
        if user not in self.users.all():
            self.users.add(user)
            self.save()
            is_user_added = True
        elif user in self.users.all():
            is_user_added = True
        return is_user_added

    def disconnect_user(self, user):
        is_user_removed = False
        if user in self.users.all():
            self.users.remove(user)
            self.save()
            is_user_removed = True
        return is_user_removed
