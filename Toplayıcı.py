import json
import time
import requests
import pandas as pd
import numpy as np
import streamlit as st
from io import BytesIO
import datetime

USERNAME   = 'muhammetfurkan.baysal@zorlu.com'
PASSWORD   = 'Zorlu.2025'
START_DATE = '2026-03-01'
END_DATE   = '2026-03-31'

COMPANIES_TOPLAYICI = [
    {"name": "PURE ENERGY ELEKTRİK TEDARİK A.Ş. (TOPLAYICI)","market": 103402, "santraller": [14684, 16783,7958, 13803, 2141, 13603, 17963, 12186, 9081, 9722, 15124, 12342, 17503, 7320, 8941, 5002821, 4609, 12324, 7586, 17905, 9482, 15624, 15623, 11627, 7598, 11703, 12184, 17886, 11646, 722, 17263, 4509, 1501, 14303, 662, 15383, 13583, 15583, 15483, 9141, 14863, 15844, 16123, 663, 9122, 9550, 11630, 9685, 13863, 19164, 8102, 15603, 17749, 9082, 16704]},
    {"name": "AKSA DENGELEME VE ENERJİ YÖNETİMİ A.Ş. (TOPLAYICI)","market": 103261, "santraller": [15909, 15912, 16643, 9624, 7199, 11987, 6540, 7198, 17845, 3753, 9421, 456, 15983, 20083, 5069, 6476, 9558, 15203, 15223, 7858, 12407, 15164, 6096, 664, 2401, 17383, 17543, 11084, 16303, 11625, 16844, 20283, 6436, 19683, 16443, 19263, 5004061, 12383, 733, 15543, 5012721, 5874, 9555, 18083, 12409, 7158, 18423, 17923, 16464, 14883, 11549, 19643, 1002, 13483, 15908, 715, 9703, 4206, 12382, 4913, 15963, 16204, 9402, 18063, 8479, 16663, 8459, 6637, 14923, 15743, 5469, 8698, 12384, 7098, 749, 3222, 15783, 2521, 17984, 11637, 15843, 4733, 9921, 728, 10702, 18663, 3182, 13703, 600, 18763, 729, 4749, 6197, 8318, 5894, 16864, 16065, 17825, 726, 5671, 15763, 8258, 4425, 9686, 6680, 17663, 7159]},
    {"name": "ZORLU DENGELEME VE ENERJİ YÖNETİMİ A.Ş. (TOPLAYICI)","market": 104280, "santraller": [9241, 645, 223, 4930, 4813, 8298, 6879, 636, 625, 215, 13851, 2501, 189, 647, 641, 8902, 6696]},
    {"name": "INAVITAS TOPLAYICILIK VE ENERJİ TİC. A.Ş. (TOPLAYICI)","market": 103600, "santraller": [5001340, 5014305, 14503, 12345, 12164, 6301, 5013946, 12427, 16323, 11104, 7340, 12183, 16746, 377, 75, 17563, 16066, 17443, 14743, 268, 575, 5011621, 20704, 5004085, 119, 6839, 7879, 17846, 16645, 10600, 5006041, 5119, 244, 5014024, 8462, 18364, 10541, 5540, 18263, 15103, 10501, 11562, 16343, 278, 483, 670, 5892, 1401, 16463, 16943, 6659, 4910, 14843, 493, 17583, 15944, 16765, 13843, 12353, 5012861, 4123, 660, 661, 16043, 13264, 18323, 10563, 17343, 7500, 9623, 13323, 15919, 15683, 682, 7398, 10402, 5699, 17763]},
    {"name": "CK TOPLAYICILIK VE ENERJİ YÖNETİMİ FAALİYETLERİ A.Ş. (TOPLAYICI)","market": 103660, "santraller": [2161, 10461, 18004, 10621, 5010, 11525, 11524, 13867, 689, 10604]},
    {"name": "ENKO ENERJİ SAN. VE TİC. A.Ş. (TOPLAYICI)","market": 103420, "santraller": [13285, 15283, 15284, 16223, 20223, 16064, 16983, 15165, 612, 2681, 11602, 15003, 5610, 15505, 5753, 15703, 6758, 17888, 9501, 9181, 7758, 16483, 15403, 5004321, 5120, 8281, 11624, 13303, 7686, 1543, 16683, 7021, 5151, 9261, 7622, 8158, 5014383, 4387, 610, 5003982]}
]

