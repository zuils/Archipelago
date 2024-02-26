
## Coding Style/Standards

### General Guidelines
- Commit messages must follow the provided format:
	- `Module: Short Description of Patch
- Please specify any additional details in the lines following this short description to better specify what has been changed in this patch
- Please create an issue and PR when you start work on a particular piece if one does not already exist. 
- YOU CANNOT UPLOAD ANYTHING THAT IS DIRECTLY FROM THE ROM FILE. THIS IS COPYRIGHT INFRINGEMENT AND WILL GET YOUR COMMIT DENIED IMMEDIATELY.
### Rom Patches
- The base patch is based on the following ROM and all contributors are expected to dump this from their legally owned copy of the game. Guidance on how to do this will not be provided.
	- Rom Header: `"POKEMON PL" (CPUE01, Rev.00)`
	- SHA1: `ce81046eda7d232513069519cb2085349896dec7  POKEMON_PL_CPUE01_00.nds
- All rom patches must be based on the latest base patch at the time of submission. You are required to keep these up to date with the latest base patch until it is ready to be merged.
- The latest base patch is created every 2 weeks if there is new patches to merge in. 
- If you are patching something with a code change based on the [pret/pokeplatinum](https://github.com/pret/pokeplatinum) project, please note what sha build is used for your patch and provide a patch file to allow project maintainers to check over your code change.
- If you need to use one of the unused item ids, save file variables, or similar in your patch, please ensure that you update the associated charts so we are aware of what you are using. The Pal Park region is reserved for Pokemon objects and any other usage will NOT be allowed.
### JSON Contributions
- All object types should be in their own JSON file as to allow for better modularity. This may be merged at some point in the future so any key values should be unique
- Any IDs should be project specific and will be transposed into a multiworld compatible number by the world script. This is so we can be compatible with ALL other multiworlds.
- Any internal ids requested should be specified as an offset from the start of the table for that object. 
### Python/World Contributions
- Python code must follow the PEP 8 code standard and must contain type hints if you are able to provide them. If not, please leave a comment saying why the type is not specified.
- An Any type specifier is allowed but also requires a comment to say what data types is supported by this function.
- Please follow the contributing guidelines from Archipelago [contributing](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/contributing.md) as we do intend to upstream this once it is stable.
## Licensing
  All contributors MUST agree to license this project and their contributions under the MIT license and MAY NOT include or be derived from ANY GPL code. This is per the Archipelago terms. 
