"""Dashboard Streamlit des offres eSIM.  Lancer : streamlit run app.py"""
import json
import math

import httpx
import pandas as pd
import plotly.express as px
import streamlit as st

from esim_data import (EXPENSIVE_THRESHOLD, clean_offers, compute_stats, load_offers, prepare_frame,
                       provider_breakdown, read_any, to_records)

st.set_page_config(page_title="Dashboard eSIM", page_icon="📶", layout="wide")

BLUE = "#2a78d6"
GRAY = "#a3a29c"


def euro(value: float) -> str:
    return f"{value:,.2f} €".replace(",", " ").replace(".", ",")


def style(fig, height=420):
    fig.update_layout(height=height, margin=dict(l=8, r=8, t=8, b=8), bargap=0.25,
                      hoverlabel=dict(font_size=13), showlegend=False)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridwidth=1, zeroline=False)
    return fig


@st.cache_data
def get_offers():
    return load_offers()


@st.cache_data(show_spinner="Import des données…")
def import_sources(files: tuple[tuple[str, bytes], ...]):
    frames = [prepare_frame(read_any(content, name), name) for name, content in files]
    return clean_offers(pd.concat(frames, ignore_index=True))


@st.cache_data(ttl=300, show_spinner="Appel de l'API…")
def fetch_url(url: str) -> tuple[str, bytes]:
    resp = httpx.get(url, timeout=20, follow_redirects=True)
    resp.raise_for_status()
    name = url.split("?")[0].rstrip("/").rsplit("/", 1)[-1] or "api"
    if "json" in resp.headers.get("content-type", "") and not name.endswith(".json"):
        name += ".json"
    return name, resp.content


offers = get_offers()

# ---------- Import ----------
with st.sidebar:
    st.header("Données")
    uploads = st.file_uploader("Importer des fichiers CSV / JSON", type=["csv", "json"], accept_multiple_files=True)
    api_url = st.text_input("…ou l'URL d'une API (JSON / CSV)", placeholder="https://mon-api.com/offres")
    replace = st.toggle("Remplacer les données d'origine", value=False)
    sources = [(f.name, f.getvalue()) for f in uploads or []]
    try:
        if api_url:
            sources.append(fetch_url(api_url))
        if sources:
            imported = import_sources(tuple(sources))
            offers = imported if replace else (pd.concat([offers, imported], ignore_index=True)
                                               .drop_duplicates(subset=["sku"], keep="last"))
            st.success(f"{len(imported)} offres importées depuis {len(sources)} source(s)")
    except Exception as exc:
        st.error(f"Import impossible : {exc}")

# ---------- Filtres ----------
with st.sidebar:
    st.header("Filtres")
    providers = st.multiselect("Fournisseurs", sorted(offers["provider"].unique()),
                               placeholder="Tous les fournisseurs")
    countries = st.multiselect("Destinations", sorted(offers["country_name"].unique()),
                               placeholder="Toutes les destinations")
    validities = st.multiselect("Validité (jours)", sorted(offers["validity_days"].dropna().unique()),
                                placeholder="Toutes les durées")
    networks = st.multiselect("Réseau", sorted(offers["network"].unique()), placeholder="4G et 5G")
    low, high = float(math.floor(offers["price"].min())), float(math.ceil(offers["price"].max()))
    price_range = st.slider("Prix (€)", low, high, (low, high), step=1.0)
    data_kind = st.radio("Type de forfait", ["Tous", "Volume limité", "Illimité"], horizontal=True)

mask = offers["price"].between(*price_range)
if providers:
    mask &= offers["provider"].isin(providers)
if countries:
    mask &= offers["country_name"].isin(countries)
if validities:
    mask &= offers["validity_days"].isin(validities)
if networks:
    mask &= offers["network"].isin(networks)
if data_kind == "Volume limité":
    mask &= ~offers["is_unlimited"]
elif data_kind == "Illimité":
    mask &= offers["is_unlimited"]