COMPANIES_TOPLAYICI_KUDUP = [
    {"name": "PURE ENERGY ELEKTRİK TEDARİK A.Ş. (TOPLAYICI)","market": 103402, "uevcbID": [3210571, 3214990, 1631731, 3218250, 3218251, 3207490, 3217351, 3218750, 3194007, 3194440, 3212651, 3204489, 3216550, 606544, 2634264, 5002822, 42023, 3217197,1236115, 3217232, 3193608, 3213531, 3213530, 3200456, 1174625, 3200590, 3204191, 3217193, 3200495, 4027, 3216019, 31459, 5545, 3208770, 3818, 3213170, 3207450, 3213490, 5011541, 5014328, 3213390, 3220770, 3211130, 3213751, 3214090, 3648, 3218752, 3196808, 3200459, 3200460, 3207910, 3219231, 1808498, 3213510, 3217049, 3006558, 3214911]},
    {"name": "AKSA DENGELEME VE ENERJİ YÖNETİMİ A.Ş. (TOPLAYICI)","market": 103261, "uevcbID": [3213836, 3213839, 3214830, 3194167, 723719, 3203814, 295303, 607810, 3217132, 3753, 3192240, 3568, 3213930, 3221470, 106456, 3222712, 3194188, 3212951, 3212935, 1930390, 3204649, 3212711, 121450, 3837, 9330, 3216270, 3216671, 3199251, 3214390, 3200454, 3215051, 3222270, 300754, 3220410, 3214570, 3220391, 5004062, 3204619, 18548, 3213411, 5012741, 114305, 3194133, 3217490, 3204651, 609493, 3218111, 3217251, 3214591, 3211190, 3200336, 3220350, 3989, 3207350, 3213835, 3969, 3194585, 26087, 3204618, 49244, 3213910, 3222090, 3192144, 3217470, 1949409, 3214850, 2643301, 539475, 3220630, 3213650, 99514, 2225698, 3204620, 609542, 4130, 3195729, 3213690, 9810, 3217371, 3200466, 3213750, 2454009, 3195222, 4049, 3197168, 3218550, 3214550, 3207730, 3768, 3218730, 3988, 37977, 121467, 2218389, 117897, 3215033, 3214013, 3217112, 4071, 106672, 3213670, 1808518, 29340, 3220390, 308335, 3216950, 804475,]},
    {"name": "ZORLU DENGELEME VE ENERJİ YÖNETİMİ A.Ş. (TOPLAYICI)","market": 104280, "uevcbID": [3192287, 3792, 3789, 340783, 112265, 49101, 1808455, 412031, 3798, 3787, 3800, 3216050, 8990, 3801, 3794, 3796, 2641852]},
    {"name": "INAVITAS TOPLAYICILIK VE ENERJİ TİC. A.Ş. (TOPLAYICI)","market": 103600, "uevcbID": [5001341, 5014323, 3209890, 3204539, 3204159, 181027, 5014023, 3204675, 3214411, 3199273, 614709, 3204190, 3214953, 2359, 268, 3216651, 117908, 3214014, 3216350, 3210770, 1930401, 3746, 5011641, 3223631, 5004063, 3204390, 410863, 1456124, 3217133, 3214832, 3208610, 5006042, 81822, 1041, 5012322, 5014025, 1930402, 3217951, 3196907, 100179, 3217810, 3212630, 3196787, 3200439, 3214430, 181020, 3645, 3981, 335505, 7490, 3214590, 3215270, 323552, 107660, 3211091, 3668, 3216850, 3213891, 3214972, 3207890, 3204560, 5012881, 26808, 3204597, 3204598, 3213990, 3206951, 3217870, 3196929, 3216110, 952551, 3194130, 3207070, 3213847, 3213590, 4066, 3218650, 3196588, 111604, 3217050]},
    {"name": "CK TOPLAYICILIK VE ENERJİ YÖNETİMİ FAALİYETLERİ A.Ş. (TOPLAYICI)","market": 103660, "uevcbID": [3218330, 3196747, 3223250, 3197087, 3218271, 3200292, 3200291, 3207917, 3218272, 3196985]},
    {"name": "ENKO ENERJİ SAN. VE TİC. A.Ş. (TOPLAYICI)","market": 103420, "uevcbID": [3206972, 3213030, 3213031, 3214290, 3222150, 3214012, 3217171, 3212712, 3781, 11255, 3206970, 3211350, 5013721, 5013702, 112264, 3213397, 117883, 3213610, 414111, 3217195, 3208550, 3004028, 3208551, 3214593, 3213190, 5004341, 3218490, 1724202, 3200453, 3206990, 1542364, 5347, 3221393, 3194923, 106710, 3208552, 1413086, 1724115, 5014441, 28389, 3208554, 5004021]}
]

