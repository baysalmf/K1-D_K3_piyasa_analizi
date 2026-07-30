import json
import time
import requests
import pandas as pd
import numpy as np
import streamlit as st
from io import BytesIO
import datetime

st.set_page_config(page_title="Zorlu Enerji Planlama", page_icon="⚡", layout="wide")
st.title("Zorlu Piyasa Analiz Raporu")
st.markdown("---")

st.markdown("""
<style>
[data-testid="stDataFrame"] td {
    text-align: center !important;
}
[data-testid="stDataFrame"] th {
    text-align: center !important;
}
</style>
""", unsafe_allow_html=True)

COMPANIES_K1 = [
    {"name": "K1 OSMANGAZİ ELEKTRİK PERAKENDE SATIŞ AŞ","market": 5959,  "dist": 224},
    {"name": "K1 YEŞİLIRMAK ELEKTRİK PERAKENDE SATIŞ AŞ","market": 5802,  "dist": 228},
    {"name": "K1 ULUDAĞ PERAKENDE ELEKTRİK SATIŞ AŞ","market": 6158,  "dist": 220},
    {"name": "K1 TÜRKERLER VANGÖLÜ ELEKTRİK PERAKENDE SATIŞ AŞ","market": 5900,  "dist": 210},
    {"name": "K1 TRAKYA ELEKTRİK PERAKENDE SATIŞ ANONİM ŞİRKETİ","market": 5844,  "dist": 221},
    {"name": "K1 SAKARYA ELEKTRİK PERAKENDE SATIŞ AŞ","market": 5781,  "dist": 223},
    {"name": "K1 MERAM ELEKTRİK PERAKENDE SATIŞ AŞ","market": 6000,  "dist": 216},
    {"name": "K1 GEDİZ ELEKTRİK PERAKENDE SATIŞ AŞ","market": 5840,  "dist": 219},
    {"name": "K1 ENERJİSA TOROSLAR ELEKTRİK PERAKENDE SATIŞ AŞ","market": 5898,  "dist": 215},
    {"name": "K1 ENERJİSA İSTANBUL ANADOLU YAKASI ELEKTRİK PERAKENDE SATIŞ AŞ","market": 5918,  "dist": 222},
    {"name": "K1 ENERJİSA BAŞKENT ELEKTRİK PERAKENDE SATIŞ AŞ","market": 5780,  "dist": 217},
    {"name": "K1 DİCLE ELEKTRİK PERAKENDE SATIŞ AŞ","market": 5938,  "dist": 209},
    {"name": "K1 CK ÇAMLIBEL ELEKTRİK PERAKENDE SATIŞ AŞ","market": 5803,  "dist": 214},
    {"name": "K1 CK BOĞAZİÇİ ELEKTRİK PERAKENDE SATIŞ AŞ","market": 5960,  "dist": 225},
    {"name": "K1 CK AKDENİZ ELEKTRİK PERAKENDE SATIŞ AŞ","market": 5843,  "dist": 218},
    {"name": "K1 AYDEM ELEKTRİK PERAKENDE SATIŞ AŞ","market": 5818,  "dist": 573},
    {"name": "K1 ARAS ELEKTRİK PERAKENDE SATIŞ AŞ","market": 5978,  "dist": 211},
    {"name": "K1 AKSA FIRAT ELEKTRİK PERAKENDE SATIŞ AŞ","market": 5879,  "dist": 213},
    {"name": "K1 AKSA ÇORUH ELEKTRİK PERAKENDE SATIŞ AŞ","market": 5838,  "dist": 212},
    {"name": "K1 AKEDAŞ ELEKTRİK PERAKENDE SATIŞ AŞ","market": 5820,  "dist": 227},
    {"name": "K1 KAYSERİ ELEKTRİK PERAKENDE SATIŞ A.Ş","market": 5839,  "dist": 841},
]

