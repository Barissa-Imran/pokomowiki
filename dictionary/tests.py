from django.test import TestCase
from django.contrib.auth import get_user_model
from dictionary.models import Term
from dictionary.forms import TermAdminForm, TermForm

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        user_a = User(username='test', email='test@invalid.com')
        user_a.is_staff = True
        user_a.is_superuser = True
        user_a.set_password('example_123_password')
        user_a.save()
        return super().setUp()

    def test_user_exists(self):
        user_count = User.objects.all().count()
        print(user_count)
        self.assertEqual(user_count, 1)
        self.assertNotEqual(user_count, 0)


class TermFormTestCase(TestCase):
    def test_term_creation(self):
        form = TermForm(data={
            'word': 'yacha',
            'definition': 'means stop',
            'example': 'yacha tabia zuka',
            'example_translation': 'stop misbehaving',
            'language': 'Upper Pokomo',
            'dialect': 'Ndera',
        })
        form.save()
        term_qs = Term.objects.filter(word='yacha')
        term_exists = term_qs.exists() and term_qs.count() == 1
        self.assertTrue(term_exists)
    
    # def test_meta_keywords_creation(self):
    #     def create_meta_keywords(form):
    #         keywords = []
    #         for keyword in form.cleaned_data['word']:
    #             keywords.append(keyword)
    #             break
    #         for keyword in form.cleaned_data['definition']:
    #             keywords.append(keyword)
    #             break
    #         if form.cleaned_data['other_definitions']:
    #             for keyword in form.cleaned_data['other_definitions']:
    #                 keywords.append(keyword)
    #         else:
    #             pass

    #         str_keywords = ', '.join([str(word) for word in keywords])

    #         form.instance.meta_keywords = str_keywords