df = offers[mask]

st.title("📶 Comparateur d'offres eSIM")
st.caption(f"{len(offers):,} offres de {offers['provider'].nunique()} fournisseurs, "
           f"issues de {offers['source_file'].nunique()} sources · prix en EUR".replace(",", " "))

if df.empty:
    st.warning("Aucune offre ne correspond aux filtres.")
    st.stop()

stats = compute_stats(df)

# ---------- KPI cards ----------
row1 = st.columns(3)
row1[0].metric("Cartes eSIM", f"{stats['total_offers']:,}".replace(",", " "),
               help="Nombre total d'offres après filtres")
row1[1].metric(f"Offres > {EXPENSIVE_THRESHOLD:.0f} €", stats["offers_over_100"],
               help="Offres dont le prix dépasse 100 €")
row1[2].metric("Prix moyen au Go", euro(stats["price_per_gb_mean"]) + "/Go"
               if stats["unlimited_offers"] < stats["total_offers"] else "—",
               help="Moyenne du prix/Go de chaque offre, hors forfaits illimités")
row2 = st.columns(3)
row2[0].metric("Prix minimum", euro(stats["price_min"]))
row2[1].metric("Prix maximum", euro(stats["price_max"]))
row2[2].metric("Prix moyen", euro(stats["price_mean"]))
row3 = st.columns(3)
row3[0].metric("Data moyenne par carte",
               f"{stats['data_mean_gb']:.1f} Go".replace(".", ",") if stats["unlimited_offers"] < stats["total_offers"] else "—",
               help="Calculée uniquement sur les forfaits à volume fini")
row3[1].metric("Forfaits illimités", stats["unlimited_offers"],
               help="Exclus des moyennes de data et de prix/Go")
row3[2].metric("Fournisseurs", stats["providers"])

st.divider()

# ---------- Graphiques ----------
breakdown = provider_breakdown(df).reset_index()

left, right = st.columns(2)
with left:
    st.subheader("Nombre d'offres par fournisseur")
    fig = px.bar(breakdown.sort_values("offres"), x="offres", y="provider", orientation="h",
                 custom_data=["part_%", "prix_moyen"],
                 labels={"offres": "Offres", "provider": ""})
    fig.update_traces(marker_color=BLUE,
                      hovertemplate="<b>%{y}</b><br>%{x} offres (%{customdata[0]:.1f} %)"
                                    "<br>Prix moyen : %{customdata[1]:.2f} €<extra></extra>")
    st.plotly_chart(style(fig, 520), width="stretch")

with right:
    st.subheader("Prix moyen au Go par fournisseur")
    per_gb = breakdown.dropna(subset=["prix_moyen_par_go"]).sort_values("prix_moyen_par_go", ascending=False)
    fig = px.bar(per_gb, x="prix_moyen_par_go", y="provider", orientation="h",
                 custom_data=["offres", "offres_illimitees"],
                 labels={"prix_moyen_par_go": "€/Go (hors illimité)", "provider": ""})
    fig.update_traces(marker_color=BLUE,
                      hovertemplate="<b>%{y}</b><br>%{x:.2f} €/Go<br>%{customdata[0]} offres "
                                    "dont %{customdata[1]} illimitées<extra></extra>")
    st.plotly_chart(style(fig, 520), width="stretch")
    st.caption("Plus la barre est courte, moins le Go est cher. Forfaits illimités exclus.")

left, right = st.columns(2)
with left:
    st.subheader("Distribution des prix")
    fig = px.histogram(df, x="price", nbins=40, labels={"price": "Prix (€)"})
    fig.update_traces(marker_color=BLUE,
                      hovertemplate="%{x} €<br>%{y} offres<extra></extra>")
    fig.add_vline(x=EXPENSIVE_THRESHOLD, line_dash="dot", line_color=GRAY,
                  annotation_text="100 €", annotation_position="top")
    fig.update_yaxes(title="Offres")
    st.plotly_chart(style(fig), width="stretch")

