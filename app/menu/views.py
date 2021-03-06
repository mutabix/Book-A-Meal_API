from flask.views import MethodView
from flask import request
from app.models.models import MenuItem
from app.custom_http_respones.responses import Success, Error
from app.decorators.decorators import token_required, admin_only
from . import menu_blueprint


class MenuView(MethodView):
    """A class based view for handling menu requests"""
    def __init__(self):
        super().__init__()
        self.success = Success()
        self.error = Error()

    @admin_only
    def post(self, user_id):
        """This method is for adding a menu item into the database"""
        json_data = request.get_json(force=True)
        meal1 = json_data.get('meal1')
        meal2 = json_data.get('meal2')
        price = json_data.get('price')
        meal_name = '{} and {}'.format(meal1, meal2)

        # check if menu item exists
        menu_item = MenuItem.query.filter_by(meals=meal_name).first()

        if not menu_item:
            try:
                # check if price exists
                if not price:
                    return self.error.bad_request('No price provided')
                if not isinstance(price, int):
                    return self.error.bad_request('Invalid price')
                if not isinstance(meal_name, str):
                    return self.error.bad_request('Invalid meal names')

                menu_item = MenuItem(meals=meal_name, price=price)
                menu_item.save()
                return self.success.create_resource('Success, id: {}'.format(menu_item.id))
            except Exception as e:
                return self.error.internal_server_error('Error occurred {}'.format(e))
        else:
            return self.error.causes_conflict('menu item exists')

    @token_required
    def get(self, user_id):
        """This is a method for getting all menu items from the database"""
        try:
            menu_items = MenuItem.query.all()
            menu_data = []

            #  make the data json serializable
            for item in menu_items:
                menu_data.append({'id': item.id, 'meals': item.meals, 'price': item.price})
            return self.success.complete_request('data: {}'.format(menu_data))
        except Exception as e:
            return self.error.internal_server_error('Error occurred'.format(e))


#  define the menu class-based view
menu_view = MenuView.as_view('menu_view')

# add a url to be used to reach the view
menu_blueprint.add_url_rule('/menu/', view_func=menu_view, methods=['GET', 'POST'])
