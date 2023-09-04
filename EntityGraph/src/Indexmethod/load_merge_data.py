import pandas as pd

def load_data():
    oersi = pd.read_csv('data/OERSI/OERSI_data_without_stpwrds_and_umlauts.csv')
    mix_yt_srlo_pdcst = pd.read_csv('data/MIX_Youtube_Serlo_Podcasts/merged_youtube_data_for_AI_without_stopwords.csv')
    merged_df = pd.concat([oersi, mix_yt_srlo_pdcst])
    return merged_df

