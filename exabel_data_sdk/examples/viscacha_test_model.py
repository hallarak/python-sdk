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
        brand_entity = client.entity_api.create_entity(
            Entity(
                name=f"entityTypes/brand/entities/{namespace}.{brand_name.lower()}",
                display_name=brand_name,
                description="This is the description",
                properties={},
            ),
            entity_type="entityTypes/brand",
        )
        print(f"Created {brand_name} entity: {brand_entity}")

        has_brand_relationship = client.relationship_api.create_relationship(
            Relationship(
                description="Relationship between Nestle and Cheerios.",
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
        brand_item_type_entity = client.entity_api.create_entity(
            Entity(
                name=f"entityTypes/brand_and_item/entities/{namespace}.{brand_name.lower()}-{item_type.lower()}",
                display_name=f"{brand_name} - {item_type}",
                description="This is the description",
                properties={},
            ),
            entity_type="entityTypes/brand_and_item",
        )

        brand_item_type_relationship = client.relationship_api.create_relationship(
            Relationship(
                description=f"Relationship between {brand_name} and {item_type}.",
                relationship_type=relationship_type.name,
                from_entity=brand.name,
                to_entity=brand_item_type_entity.name,
                properties={},
            )
        )
        return brand_item_type_entity;

    def cleanup(self,
        client: ExabelClient,
        args: argparse.Namespace,
        companies_setup: dict) -> None:

        for company in companies_setup.keys():
            brands = companies_setup.get(company).get("brands")
            print(f"brands: {brands}")
            for brand in brands:
                print(f"brand: {brand}")
                brand_name = brand["name"].lower()
                print(f"brand_name: {brand_name}")
                if client.entity_api.entity_exists(
                    name=f"entityTypes/brand/entities/{args.namespace}.{brand_name}"):
                    client.entity_api.delete_entity(
                        f"entityTypes/brand/entities/{args.namespace}.{brand_name}")
                    print(f"deleted entityTypes/brand/entities/{args.namespace}.{brand_name}")
                item_types = brand["item_types"]
                for item_type in item_types:
                    item_type = item_type.lower()
                    print(f"brand_item_type = {item_type}")
                    if client.entity_api.entity_exists(
                        name=f"entityTypes/brand_and_item/entities/{args.namespace}."
                             f"{brand_name}-{item_type}"):
                        client.entity_api.delete_entity(
                            f"entityTypes/brand_and_item/entities/{args.namespace}."
                            f"{brand_name}-{item_type}")
                        print(f"deleted entityTypes/brand_and_item/entities/{args.namespace}."
                              f"{brand_name}-{item_type}")

        try:
            client.relationship_api.delete_relationship_type(f"relationshipTypes/{args.namespace}.HAS_BRAND_JEJ")
            print(f"deleted relationshipTypes/{args.namespace}.HAS_BRAND_JEJ")
            client.relationship_api.delete_relationship_type(f"relationshipTypes/{args.namespace}.HAS_ITEM_TYPE_JEJ")
            print(f"deleted relationshipTypes/{args.namespace}.HAS_ITEM_TYPE_JEJ")
        except:
            print(f"could not remove relationship type - does not exist")
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
            client.time_series_api.create_time_series(
                signal_name,
                pd.Series(
                    signal["values"],
                    signal["dates"]
                )
            )
            print(signal)

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:

        """
        python -m viscacha_test_model --api-key <API-KEY> --exabel-api-host data.api-test.exabel.com --namespace test --teardown
        """

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
                         "values": [1, 2],
                         "dates": pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                        },
                        {"signal": "viscacha_signal2",
                         "brand": "Disney",
                         "item_type": "Movies",
                         "values": [3, 4],
                         "dates": pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                         },
                        {"signal": "viscacha_signal1",
                         "brand": "Disney",
                         "item_type": "Jewelry",
                         "values": [5, 6],
                         "dates": pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                         },
                         {"signal": "viscacha_signal2",
                         "brand": "Disney",
                         "item_type": "Jewelry",
                         "values": [7, 8],
                         "dates": pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                         }]

        self.cleanup(client, args, companies_setup)

        # need some relationship types (setup)
        # Create a new HAS_BRAND relationship type.
        has_brand_type = client.relationship_api.create_relationship_type(
            RelationshipType(
                name=f"relationshipTypes/{args.namespace}.HAS_BRAND_JEJ",
                description="The owner of a brand, usually a company",
                properties={},
            )
        )
        print(f"Created relationship type: {has_brand_type}")

        # Create a new HAS_ITEM_TYPE relationship type.
        has_item_type = client.relationship_api.create_relationship_type(
            RelationshipType(
                name=f"relationshipTypes/{args.namespace}.HAS_ITEM_TYPE_JEJ",
                description="Segment",
                properties={},
            )
        )
        print(f"Created relationship type: {has_item_type}")

        for company in companies_setup.keys():
            print(company)
            isin = companies_setup.get(company).get("isin")
            print(isin)
            entities = client.entity_api.search_for_entities(entity_type='entityTypes/company', isin=isin)
            if len(entities) == 1:
                company_entity = entities[0]
                print(f"company: {company_entity}")
            else:
                print(f"did not find exactly 1 company - found {len(entities)}")
                break;
            brands = companies_setup.get(company).get("brands")
            print(f"brands: {brands}")
            for brand in brands:
                print(f"brand: {brand}")
                brand_name = brand["name"]
                print(f"brand_name: {brand_name}")
                brand_entity = self.setupBrandAndRelationship(
                    client, args.namespace, company_entity, brand_name, has_brand_type
                )
                item_types = brand["item_types"]
                for item_type in item_types:
                    item_type = item_type.lower()
                    print(f"brand_item_type = {item_type}")
                    brand_item_type_entity = \
                        self.setupBrandItemTypeAndRelationship(
                            client,
                            args.namespace,
                            brand_entity, brand_name,
                            item_type, has_item_type)

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
            self.cleanup(client, args, companies_setup)

if __name__ == "__main__":
    SetupTestCase(sys.argv, "Set up test case.").run()
