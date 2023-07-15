import discord
from discord.ext import commands
import json
import re
import datetime
import asyncio

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all(), case_insensitive=True)
# Dictionary to store user wins
user_wins = {}
user_profiles = {}

# Dictionary to store win roles and their corresponding win counts
win_roles = {
    'Winner x6': 6,
    'Winner x7': 7,
    'Winner x9': 9,
    'Winner x10': 10,
    'Scrim Professional x20': 20,
    'Scrim Expert x40': 40,
    'Scrim Beast x60': 60,
    'Scrim Champion x80': 80,
    'Scrim God x100': 100
}

team_emojis = {
    'REVBOUNTY': '<:revbounty:1085300248290791604>',
    'BTP': '<:BTP:1127384345888423976>',
    'VALOR': '<:valor:1085302902362476677>',
    'UNTB': '<:untb:1102624693015547914>',
    'Clanless': '<:No:108530289930065104>'
}

country_flags = {
        'Not assigned': ":x:",
        'Australia': ":flag_au:",
        'Afghanistan': ":flag_af:",
        'Albania': ":flag_al:",
        'Algeria': ":flag_dz:",
        'Andorra': ":flag_ad:",
        'Angola': ":flag_ao:",
        'Antigua and Barbuda': ":flag_ag:",
        'Argentina': ":flag_ar:",
        'Armenia': ":flag_am:",
        'Aruba': ":flag_aw:",
        'Australia': ":flag_au:",
        'Austria': ":flag_at:",
        'Azerbaijan': ":flag_az:",
        'Bahamas': ":flag_bs:",
        'Bahrain': ":flag_bh:",
        'Bangladesh': ":flag_bd:",
        'Barbados': ":flag_bb:",
        'Belarus': ":flag_by:",
        'Belgium': ":flag_be:",
        'Belize': ":flag_bz:",
        'Benin': ":flag_bj:",
        'Bermuda': ":flag_bm:",
        'Bhutan': ":flag_bt:",
        'Bolivia': ":flag_bo:",
        'Bosnia and Herzegovina': ":flag_ba:",
        'Botswana': ":flag_bw:",
        'Brazil': ":flag_br:",
        'Brunei': ":flag_bn:",
        'Bulgaria': ":flag_bg:",
        'Burkina Faso': ":flag_bf:",
        'Burundi': ":flag_bi:",
        'Cambodia': ":flag_kh:",
        'Cameroon': ":flag_cm:",
        'Canada': ":flag_ca:",
        'Cape Verde': ":flag_cv:",
        'Central African Republic': ":flag_cf:",
        'Chad': ":flag_td:",
        'Chile': ":flag_cl:",
        'China': ":flag_cn:",
        'Colombia': ":flag_co:",
        'Comoros': ":flag_km:",
        'Congo': ":flag_cg:",
        'Cook Islands': ":flag_ck:",
        'Costa Rica': ":flag_cr:",
        'Croatia': ":flag_hr:",
        'Cuba': ":flag_cu:",
        'Cyprus': ":flag_cy:",
        'Czech Republic': ":flag_cz:",
        'Democratic Republic of the Congo': ":flag_cd:",
        'Denmark': ":flag_dk:",
        'Djibouti': ":flag_dj:",
        'Dominica': ":flag_dm:",
        'Dominican Republic': ":flag_do:",
        'East Timor': ":flag_tl:",
        'Ecuador': ":flag_ec:",
        'Egypt': ":flag_eg:",
        'El Salvador': ":flag_sv:",
        'Equatorial Guinea': ":flag_gq:",
        'Eritrea': ":flag_er:",
        'Estonia': ":flag_ee:",
        'Eswatini': ":flag_sz:",
        'Ethiopia': ":flag_et:",
        'Fiji': ":flag_fj:",
        'Finland': ":flag_fi:",
        'France': ":flag_fr:",
        'Gabon': ":flag_ga:",
        'Gambia': ":flag_gm:",
        'Georgia': ":flag_ge:",
        'Germany': ":flag_de:",
        'Ghana': ":flag_gh:",
        'Greece': ":flag_gr:",
        'Grenada': ":flag_gd:",
        'Guatemala': ":flag_gt:",
        'Guinea': ":flag_gn:",
        'Guinea-Bissau': ":flag_gw:",
        'Guyana': ":flag_gy:",
        'Haiti': ":flag_ht:",
        'Honduras': ":flag_hn:",
        'Hungary': ":flag_hu:",
        'Iceland': ":flag_is:",
        'India': ":flag_in:",
        'Indonesia': ":flag_id:",
        'Iran': ":flag_ir:",
        'Iraq': ":flag_iq:",
        'Ireland': ":flag_ie:",
        'Israel': ":flag_il:",
        'Italy': ":flag_it:",
        'Jamaica': ":flag_jm:",
        'Japan': ":flag_jp:",
        'Jordan': ":flag_jo:",
        'Kazakhstan': ":flag_kz:",
        'Kenya': ":flag_ke:",
        'Kiribati': ":flag_ki:",
        'North Korea': ":flag_kp:",
        'South Korea': ":flag_kr:",
        'Kosovo': ":flag_xk:",
        'Kuwait': ":flag_kw:",
        'Kyrgyzstan': ":flag_kg:",
        'Laos': ":flag_la:",
        'Latvia': ":flag_lv:",
        'Lebanon': ":flag_lb:",
        'Lesotho': ":flag_ls:",
        'Liberia': ":flag_lr:",
        'Libya': ":flag_ly:",
        'Liechtenstein': ":flag_li:",
        'Lithuania': ":flag_lt:",
        'Luxembourg': ":flag_lu:",
        'Madagascar': ":flag_mg:",
        'Malawi': ":flag_mw:",
        'Malaysia': ":flag_my:",
        'Maldives': ":flag_mv:",
        'Mali': ":flag_ml:",
        'Malta': ":flag_mt:",
        'Marshall Islands': ":flag_mh:",
        'Mauritania': ":flag_mr:",
        'Mauritius': ":flag_mu:",
        'Mexico': ":flag_mx:",
        'Micronesia': ":flag_fm:",
        'Moldova': ":flag_md:",
        'Monaco': ":flag_mc:",
        'Mongolia': ":flag_mn:",
        'Montenegro': ":flag_me:",
        'Morocco': ":flag_ma:",
        'Mozambique': ":flag_mz:",
        'Myanmar': ":flag_mm:",
        'Namibia': ":flag_na:",
        'Nauru': ":flag_nr:",
        'Nepal': ":flag_np:",
        'Netherlands': ":flag_nl:",
        'New Zealand': ":flag_nz:",
        'Nicaragua': ":flag_ni:",
        'Niger': ":flag_ne:",
        'Nigeria': ":flag_ng:",
        'North Macedonia': ":flag_mk:",
        'Norway': ":flag_no:",
        'Oman': ":flag_om:",
        'Pakistan': ":flag_pk:",
        'Palau': ":flag_pw:",
        'Palestine': ":flag_ps:",
        'Panama': ":flag_pa:",
        'Papua New Guinea': ":flag_pg:",
        'Paraguay': ":flag_py:",
        'Peru': ":flag_pe:",
        'Philippines': ":flag_ph:",
        'Poland': ":flag_pl:",
        'Portugal': ":flag_pt:",
        'Qatar': ":flag_qa:",
        'Romania': ":flag_ro:",
        'Russia': ":flag_ru:",
        'Rwanda': ":flag_rw:",
        'Saint Kitts and Nevis': ":flag_kn:",
        'Saint Lucia': ":flag_lc:",
        'Saint Vincent and the Grenadines': ":flag_vc:",
        'Samoa': ":flag_ws:",
        'San Marino': ":flag_sm:",
        'Sao Tome and Principe': ":flag_st:",
        'Saudi Arabia': ":flag_sa:",
        'Senegal': ":flag_sn:",
        'Serbia': ":flag_rs:",
        'Seychelles': ":flag_sc:",
        'Sierra Leone': ":flag_sl:",
        'Singapore': ":flag_sg:",
        'Slovakia': ":flag_sk:",
        'Slovenia': ":flag_si:",
        'Solomon Islands': ":flag_sb:",
        'Somalia': ":flag_so:",
        'South Africa': ":flag_za:",
        'South Sudan': ":flag_ss:",
        'Spain': ":flag_es:",
        'Sri Lanka': ":flag_lk:",
        'Sudan': ":flag_sd:",
        'Suriname': ":flag_sr:",
        'Sweden': ":flag_se:",
        'Switzerland': ":flag_ch:",
        'Syria': ":flag_sy:",
        'Taiwan': ":flag_tw:",
        'Tajikistan': ":flag_tj:",
        'Tanzania': ":flag_tz:",
        'Thailand': ":flag_th:",
        'Togo': ":flag_tg:",
        'Tonga': ":flag_to:",
        'Trinidad and Tobago': ":flag_tt:",
        'Tunisia': ":flag_tn:",
        'Turkey': ":flag_tr:",
        'Turkmenistan': ":flag_tm:",
        'Tuvalu': ":flag_tv:",
        'Uganda': ":flag_ug:",
        'Ukraine': ":flag_ua:",
        'United Arab Emirates': ":flag_ae:",
        'United Kingdom': ":flag_gb:",
        'United States': ":flag_us:",
        'Uruguay': ":flag_uy:",
        'Uzbekistan': ":flag_uz:",
        'Vanuatu': ":flag_vu:",
        'Vatican City': ":flag_va:",
        'Venezuela': ":flag_ve:",
        'Vietnam': ":flag_vn:",
        'Yemen': ":flag_ye:",
        'Zambia': ":flag_zm:",
        'Zimbabwe': ":flag_zw:",
        'AF': ":flag_af:",
        'AL': ":flag_al:",
        'DZ': ":flag_dz:",
        'AD': ":flag_ad:",
        'AO': ":flag_ao:",
        'AG': ":flag_ag:",
        'AR': ":flag_ar:",
        'AM': ":flag_am:",
        'AW': ":flag_aw:",
        'AU': ":flag_au:",
        'AT': ":flag_at:",
        'AZ': ":flag_az:",
        'BS': ":flag_bs:",
        'BH': ":flag_bh:",
        'BD': ":flag_bd:",
        'BB': ":flag_bb:",
        'BY': ":flag_by:",
        'BE': ":flag_be:",
        'BZ': ":flag_bz:",
        'BJ': ":flag_bj:",
        'BM': ":flag_bm:",
        'BT': ":flag_bt:",
        'BO': ":flag_bo:",
        'BA': ":flag_ba:",
        'BW': ":flag_bw:",
        'BR': ":flag_br:",
        'BN': ":flag_bn:",
        'BG': ":flag_bg:",
        'BF': ":flag_bf:",
        'BI': ":flag_bi:",
        'KH': ":flag_kh:",
        'CM': ":flag_cm:",
        'CA': ":flag_ca:",
        'CV': ":flag_cv:",
        'CF': ":flag_cf:",
        'TD': ":flag_td:",
        'CL': ":flag_cl:",
        'CN': ":flag_cn:",
        'CO': ":flag_co:",
        'KM': ":flag_km:",
        'CG': ":flag_cg:",
        'CK': ":flag_ck:",
        'CR': ":flag_cr:",
        'HR': ":flag_hr:",
        'CU': ":flag_cu:",
        'CY': ":flag_cy:",
        'CZ': ":flag_cz:",
        'CD': ":flag_cd:",
        'DK': ":flag_dk:",
        'DJ': ":flag_dj:",
        'DM': ":flag_dm:",
        'DO': ":flag_do:",
        'TL': ":flag_tl:",
        'EC': ":flag_ec:",
        'EG': ":flag_eg:",
        'SV': ":flag_sv:",
        'GQ': ":flag_gq:",
        'ER': ":flag_er:",
        'EE': ":flag_ee:",
        'SZ': ":flag_sz:",
        'ET': ":flag_et:",
        'FJ': ":flag_fj:",
        'FI': ":flag_fi:",
        'FR': ":flag_fr:",
        'GA': ":flag_ga:",
        'GM': ":flag_gm:",
        'GE': ":flag_ge:",
        'DE': ":flag_de:",
        'GH': ":flag_gh:",
        'GR': ":flag_gr:",
        'GD': ":flag_gd:",
        'GT': ":flag_gt:",
        'GN': ":flag_gn:",
        'GW': ":flag_gw:",
        'GY': ":flag_gy:",
        'HT': ":flag_ht:",
        'HN': ":flag_hn:",
        'HU': ":flag_hu:",
        'IS': ":flag_is:",
        'IN': ":flag_in:",
        'ID': ":flag_id:",
        'IR': ":flag_ir:",
        'IQ': ":flag_iq:",
        'IE': ":flag_ie:",
        'IL': ":flag_il:",
        'IT': ":flag_it:",
        'JM': ":flag_jm:",
        'JP': ":flag_jp:",
        'JO': ":flag_jo:",
        'KZ': ":flag_kz:",
        'KE': ":flag_ke:",
        'KI': ":flag_ki:",
        'KP': ":flag_kp:",
        'KR': ":flag_kr:",
        'XK': ":flag_xk:",
        'KW': ":flag_kw:",
        'KG': ":flag_kg:",
        'LA': ":flag_la:",
        'LV': ":flag_lv:",
        'LB': ":flag_lb:",
        'LS': ":flag_ls:",
        'LR': ":flag_lr:",
        'LY': ":flag_ly:",
        'LI': ":flag_li:",
        'LT': ":flag_lt:",
        'LU': ":flag_lu:",
        'MG': ":flag_mg:",
        'MW': ":flag_mw:",
        'MY': ":flag_my:",
        'MV': ":flag_mv:",
        'ML': ":flag_ml:",
        'MT': ":flag_mt:",
        'MH': ":flag_mh:",
        'MR': ":flag_mr:",
        'MU': ":flag_mu:",
        'MX': ":flag_mx:",
        'FM': ":flag_fm:",
        'MD': ":flag_md:",
        'MC': ":flag_mc:",
        'MN': ":flag_mn:",
        'ME': ":flag_me:",
        'MA': ":flag_ma:",
        'MZ': ":flag_mz:",
        'MM': ":flag_mm:",
        'NA': ":flag_na:",
        'NR': ":flag_nr:",
        'NP': ":flag_np:",
        'NL': ":flag_nl:",
        'NZ': ":flag_nz:",
        'NI': ":flag_ni:",
        'NE': ":flag_ne:",
        'NG': ":flag_ng:",
        'MK': ":flag_mk:",
        'NO': ":flag_no:",
        'OM': ":flag_om:",
        'PK': ":flag_pk:",
        'PW': ":flag_pw:",
        'PS': ":flag_ps:",
        'PA': ":flag_pa:",
        'PG': ":flag_pg:",
        'PY': ":flag_py:",
        'PE': ":flag_pe:",
        'PH': ":flag_ph:",
        'PL': ":flag_pl:",
        'PT': ":flag_pt:",
        'QA': ":flag_qa:",
        'RO': ":flag_ro:",
        'RU': ":flag_ru:",
        'RW': ":flag_rw:",
        'KN': ":flag_kn:",
        'LC': ":flag_lc:",
        'VC': ":flag_vc:",
        'WS': ":flag_ws:",
        'SM': ":flag_sm:",
        'ST': ":flag_st:",
        'SA': ":flag_sa:",
        'SN': ":flag_sn:",
        'RS': ":flag_rs:",
        'SC': ":flag_sc:",
        'SL': ":flag_sl:",
        'SG': ":flag_sg:",
        'SK': ":flag_sk:",
        'SI': ":flag_si:",
        'SB': ":flag_sb:",
        'SO': ":flag_so:",
        'ZA': ":flag_za:",
        'SS': ":flag_ss:",
        'ES': ":flag_es:",
        'LK': ":flag_lk:",
        'SD': ":flag_sd:",
        'SR': ":flag_sr:",
        'SE': ":flag_se:",
        'CH': ":flag_ch:",
        'SY': ":flag_sy:",
        'TW': ":flag_tw:",
        'TJ': ":flag_tj:",
        'TZ': ":flag_tz:",
        'TH': ":flag_th:",
        'TG': ":flag_tg:",
        'TO': ":flag_to:",
        'TT': ":flag_tt:",
        'TN': ":flag_tn:",
        'TR': ":flag_tr:",
        'TM': ":flag_tm:",
        'TV': ":flag_tv:",
        'UG': ":flag_ug:",
        'UA': ":flag_ua:",
        'AE': ":flag_ae:",
        'GB': ":flag_gb:",
        'US': ":flag_us:",
        'UY': ":flag_uy:",
        'UZ': ":flag_uz:",
        'VU': ":flag_vu:",
        'VA': ":flag_va:",
        'VE': ":flag_ve:",
        'VN': ":flag_vn:",
        'YE': ":flag_ye:",
        'ZM': ":flag_zm:",
        'ZW': ":flag_zw:"
        }

