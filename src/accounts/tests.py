from django.test import TestCase
from django.contrib.auth import get_user_model, get_user
from .models import CustomGroup, View
from django.core.management import call_command
from django.urls import reverse
from mixer.backend.django import mixer
from django.test import override_settings


User = get_user_model()

# Create your tests here.
class RoutingTestCase(TestCase):
    # ! data.json instead of permissions.json
    import_data = ["views.json", "data.json", "groups.json", "customgroups.json"]

    def setUp(self):
        for fixture in self.import_data:
            call_command("loaddata", f"import/{fixture}", verbosity=0)

    def test_unauthenticated(self):
        for reversed_url in ["/", reverse("table")]:
            response = self.client.get(reversed_url, follow=True)
            self.assertRedirects(
                response,
                f'{reverse("login")}?next=/',  # reverse because if we wanted to have e.g /prihlasit/ instead of /login/ it'd still resolve to /prihlasit/?next=/
            )

        views = ["logout", "week", "day"]
        for view in views:
            response = self.client.get(reverse(view), follow=True)
            self.assertRedirects(
                response,
                reverse("login"),
            )

    def test_going_to_allowed_view_doesnt_redirect(self):
        # * this with just turns off a runtimewarning... sth about naive datetimefield, also happens while running the server
        with override_settings(USE_TZ=False):
            for custom_group in CustomGroup.objects.all():
                user = mixer.blend(User)
                user.set_password("123456")
                user.groups.add(custom_group.group)
                user.save()

                self.client.force_login(user, backend=None)
                self.assertTrue(get_user(self.client).is_authenticated)

                allowed_views = user.groups.first().custom_group.allowed_views.all()
                for view in allowed_views:
                    response = self.client.get(reverse(view.view), follow=True)
                    self.assertEqual(response.status_code, 200)

    def test_authenticated_redirects_to_default_view_when_going_to_homepage(self):
        with override_settings(USE_TZ=False):
            for custom_group in CustomGroup.objects.all():
                user = mixer.blend(User)
                user.set_password("123456")
                user.groups.add(custom_group.group)
                user.save()

                self.client.force_login(user, backend=None)
                self.assertTrue(get_user(self.client).is_authenticated)

                response = self.client.get("/", follow=True)
                self.assertRedirects(
                    response,
                    reverse(user.groups.first().custom_group.default_view.view),
                )

    def test_authenticated_redirects_to_default_view_when_going_to_views_with_no_access(
        self,
    ):
        with override_settings(USE_TZ=False):
            for custom_group in CustomGroup.objects.exclude(
                group__name="Administrátor"
            ):
                user = mixer.blend(User)
                user.set_password("123456")
                user.groups.add(custom_group.group)
                user.save()

                self.client.force_login(user, backend=None)
                self.assertTrue(get_user(self.client).is_authenticated)
                not_allowed_views = View.objects.all().difference(
                    user.groups.first().custom_group.allowed_views.all()
                )
                for view in not_allowed_views:
                    response = self.client.get(reverse(view.view), follow=True)
                    self.assertRedirects(
                        response,
                        reverse(user.groups.first().custom_group.default_view.view),
                    )

    def test_authenticated_logout(self):
        user = mixer.blend(User)
        user.set_password("123456")
        user.save()

        self.client.force_login(user, backend=None)
        self.assertTrue(get_user(self.client).is_authenticated)

        response = self.client.get(reverse("logout"), follow=True)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertRedirects(response, reverse("login"))
