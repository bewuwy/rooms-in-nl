## Config for ROOM.nl
## Copy this file to roomnl_config.py and fill in the values

# Set to True to search only for rooms with priority
SEARCH_PRIORITY = True

# Copy this value from the browser console from payload of the 
# POST request to "https://roomapi.hexia.io/api/v1/actueel-aanbod" 
# when visiting "https://www.room.nl/en/offerings/to-rent"
ROOMNL_CONFIG = {
    "hidden-filters": {"$and": [{"dwellingType.categorie": {"$eq": "woning"}}, {"rentBuy": {"$eq": "Huur"}}, {"isExtraAanbod": {"$eq": ""}}, {"isWoningruil": {"$eq": ""}}, {"$and": [{"$or": [{"street": {"$like": ""}}, {"houseNumber": {"$like": ""}}, {"houseNumberAddition": {"$like": ""}}]}, {"$or": [{"street": {"$like": ""}}, {"houseNumber": {"$like": ""}}, {"houseNumberAddition": {"$like": ""}}]}]}, {"$and": [{"reactionData.isPassend": {"$eq": "1"}}]}]},
    "woningzoekende": {
        
    }
}
