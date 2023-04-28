import pandas as pd

def get_data(path): 
        merged_df = pd.read_csv(path)
        strings = merged_df['String']
        str_lst = strings.values

        vocab = merged_df['Title'].values
        identifier = merged_df['identifier']
        identifier_vocab = pd.DataFrame({'ID': identifier, 'Vocab': vocab})
        identifier_vocab = identifier_vocab.set_index('Vocab')['ID'].to_dict()
        return merged_df, str_lst, vocab, identifier_vocab, identifier
