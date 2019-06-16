# steam-reviews.py
Simple Python command-line script that retrieves better reviews than those found on the Steam store page.

Usage: `steam-reviews.py appId [positive | negative | all] [last x days]`

`appId` (mandatory): the product identifier on Steam, which can be easily found through its store page address. For example: the `appId` for *The Beginner's Guide* is `303210` (its address being https://store.steampowered.com/app/303210/The_Beginners_Guide/).

`positive | negative | all` (optional): show only negative or positive reviews. If not present, will default to `all`. Note that you need to explicitly provide a value here if you want to use the next parameter.

`last x days` (optional): number of days counting back from the current date to include reviews for.

Note that the script makes a single request to the Steamworks web API, so it's by no means an exhaustive search - but still qualitatively better than the reviews shown on the Steam store page (which apprently focus on a very limited time-frame only, even when you explicitly ask for the entire lifetime of the product to be considered). Hopefully Valve will improve things some day!

Steamworks web API reference https://partner.steamgames.com/doc/store/getreviews
