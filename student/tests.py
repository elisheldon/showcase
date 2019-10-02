from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.conf import settings
from django.db import models
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.contenttypes.models import ContentType
from django.utils.six import BytesIO
from PIL import Image
from json import dumps

from authentication.models import PortfolioUser
from student.models import Student, Item, Link, Gallery, Photo
from student.forms import AddForm

# Create your tests here.
class ModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up immutable data for the whole TestCase
        user = get_user_model().objects.create_user('test', 'test@test.com', 'test')
        user.first_name = 'test'
        user.last_name = 'user'
        group = Group.objects.create(name = 'students')
        user.groups.add(group)
        user.save()
        Student.objects.create(user = user)

    def test_user_created(self):
        """Test user was created"""
        user = get_user_model().objects.filter(username = 'test')
        self.assertEqual(len(user), 1)
    
    def test_student_created(self):
        """Test student was created"""
        user = get_user_model().objects.get(username = 'test')
        student = Student.objects.filter(user = user)
        self.assertEqual(len(student), 1)
    
    def test_link_creation(self):
        """Test link can be created"""
        user = get_user_model().objects.get(username = 'test')
        student = Student.objects.get(user = user)
        link = Link.objects.create(url = 'http://test.com')
        Item.objects.create(student = student, sub_item = link, title = 'test title', description = 'test description')
        link = Link.objects.get(url = 'http://test.com')
        self.assertTrue(link)
        link = Link.objects.get(image = settings.STATIC_URL + 'student/default_images/link.svg')
        self.assertTrue(link)
        item = Item.objects.get(student = student)
        self.assertTrue(item)
    
    def test_gallery_and_photo_creation(self):
        """Test gallery and photo can be created"""
        user = get_user_model().objects.get(username='test')
        student = Student.objects.get(user = user)
        gallery = Gallery.objects.create()
        Item.objects.create(student = student, sub_item = gallery, title = 'test title', description = 'test description')
        image = create_image(None, 'image.png')
        file = SimpleUploadedFile('image.png', image.getvalue())
        photo = Photo.objects.create(image = file, parent_gallery = gallery)
        gallery.cover = photo
        gallery.save()
        gallery = Gallery.objects.get()
        self.assertTrue(gallery)
        photo = Photo.objects.get()
        self.assertTrue(photo)
        item = Item.objects.get(student = student)
        self.assertTrue(item)

class StudentTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up immutable data for the whole TestCase
        user = get_user_model().objects.create_user('test', 'test@test.com', 'test')
        user.first_name = 'test'
        user.last_name = 'user'
        group = Group.objects.create(name = 'students')
        user.groups.add(group)
        user.save()
        student = Student.objects.create(user = user)
        user2 = get_user_model().objects.create_user('test2', 'test2@test.com', 'test2')
        user2.first_name = 'test2'
        user2.last_name = 'user2'
        user2.groups.add(group)
        user2.save()
        student2 = Student.objects.create(user = user2)
        link = Link.objects.create(url = 'http://test.com')
        gallery = Gallery.objects.create()
        item_link = Item.objects.create(student = student, sub_item = link, title = 'test title', description = 'test description')
        item_gallery = Item.objects.create(student = student, sub_item = gallery, title = 'test title', description = 'test description')
        image = create_image(None, 'image.png')
        file = SimpleUploadedFile('image.png', image.getvalue())
        photo = Photo.objects.create(image = file, parent_gallery = gallery)
        gallery.cover = photo
        gallery.save()
    
    def setUp(self):
        # every test needs a logged in client
        self.client = Client()
        self.client.login(username = 'test', password = 'test')
    
    def test_portfolio(self):
        """Test portfolio view"""
        response = self.client.get('/', follow=True)
        self.assertEqual(response.redirect_chain[0][0], '/student/')
        response = self.client.get('/student/', follow=True)
        self.assertEqual(response.context['name'], 'test')
        items = response.context['items']
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].sub_item_type, ContentType.objects.get(app_label = 'student', model = 'link'))
        self.assertEqual(items[1].sub_item_type, ContentType.objects.get(app_label = 'student', model = 'gallery'))
    
    def test_add_get(self):
        """Test add view via get"""
        response = self.client.get('/student/add')
        self.assertEqual(response.status_code, 200)
    
    def test_add_form_invalid(self):
        """Test add form with invalid data"""
        form = AddForm(data={'title': '', 'sub_item_type': 'link'})
        self.assertFalse(form.is_valid())
        form = AddForm(data={'title': 'test title', 'sub_item_type': 'invalid_type'})
        self.assertFalse(form.is_valid())

    def test_add_form_link_valid(self):
        """Test add form with valid link data"""
        form = AddForm(data={'title': 'test title', 'description': 'test description', 'sub_item_type': 'link', 'url': 'http://test.com', 'image': 'http://test.com/image.png'})
        self.assertTrue(form.is_valid())

    def test_add_form_gallery_valid(self):
        """Test add form with valid gallery data"""
        image = create_image(None, 'image.png')
        file = SimpleUploadedFile('image.png', image.getvalue())
        data = {'title': 'added from post', 'description': 'test description', 'sub_item_type': 'gallery', 'photos': file}
        form = AddForm(data=data)
        self.assertTrue(form.is_valid())

    def test_add_post_link(self):
        """Test add view via post with a link"""
        data = {'title': 'added from post', 'description': 'test description', 'sub_item_type': 'link', 'url': 'http://post.com', 'image': 'http://post.com/image.png'}
        response = self.client.post('/student/add', data, follow=True)
        self.assertEqual(response.status_code, 200)
        item = Item.objects.get(title = 'added from post')
        self.assertTrue(item)
        link = Link.objects.get(url = 'http://post.com')
        self.assertTrue(link)

    def test_add_post_gallery(self):
        """Test add view via post with a gallery"""
        image = create_image(None, 'image.png')
        file = SimpleUploadedFile('image.png', image.getvalue())
        data = {'title': 'added from post', 'description': 'test description', 'sub_item_type': 'gallery', 'photos': file}
        form = AddForm(data=data)
        self.assertTrue(form.is_valid())
        response = self.client.post('/student/add', data, follow=True)
        self.assertEqual(response.status_code, 200)
        item = Item.objects.get(title = 'added from post')
        self.assertTrue(item)
        galleries = Gallery.objects.all()
        self.assertEqual(len(galleries), 2)
        photos = Photo.objects.all()
        self.assertEqual(len(photos),2)
    
    def test_remove_valid(self):
        """Test removing an item with a valid post request"""
        user = get_user_model().objects.get(username='test')
        student = Student.objects.get(user = user)
        link = Link.objects.create(url = 'http://deleteme.com')
        item = Item.objects.create(student = student, sub_item = link, title = 'test title', description = 'test description')
        response = self.client.post('/student/remove', dumps({'item_id': item.id}), content_type='application/json')
        self.assertEqual(response.status_code, 204)
        links = Link.objects.all()
        self.assertEqual(len(links), 1)
        items = Item.objects.all()
        self.assertEqual(len(items), 2)
    
    def test_remove_invalid(self):
        """Test removing an item with an invalid post request"""
        user = get_user_model().objects.get(username='test2')
        student = Student.objects.get(user = user)
        link = Link.objects.create(url = 'http://deleteme.com')
        item = Item.objects.create(student = student, sub_item = link, title = 'test title', description = 'test description')
        response = self.client.post('/student/remove', dumps({'item_id': item.id}), content_type='application/json')
        self.assertEqual(response.status_code, 403)
        links = Link.objects.all()
        self.assertEqual(len(links), 2)
        items = Item.objects.all()
        self.assertEqual(len(items), 3)

    def test_gallery(self):
        """Test the gallery view"""
        """Test portfolio view"""
        response = self.client.get('/student/gallery/2')
        item = response.context['item']
        gallery = response.context['gallery']
        photo = response.context['photos'][0]
        self.assertEqual(item.id, 2)
        self.assertEqual(gallery.id, 1)
        self.assertTrue(photo)

# http://blog.cynthiakiser.com/blog/2016/06/26/testing-file-uploads-in-django/
def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)