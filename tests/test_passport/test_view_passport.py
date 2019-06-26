
import io
from api.models.user import User

def test_it_gets_image_successfully(client):
    user = User(
        full_name='John Ade',
        phone_number='(324) 324 4234',
        address='1, afsfad, asdfasf.',
        email='johnade@gmail.com',
        password='password'
    )
    user.passport_photo.new_file()
    user.passport_photo.write('sfafdadsf'.encode('utf-8'))
    user.passport_photo.close()

    user.save()

    response = client.get('/v1/passports/{}/image.png'.format(user.id))

    assert response.status_code == 200

def test_should_return_404_if_user_id_is_invalid(client):
    response = client.get('/v1/passports/asdfasdfasdf/image.png')

    assert response.status_code == 404