COMPANIES_K3 = [
    {"name": "K3 OSMANGAZİ","market": 10930, "santraller": [11961,11957,11362,5013507,5004323,5005282,5005225,5012347,12923,19985]},
    {"name": "K3 YEŞİLIRMAK","market": 10955, "santraller": [11354,11935,11937,11936,11952,11366,11955,12163]},
    {"name": "K3 ULUDAĞ","market": 10953, "santraller": [11949,11950,11951,11367,11948,5005261]},
    {"name": "K3 TÜRKERLER","market": 10940, "santraller": [11365,11962,5004382]},
    {"name": "K3 TRAKYA","market": 10959, "santraller": [11966,11364]},
    {"name": "K3 SEPAŞ","market": 10929, "santraller": [11964,11963,11363]},
    {"name": "K3 MERAM","market": 10939, "santraller": [5002220,11954,11361,12433,12443,5005371,5004261]},
    {"name": "K3 GEDİZ","market": 10935, "santraller": [11946,11945,11357,12765,5004322]},
    {"name": "K3 TOROSLAR","market": 10945, "santraller": [11940,11938,11355,11942,5014141,5004324,5004325,5014501,5013021,5014183,5004381]},
    {"name": "K3 AYEDAŞ","market": 10943, "santraller": [11354,11935,11937,11936]},
    {"name": "K3 BAŞKENT","market": 10944, "santraller": [11953,12583,11930,11353,11934,5013643]},
    {"name": "K3 DİCLE","market": 10958, "santraller": [13984,13983,12522,5004421,5005426,11352]},
    {"name": "K3 ÇAMLIBEL","market": 10949, "santraller": [12983,5013661,5013941,11350]},
    {"name": "K3 BOĞAZİÇİ","market": 10956, "santraller": [11349,11926,5004362]},
    {"name": "K3 AKDENİZ","market": 10957, "santraller": [11348,5004385]},
    {"name": "K3 AYDEM","market": 10934, "santraller": [12445,11924,11347,5011721,5004386]},
    {"name": "K3 ARAS","market": 10942, "santraller": [11346,14584,12963,5012764]},
    {"name": "K3 FIRAT","market": 10933, "santraller": [11943,11356,17927,11944,5004384,5013341,5004383]},
    {"name": "K3 ÇORUH","market": 10932, "santraller": [12022,11351]},
    {"name": "K3 AKEDAŞ","market": 10954, "santraller": [19544,11342,11923,5013901,5014381,5004361]},
    {"name": "K3 KEPSAŞ","market": 10931, "santraller": [11358]},
]

CAS_URL      = "https://giris.epias.com.tr/cas/v1/tickets"
URL_GOP      = "https://seffaflik.epias.com.tr/electricity-service/v1/markets/dam/data/clearing-quantity"
URL_GIP      = "https://seffaflik.epias.com.tr/electricity-service/v1/markets/idm/data/matching-quantity"
URL_IA_ALIS  = "https://seffaflik.epias.com.tr/electricity-service/v1/markets/bilateral-contracts/data/bilateral-contracts-bid-quantity"
URL_IA_SATIS = "https://seffaflik.epias.com.tr/electricity-service/v1/markets/bilateral-contracts/data/bilateral-contracts-offer-quantity"
URL_DSG      = "https://seffaflik.epias.com.tr/electricity-service/v1/markets/imbalance/data/dsg-imbalance-quantity"
URL_UEVM     = "https://seffaflik.epias.com.tr/electricity-service/v1/generation/data/injection-quantity"

def to_iso_tr(date_str: str) -> str:
    return f"{date_str}T00:00+03:00"

def _debug(label: str, data):
    """Sadece debug_mode aktifken terminale yazar."""
    if st.session_state.get("debug_mode"):
        print(f"[DEBUG] {label}")
        if isinstance(data, pd.DataFrame):
            print(data.to_string())
        elif isinstance(data, dict):
            print(json.dumps(data, ensure_ascii=False, indent=2, default=str))
        else:
            print(str(data))

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
    if st.session_state.get("debug_mode"):
        print(f"[DEBUG] POST -> {url}")
        print(f"[DEBUG] body: {json.dumps(body, ensure_ascii=False)}")
    for attempt in range(max_retries):
        time.sleep(0.4)
        r = requests.post(url, headers=headers, json=body)
        if r.status_code == 429:
            wait = 15 * (attempt + 1)
            if st.session_state.get("debug_mode"):
                print(f"[DEBUG] Rate limit (429) - {wait}s bekleniyor (deneme {attempt + 1})")
            time.sleep(wait)
            continue
        if not r.ok:
            raise RuntimeError(f"İstek başarısız ({r.status_code}): {r.text[:500]}")
        try:
            result = r.json()
            if st.session_state.get("debug_mode"):
                items = result.get("items", [])
                print(f"[DEBUG] Yanit - item sayisi: {len(items)}, ilk 2: {json.dumps(items[:2], ensure_ascii=False, default=str)}")
            return result
        except json.JSONDecodeError:
            raise RuntimeError(f"JSON parse hatası: {r.text[:500]}")
    raise RuntimeError(f"Rate limit aşıldı, {max_retries} denemeden sonra başarısız.")