# JSON file path
wins_file = "user_wins.json"
profiles_file = "user_profiles.json"


def load_user_profiles():
    try:
        with open(profiles_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


# Save user profiles to JSON file
def save_user_profiles():
    with open(profiles_file, "w") as file:
        json.dump(user_profiles, file)


# Load user wins from JSON file
def load_user_wins():
    try:
        with open(wins_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


# Save user wins to JSON file
def save_user_wins():
    with open(wins_file, "w") as file:
        json.dump(user_wins, file)


@bot.event
async def on_ready():
    print("Bot has logged in as {0.user}".format(bot))
    # Load user wins from JSON file
    global user_wins
    user_wins = load_user_wins()
    global user_profiles
    user_profiles = load_user_profiles()
    await bot.tree.sync()
    

@bot.command()
async def botping(ctx):
     await ctx.send(f'My ping is {round(bot.latency * 1000)}ms')


@bot.tree.command(name="leaderboard", description="Displays the leaderboard")
async def leaderboard(Interaction: discord.Interaction, page: int = 1):
    items_per_page = 10
    sorted_users = sorted(user_wins.items(), key=lambda x: x[1], reverse=True)
    total_pages = (len(sorted_users) - 1) // items_per_page + 1
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    leaderboard_items = sorted_users[start_index:end_index]

    embed = discord.Embed(title="Leaderboard", color=0x00FF98)  # Set embed color to 00FF98
    embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
    embed.set_footer(text=f"Requested by {Interaction.user.name} | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                     icon_url=Interaction.user.avatar.url if Interaction.user.avatar else discord.Embed.Empty)

    medal_emojis = {
        1: "<:Diamond:1101429384629461022>",  # Gold medal
        2: "<:Gold:1101429366728175707>",  # Silver medal
        3: "<:Silver:1101429349456035860>",
        4: "<:Bronze:1101429324793532438>"# Bronze medal
    }

    for i, (user_id, wins) in enumerate(leaderboard_items, start=start_index + 1):
        user = await bot.fetch_user(int(user_id))
        username = user.name if user else f'Unknown User ({user_id})'
        medal = medal_emojis.get(i, "")

        user_profile = user_profiles.get(user_id)
        team = user_profile.get('team', 'Not assigned') if user_profile else 'Not assigned'
        country = user_profile.get('nationality', 'Not assigned') if user_profile else 'Not assigned'

        team_emojis = {
            'REVBOUNTY': '<:revbounty:1085300248290791604>',
            'BTP': '<:BTP:1127384345888423976>',
            'VALOR': '<:valor:1085302902362476677>',
            'UNTB': '<:untb:1102624693015547914>'
        }

        team_emoji = team_emojis.get(team, "Not assigned")


        country_flag = country_flags.get(country, "")

        embed.add_field(name=f'**Rank {i} {medal}**',
                        value=f'{country_flag} {username} | Wins: {wins} | Team: {team_emoji}',
                        inline=False)

    embed.add_field(name="\u200B", value=f"Page {page}/{total_pages}", inline=False)

    await Interaction.response.send_message(embed=embed)


@bot.tree.command(name="profile", description="Display's the user's profile")
async def profile(Interaction: discord.Interaction, user: discord.Member = None):
    user = user or Interaction.user
    user_id = str(user.id)

    user_profile = user_profiles.get(user_id)
    if not user_profile:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="Profile not found, create one now using /profilesetup", inline=True)
        await Interaction.response.send_message(embed=embed)
        return

    team = user_profile.get('team', 'Not assigned')
    country = user_profile.get('nationality', 'Not assigned')
    ign = user_profile.get('ign', 'Not assigned')

    team_emoji = team_emojis.get(team, "")
    country_flag = country_flags.get(country.upper(), "")

    embed = discord.Embed(title=f"{user.name}'s Profile", color=0x00FF98)
    embed.set_thumbnail(url=user.avatar.url)

    embed.add_field(name="User", value=user.name, inline=True)
    embed.add_field(name="Team", value=f"{team_emoji} {team}", inline=True)
    embed.add_field(name="Country", value=f"{country_flag} {country.upper()}", inline=True)
    embed.add_field(name="in-game IGN", value=ign, inline=True)

    rank = None
    for i, (user_id, _) in enumerate(sorted(user_wins.items(), key=lambda x: x[1], reverse=True), start=1):
        if user_id == str(user.id):
            rank = i
            break

    embed.set_footer(text=f"Requested by {Interaction.user.name} | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                     icon_url=Interaction.user.avatar.url if Interaction.user.avatar else discord.Embed.Empty)

    if rank is not None:
        embed.set_author(name=f"Rank: {rank}", icon_url=user.avatar.url)
    
    await Interaction.response.send_message(embed=embed)


@bot.tree.command(name="profilesetup", description="Setup your server profile")
async def profilesetup(Interaction: discord.Interaction):
    user_id = str(Interaction.user.id)
    user_profile = user_profiles.get(user_id, {})

    if "nationality" in user_profile and "ign" in user_profile and "team" in user_profile:
        embed = discord.Embed(color=0xFF0000)
        embed.add_field(name="", value=f"{Interaction.user.mention}, your profile is already complete.", inline=True)
        await Interaction.response.send_message(embed=embed)
        return

    embed = discord.Embed(color=0x00FF00)
    embed.add_field(name="", value=f"{Interaction.user.mention}, I have sent you a DM. Please check your messages.", inline=True)
    await Interaction.response.send_message(embed=embed)

    dm_channel = await Interaction.user.create_dm()

    embed = discord.Embed(color=0xFFFFFF)
    embed.add_field(name="Nationality", value="What is your nationality (country code)?", inline=False)
    await dm_channel.send(embed=embed)

    try:
        nationality_msg = await bot.wait_for("message", check=lambda m: m.author == Interaction.user and m.channel == dm_channel, timeout=120)
        nationality = nationality_msg.content
        user_profile["nationality"] = nationality
    except asyncio.TimeoutError:
        embed = discord.Embed(color=0xFF0000)
        embed.add_field(name="", value="Timed out. Please run the command again to continue.", inline=True)
        await dm_channel.send(embed=embed)
        return

    embed = discord.Embed(color=0xFFFFFF)
    embed.add_field(name="IGN", value="What is your Blast Royale IGN (in-game name)?", inline=False)
    await dm_channel.send(embed=embed)

    try:
        ign_msg = await bot.wait_for("message", check=lambda m: m.author == Interaction.user and m.channel == dm_channel, timeout=120)
        ign = ign_msg.content
        user_profile["ign"] = ign
    except asyncio.TimeoutError:
        embed = discord.Embed(color=0xFF0000)
        embed.add_field(name="", value="Timed out. Please run the command again to continue.", inline=True)
        await dm_channel.send(embed=embed)
        return

    embed = discord.Embed(color=0xFFFFFF)
    embed.add_field(name="Team", value="What Blast Royale team do you associate with (REVBOUNTY, BTP, VALOR, UNTB)?\nType 'none' for no team affiliation.", inline=False)
    await dm_channel.send(embed=embed)

    try:
        team_msg = await bot.wait_for("message", check=lambda m: m.author == Interaction.user and m.channel == dm_channel, timeout=120)
        team = team_msg.content.upper()
        if team == "NONE":
            user_profile["team"] = "None"
        elif team not in ["REVBOUNTY", "BTP", "VALOR", "UNTB"]:
            embed = discord.Embed(color=0xFF0000)
            embed.add_field(name="", value="Invalid team name. Available teams: REVBOUNTY, BTP, VALOR, UNTB", inline=True)
            await dm_channel.send(embed=embed)
            return
        else:
            user_profile["team"] = team
    except asyncio.TimeoutError:
        embed = discord.Embed(color=0xFF0000)
        embed.add_field(name="", value="Timed out. Please run the command again to continue.", inline=True)
        await dm_channel.send(embed=embed)
        return

    user_profiles[user_id] = user_profile
    save_user_profiles()

    embed = discord.Embed(color=0x00FF00)
    embed.add_field(name="", value="Profile setup complete!", inline=True)
    await dm_channel.send(embed=embed)



@bot.tree.command(name="resetprofile", description="Reset your server profile")
async def resetprofile(Interaction: discord.Interaction):
    user_id = str(Interaction.user.id)
    user_profile = user_profiles.get(user_id)

    if not user_profile:
        embed = discord.Embed(color=0xFF0000)
        embed.add_field(name="", value=f"{Interaction.user.mention}, your profile is not set. There's nothing to reset.", inline=True)
        await Interaction.response.send_message(embed=embed)
        return

    user_profiles.pop(user_id)
    save_user_profiles()

    embed = discord.Embed(color=0x00FF00)
    embed.add_field(name="", value=f"{Interaction.user.mention}, your profile has been reset. You can run the profile setup command again to set up a new profile.", inline=True)
    await Interaction.response.send_message(embed=embed)


###------------------------------------------------------------------------------------------------WINS


@bot.tree.command(name="wins", description="display's the user's wins")
async def wins(Interaction: discord.Interaction, user: discord.Member = None):
    user = user or Interaction.user
    wins = user_wins.get(str(user.id), 0)

    user_profile = user_profiles.get(str(user.id))
    team = user_profile.get('team', 'Not assigned') if user_profile else 'Not assigned'

    team_emoji = team_emojis.get(team, "")

    embed = discord.Embed(title=f"{user.name}'s Wins", color=0x00FF98)  # Set embed color to 00FF98
    embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
    embed.set_thumbnail(url=user.avatar.url)

    embed.add_field(name="User", value=user.name, inline=True)
    embed.add_field(name="Team", value=f"{team_emoji} {team}", inline=True)
    embed.add_field(name="Wins", value=wins, inline=True)

    await Interaction.response.send_message(embed=embed)


@bot.tree.command(name="winsadd", description="Adds wins to the user")
@commands.has_permissions(administrator=True)
async def winsadd(Interaction: discord.Interaction, user: discord.Member, *, wins: str):
    user_id = str(user.id)

    wins_match = re.match(r'^(\d+)$', wins)
    if not wins_match:
        embed=discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value=f"Invalid number of wins. Please provide a valid integer.", inline=True)
        await Interaction.response.send_message(embed=embed)
        return

    wins = int(wins_match.group(1))

    if user_id not in user_wins:
        user_wins[user_id] = 0

    previous_wins = user_wins[user_id]
    user_wins[user_id] += wins

    # Get the previously assigned win roles
    previous_win_roles = []
    for role, win_count in win_roles.items():
        role_obj = discord.utils.get(Interaction.guild.roles, name=role)
        if role_obj is not None and role_obj in user.roles:
            previous_win_roles.append(role_obj)

    # Remove the previously assigned win roles
    await user.remove_roles(*previous_win_roles)

    # Check and update win roles
    assigned_win_roles = []
    for role, win_count in win_roles.items():
        if previous_wins < win_count <= user_wins[user_id]:
            role_obj = discord.utils.get(Interaction.guild.roles, name=role)
            if role_obj is not None:
                assigned_win_roles.append(role_obj)
        elif previous_wins >= win_count > user_wins[user_id]:
            break

    # Add the newly assigned win roles
    await user.add_roles(*assigned_win_roles)

    embed=discord.Embed(title="Profile updated", color=0x00FF00)
    embed.add_field(name="", value=f'Added {wins} win(s) to {user.mention}\'s total.', inline=True)
    await Interaction.response.send_message(embed=embed)

    # Save user wins to JSON file
    save_user_wins()



@bot.tree.command(name="winsremove", description="Remove wins from a user")
@commands.has_permissions(administrator=True)
async def winsremove(Interaction: discord.Interaction, user: discord.Member, *, wins: str):
    user_id = str(user.id)

    wins_match = re.match(r'^(\d+)$', wins)
    if not wins_match:
        embed=discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value=f"Invalid number of wins. Please provide a valid integer.", inline=True)
        await Interaction.response.send_message(embed=embed)
        return

    wins = int(wins_match.group(1))

    if user_id not in user_wins:
        embed=discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value=f"This user does not have any recorded wins.", inline=True)
        await Interaction.response.send_message(embed=embed)
        return

    previous_wins = user_wins[user_id]
    if wins > previous_wins:
        embed=discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="The specified number of wins is greater than the user's current total wins.", inline=True)
        await Interaction.response.send_message(embed=embed)
        return

    user_wins[user_id] -= wins

    # Get the previously assigned win roles
    previous_win_roles = []
    for role, win_count in win_roles.items():
        role_obj = discord.utils.get(Interaction.guild.roles, name=role)
        if role_obj is not None and role_obj in user.roles:
            previous_win_roles.append(role_obj)

    # Remove the previously assigned win roles
    await user.remove_roles(*previous_win_roles)

    # Check and update win roles
    assigned_win_roles = []
    for role, win_count in win_roles.items():
        if win_count <= user_wins[user_id]:
            role_obj = discord.utils.get(Interaction.guild.roles, name=role)
            if role_obj is not None:
                assigned_win_roles.append(role_obj)

    # Add the newly assigned win roles
    await user.add_roles(*assigned_win_roles)

    embed=discord.Embed(title="Profile updated", color=0x00FF00)
    embed.add_field(name="", value=f'Removed {wins} win(s) from {user.mention}\'s total.', inline=True)
    await Interaction.response.send_message(embed=embed)

    # Save user wins to JSON file
    save_user_wins()