CAS_URL      = "https://giris.epias.com.tr/cas/v1/tickets"
PTF_SMF_SDF =  "https://seffaflik.epias.com.tr/reporting-service/v1/data/ptf-smf-sdf"
KUDUP = "https://seffaflik.epias.com.tr/electricity-service/v1/generation/data/sbfgp"
URL_UEVM     = "https://seffaflik.epias.com.tr/electricity-service/v1/generation/data/injection-quantity"

def to_iso_tr(date_str: str) -> str:
    return f"{date_str}T00:00+03:00"

def get_tgt(username: str, password: str) -> str:
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    resp = requests.post(CAS_URL, data={"username": username, "password": password}, headers=headers)
    if resp.status_code != 201:
        raise RuntimeError("TGT alınamadı. Kullanıcı adı veya şifre hatalı olabilir.")
    loc = resp.headers.get("Location", "")
    if not loc:
        raise RuntimeError("TGT Location header bulunamadı.")
    return loc.rstrip("/").split("/")[-1]

def _post_json(url, tgt_key, body, max_retries=5):
    headers = {"Content-Type": "application/json", "Accept": "application/json", "TGT": tgt_key}
    for attempt in range(max_retries):
        time.sleep(0.4)
        r = requests.post(url, headers=headers, json=body)
        if r.status_code == 429:
            wait = 15 * (attempt + 1)
            time.sleep(wait)
            continue
        if not r.ok:
            raise RuntimeError(f"İstek başarısız ({r.status_code}): {r.text[:500]}")
        try:
            return r.json()
        except json.JSONDecodeError:
            raise RuntimeError(f"JSON parse hatası: {r.text[:500]}")
    raise RuntimeError(f"Rate limit aşıldı, {max_retries} denemeden sonra başarısız.")

tgt_key = get_tgt(USERNAME, PASSWORD)

def data_uevm_santral(start_date, end_date, tgt_key, santral_id):
    body = {
        "startDate": to_iso_tr(start_date),
        "endDate": to_iso_tr(end_date),
        "powerplantId": santral_id,
        "page": {"number": 1, "size": 1000}
    }

    js = _post_json(URL_UEVM, tgt_key, body)

    items = js.get("items", [])

    if not items:
        return pd.DataFrame(columns=["date", "uevm"])

    df = pd.DataFrame(items)

    if "total" not in df.columns:
        return pd.DataFrame(columns=["date", "uevm"])

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["uevm"] = pd.to_numeric(df["total"], errors="coerce").fillna(0)

    return df[["date", "uevm"]]

def data_uevm_sirket(start_date, end_date, tgt_key, santraller):
    frames = []

    for sid in santraller:
        try:
            df = data_uevm_santral(start_date, end_date, tgt_key, sid)
            if not df.empty:
                frames.append(df)
        except Exception as e:
            print(f"Hata santral {sid}: {e}")

    if not frames:
        return pd.DataFrame(columns=["date", "uevm"])

    combined = pd.concat(frames, ignore_index=True)

    grouped = combined.groupby("date", as_index=False)["uevm"].sum()

    return grouped

def tum_sirketler_uevm(start_date, end_date, tgt_key, companies):
    all_data = []

    for comp in companies:
        name = comp["name"].split("(")[0].strip()

        print(f"Çekiliyor: {name}")

        df = data_uevm_sirket(
            start_date,
            end_date,
            tgt_key,
            comp["santraller"]
        )

        if df.empty:
            print(f"Boş veri: {name}")
            continue

        df["company"] = name
        all_data.append(df)

    if not all_data:
        return pd.DataFrame()

    combined = pd.concat(all_data, ignore_index=True)

    pivot_df = combined.pivot_table(
        index="date",
        columns="company",
        values="uevm",
        aggfunc="sum"
    ).reset_index()

    pivot_df = pivot_df.rename(columns={
        col: f"{col}_UEVM" for col in pivot_df.columns if col != "date"})

    return pivot_df.fillna(0).sort_values("date")



def data_ptf_smf(start_date, end_date, tgt_key):
    body = {
        "startDate": to_iso_tr(start_date),
        "endDate": to_iso_tr(end_date)
    }

    js = _post_json(PTF_SMF_SDF, tgt_key, body)

    items = js.get("items", [])
    if not items:
        return pd.DataFrame(columns=["date", "ptf", "smf", "systemStatus"])

    df = pd.DataFrame(items)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    return df[["date", "ptf", "smf", "systemStatus"]]

