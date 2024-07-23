- Gym items are given in Function 3, separate from the badge. Both will need to be patched out. Badge check is before the fight every time and should be patched out (since we want to break that)
- Badge Gives are in the callee, easily patched out in a couple seconds.
- We can trigger AP Item gives via one of the unused flags and have BizHawk set the flag back to 0. There is variable addresses as well that are unused so we can communicate item IDs for give/send.

- Script 125 for initial patches