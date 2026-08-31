import pytest
from rest_framework import status
from store.models import Collection, Product
from model_bakery import baker  

@pytest.fixture
def create_collection(api_client):
        def do_create_collection(collection):
            return api_client.post('/store/collections/',collection)
        return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:
    # @pytest.mark.skip
    def test_if_user_anonymous_returns_401(self, create_collection):
        # Arrange
        # Act
        # Assert
        response = create_collection({'title':'a'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_if_user_not_admin_returns_403(self, create_collection, authenticate):
            authenticate()

            response = create_collection({'title':'a'})

            assert response.status_code == status.HTTP_403_FORBIDDEN


    def test_if_data_invalid_returns_400(self, create_collection, authenticate):
                authenticate(True)

                response = create_collection({'title':''})
    
                assert response.status_code == status.HTTP_400_BAD_REQUEST
                assert response.data['title'] is not None


    def test_if_data_valid_returns_201(self, create_collection, authenticate):
                    authenticate(True)

                    response = create_collection({'title':'a'})
        
                    assert response.status_code == status.HTTP_201_CREATED
                    assert response.data['id'] > 0

@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self, api_client):
        collection = baker.make(Collection)
        # baker.make(Product, collection=collection, _quantity=10)
        response = api_client.get(f"/store/collections/{collection.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
               'id':collection.id,
               'title':collection.title,
               'products_count':0
        }

    def test_if_collection_not_exists_return_404(self,api_client):
        response = api_client.get("/store/collections/0/")

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.fixture
def create_product(api_client):
    def do_create_product(product=None):
        payload = {
            'title': 'Laptop',
            'slug': 'laptop',
            'unit_price': '2499.99',
            'inventory': 10,
            'collection': baker.make(Collection).id
        }
        if product:
            payload.update(product)
        return api_client.post('/store/products/', payload)
    return do_create_product


@pytest.mark.django_db
class TestCreateProduct:
    def test_if_user_anonymous_returns_401(self, create_product):
        response = create_product()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_not_admin_returns_403(self, create_product, authenticate):
        authenticate()

        response = create_product()

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_invalid_returns_400(self, create_product, authenticate):
        authenticate(True)

        response = create_product({
            'title': '',
            'slug': '',
            'unit_price': '0',
            'inventory': -1,
            'collection': baker.make(Collection).id
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'title' in response.data or 'slug' in response.data or 'unit_price' in response.data or 'inventory' in response.data

    def test_if_data_valid_returns_201(self, create_product, authenticate):
        authenticate(True)

        response = create_product()

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
        assert response.data['title'] == 'Laptop'


@pytest.mark.django_db
class TestRetrieveProduct:
    def test_if_product_exists_returns_200(self, api_client):
        product = baker.make(Product, title='Phone', slug='phone', unit_price='899.99', inventory=5)

        response = api_client.get(f'/store/products/{product.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == product.id
        assert response.data['title'] == product.title

    def test_if_product_not_exists_return_404(self, api_client):
        response = api_client.get('/store/products/0/')

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateProduct:
    def test_if_user_not_admin_returns_403(self, api_client, authenticate):
        product = baker.make(Product)
        authenticate()

        response = api_client.patch(f'/store/products/{product.id}/', {'title': 'Updated Chair'})

        assert response.status_code == status.HTTP_403_FORBIDDEN


    def test_if_data_valid_returns_200(self, api_client, authenticate):
        product = baker.make(Product, title='Old Title', slug='old-title', unit_price='100.00', inventory=3)
        authenticate(True)

        response = api_client.patch(f'/store/products/{product.id}/', {'title': 'New Title'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'New Title'


@pytest.mark.django_db
class TestDeleteProduct:
    def test_if_product_has_order_items_returns_405(self, api_client, authenticate):
        product = baker.make(Product)
        customer = baker.make('store.Customer')
        order = baker.make('store.Order', customer=customer)
        baker.make('store.OrderItem', product=product, order=order, quantity=1, unit_price=product.unit_price)
        authenticate(True)

        response = api_client.delete(f'/store/products/{product.id}/')

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_if_product_has_no_order_items_returns_204(self, api_client, authenticate):
        product = baker.make(Product)
        authenticate(True)

        response = api_client.delete(f'/store/products/{product.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT