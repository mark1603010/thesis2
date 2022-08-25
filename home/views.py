from django.core.mail import message
from home.forms import SignUpForm
from home.models import *
from util.Common import *


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def error_404(request, exception):
    return render(request, 'home/404.html', {})


def home(request):
    featured = Featured.objects.all().order_by('-id')
    categories = Category.objects.all()
    payload = {
        'featured_destination': featured,
        'categories': categories
    }
    return render(request, 'home/home.html', payload)


def destination(request):
    destinations = Destination.objects.all().order_by('-id')
    filter = request.GET.get('category')
    if filter:
        category = get_object_or_404(Category, title=filter)
        destinations = Destination.objects.filter(category=category).order_by('-id')

    payload = {
        'destinations': destinations
    }
    return render(request, 'home/destination.html', payload)


def destination_details(request, destination_id):
    destination = get_object_or_404(Destination, pk=signer.unsign(destination_id))
    is_like = None
    if request.user.is_authenticated:
        is_like = destination.getIsLike(request.user)

    if request.method == "POST":
        like_action = request.POST.get('like_action')
        print(like_action)
        if not request.user.is_authenticated:
            return HttpResponse("Unauthorized")

        if like_action:
            if not is_like:
                destination.likes.add(request.user)
            else:
                destination.likes.remove(request.user)

        return HttpResponseRedirect(reverse('home:destination_details', kwargs={'destination_id': destination_id}))

    other_destinations = Destination.objects.exclude(pk=destination.pk).order_by('-id')[:10]
    other_photos = ""
    main_photo = destination.first_image
    if destination.photos.count() > 0:
        other_photos = destination.photos.all()[1:]
        other_photos = [p.photo for p in other_photos]
    payload = {
        'destination': destination,
        'other_destinations': other_destinations,
        'main_photo': main_photo,
        'other_photos': other_photos,
        'is_like': is_like
    }
    return render(request, 'home/destination_details.html', payload)


