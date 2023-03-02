import unittest
import requests

API_ENDPOINT = 'http://127.0.0.1:5000'

class TestPost(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestPost, self).__init__(*args, **kwargs)
    self.name = "TestPost"
    self.pwd = "password"
    self.mail = "truc@mail.com"
  
  # Valid test
  def test_post(self):
    response = requests.post(API_ENDPOINT+'/user', json={
      'name': self.name,
      'password': self.pwd,
      'email': self.mail
    })
    self.assertEqual(response.status_code, 200)
    json_response = response.json()
    self.assertEqual(json_response["email"], self.mail)
    self.assertEqual(json_response["name"], self.name)
    self.assertEqual(json_response["password"], self.pwd)
  
  # Return 400
  def test_post_send_data(self):
    response = requests.post(API_ENDPOINT+'/user', data={
      'name': self.name,
      'password': self.pwd,
      'email': self.mail
    })
    self.assertEqual(response.status_code, 400)
  
  # Return 400
  def test_post_empty(self):
    response = requests.post(API_ENDPOINT+'/user')
    self.assertEqual(response.status_code, 400)


class TestGet(unittest.TestCase):
  def test_get(self):
    response = requests.get(API_ENDPOINT+'/users')
    self.assertEqual(response.status_code, 200)
    json_response = response.json()
    self.assertIsInstance(json_response, list)
    self.assertTrue(len(json_response) >= 0)
  
  def test_get_bad_endpoint(self):
    response = requests.get(API_ENDPOINT+'/user') # using 'user' instead of 'users'
    self.assertEqual(response.status_code, 405)

class TestPut(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestPut, self).__init__(*args, **kwargs)
    self.name = "TestPut"
    self.pwd = "password"
    self.mail = "truc@mail.com"
    response = requests.post(API_ENDPOINT+'/user', json={
      'name': self.name,
      'password': self.pwd,
      'email': self.mail
    })
    self._id = int(response.json()["id"])

  def test_put(self):
    response = requests.put(API_ENDPOINT+'/user', json={
      'id': self._id,
      'name': 'Other-name',
      'password': self.pwd,
      'email': self.mail
    })
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), {})    

class TestDelete(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestDelete, self).__init__(*args, **kwargs)
    self.name = "TestPut"
    self.pwd = "password"
    self.mail = "truc@mail.com"
    response = requests.post(API_ENDPOINT+'/user', json={
      'name': self.name,
      'password': self.pwd,
      'email': self.mail
    })
    self._id = int(response.json()["id"])

  def test_delete(self):
    response = requests.delete(API_ENDPOINT+'/user/'+str(self._id))
    self.assertEqual(response.status_code, 200)
  
  def test_delete_no_id(self):
    response = requests.delete(API_ENDPOINT+'/user/')
    self.assertEqual(response.status_code, 404)
  
if __name__ == '__main__':
    unittest.main()