def data_kudup_sirket(start_date, end_date, tgt_key, market_id, uevcb_list):
    frames = []

    for uevcb in uevcb_list:
        body = {
            "startDate": to_iso_tr(start_date),
            "endDate": to_iso_tr(end_date),
            "organizationId": market_id,
            "uevcbId": uevcb,
            "region": "TR1",
            "page": {
                "number": 1,
                "size": 1000,
                "sort": {"direction": "ASC", "field": "date"}
            }
        }

        try:
            js = _post_json(KUDUP, tgt_key, body)
            items = js.get("items", [])

            if not items:
                continue

            df = pd.DataFrame(items)

            df["date"] = pd.to_datetime(df["date"], errors="coerce")

            df["kudup"] = pd.to_numeric(df["toplam"], errors="coerce").fillna(0)

            frames.append(df[["date", "kudup"]])

        except Exception:
            continue

    if not frames:
        return pd.DataFrame(columns=["date", "kudup"])

    combined = pd.concat(frames, ignore_index=True)

    return combined.groupby("date", as_index=False)["kudup"].sum()


def tum_sirketler_kudup(start_date, end_date, tgt_key, companies):
    all_data = []

    for comp in companies:
        name = comp["name"].split("(")[0].strip()

        print(f"KUDÜP çekiliyor: {name}")

        df = data_kudup_sirket(
            start_date,
            end_date,
            tgt_key,
            comp["market"],
            comp["uevcbID"]
        )

        if df.empty:
            continue

        df["company"] = name
        all_data.append(df)

    if not all_data:
        return pd.DataFrame()

    combined = pd.concat(all_data, ignore_index=True)

    pivot_df = combined.pivot_table(
        index="date",
        columns="company",
        values="kudup",
        aggfunc="sum"
    ).reset_index()

    pivot_df = pivot_df.rename(columns={
        col: f"{col}_KUDUP" for col in pivot_df.columns if col != "date"
    })

    return pivot_df.fillna(0)

def add_edm_columns(df):
    uevm_cols = [col for col in df.columns if col.endswith("_UEVM")]

    for u_col in uevm_cols:
        base = u_col.replace("_UEVM", "")
        k_col = f"{base}_KUDUP"

        if k_col in df.columns:
            df[f"{base}_EDM"] = df[u_col] - df[k_col]

    return df

def calculate_edt(edm, ptf, smf, system_status):
    H = 4500
    try:
        max_pf = max(ptf, smf, 150)
        min_pf = min(ptf, smf)

        if edm < 0:

            if system_status == "Enerji Açığı":
                if ptf == H or smf == H:
                    return edm * H * 1.05 * 1.06
                else:
                    return edm * max_pf * 1.06

            elif system_status == "Enerji Fazlası":
                if ptf == H or smf == H:
                    return edm * H * 1.05 * 1.03
                else:
                    return edm * max_pf * 1.03

            elif system_status == "Dengede":
                if ptf == H or smf == H:
                    return edm * H * 1.05 * 1.03
                else:
                    return edm * max_pf * 1.03
        elif edm > 0:

            if system_status == "Enerji Açığı":
                if ptf >= 150 and smf >= 150:
                    return edm * min_pf * 0.97
                else:
                    return (edm * -1 * 100 * 1.03) - (edm * smf)

            elif system_status == "Enerji Fazlası":
                if ptf >= 150 and smf >= 150:
                    return edm * min_pf * 0.94
                else:
                    return (edm * -1 * 100 * 1.06) - (edm * smf)

            elif system_status == "Dengede":
                if ptf >= 150 and smf >= 150:
                    return edm * min_pf * 0.97
                else:
                    return (edm * -1 * 100 * 0.97) - (edm * smf)
        return 0
    except:
        return 0

def add_edt_columns(df):
    edm_cols = [col for col in df.columns if col.endswith("_EDM")]

    for col in edm_cols:
        base = col.replace("_EDM", "")

        df[f"{base}_EDT"] = df.apply(
            lambda row: calculate_edt(
                row[col],
                row["ptf"],
                row["smf"],
                row["systemStatus"]
            ),
            axis=1
        )

    return df

if __name__ == "__main__":
    tgt_key = get_tgt(USERNAME, PASSWORD)

    df = tum_sirketler_uevm(START_DATE, END_DATE, tgt_key, COMPANIES_TOPLAYICI)

    df_ptf = data_ptf_smf(START_DATE, END_DATE, tgt_key)

    df_kudup = tum_sirketler_kudup(START_DATE, END_DATE, tgt_key, COMPANIES_TOPLAYICI_KUDUP)

    df = pd.merge(df, df_ptf, on="date", how="left")
    df = pd.merge(df, df_kudup, on="date", how="left")

    df = add_edt_columns(df)

    df["date"] = df["date"].dt.tz_localize(None)

    df.to_excel("final.xlsx", index=False)


