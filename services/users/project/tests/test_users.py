# services/users/project/tests/test_users.py


import json
import unittest

from project.tests.base import BaseTestCase
from project import db
from project.api.models import User


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """Test para el servicio Users."""

    def test_users(self):
        """Asegurando que la runta /ping funcione correctamente."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Asegurando que un usuario puede ser agregado a la base de datos."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'sindy',
                    'email': 'sindyepiquien@upeu.edu.pe'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn(
                'sindyepiquien@upeu.edu.pe ha sido agregado!',
                data['message']
            )
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Asegurando que se produce un erro si el objeto JSON está vacío."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Carga inválida.', data['message'])
            self.assertIn('falló', data['status'])

    def test_add_user_invalid_json_keys(self):
        """
        Asegurando se produce un error si el objeto JSON no tiene una key
        username
        """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'sindyepiquien@upeu.edu.pe'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Carga inválida.', data['message'])
            self.assertIn('falló', data['status'])

    def test_add_user_duplicate_email(self):
        """Asegurando que se produce un error si el email ya existe."""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'sindy',
                    'email': 'sindyepiquien@upeu.edu.pe'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'sindy',
                    'email': 'sindyepiquien@upeu.edu.pe'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Disculpa. El email ya existe.', data['message'])
            self.assertIn('falló', data['status'])

    def test_single_user(self):
        """Asegurando que un usuario único se comporte correctamente."""
        user = add_user('sindy', 'sindyepiquien@upeu.edu.pe')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('sindy', data['data']['username'])
            self.assertIn('sindyepiquien@upeu.edu.pe', data['data']['email'])
            self.assertIn('success', data['status'])

    
    def test_single_user_no_id(self):
        """Asegurando que se produce un error si no se ha proveido el id."""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Usuario no existe', data['message'])
            self.assertIn('falló', data['status'])

    def test_single_user_incorrect_id(self):
        """Asegurando que se produce un error si el id no existe."""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Usuario no existe', data['message'])
            self.assertIn('falló', data['status'])

    def test_all_users(self):
        """Asegurando se obtenga a todos lus usuarios correctamente."""
        add_user('sindy', 'sindyepiquien@upeu.edu.pe')
        add_user('raquel', 'raquel@gmail.com')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('sindy', data['data']['users'][0]['username'])
            self.assertIn(
                'sindyepiquien@upeu.edu.pe', data['data']['users'][0]['email'])
            self.assertIn('raquel', data['data']['users'][1]['username'])
            self.assertIn(
                'raquel@gmail.com', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])

    def test_main_no_users(self):
        """Asegurando que la ruta principal funcione correctamente cuando no
        hay usuarios añadidos a la base de datos."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Todos los usuarios', response.data)
        self.assertIn(b'<p>No hay usuarios!</p>', response.data)

    def test_main_with_users(self):
        """Asegurando que la runta principal funcione correctamente cuando un
        usuario es correctamente agregado a la base de datos."""
        add_user('sindy', 'sindyepiquien@upeu.edu.pe')
        add_user('raquel', 'raquel@gmail.com')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Todos los usuarios', response.data)
            self.assertNotIn(b'<p>No hay usuarios!</p>', response.data)
            self.assertIn(b'sindy', response.data)
            self.assertIn(b'raquel', response.data)

    def test_main_add_user(self):
        """
        Asegurando que un nuevo usuarios pueda ser agregado a la db mediante
        un POST request.
        """
        with self.client:
            response = self.client.post(
                '/',
                data=dict(username='sindy', email='sindyepiquien@upeu.edu.pe'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Todos los usuarios', response.data)
            self.assertNotIn(b'<p>No hay usuarios!</p>', response.data)
            self.assertIn(b'sindy', response.data)


if __name__ == '__main__':
    unittest.main()