@bot.tree.command(name="winsreset", description="Reset a certain user's wins")
@commands.has_permissions(administrator=True)
async def winsreset(Interaction: discord.Interaction, user: discord.Member):
    user_id = str(user.id)

    if user_id not in user_wins:
        embed=discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value=f"This user does not have any recorded wins.", inline=True)
        await Interaction.response.send_message(embed=embed)
        return

    del user_wins[user_id]

    # Get the previously assigned win roles
    previous_win_roles = []
    for role, win_count in win_roles.items():
        role_obj = discord.utils.get(Interaction.guild.roles, name=role)
        if role_obj is not None and role_obj in user.roles:
            previous_win_roles.append(role_obj)

    # Remove the previously assigned win roles
    await user.remove_roles(*previous_win_roles)

    embed=discord.Embed(title="Profile updated", color=0xff0000)
    embed.add_field(name="", value=f'Reset wins for {user.mention}.', inline=True)
    await Interaction.response.send_message(embed=embed)

    # Save user wins to JSON file
    save_user_wins()



@bot.tree.command(name="help", description="Shows a list of commands")
async def help(Interaction: discord.Interaction):
    user_commands = [
        "/leaderboard [page] - Show the leaderboard of users and their wins.",
        "/profile [user] - Show the profile of a user.",
        "/wins [user] - Show the number of wins for a user.",
        "/profilesetup - Setup your profile to assign a team and a country",
    ]

    embed = discord.Embed(title="User Commands", color=0x00FF98)
    embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
    embed.set_footer(text=f"Requested by {Interaction.user.name} | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                     icon_url=Interaction.user.avatar.url if Interaction.user.avatar else discord.Embed.Empty)

    for command in user_commands:
        embed.add_field(name=command.split(' - ')[0], value=command.split(' - ')[1], inline=False)

    await Interaction.response.send_message(embed=embed)


@bot.tree.command(name="admin-help", description="Display's a list of admin commands.")
@commands.has_permissions(administrator=True)
async def adminhelp(Interaction: discord.Interaction):
    admin_commands = [
        "/winsadd <user> <wins> - Add wins to a user's total. (Admin only)",
        "/winsremove <user> <wins> - Remove wins from a user's total. (Admin only)",
        "/winsreset <user> - Reset a user's wins to zero. (Admin only)",
    ]

    embed = discord.Embed(title="Admin Commands", color=0x00FF98)
    embed.set_author(name=Interaction.guild.name, icon_url=Interaction.guild.icon.url if Interaction.guild.icon else discord.Embed.Empty)
    embed.set_footer(text=f"Requested by {Interaction.user.name} | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                     icon_url=Interaction.user.avatar.url if Interaction.user.avatar else discord.Embed.Empty)

    for command in admin_commands:
        embed.add_field(name=command.split(' - ')[0], value=command.split(' - ')[1], inline=False)

    await Interaction.response.send_message(embed=embed)


bot.run('MTEyODI2MjczNjE2NjUzNTE5OQ.GxleDZ.jdTlDOlqVD0UtYi1Abo2wY6tx3f81fhZJZS58E')