class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, related_name="favorite", on_delete=models.CASCADE)

class FavoriteItem(models.Model):
    Favorite = models.ForeignKey(Favorite, related_name="items", on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)