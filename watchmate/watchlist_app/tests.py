from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from watchlist_app import models
from watchlist_app.api import serializers



class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)

        self.stream = models.StreamPlatform.objects.create\
                                                (name='Netflix-Test',
                                                about='about netflix-test',
                                                website='http://netflix-test.com'
                                                )
        
    def test_stream_platform_create_by_non_admin_user(self):
        data= { 'name': 'Netflix-Test',
                'about': 'about netflix-test',
                'website': 'http://netflix-test.com'
                }
        response = self.client.post(reverse('stream-platforms-list'),data,format='json')  
        #print(f'create stream response:{response}|{response.data}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_get_stream_platform_list(self):
        response = self.client.get(reverse('stream-platforms-list'))
        #print(f'get stream list response:{response}|{response.data}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_stream_platform(self):
        response = self.client.get(reverse('stream-platforms-detail',args=(self.stream.id,)))
        #print(f'get sigle stream response:{response}|{response.data}')
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_stream_platform(self):
        pass

    def test_delete_stream_platform(self):
        pass

    def test_create_stream_platform_by_admin(self):
        pass


class WatchListTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
        self.stream = models.StreamPlatform.objects.create\
                                                (name='Netflix-Test',
                                                about='about netflix-test',
                                                website='http://netflix-test.com'
                                                )
        self.watchlist = models.WatchList.objects.create\
                                                (title='Test-title',
                                                 storyline='Test-storyline',
                                                 active=True,
                                                 platform=self.stream)
        
    def test_create_watchlist_by_non_admin_user(self):
        data= { 'title': 'Test-title',
                'storyline': 'Test-storyline',
                'active': True,
                'platform': self.stream.id
                }
        response = self.client.post(reverse('all-watchlist-detail'),data,format='json')
        #print(f'create watchlist response:{response}|{response.data}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_get_all_show_list(self):
        response = self.client.get(reverse('all-watchlist-detail'))
        #print(f'get all show list response:{response}|{response.data}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_show(self):
        response = self.client.get(reverse('watchlist-detail',args=(self.watchlist.id,)))
        #print(f'get sigle show response:{response}|{response.data}')
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_show_with_invalid_id(self):
        response = self.client.get(reverse('watchlist-detail',args=(33,)))
        #print(f'get sigle show response:{response}|{response.data}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_watchlist(self):
        pass

    def test_delete_watchlist(self):
        pass

    def test_create_watchlist_by_admin(self):
        pass


class ReviewTestCase(APITestCase):#to create review we need movie/watchlist
                                #and to create movie we need platform
                                #hence adding them in test database through setUp()
    
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
        self.stream = models.StreamPlatform.objects.create\
                                                (name='Netflix-Test',
                                                about='about netflix-test',
                                                website='http://netflix-test.com'
                                                )
        self.watchlist = models.WatchList.objects.create\
                                                (title='Test-title',
                                                 storyline='Test-storyline',
                                                 active=True,
                                                 platform=self.stream)
        
        self.watchlist2 = models.WatchList.objects.create\
                                                (title='Test-title2',
                                                 storyline='Test-storyline2',
                                                 active=True,
                                                 platform=self.stream)
        
        self.review = models.Review.objects.create\
                    (review_user=self.user,
                    rating= 4,
                    description= 'Test-Description',
                    active= True,
                    watchlist= self.watchlist2)
        
    def test_create_review(self):
        data= { 'review_user': self.user.id,
                'rating': 4,
                'description': 'Test-Description',
                'active': True,
                }
        response = self.client.post(reverse('reviews-create',args=(self.watchlist.id,)),data,format='json')
        #if format == 'json': is mentioned ,then we must pass id of object
        #if not mentioned , we can pass direct object
        #print(f'create review response:{response}|{response.data}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)


        response = self.client.post(reverse('reviews-create',args=(self.watchlist.id,)),data,format='json')
        #print(f'create review response:{response}|{response.data}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_review_by_unauthenticated_user(self):
        data= { 'review_user': self.user.id,
                'rating': 4,
                'description': 'Test-Description',
                'active': True,
                'platform': self.stream.id
                }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('reviews-create',args=(self.watchlist.id,)),data,format='json')
        #print(f'create review by unauthenticatd response:{response}|{response.data}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_review(self):
        data= { 'review_use': self.user.id,
                'rating': 5,
                'description': 'Test-Description Updated',
                'active': False,
                'watchlist': self.watchlist.id
                }
        response = self.client.put(reverse('reviews-detail',args=(self.review.id,)),data,format='json')
        #print(f'update review response:{response}|{response.data}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_review_by_user_in_params(self):
        response = self.client.get(f'/watch/reviews-params/?username={self.user.username}')
        print(f'get review by user in params response:{response}|{response.data}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)






    def test_all_review_list(self):
        response = self.client.get(reverse('reviews-create',args=(self.watchlist.id,)))
        pass


    def test_single_review(self):
        response = self.client.get(reverse('reviews-create',args=(self.review.id,)))
        pass

    def test_delete_review(self):
        pass
