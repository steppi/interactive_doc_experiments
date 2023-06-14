from collections import defaultdict

from docutils.parsers.rst import directives

from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, Index
from sphinx.roles import XRefRole
from sphinx.util.nodes import make_refnode


class RecipeDirective(ObjectDescription):
    """A custom directive that describes a recipe."""
    has_content = True
    required_arguments = 1
    option_spec = {
        'contains': directives.unchanged_required,
    }

    def handle_signature(self, sig, signode):
        signode += addnodes.desc_name(text=sig)
        return sig

    def add_target_and_index(self, name_cls, sig, signode):
        signode['ids'].append('recipe' + '-' + sig)
        if 'contains' in self.options:
            ingredients = [
                x.strip() for x in self.options.get('contains').split(',')
            ]

            recipes = self.env.get_domain('recipe')
            recipes.add_recipe(sig, ingredients)


class IngredientIndex(Index):
    """A custom index that creates an ingredient matrix."""
    name = 'ingredient'
    localname = 'Ingredient Index'
    shortname = 'Ingredient'

    def generate(self, docnames=None):
        content = defaultdict(list)

        recipes = {
            name: (dispname, typ, docname, anchor)
            for name, dispname, typ, docname, anchor, _
            in self.domain.get_objects()
        }
        recipe_ingredients = self.domain.data['recipe_ingredients']
        ingredient_recipes = defaultdict(list)

        # flip from recipe_ingredients to ingredient_recipes
        for recipe_name, ingredients in recipe_ingredients.items():
            for ingredient in ingredients:
                ingredient_recipes[ingredient].append(recipe_name)

        # convert the mapping of ingredient to recipes to produce the expected
        # output, shown below, using the ingredient name as a key to group.
        #
        # name, subtype, docname, anchor, extra, qualifier, description
        for ingredient, recipe_names in ingredient_recipes.items():
            for recipe_name in recipe_names:
                dispname, typ, docname, anchor = recipes[recipe_name]
                content[ingredient].append(
                    (dispname, 0, docname, anchor, docname, '', typ)
                )

        # convert the dict to the sorted list of tuples expected
        content = sorted(content.items())

        return content, True


class RecipeIndex(Index):
    """A custom index that creates an recipe matrix."""

    name = 'recipe'
    localname = 'Recipe Index'
    shortname = 'Recipe'

    def generate(self, docnames=None):
        content = defaultdict(list)

        # sort the list of recipes in alphabetical order
        recipes = self.domain.get_objects()
        recipes = sorted(recipes, key=lambda recipe: recipe[0])

        # generate the expected output, shown below, from the above using the
        # first letter of the recipe as a key to group thing
        #
        # name, subtype, docname, anchor, extra, qualifier, description
        for _name, dispname, typ, docname, anchor, _priority in recipes:
            content[dispname[0].lower()].append(
                (dispname, 0, docname, anchor, docname, '', typ)
            )

        # convert the dict to sorted list of tuples expected
        content = sorted(content.items())

        return content, True


class RecipeDomain(Domain):
    name = 'recipe'
    label = 'Recipe Sample'
    roles = {
        'ref': XRefRole(),
    }
    directives = {
        'recipe': RecipeDirective,
    }
    indices = {
        RecipeIndex,
        IngredientIndex,
    }
    initia_data = {
        'recipes': [],  # object list
        'recipe_ingredients': {},  # name -> object
    }

    def get_full_qualified_name(self, node):
        return f'recipe.{node.arguments[0]}'

    def get_objects(self):
        yield from self.data['recipes']

    def resolve_xref(
            self, env, fromdocname, builder, typ, target, node, contnode
    ):
        
    
