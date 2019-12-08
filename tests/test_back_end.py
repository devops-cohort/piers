import unittest

from flask import url_for
from flask_testing import TestCase
from os import getenv
from application import app, db
from application.models import users, card_list, deck_list


class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql+pymysql://'+str(getenv('MYSQL_USER'))+':'+str(getenv('MYSQL_PWD'))+'@'+str(getenv('MYSQL_IP'))+'/'+str(getenv('MYSQL_TEST_DB'))        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.session.commit()
        db.drop_all()
        db.create_all()

        # create test admin user
        admin = users(user_name="admin", first_name="admin", last_name="admin", password="admin2019", admin=True)

        # create test non-admin user
        user = users(user_name="user", first_name="user", last_name="user", password="user2019", admin=False)

        #create test card
        card = card_list(card_ID=1, card_name="test card", card_attk=4000, card_def=4000)

        #create test deck
        deck = deck_list(ID=1, deck_name="test deck", user_ID=1, card_ID=1)

        # save entries to database
        db.session.add(admin)
        db.session.add(user)
        db.session.add(card)
        db.session.add(deck)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

class TestRouting(TestBase):

    def testHome(self):
        response = self.client.get(url_for('home'))

        self.assertEqual(response.status_code, 200)

    def testRegister(self):
        response = self.client.get(url_for('register'))

        self.assertEqual(response.status_code, 200)
    
    def testLogin(self):
        response = self.client.get(url_for('login'))

        self.assertEqual(response.status_code, 200)

    def testAdmin(self):
        target_url = url_for('admin')
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    
    def testLogout(self):
        target_url = url_for('logout')
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def testAccount(self):
        target_url = url_for('account')
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_C_Pass(self):
        target_url = url_for('change_password')
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    
    def testDashboard(self):
        target_url = url_for('dashboard')
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    
    def testEditCard(self):
        target_url = url_for('edit_card', card='test card', deck='test deck')
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    
    def testCreateCard(self):
        target_url = url_for('create_card')
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    
    def testEditUser(self):
        target_url = url_for('edit_user', user_ID=1)
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    
    def testDeleteUser(self):
        target_url = url_for('delete_user', user_ID=1)
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    
    def testRemoveCard(self):
        target_url = url_for('remove_card', deck='test deck', card='test card')
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def testCreateDeck(self):
        target_url = url_for('create_deck')
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    
    def testDeck(self):
        target_url = url_for('deck', deck_id='test deck')
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def testDeleteDeck(self):
        target_url = url_for('delete_deck', deck='test deck')
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def testAddCard(self):
        target_url = url_for('add_card', deck='test deck')
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    
    def testConfirmCard(self):
        target_url = url_for('confirm_card', deck='test deck', card_name='test card')
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    
class TestModels(TestBase):
    
    def test_users_model(self):
        user = users(user_name="test2", first_name="test", last_name="user", password="test2019", admin=False)

        db.session.add(user)
        db.session.commit()

        self.assertEqual(users.query.count(), 3)
    
    def test_card_list_model(self):
        card = card_list(card_ID=2, card_name="test card 2", card_attk=4000, card_def=4000)

        db.session.add(card)
        db.session.commit()

        self.assertEqual(card_list.query.count(), 2)

    def test_deck_list_model(self):
        deck = deck_list(ID=2, deck_name="test deck 2", user_ID=1, card_ID=1)

        db.session.add(deck)
        db.session.commit()

        self.assertEqual(deck_list.query.count(), 2)