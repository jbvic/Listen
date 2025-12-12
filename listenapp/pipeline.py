from .models import Profile

def save_profile_details(backend, user, response, *args, **kwargs):
    #when logging in, automatically update the display name and profile picture url in profile model
    #as they can be changed whenever and we want those changes to be reflected on the website
    if backend.name != "spotify":
        return
    profile, created = Profile.objects.get_or_create(user=user)
    display_name = response.get("display_name")
    images = response.get("images") or []
    profile_pic_url = images[0]["url"] if images else ""
    profile.display_name = display_name or ""
    profile.profile_pic_url = profile_pic_url or ""
    profile.save()
   