def data_gop(start_date, end_date, tgt_key, organization_id):
    body = {"startDate": to_iso_tr(start_date), "endDate": to_iso_tr(end_date), "organizationId": organization_id}
    js = _post_json(URL_GOP, tgt_key, body)
    df = pd.json_normalize(js.get("items", []))
    if not df.empty and "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    return df

def data_ia_alis(start_date, end_date, tgt_key, organization_id):
    body = {"startDate": to_iso_tr(start_date), "endDate": to_iso_tr(end_date), "organizationId": organization_id}
    js = _post_json(URL_IA_ALIS, tgt_key, body)
    return pd.json_normalize(js.get("items", []))

def data_ia_satis(start_date, end_date, tgt_key, organization_id):
    body = {"startDate": to_iso_tr(start_date), "endDate": to_iso_tr(end_date), "organizationId": organization_id}
    js = _post_json(URL_IA_SATIS, tgt_key, body)
    return pd.json_normalize(js.get("items", []))

def data_gip(start_date, end_date, tgt_key, organization_id):
    body = {"startDate": to_iso_tr(start_date), "endDate": to_iso_tr(end_date), "organizationId": organization_id}
    js = _post_json(URL_GIP, tgt_key, body)
    return pd.json_normalize(js.get("items", []))

def data_dsg(start_date, end_date, tgt_key, organization_id):
    body = {"startDate": to_iso_tr(start_date), "endDate": to_iso_tr(end_date), "organizationId": organization_id}
    js = _post_json(URL_DSG, tgt_key, body)
    return pd.json_normalize(js.get("items", []))

def highlight_osmangazi(row):
    if "OSMANGAZİ" in row["Şirket Adı"].upper():
        return ["background-color: #8B0000; color: white; font-weight: bold"] * len(row)
    return [""] * len(row)

def data_uevm_santral(start_date, end_date, tgt_key, santral_id):
    body = {
        "startDate": to_iso_tr(start_date),
        "endDate": to_iso_tr(end_date),
        "powerplantId": santral_id,
        "page": {"number": 1, "size": 1000}
    }
    js = _post_json(URL_UEVM, tgt_key, body)
    df = pd.DataFrame(js.get("items", []))
    if df.empty:
        return pd.DataFrame(columns=["date", "toplam"])
    df["date"] = pd.to_datetime(df["date"])
    df["toplam"] = pd.to_numeric(df["total"], errors="coerce").fillna(0)
    return df[["date", "toplam"]]

def data_uevm_sirket(start_date, end_date, tgt_key, santraller):
    if not santraller:
        return pd.DataFrame(columns=["date", "uevm_gercek"])
    frames = []
    for sid in santraller:
        try:
            df = data_uevm_santral(start_date, end_date, tgt_key, sid)
            if not df.empty:
                frames.append(df)
        except Exception:
            pass
    if not frames:
        return pd.DataFrame(columns=["date", "uevm_gercek"])
    combined = pd.concat(frames, ignore_index=True)
    combined["date"] = pd.to_datetime(combined["date"], errors="coerce")
    grouped = combined.groupby("date", as_index=False)["toplam"].sum()
    grouped.rename(columns={"toplam": "uevm_gercek"}, inplace=True)
    return grouped

