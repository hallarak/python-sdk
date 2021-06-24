import argparse
import sys
import pandas as pd
from typing import List, Sequence
from dateutil import tz

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.client.api.data_classes.relationship_type import RelationshipType
from exabel_data_sdk.client.api.data_classes.signal import Signal

from exabel_data_sdk.scripts.base_script import BaseScript

class SetupTestCase(BaseScript):

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--namespace",
            required=True,
            type=str,
            help="Namespace for this script",
        )
        self.parser.add_argument(
            "--teardown",
            required=False,
            action="store_true",
            default=False,
            help="Remove all entities and relationships"
        )

    def setupBrandAndRelationship(
        self,
        client: ExabelClient,
        namespace: str,
        company: Entity,
        brand_name: str,
        relationship_type: RelationshipType
    ) -> Entity:

        # Create new brand entity.
        brand_entity_name = f"entityTypes/brand/entities/{namespace}.{brand_name.lower()}"
        if not client.entity_api.entity_exists(brand_entity_name):
          brand_entity = client.entity_api.create_entity(
              Entity(
                  name=brand_entity_name,
                  display_name=brand_name,
                  description="This is the description",
                  properties={},
              ),
              entity_type="entityTypes/brand",
          )
          print(f"Created {brand_name} entity: {brand_entity}")
        else:
          brand_entity = client.entity_api.get_entity(brand_entity_name)

        if not client.relationship_api.relationship_exists(
            relationship_type.name, company.name, brand_entity.name):
          has_brand_relationship = client.relationship_api.create_relationship(
              Relationship(
                  description="Relationship between company and brand.",
                  relationship_type=relationship_type.name,
                  from_entity=company.name,
                  to_entity=brand_entity.name,
                  properties={},
              )
          )
          print(f"Created relationship: {has_brand_relationship}")
        return brand_entity

    def setupBrandItemTypeAndRelationship(
        self,
        client: ExabelClient,
        namespace: str,
        brand: Entity,
        brand_name: str,
        item_type: str,
        relationship_type: RelationshipType
    ) -> Entity:
        brand_item_type_name = f"entityTypes/brand_and_item/entities/" \
                               f"{namespace}.{brand_name.lower()}-{item_type.lower()}"
        brand_item_type_entity = client.entity_api.get_entity(brand_item_type_name)
        if brand_item_type_entity is None:
          brand_item_type_entity = client.entity_api.create_entity(
              Entity(
                  name=brand_item_type_name,
                  display_name=f"{brand_name} - {item_type}",
                  description="This is the description",
                  properties={},
              ),
              entity_type="entityTypes/brand_and_item",
          )

        if not client.relationship_api.relationship_exists(
            relationship_type.name, brand.name, brand_item_type_entity.name):
          brand_item_type_relationship = client.relationship_api.create_relationship(
              Relationship(
                  description=f"Relationship between {brand_name} and {item_type}.",
                  relationship_type=relationship_type.name,
                  from_entity=brand.name,
                  to_entity=brand_item_type_entity.name,
                  properties={},
              )
          )
        return brand_item_type_entity

    def setupProductToItemWithRelationship(
        self,
        client: ExabelClient,
        namespace: str,
        product_name: str,
        item_name: str,
        relationship_type: RelationshipType,
        ) -> (Entity, Entity):
      product_entity_name = f"entityTypes/product_type/entities/{namespace}.{product_name.lower()}"
      if not client.entity_api.entity_exists(product_entity_name):
        product_entity = client.entity_api.create_entity(
            Entity(
                name=product_entity_name,
                display_name=f"{product_name}",
                description="This is the description",
                properties={},
            ),
            entity_type="entityTypes/product_type",
        )
      else:
        product_entity = client.entity_api.get_entity(product_entity_name)

      item_entity_name = f"entityTypes/item_type/entities/{namespace}.{item_name.lower()}"
      if not client.entity_api.entity_exists(item_entity_name):
        item_entity = client.entity_api.create_entity(
            Entity(
                name=item_entity_name,
                display_name=f"{item_name}",
                description="This is the description",
                properties={},
            ),
            entity_type="entityTypes/item_type",
        )
      else:
        item_entity = client.entity_api.get_entity(item_entity_name)

      if not client.relationship_api.relationship_exists(
          relationship_type.name, product_entity.name, item_entity.name):
        product_item_relationship = client.relationship_api.create_relationship(
            Relationship(
                description=f"Relationship between {product_name} and {item_name}.",
                relationship_type=relationship_type.name,
                from_entity=product_entity.name,
                to_entity=item_entity.name,
                properties={},
            )
        )
        print(f"created relationship from {product_entity.name} to {item_entity.name}")
      return product_entity, item_entity

    def delete_entity(self, client: ExabelClient, entity_name: str) -> None:
      if client.entity_api.entity_exists(name=entity_name):
        client.entity_api.delete_entity(entity_name)
        print(f"deleted {entity_name}")
      else:
        print(f"not deleted: {entity_name}")

    def cleanup(self,
        client: ExabelClient,
        args: argparse.Namespace,
        companies_setup: dict,
        product_item_setup: List[dict]) -> None:
        #
        # for company in companies_setup.keys():
        #     brands = companies_setup.get(company).get("brands")
        #     for brand in brands:
        #         brand_name = brand["name"].lower()
        #         self.delete_entity(client,
        #                            f"entityTypes/brand/entities/"
        #                           f"{args.namespace}.{brand_name}")
        #         item_types = brand["item_types"]
        #         for item_type in item_types:
        #             item_type = item_type.lower()
        #             self.delete_entity(client,
        #                                f"entityTypes/brand_and_item/entities/"
        #                                f"{args.namespace}.{brand_name}-{item_type}")
        #
        # for product_item in product_item_setup:
        #   product_name = product_item["product"].lower()
        #   self.delete_entity(client,
        #                      f"entityTypes/product_type/entities/"
        #                      f"{args.namespace}.{product_name}")
        #   item_name = product_item["item"].lower()
        #   self.delete_entity(client,
        #                      f"entityTypes/item_type/entities/"
        #                      f"{args.namespace}.{item_name}")
        try:
            client.relationship_api.delete_relationship_type(f"relationshipTypes/{args.namespace}.HAS_BRAND")
            print(f"deleted relationshipTypes/{args.namespace}.HAS_BRAND")
        except Exception as e:
            print(f"could not remove relationship type '{args.namespace}.HAS_BRAND': {e}")

        try:
            client.relationship_api.delete_relationship_type(f"relationshipTypes/{args.namespace}.HAS_ITEM_TYPE")
            print(f"deleted relationshipTypes/{args.namespace}.HAS_ITEM_TYPE")
        except Exception as e:
            print(f"could not remove relationship type '{args.namespace}.HAS_ITEM_TYPE': {e}")

        # try:
        #     client.signal_api.delete_signal(f"signals/{args.namespace}.viscacha_signal1")
        #     print(f"deleted signal signals/{args.namespace}.viscacha_signal1")
        #     client.signal_api.delete_signal(f"signals/{args.namespace}.viscacha_signal2")
        #     print(f"deleted signal signals/{args.namespace}.viscacha_signal2")
        # except:
        #     print(f"could not remove signal - does not exist")

    def load_signals(self, client: ExabelClient, args: argparse.Namespace, signal_setup: List):
        for signal in signal_setup:
            signal_name = f"entityTypes/brand_and_item/entities/{args.namespace}." \
                          + signal["brand"].lower() \
                          + "-" \
                          + signal["item_type"].lower() \
                          + f"/signals/{args.namespace}." + signal["signal"]
            print(f"signal_name :" + signal_name)
            series = pd.Series(
                signal["values"],
                signal["dates"]
            )
            if not client.time_series_api.time_series_exists(signal_name):
              client.time_series_api.create_time_series(signal_name, series)
              print(f"created signal for {signal}")
            else:
              client.time_series_api.append_time_series_data(signal_name, series)
              print(f"appended signal for {signal}")

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:

        """
        python -m viscacha_test_model --api-key <API-KEY> --exabel-api-host data.api-test.exabel.com --namespace test --teardown
        """

        product_item_setup = [
          {
            "product": "Kitchen",
            "item": "Coffee_and_Espresso"
          },
          {
            "product": "Kitchen",
            "item": "Cereals"
          },
          {
            "product": "Entertainment",
            "item": "Movies"
          },
          {
            "product": "Accessories",
            "item": "Jewelry"
          },
          {
            "product": "Accessories",
            "item": "Accessories"
          }
        ]

        companies_setup = {"Nestle": {"isin": "CH0038863350",
                                      "brands": [
                                          {"name": "Cheerios",
                                           "item_types": ["Cereals", "Food"]},
                                          {"name": "Nespresso",
                                           "item_types": ["Coffee_and_Espresso", "Food"]}
                                      ]},
                           "The Walt Disney Company": {"isin": "US2546871060",
                                                       "brands": [
                                                           {"name": "Disney",
                                                            "item_types": ["Movies", "Jewelry"]},
                                                           {"name": "Mickey_Mouse",
                                                            "item_types": ["Movies", "Accessories"]}
                                                       ]}
                           }

        signal_setup = [{"signal": "viscacha_signal1",
                         "brand": "Disney",
                         "item_type": "Movies",
                         "values": [1, 2, 10, 11, 12],
                         "dates": pd.DatetimeIndex(["2021-01-01", "2021-01-02", "2021-01-03", "2021-01-04", "2021-01-05"], tz=tz.tzutc()),
                        },
                        {"signal": "viscacha_signal2",
                         "brand": "Disney",
                         "item_type": "Movies",
                         "values": [3, 4, 13, 14, 15],
                         "dates": pd.DatetimeIndex(["2021-01-01", "2021-01-02", "2021-01-03", "2021-01-04", "2021-01-05"], tz=tz.tzutc()),
                         },
                        {"signal": "viscacha_signal1",
                         "brand": "Disney",
                         "item_type": "Jewelry",
                         "values": [5, 6, 16, 17, 18],
                         "dates": pd.DatetimeIndex(["2021-01-01", "2021-01-02", "2021-01-03", "2021-01-04", "2021-01-05"], tz=tz.tzutc()),
                         },
                         {"signal": "viscacha_signal2",
                         "brand": "Disney",
                         "item_type": "Jewelry",
                         "values": [7, 8, 19, 20, 21],
                         "dates": pd.DatetimeIndex(["2021-01-01", "2021-01-02", "2021-01-03", "2021-01-04", "2021-01-05"], tz=tz.tzutc()),
                         },
                        {"signal": "viscacha_signal1",
                         "brand": "Mickey_Mouse",
                         "item_type": "Accessories",
                         "values": [9, 10, 29, 30, 31],
                         "dates": pd.DatetimeIndex(["2021-01-01", "2021-01-02", "2021-01-03", "2021-01-04", "2021-01-05"], tz=tz.tzutc()),
                         },
                        {"signal": "viscacha_signal2",
                         "brand": "Mickey_Mouse",
                         "item_type": "Accessories",
                         "values": [100, 101, 102, 103, 104],
                         "dates": pd.DatetimeIndex(["2021-01-01", "2021-01-02", "2021-01-03", "2021-01-04", "2021-01-05"], tz=tz.tzutc()),
                         },
                        ]

        self.cleanup(client, args, companies_setup, product_item_setup)

        # need some relationship types (setup)
        # Create a new HAS_BRAND relationship type.
        has_brand_type_name = f"relationshipTypes/{args.namespace}.HAS_BRAND"
        try:
          has_brand_type = client.relationship_api.create_relationship_type(
              RelationshipType(
                  name=has_brand_type_name,
                  description="The owner of a brand, usually a company",
                  properties={},
              )
          )
          print(f"Created relationship type: {has_brand_type}")
        except:
          has_brand_type = client.relationship_api.get_relationship_type(has_brand_type_name)
          print(f"{has_brand_type_name} exists")

        # Create a new HAS_ITEM_TYPE relationship type.
        has_item_type_name = f"relationshipTypes/{args.namespace}.HAS_ITEM_TYPE"
        try:
          has_item_type = client.relationship_api.create_relationship_type(
              RelationshipType(
                  name=has_item_type_name,
                  description="Item type",
                  properties={},
              )
          )
          print(f"Created relationship type: {has_item_type}")
        except:
          has_item_type = client.relationship_api.get_relationship_type(has_item_type_name)
          print(f"{has_item_type_name} exists")

        for product_item in product_item_setup:
          product_name = product_item["product"]
          item_name = product_item["item"]
          product_entity, item_entity = \
            self.setupProductToItemWithRelationship(
                client, args.namespace, product_name, item_name, has_item_type)

        for company in companies_setup.keys():
            isin = companies_setup.get(company).get("isin")
            entities = client.entity_api.search_for_entities(entity_type='entityTypes/company', isin=isin)
            if len(entities) == 1:
                company_entity = entities[0]
            else:
                print(f"did not find exactly 1 company - found {len(entities)}")
                break
            brands = companies_setup.get(company).get("brands")
            for brand in brands:
                brand_name = brand["name"]
                brand_entity = self.setupBrandAndRelationship(
                    client, args.namespace, company_entity, brand_name, has_brand_type
                )
                item_types = brand["item_types"]
                for item_type in item_types:
                    item_type = item_type.lower()
                    brand_item_type_entity = \
                        self.setupBrandItemTypeAndRelationship(
                            client,
                            args.namespace,
                            brand_entity, brand_name,
                            item_type, has_item_type)
                    item_entity = client.entity_api.get_entity(
                        f"entityTypes/item_type/entities/{args.namespace}.{item_type}")
                    if item_entity is not None:
                        if not client.relationship_api.relationship_exists(
                          has_brand_type.name, item_entity.name, brand_item_type_entity.name):
                          client.relationship_api.create_relationship(
                              Relationship(
                                  description=f"Relationship between {item_entity} and {brand_item_type_entity}.",
                                  relationship_type=has_brand_type.name,
                                  from_entity=item_entity.name,
                                  to_entity=brand_item_type_entity.name,
                                  properties={},
                              )
                          )
                          print(f"created relationship between {item_entity} and {brand_item_type_entity}")
                    else:
                      print(f"whoops! no item_entity for {item_type.lower()}")

        # need some signals
        # Add a signal.
        # signal1 = client.signal_api.create_signal(
        #     Signal(
        #         name=f"signals/{args.namespace}.viscacha_signal1",
        #         display_name="Signal 1",
        #         description="description",
        #         entity_type="entityTypes/brand_and_item",
        #     )
        # )
        # print("added signal signals/{args.namespace}.viscacha_signal1")
        # signal2 = client.signal_api.create_signal(
        #     Signal(
        #         name=f"signals/{args.namespace}.viscacha_signal2",
        #         display_name="Signal 2",
        #         description="description",
        #         entity_type="entityTypes/brand_and_item",
        #     )
        # )
        # print("added signal signals/{args.namespace}.viscacha_signal2")

        self.load_signals(client, args, signal_setup)

        if (args.teardown):
            self.cleanup(client, args, companies_setup, product_item_setup)

if __name__ == "__main__":
    SetupTestCase(sys.argv, "Set up test case.").run()
