## JSON
- Full list of items and what flag triggers them (items.json)
```json
{
	"tag": "ITEM_RAVAGED_PASS_LUCK_INCENSE",
	"long_description": "Ravaged Pass - Left Item behind Surf",
	"location": "LOCATION_RAVAGED_PASS",
	"item_flag": "0x402",
	"vanilla_item": 251,
	"requirements": ["HM_SURF & HM_ROCK_SMASH"]
}
```
- Full list of all hidden items and what flag triggers them (hidden_items.json)
```json
{
	"tag": "HIDDEN_ITEM_VICTORY_ROAD_2F_RARE_CANDY",
	"long_description":"Victory Road 2F - Hidden Item near Ace Trainer Omar",
	"location": "LOCATION_VICTORY_ROAD_2F",
	"item_flag": "0x34E",
	"vanilla_item": 50,
	"requirements": ["HM_STRENGTH", "HM_ROCK_SMASH"]
}
```
- Full list of locations and where they connect to (connections.json)
- Please treat each and every map change as a connection for now. We may optimize this later to group them into access sections instead of just marking every connection for generation speed. I prefer full accuracy first, optimize later.
```json
{
	"tag": "LOCATION_ROUTE_201",
	"connections": ["LOCATION_VERITY_LAKEFRONT", "LOCATION_TWINLEAF_TOWN", "LOCATION_SANDGEM_TOWN"],
	"requirements": []
}
```
- Trigger Flags, think NPC/Button/Door activations that cause things to unlock (triggers.json)
```json
{
	"tag": "TRIGGER_OREBURGH_MINES_ROARK",
	"location": "LOCATION_OREBURGH_MINES_LOWER",
	"trigger_flag": "",
	"trigger_group": "EVENT",
	"requirements": []
}
```
- Full list of ALL trainers in the game and where they are located (trainers.json)
```json
{
	"tag": "TRAINER_ACE_TRAINER_OMAR",
	"location": "LOCATION_VICTORY_ROAD_",
	"trigger_flag": "0x630",
	"requirements": ["HM_STRENGTH", "HM_ROCK_SMASH"]
}
```
## ROM Patches
#### AP REQUIREMENTS:
- Finish installing our AP item injection script on ALL maps as well as setting up the Level Scripts. This is just tedious, no additional programming needed. Details are in issue #
- We need a spot to put all the received items at, set this up within the string tables since this is free real estate for us to work with as only AP is changing it.
- We need to setup a spot to put our rom signatures. Also thinking this should be in a string table, just needs to be setup with a placeholder for now. Structure Idea:
```json
{
	"slot_id": 0,
	"slot_name": "",
	"ap_patch_version": "1.0",
	"options": ["RANDOMIZE_BADGES", "RANDOMIZE_HMS"],
	"options_checksum": ""
}
```
#### User Experience:
- Tidy up and make the custom badge items a bit fancier. Currently they just give you the badge with no fanfare or anything beyond a basic item. Details in issue #
- Fix all badge checks and replace them with trainer beat checks (check for the trainer flag instead of the badge). The game assumes that if you have the badge, you beat the gym leader. We break this logic just by being AP and randomizing TMs/HMs/Badges across multiple worlds.
- ~~FPS Patch~~ (Already implemented in the base patch, this was changing 2 bytes to unlock the framerate)
- Fix Pokemon evolutions. Please keep with the standards set by Pokemon Emerald, please ask about any new evolution methods if it's not covered here.
#### Additional AP Options
- Full Shops? This is a common patch for AP Pokemon games to unlock all items in all shops but IK PL has progressive shops based on badge count so this may not be doable at current time.
- Poketch skip. This may be a ROM patch or just a flag we set with the Python client
- Remove Boulders/Progression Blocks
#### Long Term (waiting on better decomp/research):
- Support randomization of TM moves
- Support Gen 3 Physical/Special Split
- Support randomization of types
## AP World
- Practically everything. What's here is basically a clone of the Pokemon Emerald AP world with changed names. A bunch of the logic requires the JSON files being ready to go.
- BizHawk needs to be able to deal with the Dynamic loading of the save file and other content. This is done by doing a pointer trick to get the start of the save file. See the test.lua script, this does it to find the player name/money on every load since this changes every load if the time is not locked.