def _normalize_gip(df4, start_date, end_date, col_alis="gip_alis", col_satis="gip_satis"):
    if df4.empty:
        date_range = pd.date_range(start=start_date, end=end_date, freq="D")
        dates = [d + pd.Timedelta(hours=h) for d in date_range for h in range(24)]
        df4 = pd.DataFrame({"date": dates, col_alis: 0, col_satis: 0})
        df4["date"] = df4["date"].dt.strftime("%Y-%m-%d %H:%M:%S+03:00")
    else:
        if "kontratAdi" in df4.columns:
            df4["date"] = pd.to_datetime(
                "20" + df4["kontratAdi"].str[2:8] + df4["kontratAdi"].str[8:10],
                format="%Y%m%d%H", errors="coerce"
            ).dt.strftime("%Y-%m-%d %H:%M:%S+03:00")
            df4.drop(["kontratTuru", "kontratAdi"], axis=1, inplace=True, errors="ignore")
    return df4

def _fix_tz(dfs):
    for d in dfs:
        if not d.empty and "date" in d.columns:
            d["date"] = pd.to_datetime(d["date"], errors="coerce")
            if not d["date"].isna().all():
                if d["date"].dt.tz is None:
                    d["date"] = d["date"].dt.tz_localize("Etc/GMT-3")
                else:
                    d["date"] = d["date"].dt.tz_convert("Etc/GMT-3")

def _merge_market_data(df1, df2, df3, df4, col_names):
    for d in [df1, df2, df3]:
        if not d.empty and "hour" in d.columns:
            d.drop("hour", axis=1, inplace=True)
    _fix_tz([df1, df2, df3, df4])
    try:
        merged = (
            pd.merge(df1, df2, on="date", how="outer")
              .merge(df3, on="date", how="outer")
              .merge(df4, on="date", how="outer")
              .fillna(0)
        )
        if not merged.empty:
            merged.columns = col_names
        return merged
    except (KeyError, ValueError):
        return pd.DataFrame()

def process_k1(start_date, end_date, tgt_key, organization_id, organization_id_dagitim, company_name):
    df4 = _normalize_gip(data_gip(start_date, end_date, tgt_key, organization_id), start_date, end_date)
    merged = _merge_market_data(
        data_gop(start_date, end_date, tgt_key, organization_id),
        data_ia_alis(start_date, end_date, tgt_key, organization_id),
        data_ia_satis(start_date, end_date, tgt_key, organization_id),
        df4,
        ["Tarih", "gop_alış", "gop_satış", "ia_alıs", "ia_satis", "gip_alis", "gip_satis"],
    )

    df4_d = _normalize_gip(data_gip(start_date, end_date, tgt_key, organization_id_dagitim), start_date, end_date,
                            col_alis="d_gip_alis", col_satis="d_gip_satis")
    merged2 = _merge_market_data(
        data_gop(start_date, end_date, tgt_key, organization_id_dagitim),
        data_ia_alis(start_date, end_date, tgt_key, organization_id_dagitim),
        data_ia_satis(start_date, end_date, tgt_key, organization_id_dagitim),
        df4_d,
        ["Tarih", "d_gop_alış", "d_gop_satış", "d_ia_alıs", "d_ia_satis", "d_gip_alis", "d_gip_satis"])

    if merged.empty and merged2.empty:
        final = pd.DataFrame()
    elif merged.empty:
        final = merged2.copy()
        for col in ["gop_alış","gop_satış","ia_alıs","ia_satis","gip_alis","gip_satis"]:
            final[col] = 0
    elif merged2.empty:
        final = merged.copy()
        for col in ["d_gop_alış","d_gop_satış","d_ia_alıs","d_ia_satis","d_gip_alis","d_gip_satis"]:
            final[col] = 0
    else:
        final = pd.merge(merged, merged2, on="Tarih", how="outer").fillna(0)

    if not final.empty:
        required = ["gop_alış","gop_satış","ia_alıs","ia_satis","gip_alis","gip_satis",
                    "d_gop_alış","d_gop_satış","d_ia_alıs","d_ia_satis","d_gip_alis","d_gip_satis"]
        for col in required:
            if col not in final.columns:
                final[col] = 0
        final["UECM"] = (
            final["gop_alış"] + final["ia_alıs"] + final["gip_alis"] +
            final["d_gop_alış"] + final["d_ia_alıs"] + final["d_gip_alis"]
        ) - (
            final["gop_satış"] + final["ia_satis"] + final["gip_satis"] +
            final["d_ia_satis"] + final["d_gop_satış"] + final["d_gip_satis"]
        )

    df6 = pd.DataFrame()
    try:
        df6 = data_dsg(start_date, end_date, tgt_key, organization_id_dagitim)
    except Exception:
        try:
            df6 = data_dsg(start_date, end_date, tgt_key, organization_id)
        except Exception:
            df6 = pd.DataFrame()

    if df6.empty:
        edm_sum, uecm_sum, imbalance_percentage = 0, 0, 0
    else:
        df6["edm"] = (df6["positiveImbalanceQuantity"] - df6["negativeImbalanceQuantity"]).abs()
        edm_sum  = df6["edm"].sum()
        uecm_sum = final["UECM"].sum() if not final.empty else 0
        total    = uecm_sum + edm_sum
        imbalance_percentage = (edm_sum / total * 100) if total != 0 else 0

    return {
        "Şirket Adı":  company_name,
        "UECM Toplam": round(uecm_sum, 2),
        "EDM Toplam":  round(edm_sum, 2),
        "% (oran)":    round(imbalance_percentage, 2),
    }

