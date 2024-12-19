import json
from model_bakery import baker
from django.urls import reverse
from test_plus.test import TestCase
from django.contrib.auth.models import User
import pytest

from library.models import Reservation

######################## Fixtures ########################

@pytest.fixture
# client is a standard fixture provided by pytest
def authenticatedUserFixture(client):
    User.objects.create_user(username="testuser", password="12345")
    client.login(username="testuser", password="12345")
    return client

@pytest.fixture
def bookFixture():
    return baker.make("Book")

@pytest.fixture
def bookInstanceFixture(bookFixture):
    return baker.make("BookInstance", book=bookFixture)

@pytest.fixture
def reservationFixture(bookInstanceFixture):
    return Reservation.objects.create(
        bookInstance=bookInstanceFixture,
        isActive=True,
        user=User.objects.get(username="testuser")
    )



######################## Mocks ########################

######################## Helper Functions ########################

######################## Tests ########################


class TestReserveBook:
    @pytest.mark.django_db
    def testNoBookId(self, authenticatedUserFixture: User):
        testCase = TestCase()
        response = authenticatedUserFixture.post(reverse("reserve_book"), data=None, follow=True)
        testCase.response_200(response)
        response = response.content.decode('utf-8')
        response = json.loads(response)
        testCase.assertFalse(response.get("success"))
        testCase.assertEqual("Buch existiert nicht.", response.get("message"))

    @pytest.mark.django_db
    def testWrongBookId(self, authenticatedUserFixture: User):
        testCase = TestCase()
        response = authenticatedUserFixture.post(reverse("reserve_book"), data={"book_id":42}, follow=True)
        testCase.response_200(response)
        response = response.content.decode('utf-8')
        response = json.loads(response)
        testCase.assertFalse(response.get("success"))
        testCase.assertEqual("Buch existiert nicht.", response.get("message"))

    @pytest.mark.django_db
    def testAlreadyReserved(self, authenticatedUserFixture: User, reservationFixture: Reservation):
        testCase = TestCase()
        response = authenticatedUserFixture.post(reverse("reserve_book"), data={"book_id":reservationFixture.bookInstance.book.id}, follow=True)
        testCase.response_200(response)
        response = response.content.decode('utf-8')
        response = json.loads(response)
        testCase.assertFalse(response.get("success"))
        testCase.assertEqual("Bereits reserviert.", response.get("message"))

    @pytest.mark.django_db
    def testNoAvailableInstances(self, authenticatedUserFixture: User, bookFixture):
        testCase = TestCase()
        response = authenticatedUserFixture.post(reverse("reserve_book"), data={"book_id":bookFixture.id}, follow=True)
        testCase.response_200(response)
        response = response.content.decode('utf-8')
        response = json.loads(response)
        testCase.assertFalse(response.get("success"))
        testCase.assertEqual("Keine verfügbaren Exemplare.", response.get("message"))

    @pytest.mark.django_db
    def testSuccessfulCreate(self, authenticatedUserFixture: User, bookInstanceFixture):
        testCase = TestCase()
        response = authenticatedUserFixture.post(reverse("reserve_book"), data={"book_id":bookInstanceFixture.book.id}, follow=True)
        testCase.response_200(response)
        response = response.content.decode('utf-8')
        response = json.loads(response)
        testCase.assertTrue(response.get("success"))
        testCase.assertEqual("Buch erfolgreich reserviert.", response.get("message"))
        testCase.assertEqual(1, Reservation.objects.all().count())
        reservation = Reservation.objects.all()[0]
        testCase.assertEqual(True, reservation.isActive)
        testCase.assertEqual(bookInstanceFixture, reservation.bookInstance)
        testCase.assertEqual(User.objects.get(username="testuser"), reservation.user)
        