from .test_setup import TestSetUp
from ..models import User
from pathlib import Path
import logging
logger = logging.getLogger('django_test')
logger.info('test_log')

class TestViews(TestSetUp):
    def test_user_cannot_register_with_no_data(self):        
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)
        print("*"*70)
        print("User Can't be added with NO details:: Passed")
        logger.info("*"*70)
        logger.info(self.assertEqual(res.status_code, 400))
        logger.info("User Can't be added with NO details:: Passed")

    def test_user_can_register_correctly(self):
        res = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(res.data['data']['email'], self.user_data['email'])
        self.assertEqual(res.data['data']['first_name'], self.user_data['first_name'])
        self.assertEqual(res.data['data']['last_name'], self.user_data['last_name'])
        self.assertEqual(res.status_code, 200)
        print("*"*70)
        print("User Registration Successful:: Passed") 
        logger.info("*"*70) 
        logger.info(self.assertEqual(res.data['data']['email'], self.user_data['email']))
        logger.info("User Registration Successful:: Passed")        

    def test_inactive_user_can_not_login(self):
        self.client.post(self.register_url, self.user_data, format="json")        
        res = self.client.post(self.login_url, self.user_data, format="json")
        print("*"*70)
        self.assertEqual(res.status_code, 400) 
        print(("Inactive User can't login:: Passed") )
        logger.info("*"*70)
        logger.info(self.assertEqual(res.status_code, 400))
        logger.info("Inactive User can't login:: Passed")      

    def test_user_can_login_after_activation(self):
        response = self.client.post(
            self.register_url, self.user_data, format="json")
        email = self.user_data['email']
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['data']['email'], self.user_data['email'])
        print("*"*70)
        print("Only Active user can login:: Passed")
        logger.info("*"*70)
        logger.info(self.assertEqual(res.status_code, 200))
        logger.info("Only Active user can login:: Passed")
        

    def test_unauthorised_user_can_not_get_user_list(self):
        res = self.client.post(self.user_list, format="json") 
        print(res)       
        self.assertNotEqual(res.status_code, 200)
        print("*"*70)
        print("Authorization Token needed for user list:: Passed")
        logger.info("*"*70)
        logger.info(self.assertNotEqual(res.status_code, 200))        
        logger.info("Authorization Token needed for user list:: Passed")
    
   