def process_k3(start_date, end_date, tgt_key, organization_id, company_name, santraller):
    df  = data_gop(start_date, end_date, tgt_key, organization_id)
    df2 = data_ia_alis(start_date, end_date, tgt_key, organization_id)
    df3 = data_ia_satis(start_date, end_date, tgt_key, organization_id)
    df4 = data_gip(start_date, end_date, tgt_key, organization_id)

    for d in [df, df2, df3, df4]:
        if not d.empty and "hour" in d.columns:
            d.drop("hour", axis=1, inplace=True)

    if df4.empty:
        date_range = pd.date_range(start=start_date, end=end_date, freq="h")
        df4 = pd.DataFrame({"date": date_range, "gip_alis": 0.0, "gip_satis": 0.0})
    else:
        if "kontratAdi" in df4.columns:
            df4["date"] = pd.to_datetime(
                "20" + df4["kontratAdi"].str[2:8] + df4["kontratAdi"].str[8:10],
                format="%Y%m%d%H", errors="coerce"
            )
            df4.drop(columns=["kontratTuru","kontratAdi"], errors="ignore", inplace=True)

    _fix_tz([df, df2, df3, df4])

    try:
        merged = (
            pd.merge(df, df2, on="date", how="outer")
              .merge(df3, on="date", how="outer")
              .merge(df4, on="date", how="outer")
              .fillna(0)
        )
        if not merged.empty:
            num_cols = [c for c in merged.columns if c != "date"]
            standard = ["gop_alış","gop_satış","ia_alış","ia_satış","gip_alış","gip_satış"]
            rename_map = {num_cols[i]: standard[i] for i in range(min(len(num_cols), len(standard)))}
            merged.rename(columns=rename_map, inplace=True)
            merged.rename(columns={"date": "Tarih"}, inplace=True)
            for col in standard:
                if col not in merged.columns:
                    merged[col] = 0
    except Exception:
        merged = pd.DataFrame()

    uevm_hesap = 0.0

    if not merged.empty:
        merged["NET"] = (
            merged["gop_alış"] - merged["gop_satış"] +
            merged["gip_alış"] - merged["gip_satış"] +
            merged["ia_alış"]  - merged["ia_satış"]
        )
        uevm_hesap = merged["NET"].sum()

    df_uevm   = data_uevm_sirket(start_date, end_date, tgt_key, santraller)
    uevm_gercek = df_uevm["uevm_gercek"].sum() if not df_uevm.empty else 0.0

    wmape = None

    if not merged.empty and not df_uevm.empty:
        try:
            mc = merged.copy()
            mc["date_key"] = mc["Tarih"].dt.tz_localize(None) if isinstance(mc["Tarih"].dtype, pd.DatetimeTZDtype) else pd.to_datetime(mc["Tarih"])

            uc = df_uevm.copy()
            uc["date_key"] = uc["date"].dt.tz_localize(None) if isinstance(uc["date"].dtype, pd.DatetimeTZDtype) else pd.to_datetime(uc["date"])

            hourly = pd.merge(mc[["date_key","NET"]], uc[["date_key","uevm_gercek"]], on="date_key", how="inner")
            hourly["net_abs"]  = hourly["NET"].abs()
            hourly["uevm_abs"] = hourly["uevm_gercek"].abs()
            hourly["error"]    = (hourly["net_abs"] - hourly["uevm_abs"]).abs()

            denom = hourly["uevm_abs"].sum()
            if denom > 0:
                wmape = round((hourly["error"].sum() / denom) * 100, 2)
        except Exception:
            pass

    return {
        "Şirket Adı":  company_name,
        "NET Toplam":  round(float(uevm_hesap), 2),
        "UEVM Gerçek": round(float(uevm_gercek), 2),
        "WMAPE (%)":   wmape if wmape is not None else "N/A",
    }