@method_decorator([], name='dispatch')
class Profile(View):
    template_name = "home/profile.html"

    def get(self, request, *args, **kwargs):
        if not request.user.get_name_is_empty():
            messages.warning(request, "Please complete your profile")

        profile_info = {}
        profile_info['First Name'] = {'value': request.user.first_name if request.user.first_name != "None" else "",
                                   'placeholder': "Enter First name"}
        profile_info['Last Name'] = {'value': request.user.last_name if request.user.last_name != "None" else "",
                                      'placeholder': "Enter Last name"}
        profile_info['Address'] = {'value': request.user.address if request.user.address != "None" else "", 'placeholder': "Enter Address"}
        profile_info['Email'] = {'value': request.user.email if request.user.email != "None" else "", 'placeholder': "Enter Email"}
        profile_info['Gender'] = {'value': request.user.gender if request.user.gender != "None" else "", 'placeholder': "Enter Gender (MALE/FEMALE)"}
        profile_info['Phone number'] = {'value': request.user.phone_number if request.user.phone_number != "None" else "", 'placeholder': "Enter phone number"}
        context = {
            'profile_info': profile_info
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        address = self.request.POST.get("Address")
        gender = request.POST.get("Gender")
        p_number = request.POST.get("Phone number")
        last_name = request.POST.get("Last Name")
        first_name = request.POST.get("First Name")
        if not gender.upper() in ["MALE", "FEMALE"]:
            messages.error(request, "Invalid Gender")
            return HttpResponseRedirect(reverse("home:profile"))

        if len(last_name) <= 0 or len(first_name) <= 0:
            messages.error(request, "First name and Last name must not be empty")
            return HttpResponseRedirect(reverse("home:profile"))

        user = get_object_or_404(User, pk=request.user.pk)
        user.address = address
        user.gender = gender.upper()
        user.phone_number = p_number
        user.last_name = last_name
        user.first_name = first_name
        user.save()
        messages.success(request, "Profile information updated")
        return HttpResponseRedirect(reverse("home:profile"))

@login_required
def post_comment(request, destination_id):
    destination = get_object_or_404(Destination, pk=signer.unsign(destination_id))
    if request.method == "POST":
        comment = request.POST.get("comment")
        commment_object = Comment.objects.create(
            message=comment,
            commenter=request.user
        )
        destination.comments.add(commment_object)
        return HttpResponseRedirect(reverse("home:destination_details", kwargs={'destination_id':destination_id}))
    return HttpResponse("Invalid Method")

@login_required
def delete_comment(request, destination_id,comment_id):
    comment = get_object_or_404(Comment, pk=signer.unsign(comment_id))
    # only users comment can be deleted
    if comment.commenter.id == request.user.id:
        comment.delete()
    return HttpResponseRedirect(reverse("home:destination_details", kwargs={'destination_id':destination_id}))


@login_required
def post_rate(request, destination_id):
    destination = get_object_or_404(Destination, pk=signer.unsign(destination_id))
    if request.method == "POST":
        #check if user already rated
        try:
            rating = UserRating.objects.get(destination=destination, user=request.user)
            messages.error(request, "You already rated this destination")
            return HttpResponseRedirect(reverse("home:destination_details", kwargs={'destination_id':destination_id}))
        except UserRating.DoesNotExist:
            rate = request.POST.get('rate')
            if not int(rate) > 0:
                messages.error(request, "Please select a number of star to rate")
                return HttpResponseRedirect(
                    reverse("home:destination_details", kwargs={'destination_id': destination_id}))
            UserRating.objects.create(
                destination=destination,
                user=request.user,
                rating=int(rate)
            )
            messages.success(request, "Your rating has been successfully submitted")
            return HttpResponseRedirect(reverse("home:destination_details", kwargs={'destination_id':destination_id}))

    return HttpResponse("Invalid method")


def category(request):
    categories = Category.objects.all()
    context = {
        'categories':categories
    }
    return render(request, 'home/category.html', context)


def search_destination(request):
    filter = request.GET.get('filter')
    destinations = []
    if filter:
        destinations = Destination.objects.filter(title__contains=filter)
    else:
        destinations = Destination.objects.all()
    context = {
        'destinations':destinations
    }
    return render(request, 'home/search_destination.html', context)

@login_required
def report_comment(request, destination_id, comment_id):
    comment = get_object_or_404(Comment, pk=signer.unsign(comment_id))
    if request.method == "POST":
        reason = request.POST.get("reason")
        ReportComment.objects.create(
            comment=comment,
            reason=reason,
            report_by=request.user
        )
        messages.success(request, "Comment has been reported")
        return HttpResponseRedirect(reverse("home:destination_details", kwargs={'destination_id':destination_id}))
    context = {
        'comment': comment
    }
    return render(request, 'home/report_comment.html', context)

def verify_email(request, verification_token):
    user = get_object_or_404(User, email_verification_token=verification_token)
    if not user.email_verified:
        user.email_verified = True
        user.save()
    context = {
        'user':user,
    }
    return render(request, 'home/verify_email.html',context)

@login_required
def reaction(request, destination_id, reaction):
    destination = get_object_or_404(Destination, pk=signer.unsign(destination_id))

    is_reacted = destination.reactions.filter(user=request.user).count()
    if is_reacted > 0:
        my_reaction = destination.reactions.filter(user=request.user).first()
        destination.reactions.remove(my_reaction)

    react = Reaction.objects.create(
        user = request.user,
        reaction = reaction,
    )
    destination.reactions.add(react)
    messages.success(request, "Reaction submitted")
    return HttpResponseRedirect(reverse("home:destination_details", kwargs={'destination_id': destination_id}))


def content_creator(request):
    return render(request, 'home/content_creator.html',{})

def about(request):
    return render(request, 'home/about.html',{})