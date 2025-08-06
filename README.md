## Len's Local Brewery

You can share different brews of **Coffee**, **Tea** and **Beer**. The brewes can be viewed by unauthenticated users. Create an account and share your brew with us!

###### \*The project is only done for the purpose of learning django and is not intended for public use.

### Features and Structure

#### Routing:

- `/` → Home (Bean List)
- `/brews/` → Global Brew History
- `/my-journal/` → User’s personal brew log
- `/add-brew/` → Form for new entries
- `/edit-brew/<id>/` → Edit existing entry
- `/login/`, `/register/`, `/logout/` → Auth views

#### Brew post data:

- brew_name: (e.g., New Earl Gray)
- brew_type: (e.g., Coffee / Tea / Beer) (dropdown)
- brew_method (e.g., French Press, Espresso, Pour Over) ( need validation (e.g., "Espresso" shouldn’t be selectable for "Tea").)
- brew_time (e.g., 10 minute 32 seconds.)
- seed_origin: (e.g.,Turkey, Colombia, Ethiopia (Bean, Leaf or etc. origin. )) `[Many Beans → One Origin]`
- seed_name: (e.g., Beans: Yirgacheffe, Sidamo. Tea Leaves: Sencha, Matcha, Ceylon, Keemun. ) `[Many brews -> One bean]`
- roast_level: (e.g., For coffee: Light, Medium, Dark)
- rating: (1-10) (dropdown)
- notes: (e.g., The proccess takes too much time.)
- post_date: (e.g., 03:44 PM / 12 May / 2025) (Automatically generated after post is published.)
- post_id: UUID

#### Data relations:

1. **Many Brews → One Bean**

- Each `Brew` is linked to a specific `Bean`.
- Example: Multiple cups of Ethiopian Yirgacheffe logged under the same bean entry.

2. **Many Beans → One Origin**

- Different beans/tea leaves can come from the same country/region.
- Example: Both "Sidamo" and "Yirgacheffe" beans originate from Ethiopia.

#### Permissions:

- Only logged-in users can **add/edit** brews.
- Users can only **edit/delete** their own entries.

#### Admin permissions:

- Full CRUD access for all models.
- Manage user accounts.
- Add/edit origins and bean types.

#### To run / Commands:

```
python3 manage.py runserver
npm run watch:css (For tailwind agent to record changes)
python3 manage.py createsuperuser
python3 manage.py makemigrations
python3 manage.py migrate
```