def to_excel_multi(df_k1: pd.DataFrame, df_k3: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_k1.to_excel(writer, index=False, sheet_name="K1+D Sonuçları")
        df_k3.to_excel(writer, index=False, sheet_name="K3 Sonuçları")
    return output.getvalue()

with st.sidebar:
    st.header("🔐 Giriş Bilgileri")
    username = st.text_input("Kullanıcı Adı", value="", placeholder="epias kullanıcı adı")
    password = st.text_input("Şifre", value="", type="password", placeholder="••••••••")

    st.markdown("---")
    st.header("⚙️ Ayarlar")
    debug_mode = st.checkbox("Debug Mode", value=False, help="Etkinleştirildiğinde API istekleri ve ara hesaplamalar terminale yazdırılır.")

    st.markdown("---")
    st.header("📅 Tarih Aralığı")

    bugun          = datetime.date.today()
    ay_basi        = bugun.replace(day=1)
    onceki_ay_sonu = ay_basi - datetime.timedelta(days=1)
    onceki_ay_basi = onceki_ay_sonu.replace(day=1)

    start_date = st.date_input("Başlangıç Tarihi", value=onceki_ay_basi)
    end_date   = st.date_input("Bitiş Tarihi",     value=onceki_ay_sonu)

    st.markdown("---")
    if st.button("Raporu Oluştur", use_container_width=True, type="primary"):
        st.session_state.clear()
        st.session_state["run"] = True
        st.session_state["debug_mode"] = debug_mode

if st.session_state.get("run") and "df_k1" not in st.session_state:
    if not username or not password:
        st.error("Lütfen kullanıcı adı ve şifre girin.")
        st.stop()
    if start_date > end_date:
        st.error("Başlangıç tarihi, bitiş tarihinden büyük olamaz.")
        st.stop()

    start_str = start_date.strftime("%Y-%m-%d")
    end_str   = end_date.strftime("%Y-%m-%d")

    with st.spinner("EPİAŞ'a giriş yapılıyor..."):
        try:
            tgt_key = get_tgt(username, password)
        except Exception as e:
            st.error(f"Giriş başarısız: {e}")
            st.stop()
    st.success("✅ Giriş başarılı!")

    st.markdown(f"### 📊 {start_str} – {end_str} dönemi işleniyor")

    # ════════════════════════════════════════════════════════════════════════
    # K1+D
    # ════════════════════════════════════════════════════════════════════════
    st.markdown("#### ⚡ K1+D Hesaplamaları")
    progress_k1 = st.progress(0)
    status_k1   = st.empty()
    results_k1  = []

    for i, company in enumerate(COMPANIES_K1):
        status_k1.info(f"⏳ K1+D İşleniyor ({i+1}/{len(COMPANIES_K1)}): **{company['name']}**")
        try:
            result = process_k1(start_str, end_str, tgt_key, company["market"], company["dist"], company["name"])
            results_k1.append(result)
            _debug(f"K1 Sonuç — {company['name']}", result)
        except Exception as e:
            if st.session_state.get("debug_mode"):
                print(f"[DEBUG] K1 HATA — {company['name']} | market_id={company['market']} dist_id={company['dist']} | {e}")
            results_k1.append({
                "Şirket Adı":  company["name"],
                "UECM Toplam": 0,
                "EDM Toplam":  0,
                "% (oran)":    0,
                "Hata":        str(e),
            })
        progress_k1.progress((i + 1) / len(COMPANIES_K1))

    status_k1.success("✅ K1+D tüm şirketler tamamlandı!")

    df_k1 = pd.DataFrame(results_k1)
    if not df_k1.empty:
        for col in ["UECM Toplam", "EDM Toplam", "% (oran)"]:
            if col in df_k1.columns:
                df_k1[col] = pd.to_numeric(df_k1[col], errors="coerce").round(2)
        df_k1 = df_k1.sort_values("% (oran)", ascending=True, na_position="last")
    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════
    # K3
    # ════════════════════════════════════════════════════════════════════════
    st.markdown("#### K3 Hesaplamaları (MAPE)")
    progress_k3 = st.progress(0)
    status_k3   = st.empty()
    results_k3  = []

    for i, company in enumerate(COMPANIES_K3):
        status_k3.info(f"⏳ K3 İşleniyor ({i+1}/{len(COMPANIES_K3)}): **{company['name']}**")
        try:
            result = process_k3(start_str, end_str, tgt_key, company["market"], company["name"], company["santraller"])
            results_k3.append(result)
            _debug(f"K3 Sonuç — {company['name']}", result)
        except Exception as e:
            if st.session_state.get("debug_mode"):
                print(f"[DEBUG] K3 HATA — {company['name']} | market_id={company['market']} santraller={company['santraller']} | {e}")
            results_k3.append({
                "Şirket Adı":  company["name"],
                "NET Toplam":  0,
                "UEVM Gerçek": 0,
                "WMAPE (%)":   "HATA",
                "Hata":        str(e),
            })
        progress_k3.progress((i + 1) / len(COMPANIES_K3))

    status_k3.success("✅ K3 tüm şirketler tamamlandı!")

    df_k3 = pd.DataFrame(results_k3)
    if not df_k3.empty:
        for col in ["NET Toplam", "UEVM Gerçek"]:
            if col in df_k3.columns:
                df_k3[col] = pd.to_numeric(df_k3[col], errors="coerce").round(2)
        df_k3["WMAPE (%)"] = pd.to_numeric(df_k3["WMAPE (%)"], errors="coerce")
        df_k3 = df_k3.sort_values("WMAPE (%)", ascending=True, na_position="last")
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        excel_data = to_excel_multi(df_k1, df_k3)
        st.download_button(
            label="⬇️ Excel olarak indir (.xlsx)",
            data=excel_data,
            file_name=f"epias_rapor_{start_str}_{end_str}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    with col2:
        csv_k1 = df_k1.to_csv(index=False).encode("utf-8-sig")
        csv_k3 = df_k3.to_csv(index=False).encode("utf-8-sig")
        combined_csv = (
                "=== K1+D SONUÇLARI ===\n".encode("utf-8-sig") + csv_k1 +
                "\n=== K3 SONUÇLARI ===\n".encode("utf-8-sig") + csv_k3
        )

        st.download_button(
            label="⬇️ CSV olarak indir (.csv)",
            data=combined_csv,
            file_name=f"epias_rapor_{start_str}_{end_str}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    st.session_state["df_k1"] = df_k1
    st.session_state["df_k3"] = df_k3
    st.session_state["excel_data"] = excel_data
    st.session_state["combined_csv"] = combined_csv

if "df_k1" in st.session_state:
    st.markdown("##### K1+D Sonuçları")
    st.dataframe(
        st.session_state["df_k1"]
        .style
        .format({
            "UECM Toplam": "{:.2f}",
            "EDM Toplam": "{:.2f}",
            "% (oran)": "{:.2f}"
        })
        .apply(highlight_osmangazi, axis=1),
        use_container_width=True,
        hide_index=True
    )

if "df_k3" in st.session_state:
    st.markdown("##### K3 Sonuçları")
    st.dataframe(
        st.session_state["df_k3"]
        .style
        .format({
            "NET Toplam": "{:.2f}",
            "UEVM Gerçek": "{:.2f}",
            "WMAPE (%)": "{:.2f}"
        })
        .apply(highlight_osmangazi, axis=1),
        use_container_width=True,
        hide_index=True
    )

if "excel_data" in st.session_state:
    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="⬇️ Excel olarak indir (.xlsx)",
            data=st.session_state["excel_data"],
            file_name="rapor.xlsx",
            use_container_width=True,
        )

    with col2:
        st.download_button(
            label="⬇️ CSV olarak indir (.csv)",
            data=st.session_state["combined_csv"],
            file_name="rapor.csv",
            use_container_width=True,
        )
