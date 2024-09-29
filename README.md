# Features

- Can use always own skin-system
- Possibility to reprox a nickname in the Ely.by system
- Automatic signature of skins
- Distribution of rights by tokens
- Beautiful smiley in /debug **:-)**

<br>

# Installation
> [!NOTE]
> After installation, remember to configure `docker-compose.yml` if needed.

## Docker (recommended)
<details><summary>Arch</summary>

```bash
sudo pacman -Syu git docker docker-compose
sudo systemctl enable docker
git clone https://github.com/steepboy/skin-system --recursive
cd skin-system
docker-compose up -d  --build
```

</details>
<details><summary>Ubuntu/Debian</summary>

```bash
sudo apt update && sudo apt upgrade
sudo apt-get install git docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable docker
git clone https://github.com/steepboy/skin-system --recursive
cd skin-system
docker-compose up -d  --build
```

</details>
<details><summary>Windows</summary>

#### Just install this: [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)

</details>

## Manually
```bash
mkdir skin-system
cd skin-system
git clone https://github.com/steepboy/skin-system --recursive
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 run
```
___
<br>
<br>

# How to use
### Request routers in the skin system are practically the same as in [Ely.by](https://docs.ely.by/ru/skins-system.html#), but there are some features

## Token system
> <h4>In `tokens.json` you can create and prioritize your access key.</h4>
> <h4>For example:</h4>
```json
{
  "valid_tokens": {
    "token1": {"priority": 0},
    "token2": {"priority": 1},
    "token3": {"priority": 2}
  }
}
```
> Here we see that tokens one two and three are access keys, and {“priority”: {\*\} its priority.<br>
> 
> In the skin system only priorities 0 and 1 are used so far, where 0 is a user who can just request access, and 1 is an administrator who can work with the database to add and remove users.
>
> Example request: `http://example.com/skin/yiski/?token=token1`

> [!TIP]
> If you don't need the token system, just turn it off in docker-compose.yml by changing `TOKEN_SYSTEM = 1` to 0 or on bash `export TOKEN_SYSTEM=0`.

## Routers

<details><summary><b>/skin/{username}</b></summary>

> **Return skin image<br>**
> 
> Has a variable: *No*<br>
> Type: *GET*<br>
> Min token priority: *0*<br>
> Working through: *Ely.by (as soon own system too)*<br>
> Example request: `http://example.com/skin/yiski/?token=test`<br>

</details>
<details><summary><b>/render/{username}</b></summary>

> **Renders the character in 2D<br>**
> 
> Has a variable: **scale=** (default: 8) **type=** (body or head) **layer** (1 or 0) # second layer of skin on or off<br>
> Type: *GET*<br>
> Min token priority: *0*<br>
> Working through: *Ely.by (as soon own system too)*<br>
> Example request: `http://example.com/render/yiski?token=test&scale=20&type=body&layer=1`<br>

</details>
<details><summary><b>/perspective/{username}</b></summary>

> WARNING!!! Render in perspective does not show the second layer on the skin

> **render the character in perspective<br>**
> Has a variable: **scale=** (default: 8) **z=** (up or down) **y=** (front or back)<br>
> Type: *GET*<br>
> Min token priority: *0*<br>
> Working through: *Ely.by (as soon own system too)*<br>
> Example request: `http://example.com/perspective/yiski?token=test&scale=40&z=up&y=front`<br>

</details>
<details><summary><b>/signature-verification-key(.der or .pem)</b></summary>

> **[This endpoint returns a public key that can be used to verify a texture’s signature](https://docs.ely.by/en/skins-system.html#url)<br>**
> 
> Has a variable: *No*<br>
> Type: *GET*<br>
> Min token priority: *0*<br>
> Working through: *Ely.by future only*<br>
> Example request: `http://example.com/signature-verification-key.pem?token=test`<br>

</details>
<details><summary><b>/textures/{username}</b></summary>

> **Returns url for skin png<br>**
> 
> Has a variable: *No*<br>
> Type: *GET*<br>
> Min token priority: *0*<br>
> Working through: *Ely.by (as soon own system too)*<br>
> Example request: `http://example.com/textures/yiski?token=test`<br>

</details>
<details><summary><b>/textures/signed/{username}</b></summary>

> **Passes nickname, signature key and skin and information in base64<br>**
> 
> Has a variable: **proxy=** (true or false) # When true, the skin is not in the skin system, it will be retransmitted from Ely.by or Mojang.API<br>
> Type: *GET*<br>
> Min token priority: *0*<br>
> Working through: *skin-system and Ely.by*<br>
> Example request: `http://example.com/textures/signed/yiski?token=test&proxy=true`<br>

</details>
<details><summary><b>/profile/{username}</b></summary>

> **Passes nickname, signature key and skin and information in base64<br>**
> 
> Has a variable: **unsigned=** (true or false) # if true, does not show the signature key. More info: [here](https://docs.ely.by/en/skins-system.html#url)<br>
> Type: *GET*<br>
> Min token priority: *0*<br>
> Working through: *Ely.by future only*<br>
> Example request: `http://example.com/profile/yiski?token=test&unsigned=false`<br>

</details>

### Skin system management

<details><summary><b>/sys/search/{args}</b></summary>

> **If you enter a nickname or skin id, it will display what is stored in the DB skin system, but if you enter `<all>`, it will display the whole DB<br>**
> 
> Has a variable: **table=** (user_data or skin_data) # Which table should be searched**<br>
> Type: *GET*<br>
> Min token priority: *1*<br>
> Working through: *skin-system future only*<br>
> Example request: `http://example.com/sys/search/yiski?token=test1&table=user_data`<br>

</details>
<details><summary><b>/sys/remove/skin/{id}</b></summary>

> **Deletes the skin and all its data in the DB<br>**
> 
> Has a variable: *No*<br>
> Type: *GET*<br>
> Min token priority: *1*<br>
> Working through: *skin-system future only*<br>
> Example request: `http://example.com/sys/remove/skin/Ihdnwj12h?token=test1`<br>

</details>
<details><summary><b>/sys/add/user</b></summary>

> **Signs the skin and adds it to the DB<br>**
> 
> Type: *POST*<br>
> Min token priority: *1*<br>
> Working through: *skin-system future only*<br>
> Example request:<br>

```bash
curl -X POST http://example.com/sys/add/user \
  -F 'file=@/path/to/your/skin.png' \
  -F 'nickname=yiski'
  -F 'redirect=0' #Immediately set the redirect value, if 0, it will show the skin system data, if 1 Ely.by (diffault is 0)
  -F 'token=token'
```

</details>
<details><summary><b>/sys/toggle/redirect/{username}</b></summary>

> **Enables or disables nick redirect from Ely.by<br>**
> 
> Has a variable: **toggle=** (0 or 1)<br>
> Type: *GET*<br>
> Min token priority: *1*<br>
> Working through: *skin-system future only*<br>
> Example request: `http://example.com/sys/toggle/redirect/yiski?token=test1&toggle=0`<br>

</details>
<details><summary><b>/ely/set/{username}</b></summary>

> **Deletes the skin and all its data in the DB<br>**
> 
> Has a variable: **redirect=** (nickname or `<del>`) # Ely.by nickname skin of which will be forwarded. if `<del>` deletes the redirection nickname, if it has been<br>
> Type: *GET*<br>
> Min token priority: *1*<br>
> Working through: *skin-system future only*<br>
> Example request: `http://example.com/ely/set/yiski?token=test1&redirect=pablo`<br>

</details>
<details><summary><b>/temp</b></summary>

> **Temporarily saves the skin and gives a link to download it (Idk why I did this)<br>**
> 
> Type: *POST*<br>
> Min token priority: *1*<br>
> Working through: *skin-system future only*<br>
> Example request:<br>

```bash
curl -X POST http://example.com/temp \
  -F 'file=@/path/to/your/skin.png' \
  -F 'token=token' \
  -F 'time=60' #Time in seconds to delete. Max 300 seconds
```
</details>
<details><summary><b>/debug</b></summary>

> **just a debugi with a smiley face<br>**
> 
> Example request: `http://example.com/debug`<br>
</details>

## Special thanks

- **[Ely.by](https://ely.by) -** *for the excellent documentation*
- **My Mom -** *for me*

## Issues or questions

If you have an issue, or a question, please [open an issue](https://github.com/steepboy/skin-system/issues) or DM me on discord: `yiskiii`
