from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.signing import Signer
from django.db.models import Sum,F,FloatField,Q
import math
from bs4 import BeautifulSoup
from django_google_maps import fields as map_fields
signer = Signer()
# Create your models here.
MALE = "MALE"
FEMALE = "FEMALE"
GENDER = (
    (MALE, MALE),
    (FEMALE, FEMALE),
)


REACTION = (
    ("LIKE", "LIKE"),
    ("HEART", "HEART"),
    ("WOW", "WOW"),
    ("SAD", "SAD"),
    ("ANGRY", "ANGRY"),
)


class User(AbstractUser):
    is_member = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=15, choices=GENDER, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=15, null=True, blank=True)

    def get_full_name(self):
        return "{}, {}".format(self.first_name,self.last_name)

    def get_name_is_empty(self):
        if not self.first_name or not self.last_name:
            return False
        return True


class Category(models.Model):
    title = models.CharField(max_length=300, null=False, blank=False)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    bg_css = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    def getEncryptedID(self):
        value = signer.sign(self.id)
        return value


class Tag(models.Model):
    title = models.CharField(max_length=300, null=False, blank=False)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reaction")
    reaction = models.CharField(choices=REACTION, blank=False, null=False, max_length=15)
    date_created = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')

    def __str__(self):
        return self.message

    def getEncryptedID(self):
        value = signer.sign(self.id)
        return value

class ReportComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_reported')
    reason = models.TextField(blank=False, null=False)
    report_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='comment_reporter')
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.comment)

    def destination(self):
        comm = self.comment.destination_comments.first()
        return comm

class Amenity(models.Model):
    title = models.CharField(max_length=350, blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def getEncryptedID(self):
        value = signer.sign(self.id)
        return value


class Photo(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True)
    photo = models.FileField(upload_to="photos")
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Destination(models.Model):
    title = models.CharField(max_length=300, null=False, blank=False)
    description = models.TextField()
    image_url = models.CharField(max_length=300, blank=True, null=True, default="https://www.agora-gallery.com/advice/wp-content/uploads/2015/10/image-placeholder.png")
    tags = models.ManyToManyField(Tag, through="DestinationTags")
    comments = models.ManyToManyField(Comment, through="DestinationComments")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='destination_category', blank=True, null=True)
    likes = models.ManyToManyField(User, through="DestinationLike", related_name="user_likes")
    date_posted = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="user_destination_post", blank=True, null=True)
    amenities = models.ManyToManyField(Amenity, through="DestinationAmenities")
    photos = models.ManyToManyField(Photo, through="DestinationPhotos")
    ratings = models.ManyToManyField(User, through="UserRating", related_name="user_ratings")
    reactions = models.ManyToManyField(Reaction, through="DestinationReaction")
    address = map_fields.AddressField(max_length=200, blank=True, null=True)
    geolocation = map_fields.GeoLocationField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

    def getEncryptedID(self):
        value = signer.sign(self.id)
        return value

    def num_likes(self):
        return self.likes.count()

    def num_comments(self):
        return self.comments.count()

    def getIsLike(self, user):
        return self.destination_likes.filter(like=user).first()

    def count_respondents(self):
        return int(self.ratings.count())

    def calculate_rating(self):
        rate = self.destination_ratings.aggregate(total=Sum('rating'))['total'] or 0
        if rate:
            rate = (rate / self.count_respondents())
        return float(rate)

    def average_rating(self):
        return "{:.1f}".format(self.calculate_rating())

    def star_display_count(self):
        stars = [False, False, False, False, False]
        count = math.floor(self.calculate_rating())
        for c in range(0, count):
            stars[c] = True
        return stars

    def first_image(self):
        p = self.photos.filter().first()
        if p:
            return p.photo.url
        return "https://www.agora-gallery.com/advice/wp-content/uploads/2015/10/image-placeholder.png"

    def short_description(self):
        bs = BeautifulSoup(self.description)
        bs = bs.get_text()
        if len(bs) > 100:
            return "{} ...".format(self.description[:100])
        else:
            return self.description

    def get_react_count(self):
        num = self.reactions.all().count()
        return num

    def get_like_count(self):
        num = self.reactions.filter(reaction='LIKE').count()
        return num

    def get_heart_count(self):
        num = self.reactions.filter(reaction='HEART').count()
        return num

    def get_wow_count(self):
        num = self.reactions.filter(reaction='WOW').count()
        return num

    def get_sad_count(self):
        num = self.reactions.filter(reaction='SAD').count()
        return num

    def get_angry_count(self):
        num = self.reactions.filter(reaction='ANGRY').count()
        return num

    def lat(self):
        if self.geolocation:
            return self.geolocation.lat
        return 0

    def long(self):
        if self.geolocation:
            return self.geolocation.lon
        return 0

class DestinationReaction(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="destination_reactions")
    reaction = models.ForeignKey(Reaction, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


class UserRating(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="destination_ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.destination, self.rating)


class DestinationPhotos(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(str(self.destination), str(self.photo))


class DestinationAmenities(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(str(self.destination))


class DestinationLike(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="destination_likes")
    like = models.ForeignKey(User, on_delete=models.CASCADE)
    date_like = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.like)

class DestinationTags(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    date_tag = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.destination)


class DestinationComments(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="destination_comments")
    date_commented = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.destination)


class Featured(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='featured_destination')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.destination)

