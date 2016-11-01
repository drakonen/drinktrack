from django.test import TestCase, Client

from .models import User, Consumption, Drink


class BeeromatViews(TestCase):
    fixtures = ['all.json']

    # def setUp(self):
    #     pass

    def test_front_list(self):
        c = Client()
        response = c.get('/')

        # print("res", dir(response))
        # print(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Johan", 1, 200)
        self.assertContains(response, "Justin", 1, 200)
        self.assertContains(response, "<tr>", 2, 200)

        self.assertContains(response, 'beer-count">-', 2, 200)

    def test_front_list_add(self):
        c = Client()
        response = c.get('/')
        self.assertContains(response, 'beer-count">-', 2, 200)

        user = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        drink1 = Drink.objects.get(pk=1)
        drink2 = Drink.objects.get(pk=2)

        # first add a non main page drink
        Consumption.objects.create(user=user, drink=drink2, count=1)

        c = Client()
        response = c.get('/')
        self.assertContains(response, 'beer-count">-', 2, 200)

        # first add a non main page drink
        Consumption.objects.create(user=user, drink=drink1, count=1)

        c = Client()
        response = c.get('/')

        expected = """
        <td class="middle text-right beer-count">
            -1
        </td>
        """

        self.assertContains(response, expected, 1, 200, html=True)

        # add a second drink to second user
        Consumption.objects.create(user=user2, drink=drink1, count=1)

        c = Client()
        response = c.get('/')

        expected = """
        <td class="middle text-right beer-count">
            -1
        </td>
        """

        self.assertContains(response, expected, 2, 200, html=True)

    def test_user_detail_empty(self):

        c = Client()
        response = c.get('/counter/user/1')

        self.assertContains(response, '<h1>Johan</h1>', 1, 200)

    def test_user_detail(self):

        user = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        drink1 = Drink.objects.get(pk=1)
        drink2 = Drink.objects.get(pk=2)

        Consumption.objects.create(user=user, drink=drink1, count=1)
        Consumption.objects.create(user=user, drink=drink1, count=1)
        Consumption.objects.create(user=user, drink=drink2, count=1)
        Consumption.objects.create(user=user2, drink=drink1, count=1)

        c = Client()
        response = c.get('/counter/user/1')

        self.assertContains(response, '<h1>Johan</h1>', 1, 200)
        self.assertContains(response, '<td class="middle">Beer</td>', 1, 200)
        self.assertContains(response, 'beer-count">-2</td>', 1, 200)
        self.assertContains(response, '<td class="middle">Club Mate</td>', 1, 200)
        self.assertContains(response, 'beer-count">-1</td>', 1, 200)

    def test_up(self):
        # assertRedirects
        c = Client()
        response = c.post('/counter/up', {
            "drink-id": 1,
            "user-id": 1,
        })

        user = User.objects.get(pk=1)
        drink1 = Drink.objects.get(pk=1)
        consumption = Consumption.objects.get(user=user, drink=drink1)
        print ("con", consumption)

    def test_remove_with_redirect(self):
        user = User.objects.get(pk=1)
        drink1 = Drink.objects.get(pk=1)
        Consumption.objects.create(user=user, drink=drink1, count=1)
        Consumption.objects.create(user=user, drink=drink1, count=1)

        c = Client()
        response = c.post('/counter/remove_consumption/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/counter/user/1')
        self.assertEqual(len(Consumption.objects.all()), 1)

    def test_remove_with_redirect(self):
        user = User.objects.get(pk=1)
        drink1 = Drink.objects.get(pk=1)
        Consumption.objects.create(user=user, drink=drink1, count=1)

        c = Client()
        response = c.post('/counter/remove_consumption/1', {
            "to-view": 'beer:stats'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/counter/stats')
        self.assertEqual(len(Consumption.objects.all()), 0)

