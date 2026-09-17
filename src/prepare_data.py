"""Extract a reproducible AppleSupport customer->brand-response dataset from TWCS."""
import argparse, os, zipfile
import pandas as pd


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--zip', default='data/archive.zip')
    ap.add_argument('--brand', default='AppleSupport')
    ap.add_argument('--n', type=int, default=15000)
    ap.add_argument('--seed', type=int, default=42)
    args=ap.parse_args()
    out=os.path.join('data', f'{args.brand.lower()}_pairs.csv')
    os.makedirs('data',exist_ok=True)
    with zipfile.ZipFile(args.zip) as z:
        with z.open('twcs/twcs.csv') as f:
            parents=set(); responses=[]
            for ch in pd.read_csv(f,chunksize=200000):
                a=ch[(ch.author_id==args.brand) & (ch.inbound==False) & ch.in_response_to_tweet_id.notna()].copy()
                responses.append(a[['tweet_id','in_response_to_tweet_id','text','created_at']])
                parents.update(a.in_response_to_tweet_id.astype('int64').tolist())
    responses=pd.concat(responses,ignore_index=True)
    parents_df=[]
    with zipfile.ZipFile(args.zip) as z:
        with z.open('twcs/twcs.csv') as f:
            for ch in pd.read_csv(f,chunksize=200000):
                m=ch.tweet_id.isin(parents)
                if m.any(): parents_df.append(ch.loc[m,['tweet_id','author_id','inbound','text','created_at']])
    parents_df=pd.concat(parents_df,ignore_index=True)
    pairs=responses.merge(parents_df,left_on='in_response_to_tweet_id',right_on='tweet_id',suffixes=('_response','_customer'))
    pairs=pairs[(pairs.inbound==True) & (pairs.author_id != args.brand)]
    pairs=pairs.rename(columns={'tweet_id_customer':'customer_tweet_id','text_customer':'customer_text','text_response':'brand_response','created_at_customer':'customer_created_at','created_at_response':'response_created_at'})
    pairs=pairs[['customer_tweet_id','customer_text','brand_response','customer_created_at','response_created_at']].drop_duplicates('customer_tweet_id')
    if len(pairs)>args.n: pairs=pairs.sample(args.n,random_state=args.seed)
    pairs.to_csv(out,index=False)
    print(f'Saved {len(pairs):,} pairs to {out}')

if __name__=='__main__': main()
