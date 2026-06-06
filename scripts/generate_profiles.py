import pandas as pd

# 100 Massive public fitness, fat loss, medical, and wellness handles (Cleaned)
top_100_fitness_handles = [
    # Top Tier Coaches & Creators
    "deltabolic", "jpgcoaching", "leanbeefpatty", "syattfitness", "cartergood", 
    "theoburn", "colinwelsch", "jordan_syatt", "clarkfit", "brenblakley",
    "coachegghad", "scimuszc", "danielle_keen", "trainwithjoan", "soheefit",
    "shona_vertue", "rebeccalouisefitness", "willcozens", "alexia_clark", "kayla_itsines",
    "emilyskyefit", "simeonpanda", "ulissesworld", "jeff_seid", "sadikhadzovic",
    "bradleymartyn", "calumvonmoger", "stevecook", "christianguzmanfitness", "nikkiblackketter",
    
    # Medical Doctors, PhDs & Science Communicators
    "dr.idz", "drjacob", "squat_university", "biolayne", "dr.sam.robbins", 
    "maxlugavere", "dr.nadolsky", "thomasdelauer", "paulsaladinomd", "dr_fatloss_example",
    "dr.markhyman", "dr.andrewhuberman", "peterattiamd", "dr_ben_bikman", "drwillbulsiewicz",
    "drjasonfung", "drchatterjee", "drgundry", "dr.williamli", "dr.rhondapatrick",
    
    # Dietitians & Evidence-Based Nutrition Specialists
    "fitnesschef_official", "nutrition_facts_org", "collegecleaneating", "maddhealthy", "sortingoutscience",
    "abbylangernutrition", "rhitrition", "thenutritionguru", "nutritionbykara", "macronutrientgenius",
    "tasteofclark", "macrochef", "fitmencook", "jalalsamfit", "stealth_health_life",
    "cheatdaydesign", "thegourmet700", "lowcalrecipes99", "countingmacros101", "theflexibledietinglifestyle",
    
    # Global Fitness Hubs & High-Performance Athletes
    "hybrid.calisthenics", "athleanx", "functional.patterns", "crossfit", "bodybuildingcom",
    "gymshark", "alphalete", "vanquishfitness", "roguefitness", "menshealthmag",
    "womenshealthmag", "muscleandfitness", "shape", "selfmagazine", "fitnessmagazine",
    "chrissy_fitness", "anllela_sagra", "michelle_lewin", "paula_cremon", "jeneselter",
    "sommerray", "tammyhembrow", "chloe_t", "madfit.ig", "growingannanas",
    "pamela_rf", "krissycela", "whitneyysimmons", "natacha.oceane", "stephanie_buttermore"
]

data = []
for index, handle in enumerate(top_100_fitness_handles):
    if index < 30:
        cat = "Online Fitness Coach"
    elif index < 50:
        cat = "Medical / Science Authority"
    elif index < 70:
        cat = "Nutrition & Recipe Creator"
    else:
        cat = "High-Reach Fitness Athlete"
        
    data.append({"username": handle, "category": cat})

df = pd.DataFrame(data)
df.to_csv("../data/profiles.csv", index=False)
print(f"✅ Success! Standardized database compiled with {len(df)} clean accounts inside profiles.csv")