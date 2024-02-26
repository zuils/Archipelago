## Accessing Memory
- Pokémon Platinum and the other DS games load the save file and other assets dynamically into memory. Therefore, we need to dynamically calculate the base address for the various structures we need to access in RAM. This is done by loading the Global Pointer (0xBA8) as a u24_le, to then load the Version Pointer (Global Pointer + 0x20) as a u24_le, which gives us the start of the save file. To line up with what is saved to file, we offset the Version Pointer by 0x14 and then can access anything in the save file from there by offsets.
## Known Free Variable Addresses
- Scripts in Pokémon Platinum use the following addresses in it's script language to access various things in memory. The table is know but not all of them are free for our use since the game uses most of these for itself. Here is the table, contributed by Silvris:
```
   Local variables [values are reset when the mapheader changes]
	0x4000-0x401F --- Generic purpose
	
	Script variables [values are reset when the script ends]
	0x8000-0x800C ---  Generic purpose 
	
	NPC sprite variables [seemingly persistent]
	0x4020-0x402F
	
	System-reserved [Persistent]
	0x4030-0x406F
	
	Storyline variables [Persistent]
	0x4070-0x411F
```
## FPS Patch
More of a note if we have to revert at any point to the base rom to redo this patch.
https://www.pokecommunity.com/threads/d-p-pt-hg-ss-remove-the-framerate-limiter.378618/ 

## Known Flags
https://docs.google.com/spreadsheets/d/1ks_zdpFXojbfD-u-h2z92y-bcwoGBBvZ3kmvjOvt2Sg/edit?usp=sharing

## Rom Script
- The Rom Script Language is well documented by our primary tool, DSPRE but not all the script files are documented. Below is the ones we care the most about:
	- Visible Item Handler: Script 404
	- Hidden Item Handler: (Apparently I didn't note this down.... it's near the Visible Item Handler and easily searchable)
	- Item Name Archive: Text Archive 392 and near by files. One of these specify a/an, the other is a formatted string for printing the item name.