with right:
    st.subheader("Prix médian selon le volume de data")
    by_volume = (df.assign(volume=df["data_gb"].map(lambda g: f"{g:g} Go").where(~df["is_unlimited"], "Illimité"),
                           order=df["data_gb"].fillna(1e9))
                 .groupby(["volume", "order"], as_index=False)["price"].agg(["median", "count"])
                 .sort_values("order"))
    fig = px.bar(by_volume, x="volume", y="median", custom_data=["count"],
                 labels={"volume": "Volume", "median": "Prix médian (€)"})
    fig.update_traces(marker_color=BLUE,
                      hovertemplate="<b>%{x}</b><br>Prix médian : %{y:.2f} €"
                                    "<br>%{customdata[0]} offres<extra></extra>")
    fig.update_xaxes(type="category")
    st.plotly_chart(style(fig), width="stretch")

# ---------- Tableaux ----------
st.subheader("Répartition par fournisseur")
st.dataframe(
    breakdown,
    hide_index=True, width="stretch",
    column_config={
        "provider": "Fournisseur",
        "offres": "Offres",
        "part_%": st.column_config.NumberColumn("Part", format="%.1f %%"),
        "prix_moyen": st.column_config.NumberColumn("Prix moyen", format="%.2f €"),
        "prix_min": st.column_config.NumberColumn("Prix min", format="%.2f €"),
        "prix_max": st.column_config.NumberColumn("Prix max", format="%.2f €"),
        "offres_illimitees": "Illimitées",
        "prix_moyen_par_go": st.column_config.NumberColumn("€/Go", format="%.2f €"),
    },
)

st.subheader("Toutes les offres")
search = st.text_input("Rechercher une offre", placeholder="ex. japon 5g -holafly",
                       help="Chaque mot est un critère (ET), une virgule donne des alternatives (japon,corée), "
                            "un « - » exclut un mot (-holafly).")
table = df
if search:
    haystack = df[["provider", "product_name", "country_name", "network"]].astype(str).agg(" ".join, axis=1).str.lower()
    mask = pd.Series(True, index=df.index)
    for word in search.lower().split():
        exclude = word.startswith("-") and len(word) > 1
        alternatives = [w for w in word.lstrip("-").split(",") if w]
        if not alternatives:
            continue
        hit = pd.concat([haystack.str.contains(w, regex=False) for w in alternatives], axis=1).any(axis=1)
        mask &= ~hit if exclude else hit
    table = df[mask]

columns = ["provider", "product_name", "country_name", "data_display", "validity_days",
           "price", "price_per_gb", "network", "top_up"]
st.dataframe(
    table[columns].sort_values("price"),
    hide_index=True, width="stretch", height=420,
    column_config={
        "provider": "Fournisseur", "product_name": "Offre", "country_name": "Destination",
        "data_display": "Data",
        "validity_days": st.column_config.NumberColumn("Validité", format="%d j"),
        "price": st.column_config.NumberColumn("Prix", format="%.2f €"),
        "price_per_gb": st.column_config.NumberColumn("€/Go", format="%.2f €"),
        "network": "Réseau",
        "top_up": st.column_config.CheckboxColumn("Recharge"),
    },
)
export = st.columns(2)
export[0].download_button("Télécharger les offres filtrées (CSV)",
                          pd.DataFrame(to_records(table)).to_csv(index=False).encode("utf-8-sig"),
                          file_name="offres_esim_filtrees.csv", mime="text/csv")
export[1].download_button("Télécharger les offres filtrées (JSON)",
                          json.dumps({"total": len(table), "stats": {k: None if pd.isna(v) else float(v)
                                                                     for k, v in compute_stats(table).items()},
                                      "offers": to_records(table)}, ensure_ascii=False, indent=1),
                          file_name="offres_esim_filtrees.json", mime="application/json")
