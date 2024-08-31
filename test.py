import asyncio
from esologs.client import Client
from access_token import get_access_token

API_ENDPOINT = "https://www.esologs.com/api/v2/client"
ACCESS_TOKEN = get_access_token()

async def test_queries():
    async with Client(url=API_ENDPOINT, headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}) as client:

        try:
            # Test getAbility with a specific ID
            ability_id = 1084 
            ability_response = await client.get_ability(id=ability_id)
            print("Get Ability Response:", ability_response)
        except Exception as e:
            print(f"An error occurred during get_ability: {e}")

        try:
            # Test getAbilities
            abilities_response = await client.get_abilities(limit=100, page=1)
            print("Get Abilities Response:", abilities_response)
        except Exception as e:
            print(f"An error occurred during get_abilities: {e}")

        try:
            # Test getClass with a specific ID
            class_id = 1   
            class_response = await client.get_class(id=class_id)
            print("Get Class Response:", class_response)
        except Exception as e:
            print(f"An error occurred during get_class: {e}")

        try:
            # Test getClasses
            classes_response = await client.get_classes()
            print("Get Classes Response:", classes_response)
        except Exception as e:
            print(f"An error occurred during get_classes: {e}")

        try:
            # Test getFactions
            factions_response = await client.get_factions()
            print("Get Factions Response:", factions_response)
        except Exception as e:
            print(f"An error occurred during get_factions: {e}")

        try:
            # Test getItem with a specific ID
            item_id = 19  
            item_response = await client.get_item(id=item_id)
            print("Get Item Response:", item_response)
        except Exception as e:
            print(f"An error occurred during get_item: {e}")

        try:
            # Test getItemSet with a specific ID
            item_set_id = 19 
            item_set_response = await client.get_item_set(id=item_set_id)
            print("Get Item Set Response:", item_set_response)
        except Exception as e:
            print(f"An error occurred during get_item_set: {e}")

        try:
            # Test getItemSets
            item_sets_response = await client.get_item_sets(limit=100, page=1)
            print("Get Item Sets Response:", item_sets_response)
        except Exception as e:
            print(f"An error occurred during get_item_sets: {e}")

        try:
            # Test getItems
            items_response = await client.get_items(limit=100, page=1)
            print("Get Items Response:", items_response)
        except Exception as e:
            print(f"An error occurred during get_items: {e}")

        try:
            # Test getMap with a specific ID
            map_id = 1  
            map_response = await client.get_map(id=map_id)
            print("Get Map Response:", map_response)
        except Exception as e:
            print(f"An error occurred during get_map: {e}")

        try:
            # Test getMaps
            maps_response = await client.get_maps(limit=100, page=1)
            print("Get Maps Response:", maps_response)
        except Exception as e:
            print(f"An error occurred during get_maps: {e}")

        try:
            # Test getNPC with a specific ID
            npc_id = 1  
            npc_response = await client.get_npc(id=npc_id)
            print("Get NPC Response:", npc_response)
        except Exception as e:
            print(f"An error occurred during get_npc: {e}")

        try:
            # Test getNPCs
            npcs_response = await client.get_np_cs(limit=100, page=1)
            print("Get NPCs Response:", npcs_response)
        except Exception as e:
            print(f"An error occurred during get_npcs: {e}")

        try:
            # Test getZones (replacing get_world_data)
            zones_response = await client.get_zones()
            print("Get Zones Response:", zones_response)
        except Exception as e:
            print(f"An error occurred during get_zones: {e}")

        try:
            # Test getCharacterById
            character_id = 34663  
            character_response = await client.get_character_by_id(id=character_id)
            print("Get Character By ID Response:", character_response)
        except Exception as e:
            print(f"An error occurred during get_character_by_id: {e}")

        try:
            # Test getCharacterEncounterRanking
            encounter_id = 27  
            character_ranking_response = await client.get_character_encounter_ranking(
                character_id=character_id, encounter_id=encounter_id)
            print("Get Character Encounter Ranking Response:", character_ranking_response)
        except Exception as e:
            print(f"An error occurred during get_character_encounter_ranking: {e}")

        try:
            # Test getCharacterReports
            character_reports_response = await client.get_character_reports(character_id=character_id, limit=10)
            print("Get Character Reports Response:", character_reports_response)
        except Exception as e:
            print(f"An error occurred during get_character_reports: {e}")

        try:
            # Test getEncountersByZone
            zone_id = 1  
            encounters_response = await client.get_encounters_by_zone(zone_id=zone_id)
            print("Get Encounters By Zone Response:", encounters_response)
        except Exception as e:
            print(f"An error occurred during get_encounters_by_zone: {e}")

        try:
            # Test getGuildById
            guild_id = 3660  
            guild_response = await client.get_guild_by_id(guild_id=guild_id)
            print("Get Guild By ID Response:", guild_response)
        except Exception as e:
            print(f"An error occurred during get_guild_by_id: {e}")

        try:
            # Test getRegions
            regions_response = await client.get_regions()
            print("Get Regions Response:", regions_response)
        except Exception as e:
            print(f"An error occurred during get_regions: {e}")

        try:
            # Test getReportByCode
            report_code = "VfxqaX47HGC98rAp"  
            report_response = await client.get_report_by_code(code=report_code)
            print("Get Report By Code Response:", report_response)
        except Exception as e:
            print(f"An error occurred during get_report_by_code: {e}")

        try:
            # Test getRateLimitData
            rate_limit_response = await client.get_rate_limit_data()
            print("Get Rate Limit Data Response:", rate_limit_response)
        except Exception as e:
            print(f"An error occurred during get_rate_limit_data: {e}")

# Run the async test function
if __name__ == "__main__":
    asyncio.run(test_queries())

